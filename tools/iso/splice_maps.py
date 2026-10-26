# 지도만 다시 만들어 public/world.js 의 MAPS 줄에 끼워 넣어요 (world.js 는 손으로 고친 부분이 많아서 world_tpl.js 로 통째로 다시 만들면 안 돼요)
#   python3 tools/iso/dcave.py && python3 tools/iso/splice_maps.py
import os, subprocess, sys
I = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(I, '..', '..'); WJ = os.path.join(ROOT, 'public', 'world.js'); TMP = os.path.join(ROOT, 'public', 'world_new.tmp.js')
subprocess.run([sys.executable, os.path.join(I, 'build_halloween.py'), TMP], check=True, cwd=ROOT)
L = open(WJ).read().split('\n'); N = open(TMP).read().split('\n')
i = [k for k, l in enumerate(L) if l.startswith('const MAPS = ')][0]; j = [k for k, l in enumerate(N) if l.startswith('const MAPS = ')][0]
L[i] = N[j]; open(WJ, 'w').write('\n'.join(L)); os.remove(TMP); print('MAPS 줄을 바꿨어요')
