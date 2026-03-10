import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
from datetime import datetime

# 1. 페이지 기본 설정 및 디자인 (전문가용 골드&블랙 테마)
st.set_page_config(page_title="정통 뮤지션 만세력 v1.0", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #d4af37; color: #000; font-weight: bold; height: 3.5rem; border: none; }
    .saju-card { background-color: #1f2937; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin: 10px 0; text-align: center; }
    .pillar-box { background: #111827; padding: 10px; border-radius: 8px; border: 1px solid #374151; }
    .element-tag { padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. 만세력 로직 라이브러리 연동
def get_full_saju(date, time_str, is_lunar):
    calendar = KoreanLunarCalendar()
    if is_lunar:
        calendar.setLunarDate(date.year, date.month, date.day, False)
    else:
        calendar.setSolarDate(date.year, date.month, date.day)
    
    # 간지 데이터 추출
    ganji = calendar.getChineseGapJaString().split() # [연, 월, 일]
    
    # 시간대별 시주(時柱) 매칭 (간략화된 전통 방식 적용)
    time_map = {
        "시간 모름": "??", "00:00": "庚子", "01:00": "辛丑", "02:00": "辛丑", "03:00": "壬寅",
        "04:00": "壬寅", "05:00": "癸卯", "06:00": "癸卯", "07:00": "甲辰", "08:00": "甲辰",
        "09:00": "乙巳", "10:00": "乙巳", "11:00": "丙午", "12:00": "丙午", "13:00": "丁未",
        "14:00": "丁未", "15:00": "戊申", "16:00": "戊申", "17:00": "己酉", "18:00": "己酉",
        "19:00": "庚戌", "20:00": "庚戌", "21:00": "辛亥", "22:00": "辛亥", "23:00": "庚子"
    }
    siju = time_map.get(time_str[:5], "??")

    # 뮤지션 성향 분석 로직 (사용자님의 '신유년 경인월 병진일' 성향 반영)
    if "庚
