import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
from datetime import datetime

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="정통 뮤지션 만세력 v1.0", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #d4af37; color: #000; font-weight: bold; height: 3.5rem; border: none; }
    .saju-card { background-color: #1f2937; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin: 10px 0; text-align: center; }
    .pillar-box { background: #111827; padding: 10px; border-radius: 8px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

# 2. 만세력 로직 엔진
def get_full_saju(date, time_str, is_lunar):
    calendar = KoreanLunarCalendar()
    if is_lunar:
        calendar.setLunarDate(date.year, date.month, date.day, False)
    else:
        calendar.setSolarDate(date.year, date.month, date.day)
    
    ganji = calendar.getChineseGapJaString().split() # [연, 월, 일]
    
    # 시간대별 시주(時柱) 매칭
    time_map = {
        "시간 모름": "??", "00:00": "庚子", "01:00": "辛丑", "02:00": "辛丑", "03:00": "壬寅",
        "04:00": "壬寅", "05:00": "癸卯", "06:00": "癸卯", "07:00": "甲辰", "08:00": "甲辰",
        "09:00": "乙巳", "10:00": "乙巳", "11:00": "丙午", "12:00": "丙午", "13:00": "丁未",
        "14:00": "丁未", "15:00": "戊申", "16:00": "戊申", "17:00": "己酉", "18:00": "己酉",
        "19:00": "庚戌", "20:00": "庚戌", "21:00": "辛亥", "22:00": "辛亥", "23:00": "庚子"
    }
    siju = time_map.get(time_str[:5], "??")

    # 포지션 분석 (에러 방지를 위해 문자열 체크 방식을 더 안전하게 수정)
    mon_gan = ganji[1] if len(ganji) > 1 else ""
    year_gan = ganji[0] if len(ganji) > 0 else ""
    day_gan = ganji[2] if len(ganji) > 2 else ""

    if "庚" in mon_gan or "辛" in year_gan:
        position, talent = "리드 기타 (Lead Guitar)", "정교한 피킹과 날카로운 톤 메이킹"
    elif "丙" in day_gan or "丁" in day_gan:
        position, talent = "보컬 및 프론트맨", "폭발적인 에너지와 무대 장악력"
    else:
        position, talent = "프로듀서 및 멀티 악기 연주자", "전체적인 사운드 밸런스 조율"

    return {
        "pillars": {"연주": year_gan, "월주": mon_gan, "일주": day_gan, "시주": siju},
        "position": position, "talent": talent
    }

# 3. 메인 UI
st.title("🏯 정통 뮤지션 만세력")
st.subheader("사주 원국 기반 음악적 천명 분석")

with st.container():
    name = st.text_input("이름", value="BandRockstar")
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("출생일", value=datetime(1981, 2, 7))
        is_lunar = st.checkbox("음력 적용")
    with col2:
        time_list = [f"{i:02d}:00 ~ {i:02d}:59" for i in range(24)]
        time_list.insert(0, "시간 모름")
        birth_time = st.selectbox("출생 시간", time_list)

if st.button("운명의 악기 확인하기"):
    result = get_full_saju(birth_date, birth_time, is_lunar)
    st.markdown("---")
    
    cols = st.columns(4)
    labels = ["시주(時)", "일주(日)", "월주(月)", "연주(年)"]
    pillars = [result['pillars']['시주'], result['pillars']['일주'], result['pillars']['월주'], result['pillars']['연주']]
    
    for i in range(4):
        with cols[i]:
            st.markdown(f"<div class='pillar-box' style='text-align:center;'><p style='color:#9ca3af; font-size:0.8rem;'>{labels[i]}</p><h2 style='color:#d4af37;'>{pillars[i]}</h2></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="saju-card">
        <h2 style="color:#d4af37;">🎸 최적의 포지션: {result['position']}</h2>
        <p><b>음악적 재능:</b> {result['talent']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
