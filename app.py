# streamlit_music_saju.py

import streamlit as st
from datetime import datetime

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
# 2️⃣ 사주 계산 함수 (예시/기본)
# -------------------------
def calculate_saju(year, month, day, hour, calendar_type, is_leap_month):
    # 실제 계산은 만세력 공식 기반
    # 여기서는 예시값 반환
    saju = {
        "년주": "甲子", "월주": "乙丑",
        "일주": "丙寅", "시주": "丁卯"
    }
    ohaeng = {
        "목": 2, "화": 2, "토": 1, "금": 1, "수": 2
    }
    sipshin = {
        "정재": "적당", "편재": "높음",
        "식신": "높음", "상관": "보통",
        "정관": "적당", "편관": "낮음",
        "비견": "보통", "겁재": "낮음"
    }
    basic_traits = "활발하고 추진력 있음, 표현력 강함, 대인관계 원만"
    return saju, ohaeng, sipshin, basic_traits

# -------------------------
# 3️⃣ 음악 맞춤 분석 함수
# -------------------------
def music_analysis(saju, sipshin, ohaeng):
    # 예시 규칙 기반 추천
    music_traits = "창의력 높음, 리듬감 우수, 표현력 강함"
    recommended_instruments = ["기타", "드럼", "보컬"]
    return music_traits, recommended_instruments

# -------------------------
# 4️⃣ 년도별 흐름 계산 함수
# -------------------------
def yearly_flow(target_year):
    # 예시 데이터
    flow_text = f"{target_year}년: 작곡/공연/발표 성공 가능성 높음"
    return flow_text

# -------------------------
# 5️⃣ 출력
# -------------------------
if submitted:
    saju, ohaeng, sipshin, basic_traits = calculate_saju(year, month, day, hour, calendar_type, is_leap_month)
    music_traits, recommended_instruments = music_analysis(saju, sipshin, ohaeng)
    flow_text = yearly_flow(target_year)

    st.subheader("📜 일반 사주 분석")
    st.write("**8자 사주팔자**")
    st.write(f"년주: {saju['년주']} | 월주: {saju['월주']} | 일주: {saju['일주']} | 시주: {saju['시주']}")
    
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
