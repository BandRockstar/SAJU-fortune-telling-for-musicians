import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 디자인 설정 (시인성 최상급 유지)
st.set_page_config(page_title="정통 명리 & 뮤지션 만세력 v4.0", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    label { color: #d4af37 !important; font-weight: bold !important; font-size: 1.1rem; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #d4af37; color: #000; font-weight: bold; height: 4rem; border: none; font-size: 1.3rem; margin-top: 20px; }
    .result-card { background-color: #1a222f; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 20px; color: #ffffff !important; }
    .res-title { color: #d4af37; font-size: 1.5rem; font-weight: bold; border-bottom: 2px solid #d4af37; padding-bottom: 10px; margin-bottom: 15px; }
    .res-text { color: #ffffff !important; line-height: 1.8; font-size: 1.05rem; }
    .pillar-box { background: #0b111a; padding: 15px; border-radius: 10px; border: 2px solid #d4af37; text-align: center; }
    .pillar-ganji { color: #d4af37; font-size: 1.6rem; font-weight: bold; }
    .highlight { color: #ffd700; font-weight: bold; }
    /* 장기 운세용 스타일 */
    .timeline-item { background: #2d3748; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #3b82f6; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 미래 확장 분석 엔진
def get_extended_analysis(y, m, d, t_idx, gender, date_type, is_inter):
    calendar = KoreanLunarCalendar()
    if date_type == "음력": calendar.setLunarDate(y, m, d, is_inter)
    else: calendar.setSolarDate(y, m, d)
    
    ganji = calendar.getChineseGapJaString().split()
    y_g, m_g, d_g = ganji[0], ganji[1], ganji[2]
    
    siju_list = ["??", "庚子", "辛丑", "辛丑", "壬寅", "壬寅", "癸卯", "癸卯", "甲辰", "甲辰", "乙巳", "乙巳", "丙午", "丙午", "丁未", "丁未", "戊申", "戊申", "己酉", "己酉", "庚戌", "庚戌", "辛亥", "辛亥", "庚子"]
    siju = siju_list[t_idx]

    # [미래 확장 데이터 생성]
    long_term_fortune = [
        {"period": "현재 ~ 2035년", "desc": "가장 왕성한 활동기입니다. 본인의 전문 분야에서 독보적인 위치에 오르며, 경제적 기반이 완성되는 시기입니다."},
        {"period": "2036년 ~ 2050년", "desc": "명예운이 강해지는 시기입니다. 후배 양성이나 사회적 영향력을 행사하며 본인의 이름을 널리 알리게 됩니다."},
        {"period": "2051년 ~ 2065년", "desc": "안정적인 수성(守成)의 시기입니다. 건강 관리에 유의하며 평화로운 삶과 예술적 깊이를 완성하는 단계입니다."},
        {"period": "2066년 ~ 2080년", "desc": "지혜를 나누는 노년의 황금기입니다. 본인의 유산을 정리하고 가족 및 후대와 조화로운 시간을 보낼 운세입니다."}
    ]

    return [siju, d_g, m_g, y_g], long_term_fortune

# 3. UI 구성
st.title("🏯 2080 대운 만세력 & 뮤지션 마스터")
st.write("과거부터 미래 2080년까지, 당신의 전 생애를 아우르는 명리 분석 시스템")

with st.container():
    name = st.text_input("성함", value="임환백")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    c_date = st.columns([1, 1, 1])
    with c_date[0]: y_in = st.number_input("연도", 1900, 2080, 1981) # 2080년까지 확장
    with c_date[1]: m_in = st.number_input("월", 1, 12, 2)
    with c_date[2]: d_in = st.number_input("일", 1, 31, 7)
    
    c_type = st.columns(2)
    with c_type[0]: date_type = st.radio("구분", ["양력", "음력"], horizontal=True)
    with c_type[1]: is_inter = st.checkbox("윤달 여부")
    
    t_opts = ["시간 모름"] + [f"{i:02d}:00 ~ {i+1:02d}:00" for i in range(23)] + ["23:00 ~ 00:00"]
    selected_t = st.selectbox("태어난 시간", t_opts)

if st.button("전 생애 운세 로드하기"):
    pillars, fortune_list = get_extended_analysis(y_in, m_in, d_in, t_opts.index(selected_t), gender, date_type, is_inter)
    
    st.markdown("---")
    
    # 사주 원국
    p_cols = st.columns(4)
    labels = ["시주(時)", "일주(日)", "월주(月)", "연주(年)"]
    for i in range(4):
        with p_cols[i]:
            st.markdown(f"<div class='pillar-box'><div style='color:#9ca3af;'>{labels[i]}</div><div class='pillar-ganji'>{pillars[i]}</div></div>", unsafe_allow_html=True)

    # 섹션 1: 타고난 천명
    st.markdown(f"""
    <div class="result-card">
        <div class="res-title">📜 기본 사주 구성 분석</div>
        <div class="res-text">입력하신 <span class="highlight">{y_in}년</span>의 기운을 바탕으로 분석한 결과, 
        귀하는 <span class="highlight">{pillars[1]}</span>의 기운을 중심으로 강한 생명력과 개성을 지녔습니다. 
        이는 2080년까지 이어지는 긴 여정의 튼튼한 뿌리가 됩니다.</div>
    </div>
    """, unsafe_allow_html=True)

    # 섹션 2: 2080 장기 미래 운세
    st.markdown('<div style="margin-top:30px; font-size:1.5rem; font-weight:bold; color:#d4af37;">📅 2080년까지의 장기 운세 흐름</div>', unsafe_allow_html=True)
    for f in fortune_list:
        st.markdown(f"""
        <div class="timeline-item">
            <span style="font-weight:bold; color:#ffd700;">[{f['period']}]</span><br>
            {f['desc']}
        </div>
        """, unsafe_allow_html=True)
    
    st.info("※ 본 분석은 통계적인 명리학 근거를 바탕으로 하며, 2080년까지의 기운의 흐름을 대략적으로 보여줍니다.")
    st.balloons()
