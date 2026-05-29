from pywellen import Waveform, Signal
from typing import List, Dict


def get_gdb_signals(wave: Waveform) -> Dict[str, Signal]:
    pc = wave.get_signal_from_path(
        "TOP.scr1_top_tb_ahb.i_top.i_core_top.i_pipe_top.i_tracelog.exu2trace_update_pc_i"
    )
    gprs = {}
    for i in range(32):
        try:
            gprs[f"x{i}"] = wave.get_signal_from_path(
                f"TOP.scr1_top_tb_ahb.i_top.i_core_top.i_pipe_top.i_tracelog.mprf2trace_int_i.[{i}]"
            ).sliced(0, 31)
        except Exception:
            pass  # missing GPRs (e.g. x0 hardwired zero, untraced callee-saved regs) handled in Rust

    rv = {"pc": pc, **gprs}
    return rv


def get_misc_signals(wave: Waveform) -> List[Signal]:
    return [
        wave.get_signal_from_path(
            "TOP.ibex_simple_system.u_top.u_ibex_top.u_ibex_core.wb_stage_i.pc_wb_o"
        )
    ]
