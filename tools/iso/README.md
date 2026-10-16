# 걸어 다니는 학교 그림 만들기

Python 3 + Pillow, 그리고 다른 픽셀 그림 스크립트의 `px.py`가 필요해요 (`chars.py`는 필요 없음).

```
python3 room.py      # 물약 연구실: out/lab_bg.png, out/lab_obj.png, out/lab.json
python3 campus.py    # 캠퍼스: out/campus_bg.png, out/campus_obj.png, out/campus.json
python3 chars.py     # 학생 걷기 그림: out/students.png
python3 build_walk.py ../../public/walk.html   # 위 json을 world_tpl.html에 넣어 walk.html 만들기
```
만든 png는 `public/art/iso/`에 복사해요.
