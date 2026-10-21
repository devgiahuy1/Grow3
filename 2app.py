"""Grow a Garden - Multiplayer Room Version
streamlit run app.py
Can file game.html cùng thư mục.
Tùy chọn: music_b64.txt để có nhạc nền.
"""
from __future__ import annotations

import json
import random
import string
import time
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

# ====================== DEFAULT SAVE ======================
DEFAULT = {
    "coins": 100,
    "xp": 0,
    "level": 1,
    "seeds": {
        "carrot": 3,
        "strawberry": 1,
        "tomato": 0,
        "blueberry": 0,
        "watermelon": 0,
        "pumpkin": 0,
        "dragonfruit": 0,
        "moonflower": 0,
    },
    "produce": {},
    "plots": {},
    "tools": {"watering_can": 1, "shovel": 1},
    "pet": None,
    "egg": None,
    "petLastDig": 0,
    "appearance": {"shirt": "#3b82f6", "pants": "#1e3a5f", "skin": "#f5c6a5"},
    "stats": {"planted": 0, "harvested": 0, "sold": 0},
    "codes": {},
    "placedSprinklers": [],
}

HERE = Path(__file__).resolve().parent
GAME_PATH = HERE / "game.html"
MUSIC_PATH = HERE / "music_b64.txt"

