import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
import pandas as pd

st.set_page_config(page_title="뮤지션을 위한 사주보기", layout="wide")

st.title("🎸 뮤지션을 위한 사주보기")

st.write("생년월일을 입력하면 사주와 음악적 성향을 분석합니다.")

# -------------------------------
# 오행 매핑
# -------------------------------

element_map = {
    "갑":"목","을":"목",
    "병":"화","정":"화",
    "무":"토","기":"토",
    "경":"금","신":"금",
    "임":"수","계":"수",

    "인":"목","묘":"목",
    "사":"화","오":"화",
    "진":"토","술":"토","축":"토","미":"토",
    "신":"금","유":"금",
    "해":"수","자":"수"
}

# -------------------------------
# 십신 표 (간단)
# -------------------------------

ten_gods = {

"목":{
"목":"비견",
"화":"식신",
"토":"편재",
"금":"편관",
"수":"편인"
},

"화":{
"목":"편인",
"화":"비견",
"토":"식신",
"금":"편재",
"수":"편관"
},

"토":{
"목":"편관",
"화":"편인",
"토":"비견",
"금":"식신",
"수":"편재"
},

"금":{
"목":"편재",
"화":"편관",
"토":"편인",
"금":"비견",
"수":"식신"
},

"수":{
"목":"식신",
"화":"편재",
"토":"편관",
"금":"편인",
"수":"비견"
}

}

# -------------------------------
# 입력
# -------------------------------

c1,c2,c3 = st.columns(3)

year = c1.number_input("출생 연도",1900,2100,1985)
month = c2.number_input("출생 월",1,12,1)
day = c3.number_input("출생 일",1,31,1)

hour = st.selectbox("출생 시간",[
"모름",
"자(23-01)","축(01-03)","인(03-05)","묘(05-07)",
"진(07-09)","사(09-11)","오(11-13)","미(13-15)",
"신(15-17)","유(17-19)","술(19-21)","해(21-23)"
])

# -------------------------------
# 사주 계산
# -------------------------------

if st.button("사주 보기"):

    cal = KoreanLunarCalendar()
    cal.setSolarDate(year,month,day)

    ganji = cal.getChineseGapJaString().split()

    if len(ganji) < 3:
        st.error("사주 계산 오류")
        st.stop()

    year_p = ganji[0]
    month_p = ganji[1]
    day_p = ganji[2]

    hour_p = "--"

    pillars = [year_p,month_p,day_p]

    # -------------------------------
    # 사주 출력
    # -------------------------------

    st.header("사주 팔자")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("년주",year_p)
    col2.metric("월주",month_p)
    col3.metric("일주",day_p)
    col4.metric("시주",hour_p)

    # -------------------------------
    # 오행 계산
    # -------------------------------

    elements = {
    "목":0,
    "화":0,
    "토":0,
    "금":0,
    "수":0
    }

    for p in pillars:

        g = p[0]
        j = p[1]

        if g in element_map:
            elements[element_map[g]] += 1

        if j in element_map:
            elements[element_map[j]] += 1

    st.header("오행 분석")

    df = pd.DataFrame(
    list(elements.items()),
    columns=["오행","개수"]
    )

    st.bar_chart(df.set_index("오행"))

    # -------------------------------
    # 일간
    # -------------------------------

    day_stem = day_p[0]

    day_element = element_map.get(day_stem,"")

    st.subheader(f"일간 : {day_stem} ({day_element})")

    # -------------------------------
    # 십신 계산
    # -------------------------------

    st.header("십신 분석")

    ten_list = []

    for p in pillars:

        g = p[0]
        g_el = element_map.get(g,"")

        if g_el and day_element:
            tg = ten_gods[day_element][g_el]
            ten_list.append((p,tg))

    tg_df = pd.DataFrame(ten_list,columns=["기둥","십신"])

    st.table(tg_df)

    # -------------------------------
    # 성향 분석
    # -------------------------------

    st.header("성향 분석")

    char = []

    if elements["목"] >= 2:
        char.append("창의적이고 새로운 것을 만드는 성향")

    if elements["화"] >= 2:
        char.append("표현력이 강하고 무대 체질")

    if elements["금"] >= 2:
        char.append("리듬감과 구조 감각이 뛰어남")

    if elements["수"] >= 2:
        char.append("감성적이고 음악적 분위기 표현이 좋음")

    if elements["토"] >= 2:
        char.append("꾸준하고 안정적인 스타일")

    if len(char)==0:
        char.append("오행 균형형 성향")

    for c in char:
        st.write("•",c)

    # -------------------------------
    # 뮤지션 분석
    # -------------------------------

    st.header("🎸 뮤지션 성향 분석")

    music = []

    if elements["목"] >= 2:
        music.append("작곡 능력 높음")

    if elements["화"] >= 2:
        music.append("무대 퍼포먼스 강함")

    if elements["금"] >= 2:
        music.append("리듬 중심 음악 적합")

    if elements["수"] >= 2:
        music.append("감성적인 음악 스타일")

    if elements["토"] >= 2:
        music.append("밴드 안정형 플레이어")

    if len(music)==0:
        music.append("다양한 장르 적응형")

    for m in music:
        st.write("•",m)

    # -------------------------------
    # 장르 추천
    # -------------------------------

    st.header("🎶 추천 음악 장르")

    genre = []

    if elements["화"] >= 2 and elements["목"] >= 2:
        genre.append("록 / 블루스")

    if elements["금"] >= 2:
        genre.append("펑크 / 재즈")

    if elements["수"] >= 2:
        genre.append("발라드 / 포크")

    if elements["토"] >= 2:
        genre.append("팝 / 세션 음악")

    if len(genre)==0:
        genre.append("올라운드 장르")

    for g in genre:
        st.write("•",g)

    # -------------------------------
    # 직업 추천
    # -------------------------------

    st.header("🎸 뮤지션 직업 추천")

    jobs = []

    if elements["목"] >= 2:
        jobs.append("작곡가")

    if elements["화"] >= 2:
        jobs.append("보컬 / 프론트맨")

    if elements["금"] >= 2:
        jobs.append("드러머 / 베이시스트")

    if elements["수"] >= 2:
        jobs.append("싱어송라이터")

    if elements["토"] >= 2:
        jobs.append("프로듀서 / 편곡가")

    if len(jobs)==0:
        jobs.append("세션 연주자")

    for j in jobs:
        st.write("•",j)

    st.success("분석 완료 🎵")
