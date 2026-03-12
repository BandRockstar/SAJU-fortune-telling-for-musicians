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

# 2️⃣ 연도별 심층 통변 엔진 (일반/음악 사주 300자 이상 구성)
def get_yearly_comprehensive_report(name, target_y):
    # 십신 계산 (간략 로직)
    ten_gods = ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"]
    current_god = ten_gods[target_y % 10]
    
    # [일반 사주 데이터베이스]
    general_db = {
        "비견": f"{target_y}년은 {name}님에게 주체성과 독립심이 극대화되는 '비견'의 기운이 강하게 작용하는 해입니다. 주변의 간섭에서 벗어나 본인이 계획한 일을 소신 있게 추진할 수 있는 에너지가 충만한 시기입니다. 대인관계에서는 동료들과 대등한 위치에서 협력하거나 때로는 선의의 경쟁을 통해 본인의 가치를 증명하게 될 것입니다. 자신의 능력을 믿고 당당하게 나아간다면 사회적 위치가 한층 단단해지는 결과를 얻을 수 있으며, 특히 장기적인 목표를 위해 기초를 다지기에 매우 유리한 흐름입니다.",
        "식신": f"{target_y}년은 {name}님에게 창의적 활동과 표현의 즐거움이 가득한 '식신'의 해입니다. 그동안 구상만 하던 아이디어를 구체화하여 세상에 내놓기에 가장 적합한 시기이며, 의식주가 풍족해지고 심리적인 여유를 찾게 되는 흐름입니다. 주변 사람들에게 본인의 재능을 인정받으며 자연스럽게 활동 범위가 넓어지게 되고, 성실하게 노력한 대가가 실질적인 보상으로 돌아오는 기분 좋은 해가 될 것입니다. 건강과 즐거움을 동시에 챙기며 에너지를 발산해 보세요."
    }
    
    # [음악적 사주 데이터베이스]
    music_db = {
        "비견": f"음악가로서 {target_y}년은 본인만의 독보적인 사운드 미학을 정립하는 '시그니처 완성'의 해입니다. 밴드 내에서 리더십을 발휘하여 본인이 추구하는 음악적 방향성을 관철시키기에 최적의 타이밍이며, 외부의 유행에 휩쓸리지 않고 가장 임환백님다운 음악을 창작하게 될 것입니다. 톤 메이킹이나 편곡 과정에서 본인의 고집이 긍정적으로 작용하여, 향후 수년간 본인의 예술적 자산이 될 기념비적인 작업물을 남길 수 있는 강력한 운세입니다.",
        "식신": f"음악적 감수성이 정교해지는 {target_y}년은 '예술적 풍요'가 깃드는 해입니다. 억지로 짜내지 않아도 일상의 감각들이 멜로디와 리듬으로 치환되는 신비로운 경험을 자주 하게 될 것이며, 사운드 디자인 과정에서 본인만의 독특한 질감을 발견하여 음악적 외연을 크게 확장하게 됩니다. 대중에게는 편안하면서도 깊은 울림을 주는 진정성 있는 작품으로 다가가게 되며, 창작 행위 자체가 큰 즐거움으로 다가와 작업의 완성도가 비약적으로 상승하는 황금기입니다."
    }

    g_report = general_db.get(current_god, f"{target_y}년은 새로운 기운이 들어와 인생의 지평을 넓히는 해입니다. (중략 - 300자 분량 로직)")
    m_report = music_db.get(current_god, f"음악적으로 {target_y}년은 새로운 감각이 깨어나는 시기입니다. (중략 - 300자 분량 로직)")
    
    return current_god, g_report, m_report

# 3️⃣ 메인 UI
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

# 4️⃣ 결과 출력
if submitted:
    god, g_report, m_report = get_yearly_comprehensive_report(u_name, target_y)
    
    # 사주 그리드
    st.markdown("<div class='saju-grid'><div class='saju-box'>신유(辛酉)<br>년주</div><div class='saju-box'>경인(庚寅)<br>월주</div><div class='saju-box'>병진(丙辰)<br>일주</div><div class='saju-box'>신묘(辛卯)<br>시주</div></div>", unsafe_allow_html=True)

    # 섹션 1~3: 타고난 사주 분석 (300자 이상 고정 텍스트)
    st.markdown(f"""
        <div class='section-card'>
            <h2>👤 타고난 성정과 일반 통변</h2>
            <div class='content-text'>
                {u_name}님은 만물을 따뜻하게 비추는 태양의 기운인 병화(丙火)를 일간으로 타고났습니다. 
                병화 특유의 밝고 정열적인 에너지는 주변 사람들에게 긍정적인 영향을 미치며, 어떤 상황에서도 공명정대함을 잃지 않는 리더의 풍모를 보여줍니다. 
                일지에 진토(辰토)를 두어 화려한 재능을 현실적인 결과물로 구체화하는 능력이 매우 탁월하며, 
                한번 시작한 일은 끝까지 책임지고 완수하는 끈기를 겸비하고 있습니다. 
                세상을 넓게 보는 안목과 포용력을 바탕으로 시간이 흐를수록 더 깊은 신뢰와 명성을 쌓아가는 귀한 명식입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class='music-card'>
            <h2>🎸 타고난 음악적 사주 통변</h2>
            <div class='content-text'>
                음악가로서 {u_name}님의 사주는 '정밀한 사운드 설계'와 '폭발적인 감성 발산'이 공존하는 구조입니다. 
                병화의 에너지가 무대 위에서의 카리스마와 보컬의 울림을 담당한다면, 사주에 흐르는 금(金)의 기운은 소리 하나하나를 주파수 단위로 분석하고 다듬는 
                하이엔드 사운드 디자이너로서의 천부적인 자질을 부여합니다. 
                특히 톤의 질감과 밸런스에 대한 집요한 완벽주의는 인디 씬과 전문 음악계에서 본인만의 독보적인 시그니처 사운드를 완성하게 하는 원동력이 됩니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 섹션 4~5: 연도별 동적 분석 (300자 이상 실시간 변화)
    st.markdown(f"### 📅 {target_y}년 심층 운세 분석")
    
    st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ 일반 운세 흐름</h2>
            <div class='content-text'>
                <b>[{god}의 운]</b><br>{g_report}
            </div>
        </div>
        <div class='music-card' style='background-color:#FFF5F7;'>
            <h2>🎹 음악적 흐름 이야기</h2>
            <div class='content-text'>{m_report}</div>
        </div>
    """, unsafe_allow_html=True)
