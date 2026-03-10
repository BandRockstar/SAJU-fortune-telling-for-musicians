import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="2080 뮤지션 만세력 마스터", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { color: #ffffff !important; }
    label { color: #d4af37 !important; font-weight: bold !important; }
    .result-card { background-color: #1a222f; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 20px; }
    .res-title { color: #d4af37 !important; font-size: 1.6rem; font-weight: bold; border-bottom: 1px solid #d4af37; padding-bottom: 10px; }
    .res-body { color: #ffffff !important; line-height: 1.8; font-size: 1.1rem; margin-top: 15px; }
    .res-sub { color: #ffd700 !important; font-weight: bold; display: block; margin-top: 15px; }
    .pillar-box { background: #0b111a; padding: 15px; border-radius: 10px; border: 2px solid #d4af37; text-align: center; }
    .pillar-ganji { color: #d4af37; font-size: 1.5rem; font-weight: bold; }
    .instrument-tag { background: #d4af37; color: #000; padding: 4px 12px; border-radius: 8px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 정밀 시두법 및 악기 매칭 함수
def get_saju_details(day_gan, time_str):
    if time_str == "시간 모름": return "??", "전천후 뮤지션"
    h = int(time_str[:2])
    
    jis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    h_map = {23:0, 0:0, 1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:9, 19:10, 20:10, 21:11, 22:11}
    idx = h_map.get(h, 0)
    
    start_gan_map = {"甲": 0, "己": 0, "乙": 2, "庚": 2, "丙": 4, "辛": 4, "丁": 6, "壬": 6, "戊": 8, "癸": 8}
    gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    start_idx = start_gan_map.get(day_gan, 0)
    siju = gans[(start_idx + idx) % 10] + jis[idx]
    
    # 악기 성향 (오행 및 지지 기반)
    inst_map = {"子":"건반/미디", "丑":"묵직한 베이스", "寅":"파워풀 기타", "卯":"섬세한 리듬기타", "辰":"프론트맨/보컬", "巳":"드럼/타악기", "午":"화려한 리드기타", "未":"부드러운 베이스", "申
