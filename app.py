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
    </style>
    """, unsafe_allow_html=True)

# 2. 만세력 분석 로직
def get_saju_analysis(y, m, d, t_str, gender, is_lunar):
    calendar = KoreanLunarCalendar()
    if is_lunar:
        calendar.setLunarDate(y, m, d, False)
    else:
        calendar.setSolarDate(y, m, d)
    
    ganji = calendar.getChineseGapJaString().split()
    
    time_map = {
        "시간 모름": "??", "00:00": "庚子", "01:00": "辛丑", "02:00": "辛丑", "03:00": "壬寅",
        "04:00": "壬寅", "05:00": "癸卯", "06:00": "癸卯", "07:00": "甲辰", "08:00": "甲辰",
        "09:00": "乙巳", "10:00": "乙巳", "11:00": "丙午", "12:00": "丙午", "13:00": "丁未",
        "14:00": "丁未", "15:00": "戊申", "16:00": "戊申", "17:00": "己酉", "18:00": "己酉",
        "19:00": "庚戌", "20:00": "庚戌", "21:00": "辛亥", "22:00": "辛亥", "23:00": "庚子"
    }
    siju = time_map.get(t_str[:5], "??")

    # 결과 메시지 조립 (따옴표 에러 방지를 위해 단순화)
    pos = "리드 기타 (Lead Guitar)" if "庚" in ganji[1] or "辛" in ganji[0] else "프론트맨"
    luck = "양(陽)의 기운이 강한 리더형" if gender == "남성" else "음(陰)의 기운이 섬세한 예술가형"

    return {
        "pillars": [siju, ganji[2], ganji[1], ganji[0]],
        "luck": luck,
        "position": pos
    }

# 3. 메인 UI
st.title("🏯 정통 뮤지션 만세력")
st.write("성별과 생년월일을 상세히 입력하여 당신의 음악적 천명을 확인하세요.")

with st.container():
    name = st.text_input("성함", value="임환백")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    col_y, col_m, col_d = st.columns(3)
    with col_y:
        y_in = st.number_input("출생 연도", min_value=1900
