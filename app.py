import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 페이지 설정 및 디자인 (시인성 극대화)
st.set_page_config(page_title="정통 명리 & 뮤지션 만세력", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    label { color: #d4af37 !important; font-weight: bold !important; font-size: 1.1rem; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #d4af37; color: #000; font-weight: bold; height: 3.5rem; border: none; margin-top: 20px; }
    .result-card { background-color: #1a222f; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 20px; color: #ffffff !important; }
    .res-title { color: #d4af37; font-size: 1.5rem; font-weight: bold; border-bottom: 2px solid #d4af37; padding-bottom: 10px; margin-bottom: 15px; }
    .res-text { color: #ffffff !important; line-height: 1.8; font-size: 1.1rem; }
    .pillar-box { background: #0b111a; padding: 15px; border-radius: 10px; border: 2px solid #d4af37; text-align: center; }
    .pillar-ganji { color: #d4af37; font-size: 1.6rem; font-weight: bold; }
    .timeline-item { background: #2d3748; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 5px solid #d4af37; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 분석 엔진 (장기 운세 포함)
def get_analysis(y, m, d, t_idx, gender, date_type, is_inter):
    calendar = KoreanLunarCalendar()
    if date_type == "음력":
        calendar.setLunarDate(y, m, d, is_inter)
    else:
        calendar.setSolarDate(y, m, d)
    
    ganji = calendar.getChineseGapJaString().split()
    y_g, m_g, d_g = ganji[0], ganji[1], ganji[2]
    
    siju_list = ["??", "庚子", "辛丑", "辛丑", "壬寅", "壬寅", "癸卯", "癸卯", "甲辰", "甲辰", "乙巳", "乙巳", "丙午", "丙午", "丁未", "丁未", "戊申", "戊申", "己酉", "己酉", "庚戌", "庚戌", "辛亥", "辛亥", "庚子"]
    siju = siju_list[t_idx]

    fortune = [
        {"p": "향후 15년", "d": "에너지가 집중되는 시기로, 계획하신 사업이나 예술적 목표를 달성하기에 최적의 시기입니다."},
        {"p": "중기 운세", "d": "안정적인 기반 위에서 명예가 높아지며, 후배나 동료들에게 큰 영향력을 발휘하게 됩니다."},
        {"p": "2080년까지", "d": "지혜와 경험이 완성되는 시기입니다. 평온한 삶과 함께 본인의 결과물들이 빛을 발할 운세입니다."}
    ]
    return [siju, d_g, m_g, y_g], fortune

# 3. UI 구성 (기본값 초기화)
st.title("🏯 정통 사주 명리 & 뮤지션 마스터")
st.write("생년월일을 입력하여 타고난 천명과 2080년까지의 대운을 확인하세요.")

with st.form("main_form"):
    name = st.text_input("성함", placeholder="이름을 입력하세요") # 기본값 삭제
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    c_date = st.columns(3)
    with c_date[0]: y_in = st.number_input("연도", 1900, 2080, 2000) # 기본 연도 조정
    with c_date[1]: m_in = st.number_input("월", 1, 12, 1)
    with c_date[2]: d_in = st.number_input("일", 1, 31, 1)
    
    c_opt = st.columns(2)
    with c_opt[0]: date_type = st.radio("구분", ["양력", "음력"], horizontal=True)
    with c_opt[1]: is_inter = st.checkbox("윤달 여부")
    
    t_opts = ["시간 모름"] + [f"{i:02d}:00 ~ {i+1:02d}:00" for i in range(23)] + ["23:00 ~ 00:00"]
    selected_t = st.selectbox("태어난 시간", t_opts)
    
    submit = st.form_submit_button("사주 풀이 확인하기")

if submit:
    if not name:
        st.warning("성함을 입력해 주세요.")
    else:
        pillars, fortune = get_analysis(y_in, m_in, d_in, t_opts.index(selected_t), gender, date_type, is_inter)
        
        st.markdown("---")
        p_cols = st.
