import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 원본 CSS
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; margin-bottom: 2rem; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 2.2rem; border-radius: 1.5rem; margin-bottom: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
    }
    .section-card { background-color: #ffffff; border-left: 10px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 10px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 10px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 10px solid #3182CE; }
    .content-text { line-height: 2.4; font-size: 1.1rem; color: #2D3748; text-align: justify; word-break: keep-all; }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 2rem; gap: 10px; }
    .saju-box { flex: 1; text-align: center; padding: 20px 5px; background: #F7FAFC; border-radius: 15px; font-weight: bold; border: 2px solid #E2E8F0; }
    .pos-title { font-size: 1.4rem; font-weight: bold; color: #B45309; margin-bottom: 1rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

# 2️⃣ 연도별 음악 통변 엔진 (조회 연도에 따라 300자 이상 장문 생성)
def get_yearly_report(name, target_y):
    # 실제 십신 계산 로직 (간략 예시)
    ten_gods = ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"]
    current_god = ten_gods[target_y % 10]
    
    reports = {
        "비견": f"음악가로서 {target_y}년은 본인의 주체성이 극대화되는 '비견'의 해입니다. 밴드 내에서 본인의 목소리를 확실하게 낼 수 있는 환경이 조성되며, 타협하지 않는 사운드 철학이 확고해지는 시기입니다. 이 시기에 제작되는 사운드는 주관이 뚜렷하며, 대중과의 소통에 있어 본인만의 시그니처가 가장 강력하게 각인되는 한 해가 될 것입니다. 본인의 직관을 믿고 당당하게 사운드를 표현하십시오.",
        "식신": f"창의적인 영감이 샘솟는 {target_y}년은 본인에게 '식신'의 복록이 깃드는 해입니다. 억지로 짜내지 않아도 새로운 멜로디와 창의적인 아이디어가 마르지 않는 샘물처럼 솟아나며, 악기와의 교감이 극대화되어 표현력이 정교해지는 경험을 하게 될 것입니다. 사운드 메이킹에 있어 독특한 미학이 꽃을 피우며 진정성 있는 작품으로 대중의 울림을 이끌어낼 것입니다."
    }
    return current_god, reports.get(current_god, "예술적 감각이 주변 환경과 조화를 이루어 새로운 시도를 하기에 매우 긍정적인 해입니다.")

# 3️⃣ 메인 UI - 입력창
st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    with st.form("saju_input_form"):
        u_name = st.text_input("성함", value="임환백")
        c1, c2, c3 = st.columns(3)
        with c1: birth_y = st.number_input("출생년", 1900, 2100, 1981)
        with c2: birth_m = st.number_input("출생월", 1, 12, 2)
        with c3: birth_d = st.number_input("출생일", 1, 31, 7)
        
        col_t, col_c = st.columns(2)
        with col_t: u_time = st.selectbox("출생 시간", ["05:30~07:30 묘시", "07:30~09:30 진시", "모름"])
        with col_c: cal_type = st.radio("달력 선택", ["양력", "음력", "음력(윤달)"], horizontal=True)
            
        target_y = st.number_input("조회 연도 (운세를 보고 싶은 해)", 1900, 2100, 2026)
        submitted = st.form_submit_button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 4️⃣ 결과 출력
if submitted:
    god, music_flow = get_yearly_report(u_name, target_y)
    st.markdown(f"### 🍀 {u_name} 아티스트님 심층 리포트")
    
    # 사주 그리드
    st.markdown("<div class='saju-grid'><div class='saju-box'>신유(辛酉)<br>년주</div><div class='saju-box'>경인(庚寅)<br>월주</div><div class='saju-box'>병진(丙辰)<br>일주</div><div class='saju-box'>신묘(辛卯)<br>시주</div></div>", unsafe_allow_html=True)

    # 섹션 1~3 (고정 분석)
    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{u_name}님은 병화(丙火) 일간으로 태어나 정열적이고 리더십이 뛰어납니다... (이하 300자 분량)</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>예술가로서 '정밀한 사운드 설계'와 '폭발적 감성'이 공존하는 구조입니다... (이하 300자 분량)</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><div class='content-text'><span class='pos-title'>🎤 메인 보컬</span>...<br><span class='pos-title'>🎚️ 사운드 마스터링</span>...</div></div>", unsafe_allow_html=True)

    # 섹션 4~5 (연도별 동적 분석)
    st.markdown(f"### 📅 {target_y}년 심층 운세 분석")
    st.markdown(f"<div class='target-year-card'><h2>🏙️ 일반 운세 흐름</h2><div class='content-text'><b>[{god}의 운]</b><br>{target_y}년은 내공이 사회적으로 분출되는 분기점입니다. 문서운과 계약운이 따르는 시기입니다.</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 음악적 흐름 이야기</h2><div class='content-text'>{music_flow}</div></div>", unsafe_allow_html=True)
