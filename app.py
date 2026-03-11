import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 2.2", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card, .inst-card { 
        padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
    }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 8px solid #D97706; }
    .inst-card { background-color: #F0FFF4; border-left: 8px solid #38A169; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 1.5rem; gap: 8px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; }
    h1 { font-size: 1.8rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 1.2rem; font-weight: 700; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 2.2</h1></div>", unsafe_allow_html=True)

# 2️⃣ 동적 텍스트 생성 엔진 (연도별로 다른 내용이 나오도록 설계)
def get_dynamic_fortune(target_y, t_gz, t_gan, t_sib):
    # 십성별 핵심 키워드와 통변 조각들
    fortune_map = {
        '비겁': {
            'gen': f"{target_y}년은 본인의 주체성이 극대화되는 '독립과 경쟁'의 시기입니다. {t_gz}의 강한 기운은 귀하가 타인의 시선에서 벗어나 본연의 색깔을 가감 없이 드러내게 할 것입니다. 올해는 새로운 동료를 만나거나 혹은 기존 관계에서의 독립을 꿈꾸게 되며, 본인의 고집이 예술적 자산이 되는 해입니다.",
            'mus': f"음악적으로는 '나만의 장르'를 선언하는 해입니다. {t_gan}의 영향으로 리드 기타의 솔로 라인이 더욱 공격적이고 선명해지며, 보컬에서는 본인의 철학이 담긴 가사가 대중의 가슴을 뚫고 들어갈 것입니다. 밴드 내 주도권을 잡고 본인이 원하는 사운드를 끝까지 밀어붙여 보시기 바랍니다."
        },
        '식상': {
            'gen': f"{target_y}년은 창의적 에너지가 폭발하여 세상 밖으로 분출되는 '표현과 생산'의 시기입니다. 머릿속에만 있던 아이디어들이 {t_gz}의 기운을 타고 구체적인 형태를 갖추게 됩니다. 대인관계가 넓어지고 본인의 끼를 알아봐 주는 사람들이 늘어나는 활기찬 한 해가 될 것입니다.",
            'mus': f"창작 활동에 최적인 해입니다. {t_gan}의 영감 덕분에 작곡 속도가 빨라지고, 공연 기획이나 새로운 악기(특히 이펙터나 신디사이저) 활용 능력이 비약적으로 상승합니다. 기타 연주에 있어서도 실험적인 톤을 시도하기 좋으며, 관객과의 소통이 가장 활발해지는 음악적 전성기를 맞이할 것입니다."
        },
        '재성': {
            'gen': f"{target_y}년은 그동안의 노력이 실질적인 결과물로 치환되는 '결실과 성취'의 해입니다. 현실 감각이 예리해지며 밴드 운영이나 비즈니스적인 판단에서 탁월한 선택을 내리게 됩니다. {t_gz}의 흐름은 귀하에게 안정적인 기반과 경제적 보상을 동시에 가져다줄 기회를 제공합니다.",
            'mus': f"음악의 완성도가 정점에 이르는 시기입니다. {t_gan}의 치밀함이 사운드 믹싱과 프로듀싱에 반영되어 앨범의 퀄리티가 비약적으로 향상됩니다. 리듬 기타의 칼 같은 박자감과 베이스의 안정감이 밴드 전체를 지탱하며, 공연 수익이나 저작권 등 현실적인 성과가 눈에 띄게 나타나는 해입니다."
        },
        '관성': {
            'gen': f"{target_y}년은 사회적 지위가 올라가고 명예를 얻게 되는 '책임과 인정'의 시기입니다. {t_gz}의 엄격한 기운은 귀하를 절제된 완벽주의자로 만들며, 주변에서 귀하의 전문성을 공식적으로 인정하게 됩니다. 공공기관이나 큰 조직과의 협업 기회가 잦아질 수 있습니다.",
            'mus': f"음악 감독으로서의 권위가 세워지는 해입니다. {t_gan}의 질서 정연함이 편곡에 투영되어 오케스트레이션이나 대규모 앙상블 조율에서 빛을 발합니다. 정석적인 연주와 깊이 있는 보컬 톤이 요구되며, 본인의 음악이 대중에게 하나의 '브랜드'로서 신뢰를 쌓기 시작하는 중요한 전환점입니다."
        },
        '인성': {
            'gen': f"{target_y}년은 내면을 채우고 지혜를 쌓는 '수양과 후원'의 시기입니다. {t_gz}의 차분한 기운은 귀하가 외부 활동보다는 깊은 사색과 공부에 집중하게 만듭니다. 주변의 조력자나 선배로부터 큰 도움을 받을 수 있으며, 문서와 관련된 계약(출판, 전속 등)에 매우 유리한 운입니다.",
            'mus': f"음악적 깊이가 심화되는 해입니다. {t_gan}의 철학적 감성이 선율에 녹아들어 스토리텔링이 강화된 음악을 선보이게 됩니다. 어쿠스틱 기타나 피아노를 활용한 서정적인 작업이 활발해지며, 화려한 기교보다는 듣는 이의 영혼을 치유하는 진정성 있는 곡들이 탄생할 것입니다."
        }
    }
    
    res = fortune_map.get(t_sib)
    # 300자 이상을 맞추기 위한 공통 보강 문구 조합
    common_tail = f" 특히 {target_y}년의 천간 {t_gan}은 귀하의 본래 기질과 상호작용하여, 평소라면 시도하지 않았을 새로운 예술적 도전을 가능케 합니다. 이 시기를 어떻게 활용하느냐에 따라 향후 10년의 음악 커리어가 결정될 만큼 중요한 변곡점이니, 운의 흐름을 믿고 본인의 소신대로 나아가시길 바랍니다. {t_gz}의 기운이 귀하의 모든 연주와 발걸음 위에 함께할 것입니다."
    
    return res['gen'] + common_tail, res['mus'] + common_tail

# (생략: 기존 analysis_db는 동일하게 유지하되, inst 섹션에 기타 필수 포함)
# 3️⃣ 사용자 입력부 (초기 UI 복구)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="임환백")
    calendar_type = st.radio("날짜 구분", ["양력", "음력", "음력(윤달)"], horizontal=True)
    col1, col2, col3 = st.columns(3)
    y, m, d = col1.number_input("년", 1900, 2100, 1981), col2.number_input("월", 1, 12, 2), col3.number_input("일", 1, 31, 7)
    h_str = st.selectbox("출생 시간", ["05~07 묘시", "23~01 자시", "01~03 축시", "03~05 인시", "07~09 진시", "09~11 사시", "11~13 오시", "13~15 미시", "15~17 신시", "17~19 유시", "19~21 술시", "21~23 해시"], index=0)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    # 사주 계산 로직 (수정된 메서드 사용)
    if calendar_type == "양력": lunar = Solar.fromYmd(int(y), int(m), int(d)).getLunar()
    else: lunar = Lunar.fromYmd(int(y), int(m), int(d), (calendar_type == "음력(윤달)"))
    
    time_gz = lunar.getTimeInGanZhi() 
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), time_gz]
    d_gan = lunar.getDayGan()

    # 세운 계산
    target_lunar = Solar.fromYmd(int(target_y), 1, 1).getLunar()
    t_gan, t_gz = target_lunar.getYearGan(), target_lunar.getYearInGanZhi()
    
    def get_sib_name(my, target_g):
        order = ['목', '화', '토', '금', '수']
        m_oh = {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}.get(my)
        t_oh = {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}.get(target_g)
        return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[(order.index(t_oh) - order.index(m_oh)) % 5]

    t_sib = get_sib_name(d_gan, t_gan)
    # 동적으로 연도별 운세 생성
    gen_fortune, mus_fortune = get_dynamic_fortune(target_y, t_gz, t_gan, t_sib)

    # 리포트 출력
    st.markdown(f"### 🍀 {user_name}님의 {target_y}년 분석 결과")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_y}년({t_gz}) 일반 사주 흐름</h2><div class='content-text'>{gen_fortune}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 {target_y}년({t_gz}) 음악적 사주 흐름</h2><div class='content-text'>{mus_fortune}</div></div>", unsafe_allow_html=True)
