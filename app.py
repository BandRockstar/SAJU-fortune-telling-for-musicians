import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인 (기초 레이아웃 완벽 복구)
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

# 2️⃣ 데이터 엔진: 십성별 사주 맞춤형 장문 텍스트 (각 섹션별 300자 이상)
analysis_db = {
    '비겁': {
        'gen': "본인은 주체성과 자존감이 대단히 강한 명식으로, 외부의 압력에 굴하지 않고 자신만의 원칙을 고수하는 강직한 성품을 지니고 있습니다. 타인에게 의지하기보다 스스로 개척하는 독립적인 힘이 삶의 원동력이며, 한번 결정한 일은 끝까지 밀어붙이는 불굴의 추진력을 보여줍니다. 인간관계에서도 신의를 중요시하지만, 본인의 영역을 침범당하는 것을 극도로 경계하는 철저한 자기관리형의 전형입니다.",
        'mus': "음악적으로는 독보적인 솔로 아티스트의 기질이 다분합니다. 남의 스타일을 모방하기보다 본인만의 고유한 음색과 연주 스타일을 정립하여 '나 자체가 장르'가 되는 음악적 완성을 추구합니다. 무대 위에서 뿜어내는 에너지는 청중을 압도하며, 타협하지 않는 예술가적 고집은 시간이 지날수록 매니아층을 견고하게 만드는 핵심적인 자산이 됩니다.",
        'pos_title': "🎤 독보적 아우라의 솔로 싱어송라이터",
        'pos_desc': "본인의 강력한 자아를 소리로 치환하는 '프런트맨' 역할에 최적화되어 있습니다. 밴드 내에서도 음악적 방향성을 결정하는 절대적인 리더십을 발휘하며, 자신만의 독특한 가치관을 가사로 표현하여 대중에게 강력한 메시지를 전달하는 데 천부적인 재능을 보입니다."
    },
    '식상': {
        'gen': "본인은 표현의 천재성을 타고나 매사에 창의적이고 유연한 사고방식을 지닌 명식입니다. 타인과의 소통 능력이 뛰어나고 감정 표현이 풍부하여 주변 사람들에게 즐거움을 주는 에너지를 가지고 있습니다. 끊임없이 새로운 것을 탐구하고 시도하는 호기심이 삶을 풍요롭게 만들며, 본인의 생각과 아이디어를 구체적인 결과물로 만들어내는 실행력이 매우 탁월한 기질을 보여줍니다.",
        'mus': "창작의 마르지 않는 샘물을 가진 명식으로, 멜로디와 가사를 직조하는 감각이 본능적으로 발달해 있습니다. 화려한 테크닉과 무대 매너를 자랑하며, 관객의 반응에 즉각적으로 대응하는 라이브의 귀재입니다. 유행을 선도하는 사운드 디자인에 능하고, 복잡한 이론보다는 영감을 바탕으로 한 감성적 호소력이 짙은 음악을 세상에 내놓으며 대중과 깊이 교감합니다.",
        'pos_title': "🎹 천재적 영감의 퍼포머 & 메인 작곡가",
        'pos_desc': "관객을 사로잡는 화려한 연주자이자 창의적인 작곡가로서 가장 큰 빛을 발합니다. 순발력이 요구되는 즉흥 연주나 대중의 심리를 꿰뚫는 멜로디 메이킹에 강점이 있으며, 자신의 감정을 소리로 투영하여 예술적 카타르시스를 느끼게 해주는 재능을 지니고 있습니다."
    },
    '재성': {
        'gen': "본인은 현실적 감각과 공간 장악력이 탁월하여 매사에 실리적이고 결과 중심적인 사고를 하는 명식입니다. 상황 판단이 빠르고 치밀하여 복잡한 문제도 효율적으로 처리하는 능력이 돋보입니다. 신용을 바탕으로 한 대인관계가 좋으며, 목표를 정하면 이를 성취하기 위한 철저한 계획과 관리를 수행하는 대단히 성실하고 주밀한 성품의 소유자입니다.",
        'mus': "음악을 하나의 거대한 건축물처럼 이해하는 안목이 있습니다. 사운드의 밸런스와 배치, 그리고 대중적 성공 가능성을 냉철하게 분석하여 음악적 완성도를 극대화합니다. 단순히 소리를 내는 것을 넘어 음악의 전체적인 흐름과 결과물의 퀄리티를 컨트롤하는 능력이 뛰어나며, 시장의 흐름과 아티스트의 개성을 조화롭게 융합시키는 전략적인 창작 활동에 능합니다.",
        'pos_title': "🎚️ 사운드 디렉터 & 총괄 프로듀서",
        'pos_desc': "전체 사운드를 조율하고 앨범의 상업적·예술적 가치를 책임지는 프로듀서 역할에 최적입니다. 세션 연주자들의 능력을 적재적소에 배치하고, 믹싱과 마스터링 등 최종 결과물의 완성도를 결정짓는 단계에서 타의 추종을 불허하는 전문성을 발휘하게 됩니다."
    },
    '관성': {
        'gen': "본인은 명예와 규율을 중시하는 강한 책임감과 완벽주의를 지닌 명식입니다. 자신에게 엄격하고 타인에게는 모범이 되는 올바른 성품을 지녔으며, 조직 내에서 신뢰받는 중심축 역할을 수행합니다. 시비지심이 명확하고 매사에 공정함을 유지하려 노력하며, 본인이 맡은 직무에 대해서는 끝까지 책임을 지는 강한 근성과 성실함이 돋보이는 전형적인 리더형입니다.",
        'mus': "음악적 형식미와 정교한 구조를 추구하는 완벽주의를 보여줍니다. 클래식한 음악 문법에 대한 이해가 깊고, 단 한 치의 오차도 허용하지 않는 정밀한 연주와 사운드 디자인을 지향합니다. 소리의 질감을 미세하게 조각하고 다듬는 과정에서 큰 성취감을 느끼며, 대중에게 신뢰감을 주는 하이엔드 퀄리티의 결과물을 생산하여 평단과 업계의 높은 평가를 얻습니다.",
        'pos_title': "🎯 완벽주의 밴드 마스터 & 마스터링 엔지니어",
        'pos_desc': "앙상블의 기강을 잡고 사운드의 규격화된 완성도를 이끄는 리더나 기술적 정점에 서 있는 엔지니어에 적합합니다. 고도의 집중력을 요하는 소리 편집 및 시스템 설계에 강점이 있으며, 본인의 철저한 관리 하에 완성된 음악은 독보적인 품격과 견고함을 지니게 됩니다."
    },
    '인성': {
        'gen': "본인은 깊은 통찰력과 지혜로운 사유를 바탕으로 세상의 이치를 탐구하는 선비와 같은 기질을 지녔습니다. 수용성이 뛰어나 지식을 습득하고 이를 자신만의 철학으로 재해석하는 능력이 탁월합니다. 감수성이 예민하고 내면의 성찰을 중시하여 겉으로 드러나는 화려함보다는 보이지 않는 본질적 가치에 집중하는 깊이 있는 인격의 소유자입니다.",
        'mus': "음악 속에 심오한 철학적 메시지와 예술적 사유를 담아내는 '아티스트의 아티스트'입니다. 화성학적 구성이 치밀하고 가사 한 줄에도 문학적인 깊이가 느껴지는 지적인 음악을 선호합니다. 유행에 휩쓸리지 않는 독자적인 예술 세계를 구축하며, 청중에게 음악을 통한 정서적 치유와 영감을 선사하는 데 탁월한 능력을 발휘합니다.",
        'pos_title': "🎼 심오한 음악 철학자 & 수석 편곡가",
        'pos_desc': "곡의 내러티브를 설계하고 세련된 화성으로 사운드를 풍성하게 만드는 편곡 분야에서 독보적입니다. 보이지 않는 감정을 선율로 치환하는 지혜로운 능력을 갖추고 있으며, 음악적 이론을 바탕으로 기존의 틀을 깨고 새로운 예술적 해석을 제시하는 역할을 수행하게 됩니다."
    }
}

