import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 시인성 극대화 및 다크 모드 스타일 설정
st.set_page_config(page_title="2080 정통 명리 & 뮤지션 마스터", layout="centered")

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

# 2. 핵심 사주 엔진 (2080년 대응)
def run_saju_engine(y, m, d, t_idx, gender, date_type, is_inter):
    calendar = KoreanLunarCalendar()
    if date_type == "음력":
        calendar.setLunarDate(y, m, d, is_inter)
    else:
        calendar.setSolarDate(y, m, d)
    
    ganji = calendar.getChineseGapJaString().split()
    y_g, m_g, d_g = ganji[0], ganji[1], ganji[2]
    
    siju_list = ["??", "庚子", "辛丑", "辛丑", "壬寅", "壬寅", "癸卯", "癸卯", "甲辰", "甲辰", "乙巳", "乙巳", "丙午", "丙午", "丁未", "丁未", "戊申", "戊申", "己酉", "己酉", "庚戌", "庚戌", "辛亥", "辛亥", "庚子"]
    siju = siju_list[t_idx]

    fortune_data = [
        {"period": "2026 ~ 2040 (장년기)", "desc": "에너지가 정점에 달하는 시기입니다. 예술적 성취와 함께 명예를 얻고 기반을 견고히 다지게 됩니다."},
        {"period": "2041 ~ 2060 (중년기)", "desc": "지혜로운 리더로서 후배들을 이끌며, 사회적으로 큰 영향력을 발휘하는 황금기입니다."},
        {"period": "2061 ~ 2080 (노년기)", "desc": "예술적 깊이가 완성되는 단계입니다. 평온하고 풍요로운 삶 속에서 본인의 유산을 정리하는 시기입니다."}
    ]
    return [siju, d_g, m_g, y_g], fortune_data

# 3. 화면 UI 구성
st.title("🏯 2080 정통 명리 & 뮤지션 마스터")
st.write("본인의 정보를 입력하여 전 생애의 흐름과 음악적 기질을 확인하세요.")

with st.form("saju_form"):
    name = st.text_input("성함", placeholder="풀이를 받으실 이름을 입력하세요")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: y_in = st.number_input("출생 연도", 1900, 2080, 2000)
    with c2: m_in = st.number_input("월", 1, 12, 1)
    with c3: d_in = st.number_input("일", 1, 31, 1)
    
    c4, c5 = st.columns(2)
    with c4:
        date_type = st.radio("날짜 선택", ["양력", "음력"], horizontal=True)
        is_inter = st.checkbox("윤달 여부 (음력 시에만 체크)")
    with c5:
        t_opts = ["시간 모름"] + [f"{i:02d}:00 ~ {i+1:02d}:00" for i in range(23)] + ["23:00 ~ 00:00"]
        selected_t = st.selectbox("태어난 시간대", t_opts)
    
    submit_btn = st.form_submit_button("운명의 흐름 분석하기")

if submit_btn:
    if not name:
        st.error("성함을 입력해야 분석이 가능합니다.")
    else:
        pillars, fortune = run_saju_engine(y_in, m_in, d_in, t_opts.index(selected_t), gender, date_type, is_inter)
        
        st.markdown("---")
        # 사주 원국 시각화
        p_cols = st.columns(4)
        labels = ["시주", "일주", "월주", "연주"]
        for i in range(4):
            with p_cols[i]:
                st.markdown(f"<div class='pillar-box'><div style='color:#9ca3af; font-size:0.85rem;'>{labels[i]}</div><div class='pillar-ganji'>{pillars[i]}</div></div>", unsafe_allow_html=True)

        # 상세 풀이 결과
        st.markdown(f"""
        <div class="result-card">
            <div class="res-title">📜 {name}님의 사주 총평</div>
            <div class="res-text">분석 결과, 귀하는 <b>{pillars[1]}</b>의 기운을 중심으로 강한 창의성과 실천력을 타고났습니다. 
            특히 예술적 기질이 뛰어나며, 나이가 들수록 그 깊이가 더해져 주변의 존경을 받는 명식입니다.</div>
        </div>
        """, unsafe_allow_html=True)

        # 2080 장기 운세
        st.markdown('<div style="margin-top:25px; font-weight:bold; color:#d4af37; font-size:1.3rem;">📅 2080년까지의 생애 주기별 흐름</div>', unsafe_allow_html=True)
        for f in fortune:
            st.markdown(f"<div class='timeline-item'><b>{f['period']}</b>: {f['desc']}</div>", unsafe_allow_html=True)
        
        st.balloons()