st.set_page_config(
    page_title="Grow a Garden",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== SHARED ROOM STATE ======================
@st.cache_resource
def get_rooms() -> dict[str, Any]:
    """Global rooms store shared across all sessions."""
    return {}


def generate_room_code(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    chars = chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "")
    return "".join(random.choices(chars, k=length))


def cleanup_rooms(rooms: dict, max_age_sec: int = 3600 * 6) -> None:
    """Xóa phòng quá cũ hoặc không còn người."""
    now = time.time()
    to_delete = []
    for code, room in list(rooms.items()):
        players = room.get("players", {})
        offline = [uid for uid, p in players.items() if now - p.get("last_seen", 0) > 90]
        for uid in offline:
            players.pop(uid, None)
        if not players and now - room.get("created_at", now) > 300:
            to_delete.append(code)
        elif now - room.get("created_at", now) > max_age_sec:
            to_delete.append(code)
    for code in to_delete:
        rooms.pop(code, None)


# ====================== SESSION STATE ======================
if "player" not in st.session_state:
    st.session_state.player = DEFAULT.copy()

if "username" not in st.session_state:
    st.session_state.username = ""

if "room_code" not in st.session_state:
    st.session_state.room_code = None

if "player_id" not in st.session_state:
    st.session_state.player_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


# ====================== STYLE ======================
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"]{background:#0b1a12}
    .block-container{padding-top:0.6rem!important;max-width:100%!important}
    #MainMenu,footer,header{visibility:hidden}
    div[data-testid="stSidebar"] {background: #0f2418; border-right: 2px solid #2d5a3a;}
    .room-card {
        background: linear-gradient(180deg, #1a3d28, #0f2418);
        border: 2px solid #4ade80;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
        color: #e8ffe8;
        font-family: system-ui, sans-serif;
    }
    .player-chip {
        display: inline-block;
        background: #14532d;
        border: 1px solid #4ade80;
        border-radius: 20px;
        padding: 3px 10px;
        margin: 3px 4px 3px 0;
        font-size: 13px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

rooms = get_rooms()
cleanup_rooms(rooms)

# ====================== SIDEBAR - ROOM SYSTEM ======================
with st.sidebar:
    st.markdown("## 🌱 Grow a Garden")
    st.caption("Multiplayer Room")

    username = st.text_input(
        "Tên của bạn",
        value=st.session_state.username or "",
        max_chars=16,
        placeholder="Nhập tên để vào phòng...",
        key="username_input",
    )
    if username.strip():
        st.session_state.username = username.strip()[:16]

    st.divider()

    # ===== ĐANG Ở TRONG PHÒNG =====
    if st.session_state.room_code and st.session_state.room_code in rooms:
        room = rooms[st.session_state.room_code]
        code = st.session_state.room_code

        pid = st.session_state.player_id
        if pid not in room["players"]:
            room["players"][pid] = {
                "name": st.session_state.username or "Người chơi",
                "last_seen": time.time(),
                "joined_at": time.time(),
            }
        else:
            room["players"][pid]["last_seen"] = time.time()
            if st.session_state.username:
                room["players"][pid]["name"] = st.session_state.username

        st.success(f"**Phòng: `{code}`**")
        st.caption(f"Chủ phòng: {room.get('owner_name', '?')}")

        now = time.time()
        online = []
        for uid, p in list(room["players"].items()):
            if now - p.get("last_seen", 0) <= 90:
                online.append(p.get("name", "???"))
            else:
                room["players"].pop(uid, None)

        st.markdown("**Người trong phòng:**")
        if online:
            chips = " ".join(f'<span class="player-chip">👤 {n}</span>' for n in online)
            st.markdown(chips, unsafe_allow_html=True)
        else:
            st.caption("Chỉ có mình bạn...")

        st.caption(f"Online: **{len(online)}** người")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Làm mới", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("🚪 Rời phòng", use_container_width=True, type="primary"):
                room["players"].pop(st.session_state.player_id, None)
                st.session_state.room_code = None
                st.rerun()

        st.divider()
        st.info("Mỗi người vẫn có **vườn riêng**. Tiền / hạt / level không dùng chung.")

    # ===== CHƯA VÀO PHÒNG =====
    else:
        st.markdown("### Tạo / Vào phòng")

        if not st.session_state.username:
            st.warning("Hãy nhập tên trước khi tạo hoặc vào phòng.")
        else:
            if st.button("✨ Tạo phòng mới", use_container_width=True, type="primary"):
                code = generate_room_code()
                while code in rooms:
                    code = generate_room_code()
                rooms[code] = {
                    "owner_id": st.session_state.player_id,
                    "owner_name": st.session_state.username,
                    "created_at": time.time(),
                    "players": {
                        st.session_state.player_id: {
                            "name": st.session_state.username,
                            "last_seen": time.time(),
                            "joined_at": time.time(),
                        }
                    },
                }
                st.session_state.room_code = code
                st.rerun()

            st.markdown("---")
            join_code = st.text_input(
                "Mã phòng",
                max_chars=6,
                placeholder="Ví dụ: K7P2M",
                key="join_code_input",
            ).strip().upper()

            if st.button("🚪 Vào phòng", use_container_width=True):
                if not join_code:
                    st.error("Nhập mã phòng")
                elif join_code not in rooms:
                    st.error("Không tìm thấy phòng này (có thể đã hết hạn)")
                else:
                    room = rooms[join_code]
                    room["players"][st.session_state.player_id] = {
                        "name": st.session_state.username,
                        "last_seen": time.time(),
                        "joined_at": time.time(),
                    }
                    st.session_state.room_code = join_code
                    st.rerun()

        st.divider()
        st.caption("Phòng sẽ tự xóa nếu không còn ai sau vài phút.")

# ====================== MAIN GAME ======================
if not GAME_PATH.exists():
    st.error("Không tìm thấy game.html — hãy để file này cùng thư mục với app.py")
    st.stop()

music_b64 = ""
if MUSIC_PATH.exists():
    music_b64 = MUSIC_PATH.read_text(encoding="utf-8").strip()

html = GAME_PATH.read_text(encoding="utf-8")

html = html.replace(
    "/*__SAVE_INJECT__*/",
    "window.__INITIAL_SAVE__ = "
    + json.dumps(st.session_state.player)
    + "; window.__MUSIC_B64__ = "
    + json.dumps(music_b64)
    + "; window.__ROOM_CODE__ = "
    + json.dumps(st.session_state.room_code)
    + "; window.__USERNAME__ = "
    + json.dumps(st.session_state.username or "")
    + ";",
)

if st.session_state.room_code:
    room = rooms.get(st.session_state.room_code)
    if room:
        online_count = sum(
            1 for p in room.get("players", {}).values() if time.time() - p.get("last_seen", 0) <= 90
        )
        st.markdown(
            f"""
            <div class="room-card">
                <b>🏠 Phòng <code>{st.session_state.room_code}</code></b> &nbsp;·&nbsp;
                {online_count} người đang chơi &nbsp;·&nbsp;
                Bạn: <b>{st.session_state.username or "???"}</b>
                <br/><span style="font-size:12px;opacity:0.8">Vườn của mỗi người vẫn riêng — chỉ cùng map thôi</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

components.html(html, height=820, scrolling=False)
