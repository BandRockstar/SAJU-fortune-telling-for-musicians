import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 디자인 및 레이아웃 설정
st.set_page_config(page_title="2080 정통 명리 & 뮤지션 마스터", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { color: #ffffff !important; }
    label { color: #d4af37 !important; font-weight: bold !important; }
    .result-card { background-color: #1a222f; padding: 30px; border-radius: 20px; border: 1px solid #d4af37; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .res-title { color: #d4af37 !important; font-size: 1.8rem; font-weight: bold; border-bottom: 2px solid #d4af37; padding-bottom: 12px; margin-bottom: 20px; }
    .res-body { color: #e0e0e0 !important; line-height: 1.9; font-size: 1.1rem; }
    .res-sub { color: #ffd700 !important; font-weight: bold; display: block; margin-top: 20px; font-size: 1.2rem; border-left: 4px solid #d4af37; padding-left: 12px; }
    .pillar-box { background: #0b111a; padding: 15px; border-radius: 12px; border: 2px solid #4a4a4a; text-align: center; transition: 0.3s; }
    .pillar-box:hover { border-color: #d4af37; }
    .pillar-ganji { color: #d4af37; font-size: 1.6rem; font-weight: bold; margin-top: 5px; }
    .instrument-tag { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 10px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 고도화된 명리 분석 엔진
def get_deep_analysis(ganji_list, siju, instrument):
    # 일주/월주/시주 데이터 추출
    yeon, wol, il = ganji_list[0], ganji_list[1], ganji_list[2]
    
    # 1단계: 일주론 및 기질 분석
    il_desc = f"당신은 <b>{il}</b>의 기운을 타고났습니다. 이는 대지 위에 떠오른 태양 혹은 강인한 생명력을 상징하며, 예술가로서 발산하는 에너지와 현실적인 균형 감각을 동시에 갖추었음을 의미합니다."
    
    # 2단계: 격국 및 조후 (월지 중심)
    wol_desc = f"<b>{wol[1]}월</b>에 태어난 당신은 독창적인 아이디어와 실험적 정신이 강한 격국을 형성하고 있습니다. 남들이 시도하지 않는 새로운 사운드나 구조를 설계하는 데 탁월한 재능이 있습니다."
    
    # 3단계: 시주와 음악적 완성도
    si_desc = f"특히 말년과 자아실현을 관장하는 시주가 <b>{siju}</b>라는 점은 매우 고무적입니다. 이는 시간이 흐를수록 당신의 음악적 테크닉이 정교해지고, 보석처럼 빛나는 결과물을 만들어낼 것임을 암시합니다."
    
    return il_desc, wol_desc, si_desc

def get_saju_engine(day_gan, time_str):
    if time_str == "시간 모름": return "??", "전천후 뮤지션"
    try: h = int(time_str[:2])
    except: return "??", "전천후 뮤지션"
    
    jis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    h_idx = {23:0, 0:0, 1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:9, 19:10, 20:10, 21:11, 22:11}
    idx = h_idx.get(h, 0)
    
    gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    start_map = {"甲": 0, "己": 0, "乙": 2, "庚": 2, "丙": 4, "辛": 4, "丁": 6, "壬": 6, "戊": 8, "癸": 8}
    siju = gans[(start_map.get(day_gan, 0) + idx) % 10] + jis[idx]
    
    inst_map = {"子":"키보드/미디", "丑":"묵직한 베이스", "寅":"파워풀 기타", "卯":"섬세한 리듬기타/보컬", "辰":"보컬/프론트맨", "巳":"드럼/퍼커션", "午":"화려한 리드기타", "未":"부드러운 베이스", "申":"테크니컬 베이스", "酉":"날카로운 솔로기타", "戌":"드럼/비트", "亥":"작곡/스트링"}
    return siju, inst_map.get(jis[idx], "뮤지션")

# 3. UI 구성
st.title("🏯 2080 정통 명리 & 뮤지션 마스터")
st.write("당신의 사주 원국을 정밀 분석하여 음악적 천명과 미래의 흐름을 제시합니다.")

with st.form("deep_form"):
    u_name = st.text_input("성함", placeholder="뮤지션 네임 입력")
    c1, c2, c3 = st.columns(3)
    with c1: u_y = st.number_input("출생 연도", 1920, 2030, value=None, placeholder="YYYY")
    with c2: u_m = st.number_input("월", 1, 12, value=None, placeholder="MM")
    with c3: u_d = st.number_input("일", 1, 31, value=None, placeholder="DD")
    
    u_type = st.radio("날짜 구분", ["양력", "음력"], horizontal=True)
    t_opt = ["시간 모름"] + [f"{i:02d}시 ~ {i+1:02d}시" for i in range(23)] + ["23시 ~ 00시"]
    u_t = st.selectbox("태어난 시간", t_opt, index=0)
    
    st.markdown("---")
    target_year = st.number_input("상세 분석 연도 (1950 ~ 2080)", 1950, 2080, 2026)
    submitted = st.form_submit_button("심층 운명 분석 실행")

# 4. 결과 출력 및 심층 리포트
if submitted:
    if not u_name or u_y is None or u_m is None or u_d is None:
        st.warning("분석을 위해 모든 정보를 입력해 주세요.")
    else:
        try:
            cal = KoreanLunarCalendar()
            if u_type == "음력": cal.setLunarDate(int(u_y), int(u_m), int(u_d), False)
            else: cal.setSolarDate(int(u_y), int(u_m), int(u_d))
            
            ganji = cal.getChineseGapJaString().split()
            siju, inst = get_saju_engine(ganji[2][0], u_t)
