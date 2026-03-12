
import streamlit as st
from datetime import datetime
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", page_icon="🎸")

# 디자인 스타일 적용
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🎸 음악인을 위한 사주통변 Ver 1.0</h2>", unsafe_allow_html=True)

# 2. 입력 섹션
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="고상현")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("출생년", min_value=1900, max_value=2026, value=1981)
    with col2:
        month = st.number_input("출생월", min_value=1, max_value=12, value=2)
    with col3:
        day = st.number_input("출생일", min_value=1, max_value=31, value=7)
        
    # 시간 선택 (사주 분석을 위해 인덱스 활용)
    times = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
    birth_time = st.selectbox("출생 시간", [f"{i*2+1:02d}~{(i*2+3)%24:02d} {t}시" for i, t in enumerate(times)], index=3)
    
    calendar_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    target_year = st.number_input("운세를 보고 싶은 연도", min_value=2024, max_value=2100, value=2026)

# 3. 사주 계산 함수 (lunar_python 활용)
def get_saju_string(y, m, d, is_lunar):
    if not is_lunar:
        solar = Solar.fromYmd(y, m, d)
        lunar = solar.getLunar()
    else:
        lunar = Lunar.fromYmd(y, m, d)
    
    # 팔자(Eight Characters) 가져오기
    eight_char = lunar.getEightChar()
    return f"{eight_char.getYearInGanZi()}년 {eight_char.getMonthInGanZi()}월 {eight_char.getDayInGanZi()}일"

# 4. 결과 출력
if st.button("🎭 심층 이원 통변 리포트 생성"):
    if name:
        is_lunar_bool = (calendar_type == "음력")
        try:
            ganji_result = get_saju_string(year, month, day, is_lunar_bool)
            
            st.divider()
            st.subheader(f"📊 {name}님의 분석 결과")
            st.info(f"**기본 사주:** {ganji_result} {birth_time}")
            
            st.markdown(f"""
            ### 🎹 음악적 통변
            * **운세 테마:** {target_year}년은 새로운 리듬과 화성이 조화를 이루는 시기입니다.
            * **조언:** 현재 사용하시는 장비나 음악적 스타일에서 '변화'를 줄 때 운이 상승합니다.
            """)
        except Exception as e:
            st.error(f"날짜 계산 중 오류가 발생했습니다: {e}")
    else:
        st.warning("성함을 입력해 주세요.")
