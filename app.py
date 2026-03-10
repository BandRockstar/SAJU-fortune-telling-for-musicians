import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 디자인 설정
st.set_page_config(page_title="2080 뮤지션 심층 만세력", layout="centered")
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stApp { background-color: #0e1117; }
    .result-card { background-color: #1a222f; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; margin-top: 20px; }
    .res-title { color: #d4af37; font-size: 1.6rem; font-weight: bold; border-bottom: 2px solid #d4af37; padding-bottom: 10px; }
    .res-sub { color: #ffd700; font-weight: bold; display: block; margin-top: 20px; font-size: 1.1rem; border-left: 4px solid #d4af37; padding-left: 10px; }
    .pillar-box { background: #0b111a; padding: 15px; border-radius: 10px; border: 2px solid #4a4a4a; text-align: center; }
    .pillar-ganji { color: #d4af37; font-size: 1.5rem; font-weight: bold; }
    .inst-tag { background: #d4af37; color: #000; padding: 3px 10px; border-radius: 5px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. 로직 엔진
def get_saju_data(day_gan, t_str):
    if t_str == "시간 모름": return "??", "전천후"
    h = int(t_str[:2])
    jis = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
    h_idx = {23:0, 0:0, 1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7, 15:8, 16:8, 17:9, 18:9, 19:10, 20:10, 21:11, 22:11}
    idx = h_idx.get(h, 0)
    gans = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    start_map = {"甲":0,"己":0,"乙":2,"庚":2,"丙":4,"辛":4,"丁":6,"壬":6,"戊":8,"癸":8}
    siju = gans[(start_map.get(day_gan, 0) + idx) % 10] + jis[idx]
    insts = {"子":"키보드","丑":"베이스","寅":"기타","卯":"리듬기타/보컬","辰":"프론트맨","巳":"드럼","午":"리드기타","未":"베이스","申":"테크니컬베이스","酉":"솔로기타","戌":"드럼","亥":"작곡"}
    return siju, insts.get(jis[idx], "뮤지션")

# 3. 입력 화면
st.title("🏯 2080 정통 명리 & 뮤지션 마스터")
with st.form("main_form"):
    name = st.text_input("성함", placeholder="이름을 입력하세요")
    c1, c2, c3 = st.columns(3)
    y = c1.number_input("연도", 1920, 2030, value=None, placeholder="YYYY")
    m = c2.number_input("월", 1, 12, value=None, placeholder="MM")
    d = c3.number_input("일", 1, 31, value=None, placeholder="DD")
    u_type = st.radio("구분", ["양력", "음력"], horizontal=True)
    t_opt = ["시간 모름"] + [f"{i:02d}시 ~ {i+1:02d}시" for i in range(23)] + ["23시 ~ 00시"]
    t = st.selectbox("시간", t_opt)
    target = st.number_input("분석 연도", 1950, 2080, 2026)
    submit = st.form_submit_button("심층 분석 시작")

# 4. 심층 리포트 출력
if submit:
    if not name or y is None or m is None or d is None:
        st.warning("정보를 입력해주세요.")
    else:
        cal = KoreanLunarCalendar()
        if u_type == "음력": cal.setLunarDate(int(y), int(m), int(d), False)
        else: cal.setSolarDate(int(y), int(m), int(d))
        ganji = cal.getChineseGapJaString().split()
        siju, inst = get_saju_data(ganji[2][0], t)
        
        # 사주 원국 시각화
        st.markdown("---")
        cols = st.columns(4)
        titles = ["시주", "일주", "월주", "연주"]
        vals = [siju, ganji[2], ganji[1], ganji[0]]
        for i in range(4):
            cols[i].markdown(f"<div class='pillar-box'><small>{titles[i]}</small><div class='pillar-ganji'>{vals[i]}</div></div>", unsafe_allow_html=True)

        # 자세한 해석 로직
        report = f"""
        <div class="result-card">
            <div class="res-title">📜 {name}님 명리/뮤지션 심층 리포트</div>
            <div class="res-body">
                <span class="res-sub">● 정통 명리학적 기질
