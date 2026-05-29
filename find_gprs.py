import sys, os

so_files = [f for f in os.listdir('target/debug/deps') if f.startswith('libpywellen') and f.endswith('.so')]
if so_files:
    src = os.path.abspath(f'target/debug/deps/{so_files[0]}')
    dst = 'target/debug/deps/pywellen.so'
    if not os.path.exists(dst):
        os.symlink(src, dst)
sys.path.insert(0, 'target/debug/deps')

from pywellen import Waveform

w = Waveform('../scr1_trace/build/run_AHB_MAX_imc_IPIC_1_TCM_1_VIRQ_1_TRACE_1/simx.fst', True, True)
h = w.hierarchy
all_vars = list(h.all_vars())

print(f'Total vars: {len(all_vars)}')

# Find tracelog / mprf related signals
mprf = [v.full_name(h) for v in all_vars if 'mprf2trace' in v.full_name(h) or 'tracelog' in v.full_name(h)]
print(f'\nFound {len(mprf)} mprf/tracelog vars:')
for v in mprf[:40]:
    print(' ', v)

# Also look for the PC signal
pc_vars = [v.full_name(h) for v in all_vars if 'update_pc' in v.full_name(h)]
print(f'\nFound {len(pc_vars)} update_pc vars:')
for v in pc_vars[:10]:
    print(' ', v)

print('\nWaveform methods with "signal" or "create":')
print([m for m in dir(w) if 'signal' in m.lower() or 'create' in m.lower()])

# Test create_new_signal
try:
    z = w.create_new_signal([0], [0], 32)
    print('\ncreate_new_signal([0],[0],32) works:', z)
except Exception as e:
    print('\ncreate_new_signal failed:', e)
