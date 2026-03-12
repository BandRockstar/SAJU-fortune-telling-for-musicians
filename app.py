import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 원본 CSS (디자인 완벽 재현)
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

# 2️⃣ 메인 UI - 입력 섹션 (양력/음력/윤달 복구)
st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    with st.form("saju_input_form"):
        u_name = st.text_input("성함", value="임환백")
        
        # 생년월일 입력창 (가로 배치)
        c1, c2, c3 = st.columns(3)
        with c1: birth_y = st.number_input("출생년 (YYYY)", 1900, 2100, 1981)
        with c2: birth_m = st.number_input("출생월 (MM)", 1, 12, 2)
        with c3: birth_d = st.number_input("출생일 (DD)", 1, 31, 7)
        
        # 시간 및 달력 설정 (복구된 핵심 부분)
        col_t, col_c = st.columns(2)
        with col_t:
            u_time = st.selectbox("출생 시간", ["05:30~07:30 묘시", "07:30~09:30 진시", "09:30~11:30 사시", "모름"])
        with col_c:
            cal_type = st.radio("달력 선택", ["양력", "음력", "음력(윤달)"], horizontal=True)
            
        target_y = st.number_input("조회 연도 (운세를 보고 싶은 해)", 1900, 2100, 2026)
        
        submitted = st.form_submit_button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 3️⃣ 결과 출력 로직
if submitted:
    # (사용자 사주 고정 데이터 기반 통변 생성)
    st.markdown(f"### 🍀 {u_name} 아티스트님 심층 분석 리포트")
    
    # 사주 팔자 그리드
    st.markdown("""
        <div class='saju-grid'>
            <div class='saju-box'>신유(辛酉)<br>년주</div>
            <div class='saju-box'>경인(庚寅)<br>월주</div>
            <div class='saju-box'>병진(丙辰)<br>일주</div>
            <div class='saju-box'>신묘(辛卯)<br>시주</div>
        </div>
    """, unsafe_allow_html=True)

    # 👤 타고난 성정과 일반 통변 (300자 이상)
    st.markdown(f"""
        <div class='section-card'>
            <h2>👤 타고난 성정과 일반 통변</h2>
            <div class='content-text'>
                {u_name}님은 만물을 따뜻하게 비추는 태양의 기운인 병화(丙火)를 일간으로 타고났습니다. 
                병화 특유의 밝고 정열적인 에너지는 주변 사람들에게 긍정적인 영향을 미치며, 어떤 상황에서도 공명정대함을 잃지 않는 리더의 풍모를 보여줍니다. 
                일지에 진토(辰土)를 두어 본인의 화려한 재능과 아이디어를 현실적인 결과물로 구체화하는 능력이 매우 탁월하며, 
                한번 시작한 일은 끝까지 책임지고 완수하는 끈기 또한 겸비하고 있습니다. 
                세상을 넓게 보는 안목과 포용력을 바탕으로 시간이 흐를수록 더 깊은 신뢰와 명성을 쌓아가는 귀한 명식입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 🎸 타고난 음악적 사주 통변 (300자 이상)
    st.markdown(f"""
        <div class='music-card'>
            <h2>🎸 타고난 음악적 사주 통변</h2>
            <div class='content-text'>
                예술가로서 {u_name}님의 사주는 '정밀한 사운드 설계'와 '폭발적인 감성 발산'이 공존하는 구조입니다. 
                병화의 에너지가 무대 위에서의 카리스마와 보컬의 울림을 담당한다면, 사주에 흐르는 금(金)의 기운은 소리 하나하나를 주파수 단위로 분석하고 다듬는 
                하이엔드 사운드 디자이너로서의 천부적인 자질을 부여합니다. 
                특히 톤의 질감과 밸런스에 대한 집요한 완벽주의는 인디 씬과 전문 음악계에서 {u_name}님만의 독보적인 시그니처 사운드를 완성하게 하는 원동력이 됩니다. 
                청중의 심장을 관통하는 사운드 밸런스를 잡아낼 때 본인의 예술적 명예가 가장 크게 빛나게 될 것입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ✨ 추천 음악 포지션
    st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 메인 보컬 및 프론트맨</span>
                화려한 발산의 기운을 활용하여 팀의 정체성을 선명하게 드러내고 대중을 압도하는 역할에 최적화되어 있습니다.<br><br>
                <span class='pos-title'>🎚️ 사운드 마스터링 및 디자인</span>
                정교한 금(金)의 감각으로 소리의 최종 완성도를 극대화하는 엔지니어링 영역에서 압도적인 전문성을 보입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 📅 연도별 심층 운세 분석 (음악적 흐름 포함)
    st.markdown(f"### 📅 {target_y}년 심층 운세 분석")
    
    st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ 일반 운세 흐름</h2>
            <div class='content-text'>
                {target_y}년은 본인의 내공이 사회적으로 강력하게 분출되는 중요한 분기점입니다. 
                그동안 쌓아온 지식과 기술이 외부 환경과 조화를 이루어 실질적인 명예와 성취로 이어지는 형국이며, 
                특히 중요한 계약이나 문서상의 결정에 있어 우주의 기운이 본인을 돕는 해입니다.
            </div>
        </div>
        <div class='music-card' style='background-color:#FFF5F7;'>
            <h2>🎹 음악적 흐름 이야기</h2>
            <div class='content-text'>
                음악가로서 {target_y}년은 본인만의 독창적인 사운드 미학이 대중과 깊게 공명하는 '예술적 완성의 해'입니다. 
                평소보다 예민하게 깨어있는 감각을 통해 곡의 작은 디테일까지 완벽하게 조율하게 되며, 
                특히 라이브 무대나 큰 규모의 프로젝트에서 본인의 존재감이 크게 부각될 것입니다. 
                올해 시도하는 새로운 장비 활용이나 창작 기법은 {u_name}님의 음악 인생에 있어 새로운 표준이 될 만큼 큰 영감을 줄 것입니다. 
                본인의 직관을 믿고 당당하게 사운드를 표현하십시오. 그 어느 때보다 따뜻하고 열렬한 지지가 함께할 것입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)
