import streamlit as st
from lunar_python import Solar, Lunar

# 1. 앱의 제목과 아이콘 설정
st.set_page_config(page_title="음악인 사주 서비스", page_icon="🎸")

st.title("🎸 음악인을 위한 사주통변")

# 2. 사용자 입력 섹션 (사진 속 디자인 반영)
with st.container():
    st.subheader("📝 사주 정보 입력")
    
    name = st.text_input("성함", value="고상현")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("출생년", 1900, 2026, 1981)
    with col2:
        month = st.number_input("출생월", 1, 12, 2)
    with col3:
        day = st.number_input("출생일", 1, 31, 7)

    # 묘시(05~07시)를 기본값으로 설정
    birth_time = st.selectbox("출생 시간", ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"], index=3)
    
    is_lunar = st.radio("달력 선택", ["양력", "음력"], horizontal=True)

# 3. 분석 버튼
if st.button("🎭 심층 이원 통변 리포트 생성"):
    st.write(f"### {name}님의 분석을 시작합니다...")
    # 여기에 사주 계산 로직이 들어갈 예정입니다.
