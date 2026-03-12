import streamlit as st
from lunar_python import Solar

st.set_page_config(page_title="사주 운세 프로그램", layout="centered")

st.title("🔮 사주 운세 분석")

name = st.text_input("이름")

gender = st.radio("성별",["남","여"])

col1,col2,col3 = st.columns(3)

with col1:
    year = st.number_input("출생년",1900,2100,1981)

with col2:
    month = st.number_input("출생월",1,12,2)

with col3:
    day = st.number_input("출생일",1,31,7)

hour = st.slider("출생시간",0,23,6)

calendar = st.radio("달력",["양력","음력"])

# 천간
stems=["갑","을","병","정","무","기","경","신","임","계"]

# 오행
elements={
"갑":"목","을":"목",
"병":"화","정":"화",
"무":"토","기":"토",
"경":"금","신":"금",
"임":"수","계":"수"
}

# 십신 계산
ten_god_table={
"병":{
"갑":"편인","을":"정인",
"병":"비견","정":"겁재",
"무":"식신","기":"상관",
"경":"편재","신":"정재",
"임":"편관","계":"정관"
}
}

def ten_god(day,other):

    if day in ten_god_table:
        return ten_god_table[day].get(other,"")

    return ""

def element_analysis(chars):

    result={"목":0,"화":0,"토":0,"금":0,"수":0}

    for c in chars:

        if c in elements:

            e=elements[c]

            result[e]+=1

    return result


if st.button("사주 분석"):

    if calendar=="양력":

        solar=Solar.fromYmdHms(year,month,day,hour,0,0)

        lunar=solar.getLunar()

    else:

        lunar=Solar.fromYmd(year,month,day).getLunar()

    eight=lunar.getEightChar()

    year_gz=eight.getYear()
    month_gz=eight.getMonth()
    day_gz=eight.getDay()
    time_gz=eight.getTime()

    st.subheader("📜 사주팔자")

    st.write("년주 :",year_gz)
    st.write("월주 :",month_gz)
    st.write("일주 :",day_gz)
    st.write("시주 :",time_gz)

    day_stem=day_gz[0]

    st.subheader("십신")

    st.write("년간 :",ten_god(day_stem,year_gz[0]))
    st.write("월간 :",ten_god(day_stem,month_gz[0]))
    st.write("시간 :",ten_god(day_stem,time_gz[0]))

    chars=list(year_gz+month_gz+day_gz+time_gz)

    elem=element_analysis(chars)

    st.subheader("🌏 오행 분포")

    for k,v in elem.items():

        st.write(k,v)

    st.subheader("🔮 간단 운세")

    if elem["화"]>=3:

        st.write("🔥 화 기운이 강해 리더십과 예술성이 강합니다")

    elif elem["금"]>=3:

        st.write("⚙ 금 기운이 강해 분석력과 판단력이 뛰어납니다")

    elif elem["수"]>=3:

        st.write("💧 수 기운이 강해 지혜와 감성이 풍부합니다")

    else:

        st.write("🌱 균형 잡힌 사주입니다")
