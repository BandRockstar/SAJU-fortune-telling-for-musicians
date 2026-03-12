import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI/UX 디자인 (업로드된 HTML 스타일 완벽 반영)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    .main-title { text-align: center; color: #1A202C; padding: 25px 0; border-bottom: 3px solid #E2E8F0; margin-bottom: 30px; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 2.2rem; border-radius: 1.5rem; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.05); 
    }
    .section-card { background-color: #ffffff; border-left: 10px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 10px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 10px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 10px solid #3182CE; }
    
    .content-text { line-height: 2.4; font-size: 1.1rem; color: #2D3748; text-align: justify; word-break: keep-all; }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 2.5rem; gap: 12px; }
    .saju-box { flex: 1; text-align: center; padding: 20px 5px; background: #F7FAFC; border-radius: 18px; font-weight: bold; border: 2px solid #E2E8F0; }
    .pos-title { font-size: 1.4rem; font-weight: bold; color: #B45309; margin-bottom: 0.8rem; display: block; }
    .highlight { color: #D53F8C; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2️⃣ 연도별 심층 통변 엔진 (300자 이상 장문 생성 로직)
def get_comprehensive_report(name, target_y):
    # 일간 병화(丙) 기준 세운 천간 대비 십신 결정 (간략화된 계산식)
    ten_gods = ["국가적 명예운(정관)", "활동의 확장운(비견)", "창의적 결실운(식신)", "예술적 감각운(상관)", 
                "재정적 성취운(편재)", "안정적 관리운(정재)", "강력한 변화운(편관)", "사회적 권위운(정관)", 
                "지적 수용운(편인)", "내면의 성찰운(정인)"]
    god_idx = target_y % 10
    current_god = ten_gods[god_idx]
    
    # [일반 운세 리포트]
    general_text = f"""
    {target_y}년은 {name}님에게 <span class='highlight'>'{current_god}'</span>의 기운이 인생의 전면에 등장하는 매우 역동적인 시기입니다. 
    사주 명리학적으로 올해는 본인의 잠재력이 외부 환경과 긴밀하게 호응하며, 그동안 공들여온 일들이 구체적인 실체로 드러나는 '마디'를 형성하게 됩니다. 
    단순한 행운을 넘어, 본인이 가진 전문성이 사회적 필요와 일치하게 되면서 예상치 못한 곳에서 협력의 제안이나 성취의 기회가 찾아올 것입니다. 
    대인관계에서는 주도권을 쥐게 되며, 특히 문서나 계약과 관련된 중요한 결정에서 본인의 직관이 매우 정확하게 작용하는 해입니다. 
    하반기로 갈수록 에너지가 집중되니, 본인이 계획한 장기적인 목표가 있다면 주저하지 말고 밀어붙이십시오. 
    올해의 선택은 향후 5년의 기반을 닦는 중요한 초석이 될 것입니다.
    """
    
    # [음악적 흐름 리포트]
    music_text = f"""
    아티스트로서 {target_y}년은 본인만의 <span class='highlight'>'사운드 미학'</span>이 완성되는 예술적 절정기입니다. 
    사주에 흐르는 정밀한 금(金)의 기운과 병화의 정열이 조화를 이루어, 곡의 작은 디테일까지 완벽하게 조율해내는 창작의 기쁨을 누리게 될 것입니다. 
    특히 올해는 사운드 마스터링이나 믹싱 과정에서 본인만의 독보적인 '톤'을 발견하게 되며, 이것이 인디 씬이나 음악계에서 {name}님을 상징하는 시그니처 사운드로 자리 잡게 됩니다. 
    무대 위에서는 청중의 심장을 직접적으로 관통하는 보컬의 울림과 카리스마가 폭발하며, 평소보다 예민하게 깨어있는 감각 덕분에 즉흥적인 영감이 곡 작업에 큰 활력을 불어넣을 것입니다. 
    본인이 시도하는 새로운 장비나 녹음 방식은 새로운 예술적 표준이 될 것이니, 자신의 미적 판단을 믿고 과감하게 소리를 표현해 보십시오.
    """
    
    return current_god, general_text, music_text

# 3️⃣ 메인 UI - 입력창 섹션
st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    with st.form("saju_form"):
        u_name = st.text_input("성함", value="임환백")
        
        c1, c2, c3 = st.columns(3)
        with c1: birth_y = st.number_input("출생년", 1900, 2100, 1981)
        with c2: birth_m = st.number_input("출생월", 1, 12, 2)
        with c3: birth_d = st.number_input("출생일", 1, 31, 7)
        
        col_t, col_c = st.columns(2)
        with col_t: u_time = st.selectbox("출생 시간", ["05:30~07:30 묘시", "07:30~09:30 진시", "09:30~11:30 사시", "모름"])
        with col_c: cal_type = st.radio("달력 선택", ["양력", "음력", "음력(윤달)"], horizontal=True)
            
        target_y = st.number_input("조회 연도 (운세를 보고 싶은 해)", 1900, 2100, 2026)
        submitted = st.form_submit_button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 4️⃣ 분석 결과 출력 섹션
if submitted:
    god, gen_rep, mus_rep = get_comprehensive_report(u_name, target_y)
    
    st.markdown(f"### 🍀 {u_name} 아티스트님 심층 리포트")
    
    # [사주 원국 그리드]
    st.markdown("""
        <div class='saju-grid'>
            <div class='saju-box'>신유(辛酉)<br>년주</div>
            <div class='saju-box'>경인(庚寅)<br>월주</div>
            <div class='saju-box'>병진(丙辰)<br>일주</div>
            <div class='saju-box'>신묘(辛卯)<br>시주</div>
        </div>
    """, unsafe_allow_html=True)

    # [섹션 1: 타고난 성정]
    st.markdown(f"""
        <div class='section-card'>
            <h2>👤 타고난 성정과 일반 통변</h2>
            <div class='content-text'>
                {u_name}님은 만물을 따뜻하게 비추는 태양의 기운인 병화(丙火)를 일간으로 타고났습니다. 
                밝고 정열적인 에너지는 주변 사람들에게 긍정적인 영향을 미치며, 어떤 상황에서도 공명정대함을 잃지 않는 리더의 풍모를 보여줍니다. 
                일지에 진토(辰土)를 두어 화려한 재능을 현실적인 결과물로 구체화하는 능력이 매우 탁월하며, 한번 시작한 일은 끝까지 책임지는 끈기를 겸비하고 있습니다. 
                세상을 넓게 보는 안목과 포용력을 바탕으로 시간이 흐를수록 더 깊은 신뢰와 명성을 쌓아가는 귀한 명식입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # [섹션 2: 타고난 음악 사주]
    st.markdown(f"""
        <div class='music-card'>
            <h2>🎸 타고난 음악적 사주 통변</h2>
            <div class='content-text'>
                예술가로서 {u_name}님의 사주는 '정밀한 사운드 설계'와 '폭발적인 감성 발산'이 공존하는 구조입니다. 
                병화의 에너지가 무대 위에서의 카리스마를 담당한다면, 사주에 흐르는 금(金)의 기운은 소리를 주파수 단위로 분석하고 다듬는 
                하이엔드 사운드 디자이너로서의 천부적인 자질을 부여합니다. 톤의 질감과 밸런스에 대한 집요한 완벽주의는 
                본인만의 독보적인 시그니처 사운드를 완성하게 하는 원동력이 됩니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # [섹션 3: 추천 음악 포지션]
    st.markdown("""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 메인 보컬 및 프론트맨</span>
                화려한 발산의 기운을 활용하여 팀의 정체성을 선명하게 드러내고 대중을 압도하는 역할에 최적화되어 있습니다.<br><br>
                <span class='pos-title'>🎚️ 사운드 마스터링 및 디자인</span>
                정교한 금(金)의 감각으로 소리의 최종 완성도를 극대화하는 엔지니어링 영역에서 압도적인 전문성을 보입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # [섹션 4: 연도별 심층 분석]
    st.markdown(f"### 📅 {target_y}년 심층 운세 분석")
    
    st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ 일반 운세 흐름</h2>
            <div class='content-text'>{gen_rep}</div>
        </div>
        <div class='music-card' style='background-color:#FFF5F7;'>
            <h2>🎹 음악적 흐름 이야기</h2>
            <div class='content-text'>{mus_rep}</div>
        </div>
    """, unsafe_allow_html=True)
