import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# CSS: 디자인 레이아웃 및 폰트 설정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; margin-bottom: 10px; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 25px; border-radius: 18px; border-left: 6px solid #4A5568; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .music-card { background-color: #FDF2F8; padding: 25px; border-radius: 18px; border-left: 6px solid #D53F8C; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(213,63,140,0.1); }
    .position-card { background-color: #FFFBEB; padding: 25px; border-radius: 18px; border-left: 6px solid #D97706; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(217,119,6,0.1); }
    .target-year-card { background-color: #F0F9FF; padding: 25px; border-radius: 18px; border-left: 6px solid #3182CE; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(49,130,206,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 20px; gap: 5px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; font-size: 0.95rem; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 15px; border-radius: 15px; margin-bottom: 20px; }
    .ohaeng-item { text-align: center; flex: 1; }
    h1 { font
