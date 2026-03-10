import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
import datetime

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="정통 명리 & 뮤지션 만세력", layout="centered")

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
st.title("🏯 정통 명리 & 뮤지션 만세력")
st.write("1950년부터 2080년까지, 당신의 전 생애 흐름을 추적합니다.")

with st.form("saju_form"):
    u_name = st.text_input("성함", placeholder="이름을 입력하세요")
    u_gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: u_y = st.number_input("출생 연도", 1920, 2026, 1981)
    with c2: u_m = st.number_input("월", 1, 12, 1)
    with c3: u_d = st.number_input("일", 1, 31, 1)
    
    u_type = st.radio("날짜 구분", ["양력", "음력"], horizontal=True)
    u_inter = st.checkbox("윤달 여부")
    
    # 1시간 단위 구간 선택 (요청 사항 반영)
    t_options = ["시간 모름"]
    for i in range(23):
        t_options.append(f"{i:02d}시 ~ {i+1:02d}시")
    t_options.append("23시 ~ 00시")
    u_t = st.selectbox("태어난 시간", t_options)
    
    st.markdown("---")
    # 보고 싶은 연도 선택창 추가 (1950~2080)
    target_year = st.slider("조회할 연도를 선택하세요", 1950, 2080, 2026)
    
    submitted = st.form_submit_button("운명과 해당 연도 운세 확인")

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
            
            # 시주 계산
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
            # 4주 원국 표시
            p_cols = st.columns(4)
            p_labels = ["시주", "일주", "월주", "연주"]
            p_values = [siju, ganji[2], ganji[1], ganji[0]]
            for i in range(4):
                with p_cols[i]:
                    st.markdown(f"<div class='pillar-box'><div style='color:#9ca3af;'>{p_labels[i]}</div><div class='pillar-ganji'>{p_values[i]}</div></div>", unsafe_allow_html=True)

            # 상세 분석 결과
            st.markdown(f"""
            <div class="result-card">
                <div class="res-title">📜 {u_name}님의 인생 분석 ({target_year}년 집중 조회)</div>
                <div class="res-body">
                    <span class="res-sub">● 타고난 기질</span>
                    {ganji[2]}의 기운을 바탕으로 한 당신은 독립적이고 창의적인 에너지가 강합니다. 특히 시주인 {siju}의 영향으로 말년까지 예술적 감각이나 기술적 전문성이 유지되는 명식입니다.
                    <br><br>
                    <span class="res-sub">● {target_year}년의 운세 흐름</span>
                    선택하신 {target_year}년은 당신의 {ganji[2]} 기운과 상호작용하여 새로운 변화를 불러오는 해입니다. 
                    이 시기에는 환경적인 변화에 유연하게 대처하면서 본인의 주관을 지키는 것이 성공의 열쇠입니다.
                    <br><br>
                    <span class="res-sub">● 2080년까지의 장기 조언</span>
                    1950년부터 시작된 세운의 흐름을 볼 때, 당신은 중장년기에 가장 큰 명예를 얻게 됩니다. 2080년까지 꾸준한 자기 관리와 예술적 탐구가 뒷받침된다면 풍요로운 삶을 완성할 수 있습니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error("날짜 계산 중 오류가 발생했습니다. 입력값을 확인해 주세요.")
