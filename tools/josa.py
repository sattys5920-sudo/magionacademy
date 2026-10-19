# 이름 변수 뒤 조사: {player|이/가}처럼 쓰면 실제 이름의 마지막 글자 받침을 보고 앞(받침 있음)·뒤(받침 없음)를 골라요
# 엔진(public/index.html의 josaPick)과 같은 규칙. 검증·대본 문서·데이터 고치기에 써요
import re
# 영문·숫자로 끝나는 이름: 한글로 읽었을 때 받침이 있는지 (L·R·1·7·8은 ㄹ 받침)
ALNUM_BAT = {**{c: False for c in 'ABCDEFGHIJKOPQSTUVWXYZ'}, **{c: True for c in 'LMNR'}, '0': True, '1': True, '2': False, '3': True, '4': False, '5': False, '6': True, '7': True, '8': True, '9': False}
ALNUM_RIEUL = set('LR178')
VAR = re.compile(r'\{([a-z_]+(?:\.[a-z_]+)?)(?:\|([^/{}]+)/([^{}]+))?\}')

def batchim(name):
    """(받침 있음, ㄹ 받침) — 끝의 기호·공백은 건너뛰고, 판단이 안 되면 받침 없음"""
    for ch in reversed(str(name)):
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3:
            j = (o - 0xAC00) % 28
            return j > 0, j == 8
        u = ch.upper()
        if u in ALNUM_BAT: return ALNUM_BAT[u], u in ALNUM_RIEUL
    return False, False

def pick(name, a, b):
    bat, rieul = batchim(name)
    if a == '으로' and b == '로': return '로' if (not bat or rieul) else '으로'
    return a if bat else b

# 변수 바로 뒤에 붙은 한글 묶음 → (조사 쌍, 남는 글자). 데이터 고치기와 검사에 같이 써요
RUN = {
 '이': ('이', '가', ''), '가': ('이', '가', ''), '은': ('은', '는', ''), '는': ('은', '는', ''), '는요': ('은', '는', '요'), '은요': ('은', '는', '요'),
 '을': ('을', '를', ''), '를': ('을', '를', ''), '과': ('과', '와', ''), '와': ('과', '와', ''), '이랑': ('이랑', '랑', ''), '랑': ('이랑', '랑', ''),
 '으로': ('으로', '로', ''), '로': ('으로', '로', ''), '이에요': ('이에요', '예요', ''), '예요': ('이에요', '예요', ''), '이나': ('이나', '나', ''), '나': ('이나', '나', ''),
 '이라는': ('이라는', '라는', ''), '라는': ('이라는', '라는', ''), '이라면': ('이라면', '라면', ''), '라면': ('이라면', '라면', ''),
 '이다': ('이다', '다', ''), '다': ('이다', '다', ''), '이었다': ('이었', '였', '다'), '였다': ('이었', '였', '다'), '이구나': ('이구나', '구나', ''), '구나': ('이구나', '구나', ''),
 '이요': ('이요', '요', ''), '요': ('이요', '요', ''), '이네': ('이네', '네', ''), '네': ('이네', '네', ''),
}
# 함수 없이 변수 바로 뒤에 오면 틀릴 수 있는 조사 (검사용)
BARE = re.compile(r'\{[a-z_]+(?:\.[a-z_]+)?\}(이에요|예요|이랑|랑|으로|로|이야|야|이나|나|이|가|은|는|을|를|과|와|아|라는|라면|구나|였)(?![가-힣])|\{[a-z_]+(?:\.[a-z_]+)?\}(이랑|으로|이에요|이라는|이라면|이었)')
PAREN = re.compile(r'\((을|를|이|가|은|는|과|와|으|으로|아|야|이랑|랑|이에요|이야|이나)\)')

def render(t, values):
    """values: 변수 이름 → 값. 이름이 들어간 자리를 표시해서 돌려줘요 [(시작, 끝, 이름)]"""
    out, marks, i = [], [], 0
    for m in VAR.finditer(t):
        out.append(t[i:m.start()]); k = m.group(1)
        v = values.get(k, values.get(k.split('.')[0] + '.name', k) if k.endswith('.name') else k)
        pos = sum(len(x) for x in out); out.append(v); marks.append((pos, pos + len(v), v))
        if m.group(2) is not None: out.append(pick(v, m.group(2), m.group(3)))
        i = m.end()
    out.append(t[i:])
    return ''.join(out), marks

WRONG_BAT = re.compile(r'^(가|는|를|와|랑(?!이)|예요|였)(?![가-힣])|^(가|는|를|와|예요)')   # 받침 있는 이름 뒤에 오면 틀림
WRONG_NOBAT = re.compile(r'^(이(?!다|야|네|요|었|구나|라|에요|랑|나)|은|을|과|이랑|으로|이에요|이었|이라는|이라면|이구나)')   # 받침 없는 이름 뒤에 오면 틀림

def check_rendered(text, marks):
    errs = []
    for s, e, v in marks:
        bat, rieul = batchim(v); after = text[e:e + 4]
        if bat:
            if WRONG_BAT.match(after): errs.append(f'「{v}{after[:3]}」')
            if after.startswith('로') and not rieul and not after.startswith('로서'): errs.append(f'「{v}{after[:3]}」')
        else:
            if WRONG_NOBAT.match(after): errs.append(f'「{v}{after[:3]}」')
    return errs
