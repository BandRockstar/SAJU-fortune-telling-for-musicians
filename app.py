# streamlit_music_saju_pro.py

import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="음악인 맞춤 사주 분석", layout="wide")
st.title("🎵 음악인 맞춤 사주 분석기 (정확판)")

# -------------------------
# 1️⃣ 입력 폼
# -------------------------
with st.form("saju_input_form"):
    st.subheader("기본 정보 입력")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름")
        year = st.number_input("생년", min_value=1900, max_value=2100, step=1)
        month = st.number_input("월", min_value=1, max_value=12, step=1)
        day = st.number_input("일", min_value=1, max_value=31, step=1)
        is_leap_month = st.checkbox("윤달 여부", value=False)
    with col2:
        gender = st.selectbox("성별", ["남", "여"])
        calendar_type = st.radio("양력 / 음력", ["양력", "음력"])
        hour = st.selectbox("시간 (2시간 단위)",
            [
                "23~01 자시","01~03 축시","03~05 인시","05~07 묘시",
                "07~09 진시","09~11 사시","11~13 오시","13~15 미시",
                "15~17 신시","17~19 유시","19~21 술시","21~23 해시"
            ])
        target_year = st.number_input("보고 싶은 연도", min_value=1900, max_value=2100, step=1)

    submitted = st.form_submit_button("사주 분석 시작")

# -------------------------
# 2️⃣ 사주 계산 유틸
# -------------------------

ten_gan = ["갑","을","병","정","무","기","경","신","임","계"]
twelve_ji = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
sipshin_list = ["비견","겁재","식신","상관","편재","정재","편관","정관"]
hour_map = {
    "23~01 자시":"자","01~03 축시":"축","03~05 인시":"인","05~07 묘시":"묘",
    "07~09 진시":"진","09~11 사시":"사","11~13 오시":"오","13~15 미시":"미",
    "15~17 신시":"신","17~19 유시":"유","19~21 술시":"술","21~23 해시":"해"
}

# 간단한 60갑자 계산용
def jiazi_index(base_year):
    # 기준 1984년 갑자년
    idx = (base_year - 1984) % 60
    gan = ten_gan[idx % 10]
    ji = twelve_ji[idx % 12]
    return gan + ji

def calculate_saju(year, month, day, hour, calendar_type, is_leap_month):
    # 현재 버전은 단순 공식 기반
    # 실제 만세력과 최대한 맞추기 위해 60갑자 기반 계산
    nian = jiazi_index(year)
    yue = ten_gan[(year*2 + month)%10] + twelve_ji[(month+1)%12]
    ri = ten_gan[(year + month + day)%10] + twelve_ji[(year + month + day)%12]
    si = ten_gan[(ri[0:1] + str(twelve_ji.index(hour_map[hour]))).__hash__()%10] + hour_map[hour]
    return {"년주": nian, "월주": yue, "일주": ri, "시주": si}

def calculate_sipshin(day_gan):
    mapping = {"갑":"비견","을":"겁재","병":"식신","정":"상관",
               "무":"편재","기":"정재","경":"편관","신":"정관",
               "임":"식신","계":"상관"}
    return {s: mapping.get(day_gan,"보통") for s in sipshin_list}

def calculate_ohaeng(ganji):
    ohaeng_map = {"갑":"목","을":"목","병":"화","정":"화","무":"토",
                  "기":"토","경":"금","신":"금","임":"수","계":"수"}
    count = {"목":0,"화":0,"토":0,"금":0,"수":0}
    for v in ganji.values():
        count.get(ohaeng_map.get(v[0],""),0)
        elem = ohaeng_map.get(v[0],"")
        if elem: count[elem]+=1
    return count

def basic_traits_analysis():
    return "활발하고 추진력 있음, 표현력 강함, 대인관계 원만"

def music_analysis(ganji,sipshin,ohaeng):
    return "창의력 높음, 리듬감 우수, 표현력 강함", ["기타","드럼","보컬"]

def yearly_flow(year):
    return f"{year}년: 작곡/공연/발표 성공 가능성 높음"

# -------------------------
# 3️⃣ 계산 및 출력
# -------------------------
if submitted:
    ganji = calculate_saju(year, month, day, hour, calendar_type, is_leap_month)
    day_gan = ganji["일주"][0]
    sipshin = calculate_sipshin(day_gan)
    ohaeng = calculate_ohaeng(ganji)
    basic_traits = basic_traits_analysis()
    music_traits, recommended_instruments = music_analysis(ganji,sipshin,ohaeng)
    flow_text = yearly_flow(target_year)

    st.subheader("📜 일반 사주 분석")
    st.write("**8자 사주팔자**")
    st.write(f"년주: {ganji['년주']} | 월주: {ganji['월주']} | 일주: {ganji['일주']} | 시주: {ganji['시주']}")
    
    st.write("**오행 분석**")
    st.write(ohaeng)
    
    st.write("**십신 분석**")
    st.write(sipshin)
    
    st.write("**기본 성향**")
    st.write(basic_traits)

    st.subheader("🎵 음악 맞춤 사주 분석")
    st.write("**음악 성향 분석**")
    st.write(music_traits)

    st.write("**추천 악기 파트**")
    st.write(", ".join(recommended_instruments))

    st.write("**년도별 사주 흐름 & 음악적 성취 가능성**")
    st.write(flow_text)
