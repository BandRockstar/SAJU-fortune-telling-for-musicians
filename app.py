import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI (사용자님 원본과 100% 동일)
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

# 2️⃣ 동적 텍스트 생성 엔진 (연도별 십성에 따른 텍스트 분리)
def get_dynamic_fortune(target_y, t_gz, t_gan, t_sib):
    # 각 십성별로 확연히 다른 통변을 제공하여 '같은 말' 반복 문제를 해결합니다.
    fortune_map = {
        '비겁': {
            'gen': f"{target_y}년({t_gz})은 주체성과 독립심이 강해지는 시기입니다. 본인의 의지가 확고해지며 주변의 간섭에서 벗어나 독자적인 길을 개척하는 흐름을 보입니다.",
            'mus': f"음악적으로는 리드 기타의 존재감이 뚜렷해지며, 본인이 주도하는 프로젝트나 밴드 내 주도권을 확보하기에 유리한 해입니다."
        },
        '식상': {
            'gen': f"{target_y}년({t_gz})은 표현력과 창의성이 폭발하는 시기입니다. 새로운 아이디어가 샘솟고 이를 대중에게 선보이고자 하는 욕구가 강해집니다.",
            'mus': f"작곡과 연주에서 실험적인 시도가 빛을 발합니다. 특히 이펙터 활용이나 독특한 톤 메이킹을 통해 본인의 끼를 마음껏 발산하는 해입니다."
        },
        '재성': {
            'gen': f"{target_y}년({t_gz})은 노력이 결과물로 이어지는 결실의 해입니다. 현실적인 감각이 예리해져 상황 판단과 추진력이 동시에 상승합니다.",
            'mus': f"앨범 제작이나 공연 계약 등 실질적인 성과가 뒤따릅니다. 사운드의 밸런스가 잡히고 대중의 소구력을 정확히 짚어내는 시기입니다."
        },
        '관성': {
            'gen': f"{target_y}년({t_gz})은 명예와 책임감이 중시되는 시기입니다. 절제된 행동과 성실함으로 주변의 신뢰와 공식적인 인정을 받게 됩니다.",
            'mus': f"음악 감독으로서 앙상블을 조율하는 능력이 탁월해집니다. 정교한 편곡과 안정적인 보컬 톤으로 팀의 전문성을 입증하는 해입니다."
        },
        '인성': {
            'gen': f"{target_y}년({t_gz})은 내실을 다지고 지혜를 얻는 수양의 시기입니다. 깊은 사유와 공부를 통해 정신적인 성장을 이루며 귀인의 도움을 얻습니다.",
            'mus': f"음악에 깊은 서사와 철학이 담깁니다. 어쿠스틱 기타나 피아노를 활용한 섬세한 작업이 어울리며, 영혼을 울리는 진정성 있는 곡이 탄생합니다."
        }
    }
    
    res = fortune_map.get(t_sib, fortune_map['비겁'])
    common_tail = f" 특히 {target_y}년의 {t_gan} 기운은 귀하의 본래 기질과 공명하여 향후 음악 커리어에 중요한 변곡점이 될 것입니다. {t_gz}의 흐름을 믿고 소신대로 나아가시길 바랍니다."
    
    return res['gen'] + common_tail, res['mus'] + common_tail

# 3️⃣ 사용자 입력부 (원본 그대로 유지)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="임환백")
    calendar_type = st.radio("날짜 구분", ["양력", "음력", "음력(윤달)"], horizontal=True)
    col1, col2, col3 = st.columns(3)
    y, m, d = col1.number_input("년", 1900, 2100, 1981), col2.number_input("월", 1, 12, 2), col3.number_input("일", 1, 31, 7)
    h_str = st.selectbox("출생 시간", ["05~07 묘시", "23~01 자시", "01~03 축시", "03~05 인시", "07~09 진시", "09~11 사시", "11~13 오시", "13~15 미시", "15~17 신시", "17~19 유시", "19~21 술시", "21~23 해시"], index=0)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    # 사주 계산 로직 (원본 유지)
    if calendar_type == "양력": lunar = Solar.fromYmd(int(y), int(m), int(d)).getLunar()
    else: lunar = Lunar.fromYmd(int(y), int(m), int(d), (calendar_type == "음력(윤달)"))
    
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    d_gan = lunar.getDayGan()

    # 세운 계산 (연도 변경 시 실시간 반영)
    target_lunar = Solar.fromYmd(int(target_y), 1, 1).getLunar()
    t_gan, t_gz = target_lunar.getYearGan(), target_lunar.getYearInGanZhi()
    
    def get_sib_name(my, target_g):
        order = ['목', '화', '토', '금', '수']
        gan_map = {'甲':'목','乙':'목','丙':'화','丁':'화','戊':'토','己':'토','庚':'금','辛':'금','壬':'수','癸':'수'}
        m_oh, t_oh = gan_map.get(my), gan_map.get(target_g)
        return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[(order.index(t_oh) - order.index(m_oh)) % 5]

    t_sib = get_sib_name(d_gan, t_gan)
    gen_fortune, mus_fortune = get_dynamic_fortune(target_y, t_gz, t_gan, t_sib)

    # 리포트 출력 (사용자님 지정 레이아웃 100% 보존)
    st.markdown(f"### 🍀 {user_name}님의 {target_y}년 분석 결과")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_y}년({t_gz}) 일반 사주 흐름</h2><div class='content-text'>{gen_fortune}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 {target_y}년({t_gz}) 음악적 사주 흐름</h2><div class='content-text'>{mus_fortune}</div></div>", unsafe_allow_html=True)
