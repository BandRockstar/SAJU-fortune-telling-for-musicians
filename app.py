import streamlit as st
from datetime import datetime
import sxtwl

st.set_page_config(page_title="뮤지션을 위한 사주보기", layout="centered")

st.title("🎸 뮤지션을 위한 사주보기")

gender = st.selectbox("성별", ["남", "여"])
birth_date = st.date_input("생년월일")
birth_hour = st.slider("출생 시간", 0, 23, 12)
target_year = st.number_input("보고 싶은 년도", 1900, 2100, 2026)

HEAVENLY = ["갑","을","병","정","무","기","경","신","임","계"]
EARTHLY = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

ELEMENT_STEM = {
"갑":"목","을":"목",
"병":"화","정":"화",
"무":"토","기":"토",
"경":"금","신":"금",
"임":"수","계":"수"
}

ELEMENT_BRANCH = {
"자":"수","축":"토","인":"목","묘":"목",
"진":"토","사":"화","오":"화","미":"토",
"신":"금","유":"금","술":"토","해":"수"
}

def element_count(pillars):

    result = {"목":0,"화":0,"토":0,"금":0,"수":0}

    for p in pillars:

        stem = p[0]
        branch = p[1]

        result[ELEMENT_STEM[stem]] += 1
        result[ELEMENT_BRANCH[branch]] += 1

    return result

def music_analysis(elements):

    score = {
        "작곡":elements["목"]*2 + elements["수"],
        "보컬":elements["화"]*2,
        "연주":elements["금"] + elements["화"],
        "프로듀싱":elements["토"] + elements["금"],
        "감성":elements["수"]*2
    }

    return score

if st.button("사주 분석"):

    day = sxtwl.fromSolar(birth_date.year, birth_date.month, birth_date.day)

    year_gz = day.getYearGZ()
    month_gz = day.getMonthGZ()
    day_gz = day.getDayGZ()
    hour_gz = day.getHourGZ(birth_hour)

    year = HEAVENLY[year_gz.tg] + EARTHLY[year_gz.dz]
    month = HEAVENLY[month_gz.tg] + EARTHLY[month_gz.dz]
    day_pillar = HEAVENLY[day_gz.tg] + EARTHLY[day_gz.dz]
    hour = HEAVENLY[hour_gz.tg] + EARTHLY[hour_gz.dz]

    pillars = [year, month, day_pillar, hour]

    st.header("사주팔자")

    st.write("년주 :", year)
    st.write("월주 :", month)
    st.write("일주 :", day_pillar)
    st.write("시주 :", hour)

    elements = element_count(pillars)

    st.header("오행 분석")

    for k,v in elements.items():
        st.write(k, v)

    st.header("뮤지션 적성")

    music = music_analysis(elements)

    for k,v in music.items():

        stars = "★"*min(5,max(1,v))

        st.write(k, stars)

    st.header("종합 해석")

    if elements["화"] >= 2 and elements["목"] >= 2:
        st.write("창작과 표현력이 강한 음악가 사주")

    elif elements["수"] >= 2:
        st.write("감성 중심 음악 스타일")

    elif elements["금"] >= 2:
        st.write("연주 중심 음악가")

    else:
        st.write("균형형 음악 성향")

    st.header(f"{target_year}년 운세")

    if elements["화"] >= 3:
        st.write("공연운 상승")

    elif elements["목"] >= 3:
        st.write("창작운 상승")

    elif elements["금"] >= 3:
        st.write("연주 활동 증가")

    else:
        st.write("안정적인 음악 활동")
