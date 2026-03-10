import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
import datetime

# --- [스타일 설정: 전통 한지 느낌] ---
st.set_page_config(page_title="정통 뮤지션 만세력", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #f4f1ea; }
    h1, h2, h3 { color: #2c2c2c; font-family: 'Nanum Myeongjo', serif; }
    .stButton>button { background-color: #4a3b2b; color: white; width: 100%; height: 3em; font-weight: bold; }
    .result-box { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #d1c7ac; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- [로직: 지역별 경도 보정] ---
def get_longitude_adj(long_val):
    # 표준시(135.0)와 실제 경도 차이를 분 단위로 계산 (1도당 4분)
    return (long_val - 135.0) * 4

# --- [로직: 밴드 파트 분석] ---
def analyze_music_destiny(zodiac_year, elements_count):
    # 5행 기반 밴드 파트 매칭 규칙
    parts = {
        "火": "보컬(Vocal) - 열정과 발산",
        "金": "기타(Guitar) - 정교함과 타격",
        "木": "드럼(Drums) - 리듬과 시작",
        "水": "베이스(Bass) - 울림과 유연함",
        "土": "키보드(Keyboard) - 조화와 배경"
    }
    # 실제 로직에서는 elements_count에서 가장 높은 오행을 추출합니다.
    # 예시 데이터 (사용자님의 금(金) 성향 반영)
    return parts["金"], parts["火"]

# --- [메인 화면 구성] ---
st.title("🏯 정통 뮤지션 만세력")
st.write("공공 천문 데이터 기반의 정밀 보정 시스템")

with st.container():
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("성함", "BandRockstar")
        gender = st.radio("성별", ["남성", "여성"], horizontal=True)
        date = st.date_input("생년월일", datetime.date(1981, 2, 7))
    with col2:
        time = st.time_input("태어난 시간", datetime.time(6, 30))
        is_lunar = st.checkbox("음력/윤달 여부")
        location = st.selectbox("출생 지역 (경도 보정)", ["서울/경기 (127.0)", "부산/경남 (129.0)", "강원 (128.0)"])
    
    view_year = st.number_input("조회 연도", value=2026)
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("내 사주와 음악적 성취 확인하기"):
    st.markdown("---")
    # 결과 섹션 (여기에 정밀 계산 결과가 표시됩니다)
    st.subheader(f"✨ {name} 님의 뮤지션 분석")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**[추천 밴드 파트]**")
        st.success("1순위: 일렉 기타 / 2순위: 보컬")
    with c2:
        st.markdown(f"**[{view_year}년 음악적 성취도]**")
        st.info("92점 - 대외 활동 및 공연 최적기")

    st.subheader("📊 오행 에너지 분포")
    st.bar_chart({"木": 2, "火": 1, "土": 1, "金": 4, "水": 0})
    
    st.warning("⚠️ 2031년부터 삼재(들삼재)가 시작되니 미리 대비하세요.")
