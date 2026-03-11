import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

st.title("🎸 음악인을 위한 사주통변")

# 시간 맵
hour_time_map = {
    "모름": None,
    "23~01 자시": 0,
    "01~03 축시": 2,
    "03~05 인시": 4,
    "05~07 묘시": 6,
    "07~09 진시": 8,
    "09~11 사시": 10,
    "11~13 오시": 12,
    "13~15 미시": 14,
    "15~17 신시": 16,
    "17~19 유시": 18,
    "19~21 술시": 20,
    "21~23 해시": 22
}

# 입력
with st.expander("사주 정보 입력", expanded=True):

    name = st.text_input("이름")

    col1, col2, col3 = st.columns(3)

    with col1:
        year = st.number_input("출생년", 1900, 2100, 1980)

    with col2:
        month = st.number_input("출생월", 1, 12, 1)

    with col3:
        day = st.number_input("출생일", 1, 31, 1)

    hour_str = st.selectbox("출생시간", list(hour_time_map.keys()))

    col4, col5 = st.columns(2)

    with col4:
        cal_type = st.radio("달력", ["양력", "음력"])

    with col5:
        is_leap = st.checkbox("윤달") if cal_type == "음력" else False

    target_year = st.number_input("운세 연도", 1900, 2100, 2026)

    run = st.button("사주 분석")

# --------------------------
# 오행 계산
# --------------------------

ohaeng_map = {
    '목': '甲乙寅卯',
    '화': '丙丁巳午',
    '토': '戊己辰戌丑未',
    '금': '庚辛申酉',
    '수': '壬癸亥子'
}

def calc_ohaeng(chars):

    counts = {}

    for k, v in ohaeng_map.items():

        counts[k] = sum(c in v for c in chars)

    return counts

# --------------------------
# 삼재 계산
# --------------------------

def get_samjae(year_zhi, target_year):

    samjae = {
        '申子辰': ['寅','卯','辰'],
        '亥卯未': ['巳','午','未'],
        '寅午戌': ['申','酉','戌'],
        '巳酉丑': ['亥','子','丑']
    }

    group = []

    for k,v in samjae.items():

        if year_zhi in k:

            group = v

    tz = Solar.fromYmd(target_year,1,1).getLunar().getYearZhi()

    if tz in group:

        idx = group.index(tz)

        return ["들삼재","눌삼재","날삼재"][idx]

    return "삼재 아님"

# --------------------------
# 실행
# --------------------------

if run:

    hour = hour_time_map[hour_str]

    try:

        if cal_type == "양력":

            if hour is None:

                solar = Solar.fromYmd(year,month,day)

            else:

                solar = Solar.fromYmdHms(year,month,day,hour,0,0)

            lunar = solar.getLunar()

        else:

            lunar = Lunar.fromYmdHms(year,month,day, hour if hour else 12,0,0)

        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()

        if hour is None:

            time_gz = "?"

        else:

            time_gz = lunar.getTimeInGanZhi()

        st.subheader("사주 팔자")

        st.write("년주:",year_gz)
        st.write("월주:",month_gz)
        st.write("일주:",day_gz)
        st.write("시주:",time_gz)

        # 오행

        chars = year_gz + month_gz + day_gz + (time_gz if time_gz!="?" else "")

        counts = calc_ohaeng(chars)

        st.subheader("오행 분석")

        st.write(counts)

        max_elem = max(counts,key=counts.get)

        st.success(f"가장 강한 오행 : {max_elem}")

        # 삼재

        samjae = get_samjae(year_gz[-1], target_year)

        st.subheader("삼재")

        st.write(f"{target_year}년 : {samjae}")

    except Exception as e:

        st.error("사주 계산 오류")

        st.write(e)
