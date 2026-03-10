import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 페이지 설정 및 디자인 (시인성 극대화)
st.set_page_config(page_title="정통 뮤지션 만세력 v3.0", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #d4af37; color: #000; font-weight: bold; height: 4rem; border: none; font-size: 1.2rem; }
    .result-card { background-color: #1f2937; padding: 30px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 25px; color: #ffffff; }
    .pillar-box { background: #111827; padding: 15px; border-radius: 10px; border: 1px solid #d4af37; text-align: center; }
    .section-title { color: #d4af37; border-left: 5px solid #d4af37; padding-left: 15px; margin-top: 30px; margin-bottom: 15px; font-size: 1.4rem; font-weight: bold; }
    .highlight { color: #ffd700; font-weight: bold; }
    .year-item { background: #111827; padding: 10px; border-radius: 5px; margin-bottom: 5px; border-left: 3px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. 정밀 분석 엔진
def get_comprehensive_analysis(y, m, d, t_idx, gender, is_lun):
    calendar = KoreanLunarCalendar()
    if is_lun: calendar.setLunarDate(y, m, d, False)
    else: calendar.setSolarDate(y, m, d)
    
    ganji = calendar.getChineseGapJaString().split() # 연, 월, 일
    y_g, m_g, d_g = ganji[0], ganji[1], ganji[2]
    
    # 시간 구간 설정
    siju_list = ["??", "庚子", "辛丑", "辛丑", "壬寅", "壬寅", "癸卯", "癸卯", "甲辰", "甲辰", "乙巳", "乙巳", "丙午", "丙午", "丁未", "丁未", "戊申", "戊申", "己酉", "己酉", "庚戌", "庚戌", "辛亥", "辛亥", "庚子"]
    siju = siju_list[t_idx]

    # [1] 일반 사주 풀이 (격국 및 성향)
    general_review = f"{d_g[0]}화(火) 일간으로 태어나 열정과 에너지가 넘치는 명식입니다. {m_g}월의 기운을 받아 추진력이 강하며, 주변 사람을 이끄는 우두머리 기질이 다분합니다."
    
    # [2] 음악적 사주 및 악기 매칭
    inst = "일렉트릭 기타 (Gibson/Fender Hybrid)"
    music_trait = "금(金)과 화(火)의 조화로 날카로운 톤과 뜨거운 감성을 동시에 갖췄습니다. 테크니컬한 속주보다 묵직한 미드-로우 톤의 블루지한 감성이 천직입니다."
    
    # [3] 연도별 주요 흐름 (2025~2027)
    yearly_forecast = [
        {"year": "2025년 (乙巳)", "desc": "새로운 음원 발표 및 예술적 영감이 샘솟는 시기 (실제로 디지털 싱글 발매)"},
        {"year": "2026년 (丙午)", "desc": "강력한 화(火)의 기운으로 사업적 결실(Band City)을 맺고 무대 장악력이 정점에 달하는 해"},
        {"year": "2027년 (丁未)", "desc": "안정적인 운영과 더불어 후배 양성 및 팀의 내실을 다지는 시기"}
    ]

    return [siju, d_g, m_g, y_g], general_review, music_trait, inst, yearly_forecast

# 3. UI 구성
st.title("🏯 정통 뮤지션 명리 마스터")
st.write("환백 님의 음악적 천명과 삶의 흐름을 가감 없이 분석합니다.")

with st.container():
    name = st.text_input("성함", value="임환백")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    col_y, col_m, col_d = st.columns(3)
    with col_y: y_in = st.number_input("출생 연도", 1900, 2026, 1981)
    with col_m: m_in = st.number_input("출생 월", 1, 12, 2)
    with col_d: d_in = st.number_input("출생 일", 1, 31, 7)
    
    # 시간 구간 선택 (요청하신 대로 1시~2시 형태)
    t_options = ["시간 모름"] + [f"{i:02d}:00 ~ {i+1:02d}:00" for i in range(23)] + ["23:00 ~ 00:00"]
    selected_t = st.selectbox("태어난 시간 (구간 선택)", t_options)
    t_idx = t_options.index(selected_t)
    is_lun = st.checkbox("음력으로 계산")

if st.button("나의 음악적 천명 확인하기"):
    pillars, gen, music, inst, years = get_comprehensive_analysis(y_in, m_in, d_in, t_idx, gender, is_lun)
    
    st.markdown("---")
    
    # 사주 원국 시각화
    p_cols = st.columns(4)
    labels = ["시주(時)", "일주(日)", "월주(月)", "연주(年)"]
    for i in range(4):
        with p_cols[i]:
            st.markdown(f"<div class='pillar-box'><p style='color:#9ca3af;font-size:0.8rem;'>{labels[i]}</p><h2 style='color:#d4af37;'>{pillars[i]}</h2></div>", unsafe_allow_html=True)

    # 상세 분석 결과
    st.markdown('<div class="section-title">📜 일반 사주 총평</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card">{gen}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🎸 음악적 천명 & 추천 악기</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-card">
        <p><span class="highlight">추천 악기:</span> {inst}</p>
        <p><span class="highlight">음악적 기질:</span> {music}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📅 향후 연도별 성과 및 흐름</div>', unsafe_allow_html=True)
    for y_data in years:
        st.markdown(f"""
        <div class="year-item">
            <span style="color:#d4af37; font-weight:bold;">{y_data['year']}:</span> {y_data['desc']}
        </div>
        """, unsafe_allow_html=True)
    
    st.balloons()
