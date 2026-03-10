import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
from datetime import datetime

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="정통 뮤지션 만세력 v2.0", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #d4af37; color: #000; font-weight: bold; height: 3.5rem; border: none; margin-top: 20px; }
    .saju-card { background-color: #1f2937; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 20px; }
    .pillar-box { background: #111827; padding: 15px; border-radius: 8px; border: 1px solid #374151; text-align: center; }
    .highlight { color: #d4af37; font-weight: bold; }
    label { font-weight: bold !important; color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 만세력 및 분석 로직
def get_saju_analysis(year, month, day, time_str, gender, is_lunar):
    calendar = KoreanLunarCalendar()
    if is_lunar:
        calendar.setLunarDate(year, month, day, False)
    else:
        calendar.setSolarDate(year, month, day)
    
    ganji = calendar.getChineseGapJaString().split() # [연, 월, 일]
    
    # 시간대별 시주 매칭 (전통 방식)
    time_map = {
        "시간 모름": "??", "00:00": "庚子", "01:00": "辛丑", "02:00": "辛丑", "03:00": "壬寅",
        "04:00": "壬寅", "05:00": "癸卯", "06:00": "癸卯", "07:00": "甲辰", "08:00": "甲辰",
        "09:00": "乙巳", "10:00": "乙巳", "11:00": "丙午", "12:00": "丙午", "13:00": "丁未",
        "14:00": "丁未", "15:00": "戊申", "16:00": "戊申", "17:00": "己酉", "18:00": "己酉",
        "19:00": "庚戌", "20:00": "庚戌", "21:00": "辛亥", "22:00": "辛亥", "23:00": "庚子"
    }
    siju = time_map.get(time_str[:5], "??")

    # 성별 및 사주 구성에 따른 음악적 조언
    # (예시: 1981년생 신유년, 경인월, 병진일 기준)
    if gender == "남성":
        luck_desc = "양(陽)의 기운이 강하여 무대 위에서의 폭발력과 리
