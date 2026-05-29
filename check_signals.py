import sys, os
# pywellen is a Rust .so with a decorated name; find and symlink it
so_files = [f for f in os.listdir('target/debug/deps') if f.startswith('libpywellen') and f.endswith('.so')]
if so_files:
    src = os.path.abspath(f'target/debug/deps/{so_files[0]}')
    dst = 'target/debug/deps/pywellen.so'
    if not os.path.exists(dst):
        os.symlink(src, dst)
sys.path.insert(0, 'target/debug/deps')
from pywellen import Waveform

wave_path = '../scr1_trace/build/run_AHB_MAX_imc_IPIC_1_TCM_1_VIRQ_1_TRACE_1/simx.fst'
try:
    w = Waveform(wave_path, True, True)
    print("Loaded OK")
    # Try the PC path from the ibex mapping
    try:
        pc = w.get_signal_from_path("TOP.scr1_top_tb_ahb.i_top.i_core_top.i_pipe_top.i_pipe_exu.update_pc")
        print("PC signal found:", pc)
    except Exception as e:
        print("PC signal NOT found:", e)
    # Search all vars for mprf-related paths
    all_vars = list(w.hierarchy.all_vars())
    h = w.hierarchy
    print("Total vars:", len(all_vars))
    # find anything with pipe in the path
    pipe_vars = [v for v in all_vars if 'pipe' in v.full_name(h)]
    print(f"Pipe vars ({len(pipe_vars)}):")
    for v in pipe_vars:
        print(" ", v.full_name(h))
except Exception as e:
    print("Error loading waveform:", e)
