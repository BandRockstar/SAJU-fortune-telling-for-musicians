import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="2080 뮤지션 만세력 마스터", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { color: #ffffff !important; }
    label { color: #d4af37 !important; font-weight: bold !important; }
    .result-card { background-color: #1a222f; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 20px; }
    .res-title { color: #d4af37 !important; font-size: 1.6rem; font-weight: bold; border-bottom: 1px solid #d4af37; padding-bottom: 10px; }
    .res-body { color: #ffffff !important; line-height: 1.8; font-size: 1.1rem; margin-top: 15px; }
    .res-sub { color: #ffd700 !important; font-weight: bold; display: block; margin-top: 15px; }
    .pillar-box { background: #0b111a; padding: 15px; border-radius: 10px; border: 2px solid #d4af37; text-align: center; }
    .pillar-ganji { color: #d4af37; font-size: 1.5rem; font-weight: bold; }
    .instrument-tag { background: #d4af37; color: #000; padding: 4px 12px; border-radius: 8px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 정밀 시두법 및 악기 매칭 함수
def get_saju_details(day_gan, time_str):
    if time_str == "시간 모름": return "??", "전천후 뮤지션"
    try:
        h = int(time_str[:2])
    except:
        return "??", "전천후 뮤지션"
    
    jis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    h_map = {23:0, 0:0, 1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:9, 19:10, 20:10, 21:11, 22:11}
    idx = h_map.get(h, 0)
    
    start_gan_map = {"甲": 0, "己": 0, "乙": 2, "庚": 2, "丙": 4, "辛": 4, "丁": 6, "壬": 6, "戊": 8, "癸": 8}
    gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    start_idx = start_gan_map.get(day_gan, 0)
    siju = gans[(start_idx + idx) % 10] + jis[idx]
    
    inst_map = {
        "子":"건반/미디", "丑":"묵직한 베이스", "寅":"파워풀 기타", "卯":"섬세한 리듬기타",
        "辰":"프론트맨/보컬", "巳":"드럼/타악기", "午":"화려한 리드기타", "未":"부드러운 베이스",
        "申":"테크니컬 베이스", "酉":"샤우팅/솔로기타", "戌":"드럼/비트메이커", "亥":"작곡/스트링"
    }
    inst = inst_map.get(jis[idx], "멀티플레이어")
    return siju, inst

# 3. UI 구성
st.title("🏯 뮤지션 만세력: 2080 마스터 플랜")

with st.form("music_saju"):
    u_name = st.text_input("성함", placeholder="이름을 입력하세요")
    u_gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: u_y = st.number_input("출생 연도", 1920, 2030, 1981)
    with col2: u_m = st.number_input("월", 1, 12, 2)
    with col3: u_d = st.number_input("일", 1, 31, 7)
    
    u_type = st.radio("날짜 구분", ["양력", "음력"], horizontal=True)
    u_inter = st.checkbox("윤달 여부")
    
    t_options = ["시간 모름"] + [f"{i:02d}시 ~ {i+1:02d}시" for i in range(23)] + ["23시 ~ 00시"]
    u_t = st.selectbox("태어난 시간", t_options)
    
    st.markdown("---")
    target_year = st.number_input("조회할 연도 입력 (1950 ~ 2080)", 1950, 2080, 2026)
    
    submitted = st.form_submit_button("분석 실행")

# 4. 결과 출력
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
            day_gan = ganji[2][0]
            siju, instrument = get_saju_details(day_gan, u_t)

            st.markdown("---")
            p_cols = st.columns(4)
            p_labels = ["시주", "일주", "월주", "연주"]
            p_values = [siju, ganji[2], ganji[1], ganji[0]]
            
            for i in range(4):
                with p_cols[i]:
                    st.markdown(f"<div class='pillar-box'><div style='color:#9ca3af; font-size:0.8rem;'>{p_labels[i]}</div><div class='pillar-ganji'>{p_values[i]}</div></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card">
                <div class="res-title">🎸 {u_name}님의 뮤지션 정밀 분석</div>
                <div class="res-body">
                    <span class="res-sub">● 당신의 운명적 포지션</span>
                    <div class="instrument-tag">{instrument}</div><br>
                    당신의 일주 <b>{ganji[2]}</b>와 시주 <b>{siju}</b>의 조합은 음악적 완성도를 높이는 강력한 힘이 됩니다.
                    <br><br>
                    <span class="res-sub">● {target_year}년의 음악적 성취</span>
                    {target_year}년은 당신의 기운이 사회적 흐름과 만나 큰 시너지를 내는 해입니다. 
                    공연과 창작 활동 모두에서 뚜렷한 족적을 남길 수 있는 시기입니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
