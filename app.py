import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 페이지 설정
st.set_page_config(page_title="정통 뮤지션 만세력", layout="centered")

# 스타일 적용
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #d4af37; color: #000; font-weight: bold; height: 3rem; }
    .saju-card { background-color: #1f2937; padding: 20px; border-radius: 12px; border: 1px solid #d4af37; margin-top: 20px; }
    .pillar-box { background: #111827; padding: 10px; border-radius: 8px; border: 1px solid #374151; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. 분석 함수
def get_analysis(y, m, d, t_idx, gender, is_lun):
    calendar = KoreanLunarCalendar()
    if is_lun:
        calendar.setLunarDate(y, m, d, False)
    else:
        calendar.setSolarDate(y, m, d)
    
    ganji = calendar.getChineseGapJaString().split()
    
    # 시간 매칭 (가장 안전한 리스트 방식)
    siju_list = ["??", "庚子", "辛丑", "辛丑", "壬寅", "壬寅", "癸卯", "癸卯", "甲辰", "甲辰", "乙巳", "乙巳", "丙午", "丙午", "丁未", "丁未", "戊申", "戊申", "己酉", "己酉", "庚戌", "庚戌", "辛亥", "辛亥", "庚子"]
    siju = siju_list[t_idx]
    
    pos = "리드 기타 (Lead Guitar)" if "庚" in ganji[1] or "辛" in ganji[0] else "프론트맨"
    luck = "양(陽)의 기운이 강한 리더" if gender == "남성" else "음(陰)의 기운이 섬세한 예술가"
    
    return [siju, ganji[2], ganji[1], ganji[0]], pos, luck

# 3. 화면 구성
st.title("🏯 정통 뮤지션 만세력")

name = st.text_input("성함", value="임환백")
gender = st.radio("성별", ["남성", "여성"], horizontal=True)

# 연/월/일 개별 입력
c1, c2, c3 = st.columns(3)
with c1: y_in = st.number_input("연도", 1900, 2026, 1981)
with c2: m_in = st.number_input("월", 1, 12, 2)
with c3: d_in = st.number_input("일", 1, 31, 7)

# 시간 선택지 (오류 방지를 위해 단순 텍스트 리스트 사용)
t_options = ["시간 모름", "00시", "01시", "02시", "03시", "04시", "05시", "06시", "07시", "08시", "09시", "10시", "11시", "12시", "13시", "14시", "15시", "16시", "17시", "18시", "19시", "20시", "21시", "22시", "23시"]
selected_t = st.selectbox("태어난 시간", t_options)
t_idx = t_options.index(selected_t)

is_lun = st.checkbox("음력 입력")

if st.button("운명의 구성 확인하기"):
    pillars, pos, luck = get_analysis(y_in, m_in, d_in, t_idx, gender, is_lun)
    
    st.markdown("---")
    cols = st.columns(4)
    labels = ["시주", "일주", "월주", "연주"]
    for i in range(4):
        with cols[i]:
            st.markdown(f"<div class='pillar-box'><p style='font-size:0.8rem;'>{labels[i]}</p><h3>{pillars[i]}</h3></div>", unsafe_allow_html=True)
            
    st.markdown(f"""
    <div class="saju-card">
        <h3>🎸 {name}님의 분석 결과</h3>
        <p><b>최적 포지션:</b> {pos}</p>
        <p><b>운세 특징:</b> {luck}</p>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
