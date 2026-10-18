# 머리 40종: 앞모습·뒷모습·옆모습 칸 고르기 (시트 이름, 칸 번호)
FRONT = [('hairA', i) for i in range(10)] + [('hairB', i) for i in range(10)] + [('hairC', i) for i in range(10)] + [('hairD', i) for i in (0, 1, 2, 4, 5, 6, 7, 8, 9, 10)]
BACK = {20 + i: ('hairC', 10 + i) for i in range(10)}          # 21~30번은 진짜 뒷모습, 나머지는 앞모습에서 만들어요
SIDE = [('side%d' % (1 + i // 10), i % 10) for i in range(40)]
SIDE[3] = ('side3', 6)   # 4번 올림머리 옆모습이 양쪽 똥머리로 나와서 27번(정수리 묶음)으로
