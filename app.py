import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(page_title="음악인 사주 서비스", page_icon="🎸")

st.title("🎸 음악인을 위한 사주통변")

# 2. 사주 정보 입력 섹션 (기존 코드 보존)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("출생년", 1900, 2026, value=2000)
    with col2:
        month = st.number_input("출생월", 1, 12, value=1)
    with col3:
        day = st.number_input("출생일", 1, 31, value=1)

    time_options = [
        "모름",
        "23:30~01:30 자시 (子)", "01:30~03:30 축시 (丑)", "03:30~05:30 인시 (寅)",
        "05:30~07:30 묘시 (卯)", "07:30~09:30 진시 (辰)", "09:30~11:30 사시 (巳)",
        "11:30~13:30 오시 (午)", "13:30~15:30 미시 (未)", "15:30~17:30 신시 (申)",
        "17:30~19:30 유시 (酉)", "19:30~21:30 술시 (戌)", "21:30~23:30 해시 (亥)"
    ]
    birth_time = st.selectbox("출생 시간", time_options, index=0)
    
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달인가요?")

    target_year = st.number_input("운세를 보고 싶은 연도", min_value=2024, max_value=2100, value=2026)
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

# 3. 분석 버튼 및 결과 출력 (시주 로직 수정)
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
        
        # 간지 한글 매핑 데이터
        gan_ko = {"甲":"갑", "乙":"을", "丙":"병", "丁":"정", "戊":"무", "己":"기", "庚":"경", "辛":"신", "壬":"임", "癸":"계"}
        zi_ko = {"子":"자", "丑":"축", "寅":"인", "卯":"묘", "辰":"진", "巳":"사", "午":"오", "未":"미", "申":"신", "酉":"유", "戌":"술", "亥":"해"}

        def format_ganzi(ganzi_str):
            if not ganzi_str or len(ganzi_str) < 2: return "?", "?"
            gan, zi = ganzi_str[0], ganzi_str[1]
            return f"{gan}({gan_ko.get(gan, '')})", f"{zi}({zi_ko.get(zi, '')})"

        # 년, 월, 일 정보 추출
        y_gan, y_zi = format_ganzi(eight_char.getYear())
        m_gan, m_zi = format_ganzi(eight_char.getMonth())
        d_gan, d_zi = format_ganzi(eight_char.getDay())
        
        # --- 시주(時柱) 정확한 계산 로직 ---
        if birth_time == "모름":
            t_gan, t_zi = "?", "?"
        else:
            # 선택된 텍스트에서 한자 지지(예: 子)만 추출
            selected_zi = birth_time.split("(")[1][0] 
            
            # 일간(日干)을 기준으로 시주 천간을 찾아주는 로직 (시두법)
            # lunar_python의 기능을 활용하기 위해 시간을 강제로 설정한 새로운 객체 생성
            # 자시는 0시, 축시는 2시... 이런 식으로 대표 시간을 설정합니다.
            hour_map = {"子":0, "丑":2, "寅":4, "卯":6, "辰":8, "巳":10, "午":12, "未":14, "申":16, "酉":18, "戌":20, "亥":22}
            target_hour = hour_map.get(selected_zi, 0)
            
            # 시간을 반영한 정확한 사주 객체 재생성
            if calendar_type == "양력":
                precise_solar = Solar.fromYmdHms(year, month, day, target_hour, 0, 0)
                precise_eight_char = precise_solar.getLunar().getEightChar()
            else:
                precise_lunar = Lunar.fromYmdHms(year, month, day, target_hour, 0, 0)
                precise_eight_char = precise_lunar.getEightChar()
            
            t_gan, t_zi = format_ganzi(precise_eight_char.getTime())
        # --------------------------------

        st.divider()
        st.subheader(f"📊 {name}님의 사주 원국 (8글자)")

        col_t, col_d, col_m, col_y = st.columns(4)
        
        with col_y:
            st.markdown("### 년주")
            st.info(f"{y_gan}\n\n{y_zi}")
        with col_m:
            st.markdown("### 월주")
            st.info(f"{m_gan}\n\n{m_zi}")
        with col_d:
            st.markdown("### 일주")
            st.info(f"{d_gan}\n\n{d_zi}")
        with col_t:
            st.markdown("### 시주")
            st.info(f"{t_gan}\n\n{t_zi}")

        st.write(f"**입력 정보:** {display_text} | {gender} | {birth_time}")
        st.write(f"**분석 연도:** {target_year}년")
        
    else:
        st.warning("성함을 입력해 주세요.")
