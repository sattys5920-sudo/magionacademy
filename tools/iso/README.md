# 걸어 다니는 학교 그림 만들기 (별빛고등학교)

Python 3 + Pillow. `school.py`는 `world.py`의 그리기 도구를, 그 둘은 `px.py`가 아닌 자체 코드를 써요.

```
python3 school.py    # 학교 캠퍼스(72×72): out/school_bg.png, out/school_obj.png, out/school.json
python3 sci.py       # 과학실: out/sci_bg.png, out/sci_obj.png, out/sci.json
python3 chars2.py    # 교복 학생 걷기 그림: out/students2.png (→ public/art/iso/students.png)
python3 build_school.py ../../public/walk.html
```
만든 png는 `public/art/iso/`에 복사해요.
이전 마법학교 시안: `world.py`(72×72), `campus.py`(34×34), `room.py`(물약 연구실), `chars.py`, `world2_tpl.html`, `build_walk.py`
