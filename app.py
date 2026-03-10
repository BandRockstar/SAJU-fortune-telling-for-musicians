import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 스타일 설정
st.set_page_config(page_title="2080 만세력", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .result-card { background-color: #1a222f; padding: 20px; border-radius: 10px; border: 1px solid #d4af37; margin-top: 20px; }
    .pillar-box { background: #0b111a; padding: 10px; border-radius: 5px; border: 1px solid #d4af37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. 메인 UI
st.title("🏯 2080 정통 명리 마스터")

with st.form("saju_form"):
    u_name = st.text_input("성함", placeholder="이름 입력")
    u_gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: u_y = st.number_input("연도", 1900, 2080, 2000)
    with c2: u_m = st.number_input("월", 1, 12, 1)
    with c3: u_d = st.number_input("일", 1, 31, 1)
    
    u_type = st.radio("구분", ["양력", "음력"], horizontal=True)
    u_inter = st.checkbox("윤달 여부")
    
    t_list = ["시간 모름"] + [f"{i:02d}:00" for i in range(24)]
    u_t = st.selectbox("시간", t_list)
    
    submitted = st.form_submit_button("분석 시작")

if submitted:
    if not u_name:
        st.error("이름을 입력하세요.")
    else:
        cal = KoreanLunarCalendar()
        if u_type == "음력": cal.setLunarDate(u_y, u_m, u_d, u_inter)
        else: cal.setSolarDate(u_y, u_m, u_d)
        
        ganji = cal.getChineseGapJaString().split()
        
        st.markdown("---")
        cols = st.columns(3)
        labels = ["일주", "월주", "연주"]
        for i in range(3):
            with cols[i]:
                st.markdown(f"<div class='pillar-box'><p>{labels[i]}</p><h3>{ganji[2-i]}</h3></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card">
            <h3 style='color:#d4af37;'>{u_name}님의 분석</h3>
            <p>2080년까지의 대운 흐름이 시작됩니다. 본인의 기운을 믿고 나아가세요.</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
