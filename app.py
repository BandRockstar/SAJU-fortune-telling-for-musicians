import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.1", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    html { font-size: 14px; }
    @media (min-width: 600px) { html { font-size: 16px; } }
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
    .pos-title { font-size: 1.3rem; font-weight: bold; color: #B45309; margin-bottom: 0.8rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.1</h1></div>", unsafe_allow_html=True)

# 2️⃣ 데이터 엔진: 5대 악기군 한정 및 300자 통변
analysis_db = {
    '비겁': {
        'gen': "귀하는 주체성과 독립심이 대단히 강한 명식으로, 외부의 압력이나 타인의 시선에 굴하지 않고 자신만의 뚜렷한 가치관을 관철하는 강직한 성품을 지니고 있습니다. 비견과 겁재의 강한 에너지는 삶의 고비마다 스스로를 일으켜 세우는 불굴의 의지가 되며, 어떤 환경에서도 본인의 색깔을 잃지 않는 독보적인 존재감을 드러내게 합니다. 타인에게 의지하기보다 자신의 실력을 믿고 나아가는 자수성가형의 전형이며, 인간관계에서는 한 번 맺은 인연에 대해 깊은 신의를 지키지만 자신의 영역을 침범당하는 것에는 타협이 없는 철저한 면모를 보입니다.",
        'mus': "음악적으로는 그 누구와도 비교할 수 없는 독창적인 사운드를 구축하는 솔로 아티스트의 기질이 매우 농후합니다. 남들의 유행을 쫓기보다는 본인이 느끼는 감정과 철학을 소리로 투영하는 데 집중하며, '나 자신이 곧 장르'가 되는 예술적 경지를 지향합니다. 보컬의 음색이나 연주의 톤에 있어서 본인만의 시그니처가 확실하여 청중에게 강렬한 인상을 남기며, 밴드 활동 시에도 전체적인 음악적 방향성을 주도하는 절대적인 존재감을 발휘합니다.",
        'pos_title': "🎤 독보적 아우라의 프런트맨",
        'pos_desc': "귀하의 명식에서 가장 빛나는 포지션은 본인의 강력한 자아를 무대 위에서 가감 없이 표출하는 리드 보컬입니다. 타인의 간섭 없이 곡의 기획부터 최종 연주까지 본인의 의도대로 끌고 나갈 때 최고의 시너지가 발생합니다.",
        'instrument': """
            귀하에게 가장 어울리는 파트는 **보컬**과 **기타**입니다. 비겁의 강한 주체성은 무대 중앙에서 군중을 압도하는 에너지를 필요로 합니다. 보컬로서는 가창의 기교보다는 목소리 자체의 힘(Tone)과 진정성으로 청중의 심장을 관통하는 스타일이 적합하며, 직선적이고 파워풀한 벨팅 창법이 기질과 잘 맞습니다. 기타를 잡는다면 섬세한 백킹보다는 화려하고 공격적인 리드 기타가 운명적입니다. 본인만의 독보적인 톤을 구축하여 전체 사운드의 중심을 뚫고 나오는 선명한 존재감을 드러낼 때, 비로소 예술적 갈증이 해소될 것입니다. 밴드 내에서도 다른 악기에 묻히기보다 사운드의 주인공으로서 기능할 때 가장 큰 음악적 성취를 거둘 수 있습니다.
        """
    },
    '식상': {
        'gen': "본인은 천재적인 영감과 표현의 수려함을 타고난 명식으로, 일상의 모든 경험을 예술적 가치로 치환하는 비범한 재능을 지니고 있습니다. 식신과 상관의 발달은 언어적, 비언어적 표현력을 극대화하여 타인과의 교감 능력을 높여주며, 매사에 유연하고 창의적인 사고방식을 통해 주변을 밝히는 에너지를 전파합니다.",
        'mus': "창작의 마르지 않는 샘물을 가진 아티스트로서, 멜로디와 가사를 직조하는 감각이 본능적으로 발달해 있습니다. 화려한 연주 테크닉은 물론, 청중의 심리를 파고드는 감성적인 톤 메이킹에 천부적인 소질을 보입니다. 정형화된 틀에 얽매이지 않고 즉흥적인 영감을 소리로 표현하는 데 능합니다.",
        'pos_title': "🎹 천재적 영감의 퍼포머",
        'pos_desc': "관객을 사로잡는 화려한 연주자이자 창의적인 작곡가로서 가장 큰 빛을 발합니다. 순발력이 요구되는 즉흥 연주나 대중의 심리를 꿰뚫는 멜로디 메이킹에 강점이 있습니다.",
        'instrument': """
            다채로운 감수성을 표출해야 하는 귀하에게는 **키보드(신디사이저)**와 **기타**가 최적의 도구입니다. 식상의 창의성은 무한한 소리의 변화를 추구하므로, 수만 가지 음색을 디자인할 수 있는 키보드를 통해 본인의 상상력을 현실화할 때 최고의 희열을 느낍니다. 기타를 연주할 때도 정석적인 플레이보다는 각종 이펙터를 적극 활용하여 세상에 없던 사운드 텍스처를 만들어내는 능력이 탁월합니다. 보컬을 겸한다면 화려한 애드리브와 넓은 음역대를 활용하는 스타일이 어울립니다. 귀하의 연주는 단순히 음을 나열하는 것이 아니라, 매 순간 변화하는 감정의 물결을 소리로 치환하는 과정이기에 관객들에게 강렬한 퍼포먼스적 쾌감을 선사하게 될 것입니다.
        """
    },
    '재성': {
        'gen': "본인은 현실을 꿰뚫어 보는 안목과 공간을 장악하는 능력이 남다른 명식으로, 매사에 실리적이고 결과 중심적인 사고를 통해 목표를 성취하는 대단히 유능한 성품의 소유자입니다. 재성의 기운은 환경을 본인에게 유리하게 조율하는 힘을 상징하며, 복잡한 상황 속에서도 본질을 빠르게 파악하여 가장 효율적인 해결책을 찾아냅니다.",
        'mus': "음악을 하나의 거대한 건축물처럼 이해하고 설계하는 프로듀싱 능력이 탁월합니다. 단순히 악기를 연주하는 단계를 넘어 사운드의 전체적인 밸런스와 대중적 성공 가능성을 냉철하게 판단하는 안목을 지녔습니다.",
        'pos_title': "🥁 사운드의 설계자 & 리더",
        'pos_desc': "전체 사운드를 조율하고 앨범의 상업적·예술적 가치를 책임지는 프로듀서 역할에 최적입니다. 세션 연주자들의 능력을 적재적소에 배치하는 탁월한 관리 능력을 보여줍니다.",
        'instrument': """
            음악의 뼈대를 형성하고 전체 흐름을 제어하는 귀하에게는 **드럼**과 **베이스**가 운명적인 악기입니다. 재성의 현실 장악력은 무대 뒤편에서 전체 앙상블의 박자와 리듬을 완벽하게 통제할 때 가장 빛납니다. 드럼은 곡의 구조를 결정짓는 설계도와 같으며, 베이스는 화성과 리듬을 연결하는 가교 역할을 하기에 본인의 관리자적 기질과 공명합니다. 화려한 솔로보다는 팀 전체의 사운드가 비지 않도록 채워주는 견고한 플레이에서 깊은 만족감을 느낍니다. 보컬을 한다면 감정의 과잉 없이 정확한 음정과 박자로 곡의 중심을 잡아주는 스타일이 적합합니다. 귀하가 구축하는 탄탄한 리듬 섹션은 동료 뮤지션들이 마음 놓고 연주할 수 있는 가장 든든한 기반이 될 것입니다.
        """
    },
    '관성': {
        'gen': "본인은 명예와 규율을 목숨처럼 중요하게 여기는 강직한 성품과 완벽주의를 소유한 명식입니다. 자신에게 엄격한 기준을 적용하는 만큼 타인에게도 정직과 신뢰를 요구하며, 조직이나 사회 내에서 올바른 질서를 확립하고 유지하는 데 중추적인 역할을 수행합니다.",
        'mus': "음악적 형식미와 정교한 구조를 추구하는 완벽주의자의 면모를 보여줍니다. 단 한 치의 오차도 허용하지 않는 정밀한 연주와 사운드 디자인을 지향하며, 불필요한 장식을 걷어낸 본질적인 가치를 추구합니다.",
        'pos_title': "🎯 완벽주의 밴드 마스터",
        'pos_desc': "앙상블의 기강을 잡고 사운드의 규격화된 완성도를 이끄는 리더에 적합합니다. 고도의 집중력을 요하는 소리 편집 및 시스템 설계에 강점이 있습니다.",
        'instrument': """
            정밀함과 규율을 중시하는 귀하에게는 **키보드**와 **베이스**가 가장 적합합니다. 키보드는 화성학적 기초가 탄탄해야 하며 정교한 터치가 요구되는 악기이기에 귀하의 완벽주의적 기질을 투영하기 좋습니다. 또한 베이스 연주 시에도 단 한 박의 오차도 허용하지 않는 메트로놈 같은 정확성을 보여주어 밴드의 음악적 품격을 높입니다. 보컬 스타일은 정석적인 발성과 정갈한 창법을 선호하며, 가사의 전달력을 극대화하는 클래식한 창법에서 강점을 보입니다. 귀하의 소리는 청중에게 깊은 신뢰감을 주며, 불필요한 장식 없이 본질에 집중하는 정교하게 세공된 사운드의 정수를 보여줄 것입니다. 정해진 약속(Score)을 완벽하게 이행하는 모습에서 아티스트로서의 독보적 권위가 세워질 것입니다.
        """
    },
    '인성': {
        'gen': "본인은 깊은 통찰력과 지혜로운 사유를 바탕으로 현상의 본질을 탐구하는 선비와 같은 기질을 지닌 명식입니다. 지식의 습득 능력이 대단히 뛰어나고 이를 본인만의 철학으로 재해석하여 세상에 내놓는 정신적인 창조 능력이 탁월합니다.",
        'mus': "음악 속에 심오한 철학적 메시지와 신비로운 무의식의 영역을 담아내는 능력이 탁월합니다. 단순히 청각적 즐거움을 넘어 하나의 완벽한 세계관을 창조하는 과정을 즐기며, 보이지 않는 정서를 유려한 선율로 치환합니다.",
        'pos_title': "🎼 수석 편곡가 & 작사가",
        'pos_desc': "곡의 내러티브를 설계하고 세련된 화성으로 사운드를 풍성하게 만드는 분야에서 독보적입니다. 보이지 않는 감정을 선율로 치환하는 지혜로운 능력을 갖추고 있습니다.",
        'instrument': """
            깊은 사유와 영적인 울림을 추구하는 귀하에게는 **기타(어쿠스틱/할로우바디)**와 **키보드(피아노 계열)**가 가장 잘 어울립니다. 화성적으로 풍부한 울림을 가진 악기를 통해 본인의 내면세계를 확장하며, 여운이 길게 남는 선율을 직조할 때 예술적 영감이 극대화됩니다. 보컬 스타일은 가사의 이면을 읽어내어 관객에게 이야기를 들려주는 스토리텔링형 보컬이 적합하며, 몽환적인 분위기를 자아내는 창법이 기질과 공명합니다. 기술적인 화려함보다는 소리 한 점에 담긴 감정의 밀도를 중시하므로, 청중의 무의식을 건드리는 지혜로운 선율을 구사합니다. 귀하가 연주하는 잔향이 깊은 소리들은 단순한 음악을 넘어 듣는 이의 영혼을 치유하고 정서적인 평온을 안겨주는 특별한 힘을 발휘하게 될 것입니다.
        """
    }
}

# 3️⃣ 연도별 운세 DB (생략 - 이전 버전과 동일)
yearly_luck_db = {
    '비겁': "올해는 본인의 주체성과 독립심이 극대화되는 시기입니다...",
    '식상': "창작의 마르지 않는 샘물을 만난 듯 영감이 쏟아지는 해입니다...",
    '재성': "음악을 하나의 거대한 건축물처럼 이해하고 설계하는 해입니다...",
    '관성': "명예와 규율을 중요시하며 음악적 위상이 공적으로 인정받는 해입니다...",
    '인성': "깊은 통찰력과 지혜로운 사유를 바탕으로 철학적 메시지를 담는 해입니다..."
}

# 4️⃣ 계산 로직 함수들
def get_ohaeng_max(ba_zi):
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    return max(counts, key=counts.get)

def get_ohaeng(gan):
    return {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}.get(gan, '목')

def get_sibsung_name(my_gan, target_gan):
    order = ['목', '화', '토', '금', '수']
    my_oh = get_ohaeng(my_gan)
    target_oh = get_ohaeng(target_gan)
    idx_diff = (order.index(target_oh) - order.index(my_oh)) % 5
    return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[idx_diff]

# 5️⃣ 실행 UI 및 출력
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="임환백")
    col1, col2, col3 = st.columns(3)
    y = col1.number_input("출생년", 1900, 2100, value=1981)
    m = col2.number_input("출생월", 1, 12, value=2)
    d = col3.number_input("출생일", 1, 31, value=7)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    lunar = Solar.fromYmd(int(y), int(m), int(d)).getLunar()
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "辛卯"]
    d_gan = lunar.getDayGan()
    
    # 분석 데이터 매칭
    max_oh = get_ohaeng_max(ba_zi)
    origin_sib = get_sibsung_name(d_gan, max_oh)
    data = analysis_db[origin_sib]
    
    target_lunar = Solar.fromYmd(int(target_y), 1, 1).getLunar()
    target_gan = target_lunar.getYearGan()
    target_gz = target_lunar.getYearInGanZhi()
    target_sib = get_sibsung_name(d_gan, target_gan)

    # 출력
    st.markdown(f"### 🍀 {user_name}님의 심층 리포트")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 운명적 기질</h2><div class='content-text'>{data['gen']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주와 예술성</h2><div class='content-text'>{data['mus']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='inst-card'><h2>🎻 운명적 악기 및 보컬 스타일</h2><div class='content-text'>{data['instrument']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='position-card'><h2>✨ 추천 포지션 및 전문 역량</h2><div class='content-text'><span class='pos-title'>{data['pos_title']}</span>{data['pos_desc']}</div></div>", unsafe_allow_html=True)

    # 연도별 동적 리포트
    st.markdown(f"""
    <div class='target-year-card'>
        <h2>🏙️ {target_y}년({target_gz}) 종합 운세 리포트</h2>
        <div class='content-text'>
            <b>{target_y}년은 귀하의 {d_gan} 일간이 세운의 천간 {target_gan}을(를) 만나 '{target_sib}'의 기운이 지배하는 해입니다.</b><br><br>
            {yearly_luck_db[target_sib]}
        </div>
    </div>
    """, unsafe_allow_html=True)
