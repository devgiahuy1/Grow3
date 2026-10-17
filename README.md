# Grow a Garden – 3D (Roblox-style)

Game mô phỏng trồng cây 3D, phong cách low-poly giống Roblox, chạy bằng **Python Streamlit** + **Three.js (WebGL)**.

## Chạy game

```bash
pip install -r requirements.txt
streamlit run app.py
```

Mở trình duyệt tại địa chỉ Streamlit in ra (thường `http://localhost:8501`).

## Điều khiển

| Phím / thao tác | Hành động |
|-----------------|-----------|
| **W A S D** | Di chuyển |
| **Shift** | Chạy |
| **Space** | Nhảy |
| **E** | Tương tác (gieo / tưới / thu hoạch / shop) |
| **Chuột** | Xoay camera (click vào canvas hoặc pointer lock) |
| **1–8** | Chọn hạt trên hotbar |
| **Q** | Cầm bình tưới |

**Mobile:** joystick trái, nút Jump / Run / E bên phải, vuốt nửa phải màn hình để xoay camera.

## Gameplay

1. Nhấn **Play**.
2. Đi tới **cửa hàng** (nhà đỏ bên phải), nhấn **E** mua hạt.
3. Chọn hạt (hotbar hoặc Kho → Cầm), đi tới **ô đất nâu** trong hàng rào.
4. Nhấn **E** để gieo. Tưới bằng E (cầm bình tưới) để cây lớn nhanh hơn.
5. Khi cây chín (100%), **E** để thu hoạch.
6. **Hái nhiều lần:** dâu tây, cà chua, việt quất, thanh long vẫn còn cây sau khi hái, trái mọc lại sau ~40% thời gian lớn. Cà rốt, dưa hấu, bí ngô, hoa mặt trăng chỉ hái 1 lần.
7. Đi tới **NPC tím** để bán nông sản.

## File

- `app.py` – Streamlit shell, lưu `player_save.json`
- `game.html` – thế giới 3D Three.js, nhân vật, va chạm, UI
- Tiến trình chính lưu **localStorage** trình duyệt (`gag3d-v1`); nút **Đồng bộ** ghi JSON phía server khi dùng Streamlit

## Ghi chú kỹ thuật

- Three.js 0.160 qua CDN (unpkg), không cần API key.
- Camera góc thứ ba theo nhân vật; va chạm AABB với hàng rào, cây, hồ, nhà.
- Cây có 4 giai đoạn mesh 3D; thời gian phát triển tính theo giây thực.
