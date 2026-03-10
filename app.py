import streamlit as st
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar
import random

st.set_page_config(page_title="뮤지션을 위한 사주보기", layout="centered")

st.title("🎸 뮤지션을 위한 사주보기")

gender = st.selectbox("성별", ["남", "여"])
calendar_type = st.selectbox("달력", ["양력", "음력"])
leap_month = st.checkbox("윤달")

birth_date = st.date_input("생년월일")
birth_hour = st.slider("태어난 시간", 0, 23, 6)

target_year = st.number_input("보고 싶은 년도", 1900, 2100, 2026)

heavenly = ["갑","을","병","정","무","기","경","신","임","계"]
earthly = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

elements = {
    "갑":"목","을":"목",
    "병":"화","정":"화",
    "무":"토","기":"토",
    "경":"금","신":"금",
    "임":"수","계":"수"
}

ten_gods = [
"비견","겁재","식신","상관",
"편재","정재","편관","정관",
"편인","정인"
]

def calculate_saju(date, hour):

    y = heavenly[date.year % 10] + earthly[date.year % 12]
    m = heavenly[(date.month+1) % 10] + earthly[(date.month+1) % 12]
    d = heavenly[(date.day+2) % 10] + earthly[(date.day+2) % 12]
    h = heavenly[hour % 10] + earthly[hour % 12]

    return y,m,d,h

def element_count(saju):

    count = {"목":0,"화":0,"토":0,"금":0,"수":0}

    for s in saju:
        stem = s[0]
        e = elements.get(stem,"")
        if e:
            count[e]+=1

    return count

def music_score(elements):

    score = {
        "작곡":elements["목"]*2 + elements["수"],
        "보컬":elements["화"]*2,
        "연주":elements["금"] + elements["화"],
        "프로듀싱":elements["토"] + elements["금"]
    }

    return score

def strong_weak(elements):

    if elements["화"] + elements["목"] >= 4:
        return "신강"
    elif elements["수"] + elements["금"] >=4:
        return "신약"
    else:
        return "중화"

if st.button("사주 분석하기"):

    year,month,day,hour = calculate_saju(birth_date,birth_hour)

    st.header("사주팔자")

    st.write(f"년주 : {year}")
    st.write(f"월주 : {month}")
    st.write(f"일주 : {day}")
    st.write(f"시주 : {hour}")

    saju = [year,month,day,hour]

    el = element_count(saju)

    st.header("오행 분석")

    for k,v in el.items():
        st.write(f"{k} : {v}")

    st.header("신강 / 신약")

    sw = strong_weak(el)

    st.write(sw)

    st.header("십신")

    for i in saju:
        st.write(random.choice(ten_gods))

    st.header("뮤지션 적성")

    score = music_score(el)

    for k,v in score.items():

        stars = "★"*min(v,5)

        st.write(f"{k} : {stars}")

    st.header("직업 성향")

    if el["화"] >=3:
        st.write("무대형 예술가")

    if el["목"] >=3:
        st.write("창작형 음악가")

    if el["금"] >=2:
        st.write("연주 중심 음악가")

    if el["토"] >=2:
        st.write("프로듀서형")

    st.header("대운")

    start = birth_date.year + 10

    for i in range(8):

        y = start + i*10

        st.write(f"{y} ~ {y+9}")

    st.header(f"{target_year}년 운세")

    luck = random.choice([
        "창작운 상승",
        "공연 기회 증가",
        "새로운 음악 인연",
        "음악 활동 확장",
        "작품 발표 운"
    ])

    st.write(luck)

    st.header("종합 해석")

    if el["화"] >=2 and el["목"] >=2:
        st.write("예술성과 표현력이 강한 음악가 사주")

    elif el["수"] >=2:
        st.write("감성 중심 음악가")

    else:
        st.write("균형형 음악가")
