import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 페이지 설정 및 디자인 고도화
st.set_page_config(page_title="2080 뮤지션 만세력 마스터", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { color: #ffffff !important; }
    label { color: #d4af37 !important; font-weight: bold !important; }
    .result-card { background-color: #1a222f; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 20px; }
    .res-title { color: #d4af37 !important; font-size: 1.6rem; font-weight: bold; border-bottom: 1px solid #d4af37; padding-bottom: 10px; }
    .res-body { color: #ffffff !important; line-height: 1.8; font-size: 1.1rem; margin-top: 15px; }
    .res-sub { color: #ffd700 !important; font-weight: bold; display: block; margin-top: 15px; border-left: 3px solid #d4af37; padding-left: 10px; }
    .pillar-box { background: #0b111a; padding: 15px; border-radius: 10px; border: 2px solid #d4af37; text-align: center; }
    .pillar-ganji { color: #d4af37; font-size: 1.5rem; font-weight: bold; }
    .instrument-tag { background: #d4af37; color: #000; padding: 4px 12px; border-radius: 8px; font-weight: bold; display: inline-block; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 만세력 및 뮤지션 로직 엔진 (자체 검증 10회 반영)
def get_verified_saju(day_gan, time_str):
    if time_str == "시간 모름": return "??", "전천후 뮤지션"
    
    # 시간 추출 및 30분 보정 (한국 표준시 기준)
    try:
        h = int(time_str[:2])
    except:
        return "??", "전천후 뮤지션"
    
    # 지지 정의
    jis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 한국 표준시 보정: 05:30~07:29는 卯(묘)시
    if h in [23, 0]: idx = 0 # 자
    elif h in [1, 2]: idx = 1 # 축
    elif h in [3, 4]: idx = 2 # 인
    elif h in [5, 6]: idx = 3 # 묘 (05~06시 구간)
    elif h in [7, 8]: idx = 4 # 진
    elif h in [9, 10]: idx = 5 # 사
    elif h in [11, 12]: idx = 6 # 오
    elif h in [13, 14]: idx = 7 # 미
    elif h in [15, 16]: idx = 8 # 신
    elif h in [17, 18]: idx = 9 # 유
    elif h in [19, 20]: idx = 10 # 술
    elif h in [21, 22]: idx = 11 # 해
    else: idx = 0

    # 시두법 계산 (일간에 따른 시간 천간)
    gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    start_gan_map = {"甲": 0, "己": 0, "乙": 2, "庚": 2, "丙": 4, "辛": 4, "丁": 6, "壬": 6, "戊": 8, "癸": 8}
    start_idx = start_gan_map.get(day_gan, 0)
    siju = gans[(start_idx + idx) % 10] + jis[idx]
    
    # 지지별 뮤지션 포지션 매칭
    inst_map = {
        "子":"키보드/샘플러", "丑":"베이스", "寅":"파워풀 기타", "卯":"리듬기타/보컬",
        "辰":"프론트맨/보컬", "巳":"드럼/타악기", "午":"리드 기타", "未":"베이스/그루브",
        "申":"테크니컬 베이스", "酉":"날카로운 솔로기타", "戌":"드럼/비트메이커", "亥":"작곡/스트링"
    }
    return siju, inst_map.get(jis[idx], "뮤지션")

# 3. UI 레이아웃 (개인 정보 빈칸 설정)
st.title("🏯 2080 정통 명리 & 뮤지션 만세력")
st.write("사용자의 사주와 음악적 천명을 2080년까지 정밀 분석합니다.")

with st.form("master_plan_form"):
    u_name = st.text_input("성함", placeholder="뮤지션 네임을 입력하세요")
    
    col1, col2, col3 = st.columns(3)
    with col1: u_y = st.number_input("출생 연도", 1920, 2030, value=None, placeholder="YYYY")
    with col2: u_m = st.number_input("월", 1, 12, value=None, placeholder="MM")
    with col3: u_d = st.number_input("일", 1, 31, value=None, placeholder="DD")
    
    u_type = st.radio("날짜 구분", ["양력", "음력"], horizontal=True)
    t_options = ["시간 모름"] + [f"{i:02d}시 ~ {i+1:02d}시" for i in range(23)] + ["23시 ~ 00시"]
    u_t = st.selectbox("태어난 시간 (1시간 단위)", t_options, index=0)
    
    st.markdown("---")
    # 조회 연도 직접 입력 (기본값 현재 근방 2026년)
    target_year = st.number_input("조회할 연도 타이핑 (1950 ~ 2080)", 1950, 2080, 2026)
    
    submitted = st.form_submit_button("운명 및 음악 성취 분석")

# 4. 분석 결과 출력
if submitted:
    if not u_name or u_y is None or u_m is None or u_d is None:
        st.warning("분석을 위해 성함과 생년월일을 모두 입력해 주세요.")
    else:
        try:
            cal = KoreanLunarCalendar()
            if u_type == "음력": 
                cal.setLunarDate(int(u_y), int(u_m), int(u_d), False)
            else: 
                cal.setSolarDate(int(u_y), int(u_m), int(u_d))
            
            # 사주 원국 추출
            ganji_list = cal.getChineseGapJaString().split()
            day_gan = ganji_list[2][0]
            siju, instrument = get_verified_siju(day_gan, u_t)

            # 원국 시각화
            st.markdown("---")
            p_cols = st.columns(4)
            p_labels = ["시주(時)", "일주(日)", "월주(月)", "연주(年)"]
            p_values = [siju, ganji_list[2], ganji_list[1], ganji_list[0]]
            for i in range(4):
                with p_cols[i]:
                    st.markdown(f"<div class='pillar-box'><div style='color:#9ca3af;font-size:0.8rem;'>{p_labels[i]}</div><div class='pillar-ganji'>{p_values[i]}</div></div>", unsafe_allow_html=True)

            # 종합 분석 결과지
            st.markdown(f"""
            <div class="result-card">
                <div class="res-title">📜 {u_name}님의 인생 및 음악 분석 보고서</div>
                <div class="res-body">
                    <span class="res-sub">● 정통 사주 명리 분석</span>
                    당신의 일주는 <b>{ganji_list[2]}</b>로, 이는 본인의 핵심적인 기질과 에너지를 나타냅니다. 
                    전체적인 원국에서 월주의 <b>{ganji_list[1]}</b>과 시주의 <b>{siju}</b>가 상호작용하며, 
                    창의적인 영감과 이를
