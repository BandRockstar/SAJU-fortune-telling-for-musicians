import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

# 1. 화면 스타일 설정
st.set_page_config(page_title="2080 뮤지션 만세력", layout="centered")
st.markdown("<style>.res-card{background-color:#1a222f;padding:25px;border-radius:15px;border:1px solid #d4af37;margin-top:20px;}.pillar-box{background:#0b111a;padding:15px;border-radius:10px;border:2px solid #4a4a4a;text-align:center;}.pillar-ganji{color:#d4af37;font-size:1.5rem;font-weight:bold;}</style>", unsafe_allow_html=True)

# 2. 로직 (가장 단순한 구조로 재작성)
def get_saju(day_gan, t_str):
    if t_str == "시간 모름": return "??", "전천후"
    h = int(t_str[:2])
    jis = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
    h_idx = {23:0,0:0,1:1,2:1,3:2,4:2,5:3,6:3,7:4,8:4,9:5,10:5,11:6,12:6,13:7,14:7,15:8,16:8,17:9,18:9,19:10,20:10,21:11,22:11}
    idx = h_idx.get(h, 0)
    gans = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    s_map = {"甲":0,"己":0,"乙":2,"庚":2,"丙":4,"辛":4,"丁":6,"壬":6,"戊":8,"癸":8}
    siju = gans[(s_map.get(day_gan, 0) + idx) % 10] + jis[idx]
    insts = {"子":"키보드","丑":"베이스","寅":"기타","卯":"리듬기타/보컬","辰":"프론트맨","巳":"드럼","午":"리드기타","未":"베이스","申":"테크니컬베이스","酉":"솔로기타","戌":"드럼","亥":"작곡"}
    return siju, insts.get(jis[idx], "뮤지션")

# 3. 입력창 (모두 빈칸)
st.title("🏯 2080 정통 명리 & 뮤지션 마스터")
with st.form("main"):
    name = st.text_input("성함")
    c1, c2, c3 = st.columns(3)
    y = c1.number_input("연도", 1920, 2030, value=None)
    m = c2.number_input("월", 1, 12, value=None)
    d = c3.number_input("일", 1, 31, value=None)
    u_type = st.radio("날짜 구분", ["양력", "음력"], horizontal=True)
    t_opt = ["시간 모름"] + [f"{i:02d}시 ~ {i+1:02d}시" for i in range(23)]
    t = st.selectbox("태어난 시간", t_opt)
    target = st.number_input("분석 연도", 1950, 2080, 2026)
    btn = st.form_submit_button("분석 실행")

# 4. 결과 출력
if btn:
    if not name or y is None or m is None or d is None:
        st.warning("모든 정보를 입력해주세요.")
    else:
        cal = KoreanLunarCalendar()
        if u_type == "음력": cal.setLunarDate(int(y), int(m), int(d), False)
        else: cal.setSolarDate(int(y), int(m), int(d))
        ganji = cal.getChineseGapJaString().split()
        siju, inst = get_saju(ganji[2][0], t)
        
        st.markdown("---")
        cols = st.columns(4)
        vals = [siju, ganji[2], ganji[1], ganji[0]]
        for i, v in enumerate(vals):
            cols[i].markdown(f"<div class='pillar-box'><div class='pillar-ganji'>{v}</div></div>", unsafe_allow_html=True)

        # 심층 리포트 (에러 방지를 위해 변수 분리)
        line1 = f"당신은 <b>{ganji[2]}</b> 일주로, 태양과 같은 발산의 기운을 가졌습니다."
        line2 = f"격국상 <b>{ganji[1][1]}</b>월의 기운을 써서 독창적인 예술성을 발휘합니다."
        line3 = f"포지션은 <b>{inst}</b>이며, <b>{siju}</b>시의 영향으로 정교한 테크닉을 완성합니다."
        line4 = f"{target}년은 당신의 잠재력이 현실적 성취로 이어지는 중요한 해가 될 것입니다."
        
        st.markdown(f"<div class='result-card'><h3>📜 {name}님 심층 리포트</h3><p>{line1}<br>{line2}<br><br><b>포지션: {inst}</b><br>{line3}<br><br>{line4}</p></div>", unsafe_allow_html=True
