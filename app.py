# musician_saju_app.py
# MIT compatible implementation
# Streamlit single-file app

import streamlit as st
from datetime import datetime, timedelta
from korean_lunar_calendar import KoreanLunarCalendar
import math

st.set_page_config(page_title="뮤지션을 위한 사주보기", layout="centered")

# 천간 / 지지
HEAVENLY = ["갑","을","병","정","무","기","경","신","임","계"]
EARTHLY = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

# 오행
STEM_ELEMENT = {
"갑":"목","을":"목",
"병":"화","정":"화",
"무":"토","기":"토",
"경":"금","신":"금",
"임":"수","계":"수"
}

BRANCH_ELEMENT = {
"자":"수","축":"토","인":"목","묘":"목","진":"토","사":"화",
"오":"화","미":"토","신":"금","유":"금","술":"토","해":"수"
}

# 십신 테이블
TEN_GODS_TABLE = {
"목":["비견","겁재","식신","상관","편재","정재","편관","정관","편인","정인"],
"화":["비견","겁재","식신","상관","편재","정재","편관","정관","편인","정인"],
"토":["비견","겁재","식신","상관","편재","정재","편관","정관","편인","정인"],
"금":["비견","겁재","식신","상관","편재","정재","편관","정관","편인","정인"],
"수":["비견","겁재","식신","상관","편재","정재","편관","정관","편인","정인"]
}

MUSIC_RULE = {
"목":{"작곡":2,"기타":1},
"화":{"보컬":2,"퍼포먼스":2},
"토":{"프로듀싱":2},
"금":{"연주":2},
"수":{"감성":2}
}

REFERENCE_DAY = datetime(1900,1,31)  # 갑자일 기준

def get_year_ganzhi(year):

    stem = HEAVENLY[(year-4)%10]
    branch = EARTHLY[(year-4)%12]
    return stem+branch

def get_month_ganzhi(year_stem, month):

    stem_index = HEAVENLY.index(year_stem)
    stem = HEAVENLY[(stem_index*2 + month)%10]
    branch = EARTHLY[(month+1)%12]
    return stem+branch

def get_day_ganzhi(date):

    diff = (date - REFERENCE_DAY).days
    stem = HEAVENLY[diff%10]
    branch = EARTHLY[diff%12]
    return stem+branch

def get_hour_ganzhi(day_stem, hour):

    stem_index = HEAVENLY.index(day_stem)
    branch = EARTHLY[((hour+1)//2)%12]
    stem = HEAVENLY[(stem_index*2 + ((hour+1)//2))%10]

    return stem+branch

def count_elements(pillars):

    result = {"목":0,"화":0,"토":0,"금":0,"수":0}

    for p in pillars:
        stem = p[0]
        branch = p[1]

        result[STEM_ELEMENT[stem]] +=1
        result[BRANCH_ELEMENT[branch]] +=1

    return result

def strong_weak(elements):

    fire = elements["화"]
    wood = elements["목"]
    water = elements["수"]
    metal = elements["금"]

    score = wood+fire - (water+metal)

    if score >=2:
        return "신강"
    if score <= -2:
        return "신약"
    return "중화"

def calculate_ten_god(day_stem, other_stem):

    dm = STEM_ELEMENT[day_stem]
    idx = HEAVENLY.index(other_stem)

    return TEN_GODS_TABLE[dm][idx]

def calc_music(elements):

    score = {
    "작곡":0,
    "보컬":0,
    "연주":0,
    "프로듀싱":0,
    "감성":0
    }

    for e,c in elements.items():

        if e in MUSIC_RULE:
            for k,v in MUSIC_RULE[e].items():
                score[k]+=c*v

    return score

def calc_luck_cycles(birth_year):

    start = birth_year + 8

    cycles=[]
    for i in range(8):
        s = start + i*10
        e = s+9
        cycles.append(f"{s} ~ {e}")

    return cycles

def yearly_luck(elements):

    if elements["화"]>=3:
        return "공연운 상승"

    if elements["목"]>=3:
        return "창작운 상승"

    if elements["금"]>=3:
        return "연주활동 증가"

    if elements["수"]>=3:
        return "감성적 작품 시기"

    return "안정적인 음악 활동"

st.title("뮤지션을 위한 사주보기")

gender = st.selectbox("성별",["남","여"])

calendar_type = st.selectbox("달력",["양력","음력"])

leap = st.checkbox("윤달")

birth_date = st.date_input("생년월일")

hour = st.slider("출생 시간",0,23,6)

target_year = st.number_input("보고 싶은 년도",1900,2100,2026)

if st.button("사주 분석"):

    if calendar_type=="음력":

        cal = KoreanLunarCalendar()
        cal.setLunarDate(birth_date.year,birth_date.month,birth_date.day,leap)
        solar = datetime.strptime(cal.SolarIsoFormat(),"%Y-%m-%d")

    else:
        solar = birth_date

    y = get_year_ganzhi(solar.year)

    m = get_month_ganzhi(y[0],solar.month)

    d = get_day_ganzhi(solar)

    h = get_hour_ganzhi(d[0],hour)

    pillars=[y,m,d,h]

    st.header("사주팔자")

    st.write("년주:",y)
    st.write("월주:",m)
    st.write("일주:",d)
    st.write("시주:",h)

    elements = count_elements(pillars)

    st.header("오행 분석")

    for k,v in elements.items():
        st.write(k,v)

    sw = strong_weak(elements)

    st.header("신강 신약")

    st.write(sw)

    st.header("십신")

    for p in pillars:

        tg = calculate_ten_god(d[0],p[0])

        st.write(p, tg)

    st.header("뮤지션 적성")

    music = calc_music(elements)

    for k,v in music.items():

        stars = "★"*min(5,max(1,v))

        st.write(k,stars)

    st.header("직업 성향")

    if elements["목"]>=2:
        st.write("창작형 음악가")

    if elements["화"]>=2:
        st.write("무대형 아티스트")

    if elements["금"]>=2:
        st.write("연주 중심 음악가")

    if elements["토"]>=2:
        st.write("프로듀서 성향")

    st.header("대운")

    cycles = calc_luck_cycles(solar.year)

    for c in cycles:
        st.write(c)

    st.header(f"{target_year} 운세")

    st.write(yearly_luck(elements))

    st.header("종합 해석")

    if elements["화"]>=2 and elements["목"]>=2:
        st.write("예술성과 표현력이 강한 뮤지션 사주")

    elif elements["수"]>=2:
        st.write("감성 중심 음악가")

    else:
        st.write("균형형 음악 활동")
