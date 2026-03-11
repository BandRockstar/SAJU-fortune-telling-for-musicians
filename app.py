# streamlit_music_saju_real.py

import streamlit as st
from datetime import datetime
from lunardate import LunarDate  # pip install lunardate

st.set_page_config(page_title="음악인 맞춤 사주 분석", layout="wide")
st.title("🎵 음악인 맞춤 사주 분석기")

# -------------------------
# 1️⃣ 사용자 입력 폼
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
                "23~01 자시", "01~03 축시", "03~05 인시", "05~07 묘시",
                "07~09 진시", "09~11 사시", "11~13 오시", "13~15 미시",
                "15~17 신시", "17~19 유시", "19~21 술시", "21~23 해시"
            ]
        )
        target_year = st.number_input("보고 싶은 연도", min_value=1900, max_value=2100, step=1)

    submitted = st.form_submit_button("사주 분석 시작")

# -------------------------
# 2️⃣ 사주 계산 유틸리티
# -------------------------

# 천간, 지지, 십신 정의
ten_gan = ["갑","을","병","정","무","기","경","신","임","계"]
twelve_ji = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
# 십신 예시
sipshin_list = ["비견","겁재","식신","상관","편재","정재","편관","정관"]

# 시각 → 시지 매핑
hour_map = {
    "23~01 자시":"자","01~03 축시":"축","03~05 인시":"인","05~07 묘시":"묘",
    "07~09 진시":"진","09~11 사시":"사","11~13 오시":"오","13~15 미시":"미",
    "15~17 신시":"신","17~19 유시":"유","19~21 술시":"술","21~23 해시":"해"
}

def convert_to_lunar(y, m, d, calendar_type, is_leap):
    if calendar_type == "양력":
        # 양력 → 음력
        try:
            lunar = LunarDate.fromSolarDate(y, m, d)
            return lunar.year, lunar.month, lunar.day
        except:
            return y, m, d  # 변환 실패 시 그대로
    else:
        # 음력 그대로
        return y, m, d

def calculate_ganji(y, m, d, hour_str):
    # 간단 공식 기반 계산 (연주, 월주, 일주, 시주)
    # 실제 만세력 공식은 복잡 → 여기서는 예시용
    year_index = (y - 4) % 10
    year_j = (y - 4) % 12
    ganji = {
        "년주": ten_gan[year_index] + twelve_ji[year_j],
        "월주": ten_gan[(year_index*2 + m) % 10] + twelve_ji[(m+1)%12],
        "일주": ten_gan[(y + m + d)%10] + twelve_ji[(y + m + d)%12],
        "시주": ten_gan[(year_index + twelve_ji.index(hour_map[hour_str]))%10] + hour_map[hour_str]
    }
    return ganji

def calculate_sipshin(day_gan):
    # 일간 기준으로 십신 예시 생성
    mapping = {
        "갑":"비견","을":"겁재","병":"식신","정":"상관",
        "무":"편재","기":"정재","경":"편관","신":"정관",
        "임":"식신","계":"상관"
    }
    sipshin = {}
    for s in sipshin_list:
        sipshin[s] = mapping.get(day_gan, "보통")
    return sipshin

def calculate_ohaeng(ganji):
    # 천간 기준 오행 분포 예시
    ohaeng_map = {
        "갑":"목","을":"목","병":"화","정":"화","무":"토",
        "기":"토","경":"금","신":"금","임":"수","계":"수"
    }
    count = {"목":0,"화":0,"토":0,"금":0,"수":0}
    for k,v in ganji.items():
        gan = v[0]
        elem = ohaeng_map.get(gan,"")
        if elem: count[elem] +=1
    return count

def basic_traits_analysis():
    return "활발하고 추진력 있음, 표현력 강함, 대인관계 원만"

def music_analysis(ganji, sipshin, ohaeng):
    return "창의력 높음, 리듬감 우수, 표현력 강함", ["기타","드럼","보컬"]

def yearly_flow(year):
    return f"{year}년: 작곡/공연/발표 성공 가능성 높음"

# -------------------------
# 3️⃣ 사주 계산 및 출력
# -------------------------
if submitted:
    lunar_y, lunar_m, lunar_d = convert_to_lunar(year, month, day, calendar_type, is_leap_month)
    ganji = calculate_ganji(lunar_y, lunar_m, lunar_d, hour)
    day_gan = ganji["일주"][0]
    sipshin = calculate_sipshin(day_gan)
    ohaeng = calculate_ohaeng(ganji)
    basic_traits = basic_traits_analysis()
    music_traits, recommended_instruments = music_analysis(ganji, sipshin, ohaeng)
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
