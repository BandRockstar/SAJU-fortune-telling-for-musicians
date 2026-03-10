import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 시각적 가시성 및 다크모드 최적화 설정
st.set_page_config(page_title="2080 정통 명리 마스터", layout="centered")

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

# 2. 사주 분석 코어 (오류 방지를 위한 간결한 로직)
def analyze_saju(y, m, d, t_idx, date_type, is_inter):
    calendar = KoreanLunarCalendar()
    if date_type == "음력":
        calendar.setLunarDate(y, m, d, is_inter)
    else:
        calendar.setSolarDate(y, m, d)
    
    ganji = calendar.getChineseGapJaString().split()
    y_g, m_g, d_g = ganji[0], ganji[1], ganji[2]
    
    # 시간 구간에 따른 시주 매칭
    siju_list = ["??", "庚子", "辛丑", "辛丑", "壬寅", "壬寅", "癸卯", "癸卯", "甲辰", "甲辰", "乙巳", "乙巳", "丙午", "丙午", "丁未", "丁未", "戊申", "戊申", "己酉", "己酉", "庚戌", "庚戌", "辛亥", "辛亥", "庚子"]
    siju = siju_list[t_idx]

    # 2080년까지의 장기 운세 데이터
    fortune = [
        {"period": "2026~2040년", "desc": "인생의 황금기로, 추진해오던 일들이 큰 결실을 맺고 사회적 지위가 확립되는 시기입니다."},
        {"period": "2041~2060년", "desc": "명예와 안정이 따르는 시기입니다. 본인의 전문성을 널리 알리고 후대를 양성하게 됩니다."},
        {"period": "2061~2080년", "desc": "예술적 감각과 지혜가 완성되는 노년의 전성기입니다. 평온하고 풍요로운 삶이 지속됩니다."}
    ]
    return [siju, d_g, m_g, y_g], fortune

# 3. 사용자 인터페이스 (개인정보 초기화 상태)
st.title("🏯 2080 정통 명리 & 뮤지션 마스터")
st.write("본인의 정보를 입력하여 타고난 기질과 2080년까지의 대운을 확인하세요.")

with st.form("main_form"):
    u_name = st.text_input("성함", placeholder="풀이를 받으실 분의 성함")
    u_gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: u_y = st.number_input("연도", 1900, 2080, 2000)
    with c2: u_m = st.number_input("월", 1, 12, 1)
    with c3: u_d = st.number_input("일", 1, 31, 1)
    
    c4, c5 = st.columns(2)
    with c4:
        u_type = st.radio("날짜 구분", ["양력", "음력"], horizontal=True)
        u_inter = st.checkbox("윤달 여부 (음력일 때만)")
    with c5:
        t_opts = ["시간 모름"] + [f"{i:02d}:00 ~ {i+1:02d}:00" for i in range(23)] + ["23:00 ~ 00:00"]
        u_t = st.selectbox("태어난 시간대", t_opts)
    
    submitted = st.form_submit_button("운명 분석 시작")

if submitted:
    if not u_name:
        st.error("성함을 입력해 주세요.")
    else:
        pillars, fortune_list = analyze_saju(u_y, u_m, u_d, t_opts.index(u_t), u_type, u_inter)
        
        st.markdown("---")
        # 4주 원국 표시
        p_cols = st.columns(4)
        labels = ["시주", "일주", "월주", "연주"]
        for i in range(4):
            with p_cols[i]:
                st.markdown(f"<div class='pillar-box'><div style='color:#9ca3af; font-size:0.8rem;'>{labels[i]}</div><div class='pillar-ganji'>{pillars[i]}</div></div>", unsafe_allow_html=True)

        # 분석 결과 카드
        st.markdown(f"""
        <div class="result-card">
            <div class="res-title">📜 {u_name}님의 정통 사주 풀이</div>
            <div class="res-text">입력하신 데이터를 기반으로 분석한 결과, <b>{pillars[1]}</b>의 기운을 타고난 당신은 강한 추진력과 남다른 예술적 감각을 지녔습니다. 
            이는 인생 전반에 걸쳐 큰 무기가 될 것입니다.</div>
        </div>
        """, unsafe_allow_html=True)

        # 2080 장기 운세
        st.markdown('<div style="margin-top:25px; font-weight:bold; color:#d4af37; font-size:1.3rem;">📅 2080년까지의 생애 대운 흐름</div>', unsafe_allow_html=True)
        for item in fortune_list:
            st.markdown(f"<div class='timeline-item'><b>{item['period']}</b>: {item['desc']}</div>", unsafe_allow_html=True)
        
        st.balloons()
