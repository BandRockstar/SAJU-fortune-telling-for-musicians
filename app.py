import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(page_title="음악인 사주 서비스", page_icon="🎸")

st.title("🎸 음악인을 위한 사주통변")

# 2. 사주 정보 입력 섹션
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    # 성함을 빈칸으로 설정
    name = st.text_input("성함", value="")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        # 연도를 현재 연도 기준으로 하거나 최소값으로 설정 (0은 불가능하므로 빈칸 느낌의 기본값 적용)
        year = st.number_input("출생년", 1900, 2026, value=2000)
    with col2:
        month = st.number_input("출생월", 1, 12, value=1)
    with col3:
        day = st.number_input("출생일", 1, 31, value=1)

    time_options = [
        "모름",
        "23:30~01:30 자시 (子)",
        "01:30~03:30 축시 (丑)",
        "03:30~05:30 인시 (寅)",
        "05:30~07:30 묘시 (卯)",
        "07:30~09:30 진시 (辰)",
        "09:30~11:30 사시 (巳)",
        "11:30~13:30 오시 (午)",
        "13:30~15:30 미시 (未)",
        "15:30~17:30 신시 (申)",
        "17:30~19:30 유시 (酉)",
        "19:30~21:30 술시 (戌)",
        "21:30~23:30 해시 (亥)"
    ]
    # '모름'을 기본 선택으로 설정 (index=0)
    birth_time = st.selectbox("출생 시간", time_options, index=0)
    
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달인가요?")

    # 분석 연도는 현재 시점에 맞춰 2026으로 유지하거나 원하는 값으로 변경 가능
    target_year = st.number_input("운세를 보고 싶은 연도", min_value=2024, max_value=2100, value=2026)

    # 성별 선택도 기본 선택 없이 사용자가 누르게 유도 (라디오 버튼은 기본값이 항상 하나 있으므로 남성을 기본으로 유지)
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

# 3. 분석 버튼 및 결과 출력
if st.button("🎭 심층 이원 통변 리포트 생성"):
    if name:
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_text = f"양력 {year}년 {month}월 {day}일"
        else:
            lunar_obj = Lunar.fromYmd(year, month, day)
            display_text = f"음력 {year}년 {month}월 {day}일" + (" (윤달)" if is_leap_month else " (평달)")

        eight_char = lunar_obj.getEightChar()
        
        st.divider()
        st.subheader(f"📊 {name}님의 분석 결과")
        
        st.write(f"**입력하신 날짜:** {display_text}")
        st.write(f"**성별:** {gender}")
        st.write(f"**분석 대상 연도:** {target_year}년")
        
        st.success(f"**사주 팔자:** {eight_char.getYearInGanZi()}년 {eight_char.getMonthInGanZi()}월 {eight_char.getDayInGanZi()}일")
        
        st.write(f"**출생 시간:** {birth_time}")
        
        st.markdown(f"""
        ---
        ### 🎹 음악적 메시지
        * **{gender}** 아티스트로서 {name}님은 {target_year}년에 새로운 음악적 영감을 마주하게 될 것입니다.
        * 분석하신 **{eight_char.getDayInGanZi()}**의 기운을 바탕으로 맞춤형 리포트가 생성되었습니다.
        """)
    else:
        st.warning("성함을 입력해 주세요.")
