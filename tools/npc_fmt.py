# 하트 이벤트 JSON을 저장할 때 쓰는 모양: 머리 4 줄 + script/cold 한 줄에 명령 하나 (git diff가 줄 단위로 깔끔하게 나와요)
#   python3 tools/npc_fmt.py <파일...>  → 그 모양으로 다시 써요 (내용은 그대로)
#   스크립트에서: from npc_fmt import dump; open(fn, 'w').write(dump(ev))
import json, sys
def j(o): return json.dumps(o, ensure_ascii=False)
def dump(ev):
    head = ['id', 'npc', 'heart', 'title']; out = ['{', '  ' + ', '.join(f'{j(k)}: {j(ev[k])}' for k in head if k in ev) + ',']
    keys = [k for k in ev if k not in head]
    for n, k in enumerate(keys):
        end = ',' if n < len(keys) - 1 else ''
        if k in ('script', 'cold', 'fail') and isinstance(ev[k], list):
            out.append(f'  {j(k)}: [')
            out += ['    ' + j(s) + (',' if i < len(ev[k]) - 1 else '') for i, s in enumerate(ev[k])]
            out.append('  ]' + end)
        else: out.append(f'  {j(k)}: {j(ev[k])}{end}')
    return '\n'.join(out + ['}']) + '\n'
if __name__ == '__main__':
    for fn in sys.argv[1:]: ev = json.load(open(fn)); open(fn, 'w').write(dump(ev))
