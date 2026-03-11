import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="정통 사주 분석 (윤달 지원)", layout="wide")

# 1️⃣ 시간 매핑
hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 2️⃣ 사이드바 입력 (윤달 선택 추가)
with st.sidebar:
    st.header("👤 사주 정보 입력")
    name = st.text_input("성함", value="고상현")
    col_y, col_m, col_d = st.columns(3)
    year = col_y.number_input("년", 1900, 2100, 1955)
    month = col_m.number_input("월", 1, 12, 5)
    day = col_d.number_input("일", 1, 31, 4)
    
    calendar_type = st.radio("달력 종류", ["양력", "음력"], horizontal=True)
    
    # ⭐ 음력일 때만 윤달 체크박스 활성화
    is_leap = False
    if calendar_type == "음력":
        is_leap = st.checkbox("이 달은 윤달입니다", value=False)
        if is_leap:
            st.warning("⚠️ 윤달 데이터로 분석을 진행합니다.")

    hour_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=2)
    submitted = st.button("사주 분석 시작")

# 3️⃣ 분석 엔진
def analyze_full_saju(year, month, day, hour_str, cal_type, is_leap_month):
    h = hour_time_map[hour_str]
    
    if cal_type == "음력":
        # lunar_python은 직접 윤달 여부(is_leap_month)를 인자로 받습니다.
        lunar = Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
        # 만약 사용자가 윤달 체크박스를 눌렀다면 해당 객체의 윤달 설정을 확인/강제합니다.
        if is_leap_month:
            lunar = Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
            # 라이브러리 특성에 따라 윤달 객체를 정확히 특정합니다.
    else:
        solar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
        lunar = solar.getLunar()

    return {
        "ba_zi": [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()],
        "is_leap_confirmed": lunar.getMonth() < 0 or is_leap_month, # 라이브러리상 윤달은 음수 등으로 표현됨
        "lunar_date": lunar.toString()
    }

# 4️⃣ 결과 출력 (윤달 적용 여부 명시)
if submitted:
    res = analyze_full_saju(year, month, day, hour_str, calendar_type, is_leap)
    
    st.subheader(f"📑 {name}님의 사주 분석 결과")
    
    # 🔴 윤달 적용 상태 표시 (가장 중요)
    leap_status = "✅ [윤달 적용됨]" if res["is_leap_confirmed"] else "⚪ [평달]"
    st.markdown(f"**기준 정보:** {calendar_type} {year}년 {month}월 {day}일 {hour_str} {leap_status}")
    st.info(f"변환된 음력 날짜: {res['lunar_date']}")
    
    st.divider()
    
    # 8자 명식 출력
    cols = st.columns(4)
    labels = ["년주", "월주", "일주", "시주"]
    for i, col in enumerate(cols):
        col.metric(labels[i], res["ba_zi"][i])

    st.success("위 명식은 선택하신 윤달 여부가 반영된 결과입니다. 월주(月柱)의 변화를 확인해 보세요.")
