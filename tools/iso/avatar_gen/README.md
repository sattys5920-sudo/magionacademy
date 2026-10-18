# 캐릭터 부품 만들기 (생성 이미지 → 게임 부품)

`src/`의 생성 이미지(머리 48개 중 40개, 얼굴 24개에서 눈 15·입 10, 교복 5종 앞뒤)를 원래 픽셀 크기로 줄이고, 층별로 나눠요.

```
python3 extract.py    # src/*.png → cells.pkl (칸마다 격자를 찾아 줄이고 픽셀 종류를 나눠요)
python3 assemble.py   # cells.pkl → out/avatar_parts.png + out/avatar_parts.json
python3 prev2.py 1 8  # 아무 조합 8개 미리보기 → out/prev.png
```
- 색을 고를 수 있는 곳(피부·눈·머리·신발·교복 기숙사 색)은 회색 열쇠색(240/200/150/100)으로 저장해요. 게임이 고른 팔레트로 칠해요.
- 교복의 마젠타 부분 = 기숙사 색, 회색 옷감 = 학교 공통색.
- 걷기 프레임은 다리를 2칸 들어서 만들어요. 뒷머리는 앞머리 모양에서 만들어요.
- 만든 두 파일을 `../out/`(빌드 스크립트가 읽는 곳)에 두고 `build_halloween.py`를 돌려요. png는 `public/art/iso/`에도 복사해요.
