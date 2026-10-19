""Grow a Garden – streamlit run app.py
Cần file game.html cùng thư mục.
Tùy chọn: music_b64.txt (base64 mp3) để có nhạc nền.
"""
from __future__ import annotations
import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

DEFAULT = {
    "coins": 100, "xp": 0, "level": 1,
    "seeds": {
        "carrot": 3, "strawberry": 1, "tomato": 0, "blueberry": 0,
        "watermelon": 0, "pumpkin": 0, "dragonfruit": 0, "moonflower": 0,
    },
    "produce": {}, "plots": {},
    "tools": {"watering_can": 1, "shovel": 1},
    "pet": None, "egg": None, "petLastDig": 0,
    "appearance": {"shirt": "#3b82f6", "pants": "#1e3a5f", "skin": "#f5c6a5"},
    "stats": {"planted": 0, "harvested": 0, "sold": 0},
    "codes": {}, "placedSprinklers": [],
}

HERE = Path(__file__).resolve().parent
GAME_PATH = HERE / "game.html"
MUSIC_PATH = HERE / "music_b64.txt"

st.set_page_config(
    page_title="Grow a Garden",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """<style>
    [data-testid="stAppViewContainer"]{background:#0b1a12}
    .block-container{padding:.15rem!important;max-width:100%!important}
    #MainMenu,footer,header{visibility:hidden}
    </style>""",
    unsafe_allow_html=True,
)

if "player" not in st.session_state:
    st.session_state.player = DEFAULT

if not GAME_PATH.exists():
    st.error("Không tìm thấy game.html — để file này cùng thư mục với app.py")
    st.stop()

music_b64 = ""
if MUSIC_PATH.exists():
    music_b64 = MUSIC_PATH.read_text(encoding="utf-8").strip()

html = GAME_PATH.read_text(encoding="utf-8")
html = html.replace(
    "/*__SAVE_INJECT__*/",
    f"window.__INITIAL_SAVE__ = {json.dumps(st.session_state.player)}; "
    f"window.__MUSIC_B64__ = {json.dumps(music_b64)};",
)
components.html(html, height=820, scrolling=False)
