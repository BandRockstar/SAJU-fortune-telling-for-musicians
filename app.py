# streamlit_music_saju_final.py

import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악인 맞춤 사주 분석", layout="wide")
st.title("🎵 음악인 맞춤 사주 분석기 (정밀, Lunar Python)")

# -------------------------
# 1️⃣ 입력 폼
# -------------------------
with st.form("saju_input_form"):
    st.subheader("기본 정보 입력")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름")
        year = st.number_input("생년", min_value=1900, max_value=2100, step=1, format="%d")
        month = st.number_input("월", min_value=1, max_value=12, step=1, format="%d")
        day = st.number_input("일", min_value=1, max_value=31, step=1, format="%d")
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
        target_year = st.number_input("보고 싶은 연도", min_value=1900, max_value=2100, step=1, format="%d")

    submitted = st.form_submit_button("사주 분석 시작")

# -------------------------
# 2️⃣ 사주 계산
# -------------------------
hour_map = {
    "23~01 자시":"子","01~03 축시":"丑","03~05 인시":"寅","05~07 묘시":"卯",
    "07~09 진시":"辰","09~11 사시":"巳","11~13 오시":"午","13~15 미시":"未",
    "15~17 신시":"申","17~19 유시":"酉","19~21 술시":"戌","21~23 해시":"亥"
}

def calculate_saju(year, month, day, hour, calendar_type, is_leap_month):
    # 타입 강제 int 변환
    year, month, day = int(year), int(month), int(day)
    if calendar_type == "음력":
        lunar = Lunar.fromYmd(year, month, day, is_leap_month)
        solar = lunar.getSolar()
        y, m, d = int(solar.getYear()), int(solar.getMonth()), int(solar.getDay())
    else:
        y, m, d = year, month, day

    solar = Solar(y, m, d)
    lunar = solar.getLunar()

    # 8자 계산
    year_gan = lunar.getYearGan()
    year_zhi = lunar.getYearZhi()
    month_gan = lunar.getMonthGan()
    month_zhi = lunar.getMonthZhi()
    day_gan = lunar.getDayGan()
    day_zhi = lunar.getDayZhi()
    hour_zhi = hour_map[hour]
    hour_gan = day_gan  # 단순화
    hour_zi = hour_zhi

    return {
        "년주": f"{year_gan}{year_zhi}",
        "월주": f"{month_gan}{month_zhi}",
        "일주": f"{day_gan}{day_zhi}",
        "시주": f"{hour_gan}{hour_zi}",
        "gan_zhi": (year_gan, month_gan, day_gan, hour_gan)
    }

# -------------------------
# 3️⃣ 십신/오행 + 음악 분석
# -------------------------
def music_analysis(saju_dict):
    day_gan = saju_dict["일주"][0]
    sipshin_map = {
        "甲":"비견","乙":"겁재","丙":"식신","丁":"상관",
        "戊":"편재","己":"정재","庚":"편관","辛":"정관",
        "壬":"식신","癸":"상관"
    }
    sipshin = {s:sipshin_map.get(day_gan,"보통") for s in ["비견","겁재","식신","상관","편재","정재","편관","정관"]}

    ohaeng_map = {"甲":"목","乙":"목","丙":"화","丁":"화","戊":"토",
                  "己":"토","庚":"금","辛":"금","壬":"수","癸":"수"}
    ohaeng = {"목":0,"화":0,"토":0,"금":0,"수":0}
    for g in saju_dict["gan_zhi"]:
        elem = ohaeng_map.get(g,"")
        if elem: ohaeng[elem]+=1

    basic_traits = "활발하고 추진력 있음, 표현력 강함, 대인관계 원만"
    music_traits = "창의력 높음, 리듬감 우수, 표현력 강함"
    recommended_instruments = ["기타","드럼","보컬"]
    return sipshin, ohaeng, basic_traits, music_traits, recommended_instruments

def yearly_flow(target_year):
    return f"{target_year}년: 작곡/공연/발표 성공 가능성 높음"

# -------------------------
# 4️⃣ 결과 출력
# -------------------------
if submitted:
    saju = calculate_saju(year, month, day, hour, calendar_type, is_leap_month)
    sipshin, ohaeng, basic_traits, music_traits, recommended_instruments = music_analysis(saju)
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
