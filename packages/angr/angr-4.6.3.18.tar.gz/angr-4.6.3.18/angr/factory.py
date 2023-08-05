from simuvex import SimIRSB, SimProcedures, SimState, BP_BEFORE, BP_AFTER
from simuvex import s_options as o
from .surveyors.caller import Callable

import logging
l = logging.getLogger('angr.factory')

class AngrObjectFactory(object):
    """
    This factory provides access to important analysis elements.
    """
    def __init__(self, project, translation_cache=False):
        self._project = project
        self._lifter = Lifter(project, cache=translation_cache)
        self.block = self._lifter.lift

    def snippet(self, addr, jumpkind=None, **block_opts):
        if self._project.is_hooked(addr) and jumpkind != 'Ijk_NoHook':
            _, kwargs = self._project._sim_procedures[addr]
            size = kwargs.get('length', 0)
            return HookNode(addr, size, self._project._sim_procedures[addr])
        else:
            return self.block(addr, **block_opts).codenode # pylint: disable=no-member

    def sim_block(self, state, stmt_whitelist=None, last_stmt=None,
                  addr=None, opt_level=None, **block_opts):
        """
        Returns a SimIRSB object with execution based on state.

        :param state:           The state to tick forward with this block.

        The following parameters are optional:

        :param stmt_whitelist:  A list of stmt indexes to which to confine execution.
        :param last_stmt:       A statement index at which to stop execution.
        :param addr:            The address at which to start the block.
        :param thumb:           Whether the block should be lifted in ARM's THUMB mode.
        :param backup_state:    A state to read bytes from instead of using project memory.
        :param opt_level:       The VEX optimization level to use.
        :param insn_bytes:      A string of bytes to use for the block instead of the project.
        :param max_size:        The maximum size of the block, in bytes.
        :param num_inst:        The maximum number of instructions.
        :param traceflags:      traceflags to be passed to VEX. Default: 0
        """

        if 'thumb' in block_opts:
            raise AngrValueError('You are not allowed to pass in a thumb=x property to sim_block')

        if addr is None:
            addr = state.se.any_int(state.regs.ip)

        thumb = False
        if addr % state.arch.instruction_alignment != 0:
            if state.thumb:
                thumb = True
            else:
                raise AngrExitError("Address %#x does not align to alignment %d "
                                    "for architecture %s." % (addr,
                                    state.arch.instruction_alignment,
                                    state.arch.name))

        if opt_level is None:
            opt_level = 1 if o.OPTIMIZE_IR in state.options else 0
        backup_state = state if self._project._support_selfmodifying_code else None

        bb = self.block(addr,
                        arch=state.arch,
                        opt_level=opt_level,
                        thumb=thumb,
                        backup_state=backup_state,
                        **block_opts)

        return SimIRSB(state,
                       bb.vex,
                       addr=addr,
                       whitelist=stmt_whitelist,
                       last_stmt=last_stmt)

    def sim_run(self, state, addr=None, jumpkind=None, **block_opts):
        """
        Returns a simuvex SimRun object (supporting refs() and exits()), automatically choosing whether to create a
        SimIRSB or a SimProcedure.

        :param state:       The state to analyze
        :param jumpkind:    optional, the jumpkind of the previous exit
        :param addr:        optional, an address to execute at instead of the state's ip

        Additional keyword arguments will be passed directly into factory.sim_block if appropriate.

        :keyword stmt_whitelist:    a list of stmt indexes to which to confine execution.
        :keyword last_stmt:         a statement index at which to stop execution.
        :keyword thumb:             whether the block should be lifted in ARM's THUMB mode.
        :keyword backup_state:      a state to read bytes from instead of using project memory.
        :keyword opt_level:         the VEX optimization level to use.
        :keyword insn_bytes:        a string of bytes to use for the block instead of the project.
        :keyword max_size:          the maximum size of the block, in bytes.
        :keyword num_inst:          the maximum number of instructions.
        :keyword traceflags:        traceflags to be passed to VEX. Default: 0
        """

        if addr is None:
            addr = state.se.any_int(state.regs.ip)
        if jumpkind is None:
            jumpkind = state.scratch.jumpkind

        if jumpkind == 'Ijk_Exit':
            l.debug('Execution hit exit at %#x', addr)
            return SimProcedures['stubs']['PathTerminator'](state, addr=addr)

        if jumpkind.startswith("Ijk_Sys"):
            l.debug("Invoking system call handler (originally at %#x)", addr)
            return SimProcedures['syscalls']['handler'](state, addr=addr, ret_to=state.ip)

        if jumpkind in ("Ijk_EmFail", "Ijk_MapFail") or "Ijk_Sig" in jumpkind:
            raise AngrExitError("Cannot create run following jumpkind %s" % jumpkind)

        if jumpkind == "Ijk_NoDecode" and not self._project.is_hooked(addr):
            raise AngrExitError("IR decoding error at #%x. You can hook this instruction with a python replacement using project.hook(%#x, your_function, length=length_of_instruction)." % (addr, addr))

        elif self._project.is_hooked(addr) and jumpkind != 'Ijk_NoHook':
            sim_proc_class, kwargs = self._project._sim_procedures[addr]
            l.debug("Creating SimProcedure %s (originally at %#x)",
                    sim_proc_class.__name__, addr)
            state._inspect('call', BP_BEFORE, function_name=sim_proc_class.__name__)
            r = sim_proc_class(state, addr=addr, sim_kwargs=kwargs)
            state._inspect('call', BP_AFTER, function_name=sim_proc_class.__name__)
            l.debug("... %s created", r)

        else:
            l.debug("Creating SimIRSB at %#x", addr)
            r = self.sim_block(state, addr=addr, **block_opts)

        return r

    def blank_state(self, **kwargs):
        """
        Returns a blank state object.

        Additional keyword arguments will be passed into the appropriate SimOS's blank_state method.

        :keyword fs:          A dictionary of file names with associated preset SimFile objects.
        :keyword concrete_fs: bool describing whether the host filesystem should be consulted when opening files.
        :keyword chroot:      A path to use as a fake root directory, Behaves similarly to a real chroot. Used only
                              when concrete_fs is set to True.
        :return:              The blank state.
        :rtype:               simuvex.SimState
        """
        return self._project._simos.state_blank(**kwargs)

    def entry_state(self, **kwargs):
        """
        Returns a state object representing the program at its entry point.

        Additional keyword arguments will be passed into the appropriate SimOS's entry_state method:

        :param fs:          a dictionary of file names with associated preset SimFile objects.
        :param concrete_fs: boolean describing whether the host filesystem should be consulted when opening files.
        :param chroot:      a path to use as a fake root directory, behaves similar to a real chroot. used only when
                            concrete_fs is set to True.
        :return:            The entry state.
        :rtype:             simuvex.SimState
        """

        return self._project._simos.state_entry(**kwargs)

    def full_init_state(self, **kwargs):
        return self._project._simos.state_full_init(**kwargs)

    def path(self, state=None, **options):
        if state is None:
            state = self.entry_state(**options)

        return Path(self._project, state)

    def path_group(self, thing=None, **kwargs):
        if thing is None:
            thing = [self.path()]

        if isinstance(thing, (list, tuple)):
            thing = list(thing)
            for i, val in enumerate(thing):
                if isinstance(val, SimState):
                    thing[i] = self.path(val)
                elif not isinstance(val, Path):
                    raise AngrError("Bad type to initialize path group: %s" % repr(val))
        elif isinstance(thing, Path):
            thing = [thing]
        elif isinstance(thing, SimState):
            thing = [self.path(thing)]
        else:
            raise AngrError("BadType to initialze path group: %s" % repr(thing))

        return PathGroup(self._project, active_paths=thing, **kwargs)

    def callable(self, addr, concrete_only=False, prototype=None, base_state=None, toc=None):
        """
        Callable is a representation of a function in the binary that can be interacted with like a native python
        function.

        :param addr:            The address of the function to use.
        :param concrete_only:   Optional: Throw an exception if the execution splits into multiple paths.
        :param prototype:       Optional: A SimTypeFunction instance describing the functions args and return type.
        :param base_state:      Optional: The state from which to do these runs.
        :param toc:             Optional: The address of the table of contents for ppc64.
        """
        return Callable(self._project, addr, concrete_only, prototype, base_state, toc)

    callable.PointerWrapper = Callable.PointerWrapper



from .lifter import Lifter
from .errors import AngrExitError, AngrError, AngrValueError
from .path import Path
from .path_group import PathGroup
from .knowledge import HookNode
