import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="2080 정통 명리 마스터", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { color: #ffffff !important; }
    label { color: #d4af37 !important; font-weight: bold !important; }
    .result-card { 
        background-color: #1a222f; padding: 25px; border-radius: 15px; 
        border: 1px solid #d4af37; margin-top: 20px;
    }
    .res-title { color: #d4af37 !important; font-size: 1.6rem; font-weight: bold; border-bottom: 1px solid #d4af37; padding-bottom: 10px; }
    .res-body { color: #ffffff !important; line-height: 1.8; font-size: 1.1rem; margin-top: 15px; }
    .res-sub { color: #ffd700 !important; font-weight: bold; display: block; margin-top: 15px; }
    .pillar-box { 
        background: #0b111a; padding: 15px; border-radius: 10px; 
        border: 2px solid #d4af37; text-align: center;
    }
    .pillar-ganji { color: #d4af37; font-size: 1.5rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. UI 구성
st.title("🏯 2080 정통 명리 마스터")

with st.form("saju_form"):
    u_name = st.text_input("성함", placeholder="이름을 입력하세요")
    u_gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: u_y = st.number_input("연도", 1900, 2080, 2000)
    with c2: u_m = st.number_input("월", 1, 12, 1)
    with c3: u_d = st.number_input("일", 1, 31, 1)
    
    u_type = st.radio("구분", ["양력", "음력"], horizontal=True)
    u_inter = st.checkbox("윤달 여부")
    
    # 요청하신 1시간 단위 구간 리스트
    t_options = ["시간 모름"]
    for i in range(23):
        t_options.append(f"{i:02d}시 ~ {i+1:02d}시")
    t_options.append("23시 ~ 00시")
    
    u_t = st.selectbox("태어난 시간", t_options)
    
    submitted = st.form_submit_button("운명의 흐름 분석 시작")

# 3. 분석 및 결과 출력
if submitted:
    if not u_name:
        st.error("성함을 입력해 주세요.")
    else:
        try:
            cal = KoreanLunarCalendar()
            if u_type == "음력":
                cal.setLunarDate(u_y, u_m, u_d, u_inter)
            else:
                cal.setSolarDate(u_y, u_m, u_d)
            
            ganji = cal.getChineseGapJaString().split()
            
            # 시간 구간 매칭 함수
            def get_siju_name(time_str):
                if time_str == "시간 모름": return "??"
                h = int(time_str[:2])
                if h in [23, 0]: return "庚子"
                if h in [1, 2]: return "辛丑"
                if h in [3, 4]: return "壬寅"
                if h in [5, 6]: return "癸卯"
                if h in [7, 8]: return "甲辰"
                if h in [9, 10]: return "乙巳"
                if h in [11, 12]: return "丙午"
                if h in [13, 14]: return "丁未"
                if h in [15, 16]: return "戊申"
                if h in [17, 18]: return "己酉"
                if h in [19, 20]: return "庚戌"
                if h in [21, 22]: return "辛亥"
                return "??"

            siju = get_siju_name(u_t)

            st.markdown("---")
            p_cols = st.columns(4)
            p_labels = ["시주", "일주", "월주", "연주"]
            p_values = [siju, ganji[2], ganji[1], ganji[0]]
            
            for i in range(4):
                with p_cols[i]:
                    st.markdown(f"<div class='pillar-box'><div style='color:#9ca3af;'>{p_labels[i]}</div><div class='pillar-ganji'>{p_values[i]}</div></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card">
                <div class="res-title">📜 {u_name}님의 분석 결과</div>
                <div class="res-body">
                    <span class="res-sub">● 타고난 기질</span>
                    분석 결과 귀하는 {ganji[2]}의 기운을 바탕으로 매우 창의적이고 독립적인 성향을 지니고 있습니다. 
                    <br><br>
                    <span class="res-sub">● 2080년까지의 대운 흐름</span>
                    2026년부터 본격적으로 기운이 상승하며 사회적 명예와 성취가 따르는 시기로 진입합니다. 중년 이후에는 안정적인 기반 위에서 본인의 전문성을 널리 알리게 되며, 2080년까지 평온하고 풍요로운 삶이 지속되는 명식입니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error("입력하신 날짜를 다시 확인해 주세요.")