# 3️⃣ 입력 및 처리 로직
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

# 4️⃣ 핵심 계산 함수
def get_sibsung_logic(d_gan, max_elem):
    gan_to_ohaeng = {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}
    my_ohaeng = gan_to_ohaeng.get(d_gan, '목')
    order = ['목', '화', '토', '금', '수']
    idx_diff = (order.index(max_elem) - order.index(my_ohaeng)) % 5
    return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[idx_diff]

def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {'申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'], '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']}
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

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
        counts = {k: sum(1 for c in "".join(ba_zi[:4]) if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        # 사주 원리(십성)에 따른 데이터 추출
        sib_key = get_sibsung_logic(d_gan, max_elem)
        data = analysis_db[sib_key]
        display_name = user_name if user_name else "아티스트"
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

        # UI 출력
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b></div>", unsafe_allow_html=True)

        # 각 메뉴(섹션) 완벽 복구 및 사주 데이터 바인딩
        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{data['gen']}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{data['mus']}</div></div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>{data['pos_title']}</span>
                {data['pos_desc']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ {target_y}년 운세 및 음악적 흐름</h2>
            <div class='content-text'>
                {target_y}년은 {display_name}님의 {d_gan} 일간과 세운의 기운이 만나 새로운 음악적 성취를 이루는 시기입니다. 
                올해는 특히 사주 내의 **{sib_key}**의 기운이 극대화되면서, 본인의 '{data['pos_title']}'로서의 역량이 
                사회적으로 큰 인정을 받게 될 것입니다. 창작 활동에 있어 우주의 기운이 본인의 뒤를 든든하게 받쳐주고 있으니, 
                망설임 없이 본인의 예술적 철학을 세상에 투영하시길 바랍니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
