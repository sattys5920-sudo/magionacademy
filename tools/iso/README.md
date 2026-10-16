# 걸어 다니는 학교 그림 만들기

Python 3 + Pillow, 그리고 다른 픽셀 그림 스크립트의 `px.py`가 필요해요 (`chars.py`는 필요 없음).

```
python3 room.py      # 물약 연구실: out/lab_bg.png, out/lab_obj.png, out/lab.json
python3 world.py     # 넓은 학교 맵(72×72): out/world_bg.png, out/world_obj.png, out/world.json
python3 chars.py     # 학생 걷기 그림: out/students.png
python3 build_walk.py ../../public/walk.html   # 위 json을 world2_tpl.html에 넣어 walk.html 만들기
```
만든 png는 `public/art/iso/`에 복사해요.

`campus.py`, `world_tpl.html`은 이전(34×34) 시안이에요.
