import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(page_title="음악인 사주 서비스", page_icon="🎸")

st.title("🎸 음악인을 위한 사주통변")

# 2. 사주 정보 입력 섹션
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="고상현")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("출생년", 1900, 2026, 1981)
    with col2:
        month = st.number_input("출생월", 1, 12, 2)
    with col3:
        day = st.number_input("출생일", 1, 31, 7)

    # --- 시간 선택 옵션에 '모름' 추가 ---
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
    # '모름'이 추가되었으므로, 기존 '묘시'를 기본값으로 유지하기 위해 index를 4로 변경합니다.
    birth_time = st.selectbox("출생 시간", time_options, index=4)
    # ------------------------------
    
    # 양력/음력 선택 및 음력일 경우 윤달 체크박스 표시
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달인가요?")

# 3. 분석 버튼 및 결과 출력
if st.button("🎭 심층 이원 통변 리포트 생성"):
    if name:
        # 입력된 날짜를 바탕으로 객체 생성
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_text = f"양력 {year}년 {month}월 {day}일"
        else:
            # 음력 설정 (윤달 여부 포함)
            lunar_obj = Lunar.fromYmd(year, month, day)
            display_text = f"음력 {year}년 {month}월 {day}일" + (" (윤달)" if is_leap_month else " (평달)")

        # 사주 팔자(간지) 가져오기
        eight_char = lunar_obj.getEightChar()
        
        st.divider()
        st.subheader(f"📊 {name}님의 분석 결과")
        
        # 선택한 날짜 형식 표기
        st.write(f"**입력하신 날짜:** {display_text}")
        
        # 간지(사주) 출력
        st.success(f"**사주 팔자:** {eight_char.getYearInGanZi()}년 {eight_char.getMonthInGanZi()}월 {eight_char.getDayInGanZi()}일")
        
        # 시간이 '모름'일 때와 아닐 때의 안내 문구를 다르게 표시할 수 있습니다.
        time_display = f"**출생 시간:** {birth_time}"
        st.write(time_display)
        
        st.markdown(f"""
        ---
        ### 🎹 음악적 메시지
        * 분석하신 **{eight_char.getDayInGanZi()}**의 기운은 예술적 감수성이 풍부한 시기입니다.
        * 이 리포트는 GitHub에 저장된 최신 로직을 바탕으로 생성되었습니다.
        """)
    else:
        st.warning("성함을 입력해 주세요.")
