import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 모바일 최적화 UI 디자인 (기존 유지)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    html { font-size: 14px; }
    @media (min-width: 600px) { html { font-size: 16px; } }

    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
    }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 8px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    
    .samjae-active { background-color: #FEF2F2; border: 2px solid #EF4444; color: #991B1B; padding: 1.5rem; border-radius: 1.2rem; margin-bottom: 1.5rem; }
    .samjae-inactive { background-color: #F0FDF4; border: 2px solid #22C55E; color: #166534; padding: 1.5rem; border-radius: 1.2rem; margin-bottom: 1.5rem; }

    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 1.5rem; gap: 8px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 20px; border-radius: 15px; margin-bottom: 1.5rem; }
    
    h1 { font-size: 1.8rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 1.2rem; font-weight: 700; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.3rem; font-weight: bold; color: #B45309; margin-bottom: 0.8rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

# 2️⃣ 데이터 엔진: 십성별 300자 이상 전문 통변 DB
analysis_db = {
    '비겁': {
        'pos': "독보적인 아우라의 솔로 아티스트 (Soloist)",
        'text': "귀하의 명식은 비견과 겁재의 기운이 강하여 주체성이 뚜렷하고 자기 세계가 대단히 견고합니다. 음악적으로는 타인의 간섭을 받기보다 본인만의 독창적인 색깔을 관철할 때 가장 큰 빛을 발하며, 무대 위에서 뿜어내는 에너지가 청중을 압도하는 힘이 있습니다. 자존심과 독립심이 강해 밴드 내에서도 본인의 음악적 고집을 끝까지 밀어붙이는 프런트맨의 기질을 타고났습니다. 이러한 성향은 대중에게 '대체 불가능한 독창성'으로 비춰지며, 본인만이 소화할 수 있는 독특한 음색이나 연주 스타일을 구축하게 됩니다. 타협하지 않는 예술가적 자존심은 시간이 흐를수록 매니아층을 형성하는 강력한 자산이 될 것이며, 자신을 믿고 나아갈 때 가장 거대한 성취를 이루는 운명입니다."
    },
    '식상': {
        'pos': "천재적 영감의 퍼포머 & 작곡가 (Creator)",
        'text': "식신과 상관의 기운이 수려하게 발달하여 표현의 한계가 없는 명식입니다. 악기를 다루는 테크닉이 화려하고, 일상의 사소한 감정도 즉각적인 멜로디로 치환하는 천부적인 재능을 지니고 있습니다. 무대 위에서의 끼와 순발력이 뛰어나 관객의 반응에 따라 유연하게 호흡하는 라이브의 귀재입니다. 창의적인 아이디어가 샘솟듯 쏟아지며, 복잡한 이론보다는 본능적인 감각으로 사운드를 직조하는 능력이 돋보입니다. 가사 한 구절에도 재치와 감수성을 담아내는 능력이 탁월하여, 시대의 트렌드를 앞서가는 사운드 메이커로서 대중의 큰 사랑을 받게 될 것입니다. 본인의 창조적 에너지를 아낌없이 쏟아낼수록 명성은 더욱 높아지는 구조입니다."
    },
    '재성': {
        'pos': "사운드 디렉터 & 총괄 프로듀서 (Director)",
        'text': "재성의 기운은 공간을 장악하는 능력과 결과물을 완성하는 치밀함을 상징합니다. 단순히 연주하는 것에 그치지 않고 사운드의 전체적인 밸런스와 대중적 성공 가능성을 냉철하게 판단하는 안목이 탁월합니다. 앨범의 기획부터 마케팅적 가치까지 고려하는 '음악적 전략가'로서, 무엇이 대중의 귀를 사로잡을지 본능적으로 파악합니다. 수치와 결과에 밝아 효율적인 작업 공정을 설계하며, 세션 연주자들의 능력을 적재적소에 배치하여 최상의 결과물을 도출해내는 지휘관의 역량을 보여줍니다. 현실적인 감각과 예술적 가치를 조화롭게 융합시키는 능력은 본인을 음악 산업 내에서 가장 신뢰받는 프로듀서의 위치로 이끌 것입니다."
    },
    '관성': {
        'pos': "완벽주의 리더 & 마스터 엔지니어 (Master)",
        'text': "정관과 편관의 기운은 엄격한 질서와 완벽한 형식을 의미합니다. 오케스트라의 지휘자나 밴드의 리더처럼 팀의 기강을 잡고 조화를 이끌어내는 역할에 최적화되어 있습니다. 본인의 음악은 단 한 치의 오차도 허용하지 않는 정교한 구조미를 자랑하며, 특히 믹싱이나 마스터링처럼 극도의 집중력과 규율을 요하는 작업에서 타의 추종을 불허합니다. 소리의 질감을 미세하게 깎고 다듬어 표준 이상의 퀄리티를 유지하는 '마스터'의 자질을 갖추고 있습니다. 명예를 중시하는 성정 덕분에 자신의 이름이 걸린 작업물에 대해 무한한 책임감을 느끼며, 이러한 철저함이 본인을 해당 분야의 독보적인 권위자로 만들 것입니다."
    },
    '인성': {
        'pos': "심오한 음악 철학자 & 편곡가 (Philosopher)",
        'text': "인성의 기운은 깊은 사유와 정신적인 수양을 뜻합니다. 가사 하나에도 인문학적인 메시지를 담고, 화성학적으로 깊이 있고 복잡한 구성을 선호하는 경향이 있습니다. 학습 능력이 뛰어나 전통적인 음악 문법을 마스터한 뒤 이를 자신만의 철학으로 재해석하는 데 능합니다. 유행을 따르는 소모적인 음악보다는 시간이 흘러도 변하지 않는 예술적 가치를 추구하며, '아티스트의 아티스트'로 불릴 만큼 깊이 있는 통찰력을 선사합니다. 음악을 통해 세상에 메시지를 던지는 계몽적인 성향을 띠기도 하며, 본인이 정립한 음악 이론이나 스타일은 후배 뮤지션들에게 커다란 영감의 원천이자 지침서가 될 것입니다."
    }
}

# 3️⃣ 입력 설정
hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="", placeholder="성함을 입력하세요")
    y = st.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    m = st.number_input("출생월", 1, 12, value=None, placeholder="MM")
    d = st.number_input("출생일", 1, 31, value=None, placeholder="DD")
    h_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    
    col1, col2 = st.columns(2)
    with col1: cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    with col2: is_leap = st.checkbox("윤달 여부") if cal_type == "음력" else False
    
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 4️⃣ 핵심 로직 함수들
def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {'申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'], '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']}
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

