import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 원본 스타일 CSS
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 25px 0; border-bottom: 3px solid #E2E8F0; margin-bottom: 30px; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 2.2rem; border-radius: 1.5rem; margin-bottom: 2rem; box-shadow: 0 6px 20px rgba(0,0,0,0.07); 
    }
    .section-card { background-color: #ffffff; border-left: 10px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 10px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 10px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 10px solid #3182CE; }
    .content-text { line-height: 2.3; font-size: 1.1rem; color: #2D3748; text-align: justify; word-break: keep-all; }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 2rem; gap: 10px; }
    .saju-box { flex: 1; text-align: center; padding: 20px 5px; background: #F7FAFC; border-radius: 15px; font-weight: bold; border: 2px solid #E2E8F0; }
    .pos-title { font-size: 1.4rem; font-weight: bold; color: #B45309; margin-bottom: 1rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

# 2️⃣ 연도별 음악적 분석 엔진
def get_music_analysis(target_y, name):
    # 십신 계산 로직 (간략화된 예시 데이터)
    analysis_db = {
        "비견": f"{target_y}년은 {name}님에게 주체성이 극대화되는 '비견'의 해입니다. 밴드 활동에서 본인의 음악적 시그니처를 가장 강력하게 투영할 수 있는 시기이며, 외부의 압력에 굴하지 않고 본인이 추구하는 사운드 미학을 완성하는 데 집중하게 됩니다. (중략 - 300자 이상의 상세 텍스트 로직 적용)",
        "식신": f"예술적 영감이 샘솟는 {target_y}년은 {name}님에게 창의적 에너지가 솟구치는 '식신'의 해입니다. 멜로디와 리듬이 일상의 감각들과 공명하며 자연스럽게 흘러나오며, 특히 사운드 디자인에 있어 본인만의 독보적인 질감을 발견하게 될 것입니다. (중략 - 300자 이상의 상세 텍스트 로직 적용)"
    }
    # 연도별로 다른 결과 반환
    god = "비견" if target_y % 2 == 0 else "식신"
    return god, analysis_db.get(god)

# 3️⃣ 메인 인터페이스 (입력 섹션)
st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

with st.expander("📝 사주 정보 및 조회 연도 입력", expanded=True):
    with st.form("input_form"):
        u_name = st.text_input("성함", value="임환백")
        c1, c2, c3 = st.columns(3)
        with c1: b_y = st.number_input("출생년", 1900, 2100, 1981)
        with c2: b_m = st.number_input("출생월", 1, 12, 2)
        with c3: b_d = st.number_input("출생일", 1, 31, 7)
        u_time = st.selectbox("출생 시간", ["05:30~07:30 묘시", "07:30~09:30 진시", "모름"])
        target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
        submitted = st.form_submit_button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 4️⃣ 결과 출력 섹션
if submitted:
    ten_god, music_flow = get_music_analysis(target_y, u_name)

    # 사주 그리드 레이아웃
    st.markdown("""<div class='saju-grid'>
        <div class='saju-box'>신유(辛酉)<br>년주</div><div class='saju-box'>경인(庚寅)<br>월주</div>
        <div class='saju-box'>병진(丙辰)<br>일주</div><div class='saju-box'>신묘(辛卯)<br>시주</div>
    </div>""", unsafe_allow_html=True)

    # [1] 👤 타고난 성정과 일반 통변
    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{u_name}님은 병화(丙火) 일간으로 태어나... (300자 이상)</div></div>", unsafe_allow_html=True)

    # [2] 🎸 타고난 음악적 사주 통변
    st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>음악가로서 {u_name}님은 정교한 사운드와... (300자 이상)</div></div>", unsafe_allow_html=True)

    # [3] ✨ 추천 음악 포지션
    st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><div class='content-text'><span class='pos-title'>🎤 메인 보컬 및 프론트맨</span>...</div></div>", unsafe_allow_html=True)

    # [4 & 5] 연도별 심층 분석 (질문하신 레이아웃 확인 부분)
    st.markdown(f"### 📅 {target_y}년 심층 운세 분석")
    
    st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ 일반 운세 흐름</h2>
            <div class='content-text'><b>[{ten_god}의 운]</b><br>{target_y}년은 본인의 기운이 외부 환경과 조화롭게... (300자 이상)</div>
        </div>
        <div class='music-card' style='background-color:#FFF5F7;'>
            <h2>🎹 음악적 흐름 이야기</h2>
            <div class='content-text'>{music_flow}</div>
        </div>
    """, unsafe_allow_html=True)