def get_sibsung_key(d_gan, max_elem):
    gan_to_ohaeng = {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}
    my_ohaeng = gan_to_ohaeng.get(d_gan, '목')
    order = ['목', '화', '토', '금', '수']
    idx_diff = (order.index(max_elem) - order.index(my_ohaeng)) % 5
    return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[idx_diff]

# 5️⃣ 결과 출력
if submitted:
    if not (y and m and d) or h_str == "시간 선택 (또는 모름)":
        st.error("생년월일과 시간을 정확히 입력해주세요.")
    else:
        h_val = hour_time_map[h_str]
        calc_h = 12 if h_val == "unknown" else h_val
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), (int(m) * -1) if is_leap else int(m), int(d), calc_h, 0, 0)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
        d_gan = lunar.getDayGan()
        
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        count_target = "".join(ba_zi[:3]) if h_val == "unknown" else "".join(ba_zi)
        counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        # 십성 도출 및 데이터 매칭
        sib_key = get_sibsung_key(d_gan, max_elem)
        report = analysis_db[sib_key]
        display_name = user_name if user_name else "아티스트"
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

        # 리포트 출력 시작
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b></div>", unsafe_allow_html=True)

        # 1. 포지션 섹션 (사주 원리 연동됨)
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션: {report['pos']}</h2>
            <div class='content-text'>
                {report['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. 운세 섹션 (가변 텍스트 예시)
        st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ {target_y}년 운세 흐름</h2>
            <div class='content-text'>
                올해는 {display_name}님의 일간 {d_gan}이 세운의 기운과 조우하여 새로운 변화의 물결을 타는 시기입니다. 
                특히 {sib_key}의 기운이 강화되는 해로, 본인의 주된 음악적 재능인 '{report['pos']}'로서의 역량이 
                사회적으로 강력하게 투사될 기회를 맞이하게 됩니다. 문서운과 명예운이 동시에 상승하는 시기이므로 
                중요한 계약이나 앨범 발표에 최적의 타이밍이 될 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
