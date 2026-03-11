import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인 (사용자 정의 스타일 유지)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.3", layout="centered")
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

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.3</h1></div>", unsafe_allow_html=True)

# 2️⃣ 복구된 데이터 엔진: 5대 악기군 분석 포함
analysis_db = {
    '비겁': {
        'gen': "귀하는 주체성과 독립심이 대단히 강한 명식으로, 외부의 압력이나 타인의 시선에 굴하지 않고 자신만의 뚜렷한 가치관을 관철하는 강직한 성품을 지니고 있습니다. 비견과 겁재의 강한 에너지는 삶의 고비마다 스스로를 일으켜 세우는 불굴의 의지가 되며, 어떤 환경에서도 본인의 색깔을 잃지 않는 독보적인 존재감을 드러내게 합니다. 타인에게 의지하기보다 자신의 실력을 믿고 나아가는 자수성가형의 전형이며, 인간관계에서는 한 번 맺은 인연에 대해 깊은 신의를 지키지만 자신의 영역을 침범당하는 것에는 타협이 없는 철저한 면모를 보입니다. 이러한 기질은 사회생활에서 카리스마로 나타나며, 본인만의 확고한 지지 세력을 형성하여 큰 성취를 이루는 원동력이 될 것입니다.",
        'mus': "음악적으로는 그 누구와도 비교할 수 없는 독창적인 사운드를 구축하는 솔로 아티스트의 기질이 매우 농후합니다. 남들의 유행을 쫓기보다는 본인이 느끼는 감정과 철학을 소리로 투영하는 데 집중하며, '나 자신이 곧 장르'가 되는 예술적 경지를 지향합니다. 보컬의 음색이나 연주의 톤에 있어서 본인만의 시그니처가 확실하여 청중에게 강렬한 인상을 남기며, 밴드 활동 시에도 전체적인 음악적 방향성을 주도하는 절대적인 존재감을 발휘합니다. 자존심이 강한 만큼 창작물에 대한 애착이 대단하며, 타협하지 않는 예술가적 고집은 시간이 흐를수록 범접할 수 없는 아티스트로서의 명성을 얻게 할 것입니다.",
        'pos_title': "🎤 독보적 아우라의 리드 보컬",
        'pos_desc': "귀하의 명식에서 가장 빛나는 포지션은 본인의 강력한 자아를 무대 위에서 가감 없이 표출하는 프런트맨입니다. 타인의 간섭 없이 곡의 기획부터 최종 연주까지 본인의 의도대로 끌고 나갈 때 최고의 시너지가 발생하며, 청중의 시선을 단숨에 사로잡는 강력한 무대 장악력을 타고났습니다.",
        'instrument': "귀하에게 가장 어울리는 파트는 **보컬**과 **기타**입니다. 비겁의 강한 주체성은 무대 중앙에서 군중을 압도하는 에너지를 필요로 합니다. 보컬로서는 목소리 자체의 힘과 진정성으로 청중의 심장을 관통하는 스타일이 적합하며, 직선적인 벨팅 창법이 기질과 잘 맞습니다. 기타를 잡는다면 섬세한 백킹보다는 화려하고 공격적인 리드 기타가 운명적입니다. 본인만의 독보적인 톤을 구축하여 사운드의 중심을 뚫고 나오는 선명한 존재감을 드러낼 때 예술적 갈증이 해소될 것입니다."
    },
    '식상': {
        'gen': "본인은 천재적인 영감과 표현의 수려함을 타고난 명식으로, 일상의 모든 경험을 예술적 가치로 치환하는 비범한 재능을 지니고 있습니다. 식신과 상관의 발달은 표현력을 극대화하여 타인과의 교감 능력을 높여주며, 창의적인 사고방식을 통해 주변을 밝히는 에너지를 전파합니다. 호기심이 많고 탐구심이 강하여 새로운 기술이나 장르를 습득하는 속도가 매우 빠르며, 본인의 아이디어를 구체적인 형상으로 만들어내는 실행력 또한 탁월합니다. 감수성이 예민하여 주변의 변화를 본능적으로 감지하고 이를 세련된 방식으로 표출하는 능력이 돋보입니다.",
        'mus': "창작의 마르지 않는 샘물을 가진 아티스트로서, 멜로디와 가사를 직조하는 감각이 본능적으로 발달해 있습니다. 화려한 연주 테크닉은 물론, 청중의 심리를 파고드는 감성적인 톤 메이킹에 소질을 보입니다. 정형화된 틀에 얽매이지 않고 즉흥적인 영감을 소리로 표현하는 데 능하며, 장르를 넘나드는 유연한 창작 활동을 통해 대중과 소통합니다. 가사 한 구절에도 재치와 감수성을 담아내는 능력이 탁월하며, 이는 듣는 이에게 입체적인 감동을 선사합니다. 시대의 트렌드를 선도하는 사운드 메이커로서 명성을 얻게 될 것입니다.",
        'pos_title': "🎹 천재적 영감의 키보디스트 & 작곡가",
        'pos_desc': "관객을 사로잡는 화려한 연주자이자 창의적인 작곡가로서 가장 큰 빛을 발합니다. 순발력이 요구되는 즉흥 연주나 대중의 심리를 꿰뚫는 멜로디 메이킹에 강점이 있으며, 자신의 감정을 소리로 투영하여 예술적 카타르시스를 느끼게 해주는 재능을 지니고 있습니다.",
        'instrument': "다채로운 감수성을 표출해야 하는 귀하에게는 **키보드(신디사이저)**와 **기타**가 최적입니다. 식상의 창의성은 무한한 소리의 변화를 추구하므로, 음색을 자유자재로 디자인할 수 있는 키보드를 통해 상상력을 현실화할 때 희열을 느낍니다. 기타를 연주할 때도 이펙터를 적극 활용하여 세상에 없던 사운드 텍스처를 만들어내는 능력이 탁월합니다. 보컬을 겸한다면 화려한 애드리브와 넓은 음역대를 활용하는 스타일이 어울리며, 매 순간 변화하는 감정의 물결을 퍼포먼스로 승화시키게 됩니다."
    },
    '재성': {
        'gen': "본인은 현실을 꿰뚫어 보는 안목과 공간을 장악하는 능력이 남다른 명식으로, 매사에 실리적이고 결과 중심적인 사고를 통해 목표를 성취하는 유능한 성품의 소유자입니다. 환경을 본인에게 유리하게 조율하는 힘을 상징하며, 복잡한 상황 속에서도 본질을 빠르게 파악하여 가장 효율적인 해결책을 찾아냅니다. 신용을 소중히 여기며 대인관계가 확실하여 사회적으로 높은 신뢰를 얻습니다. 철저한 계획과 관리를 통해 성과를 도출해내는 능력이 탁월하며, 주변 사람들에게는 믿고 의지할 수 있는 리더로서 평가받게 될 것입니다.",
        'mus': "음악을 하나의 거대한 건축물처럼 이해하고 설계하는 프로듀싱 능력이 탁월합니다. 단순히 연주하는 단계를 넘어 사운드의 밸런스와 대중적 성공 가능성을 냉철하게 판단하는 안목을 지녔습니다. 시장의 트렌드와 본인의 예술적 개성을 조화롭게 융합시켜 매력적인 결과물을 도출해내며, 앨범의 기획부터 마케팅 단계까지 고려하는 전략적인 음악 활동을 전개합니다. 복잡한 세션 구성 속에서도 사운드의 핵심 톤을 명확히 짚어내어 완성도를 극대화합니다. 정서적인 안정감과 묵직한 감동을 동시에 선사하는 음악 세계를 완성하게 될 것입니다.",
        'pos_title': "🥁 사운드 디렉터 & 드러머",
        'pos_desc': "전체 사운드를 조율하고 앨범의 가치를 책임지는 프로듀서 역할에 최적입니다. 세션 연주자들의 능력을 적재적소에 배치하고, 완성도를 결정짓는 단계에서 타의 추종을 불허하는 전문성을 발휘하게 됩니다.",
        'instrument': "음악의 뼈대를 형성하고 전체 흐름을 제어하는 귀하에게는 **드럼**과 **베이스**가 운명적입니다. 재성의 현실 장악력은 무대 뒤편에서 앙상블의 박자와 리듬을 완벽하게 통제할 때 빛납니다. 드럼은 곡의 구조를 결정짓는 설계도와 같으며, 베이스는 화성과 리듬을 연결하는 가교이기에 본인의 관리자적 기질과 공명합니다. 화려한 솔로보다는 팀 전체의 사운드가 비지 않도록 채워주는 견고한 플레이에서 깊은 만족감을 느끼며, 동료들에게 가장 든든한 기반이 되어줍니다."
    },
    '관성': {
        'gen': "본인은 명예와 규율을 중요하게 여기는 강직한 성품과 완벽주의를 소유한 명식입니다. 자신에게 엄격한 기준을 적용하며 정직과 신뢰를 요구합니다. 조직 내에서 올바른 질서를 유지하는 데 중추적인 역할을 수행하며, 책임감이 대단히 강하여 맡은 임무는 어떤 난관이 있어도 끝까지 완수해내는 뚝심을 지녔습니다. 이러한 성정은 주변의 존경을 얻는 근간이 됩니다. 공정함을 잃지 않으려 노력하는 모습은 사회적으로 높은 지위에 오르게 하며, 시간이 흐를수록 견고함이 빛을 발하는 품격 있는 운명적 특징을 지닙니다.",
        'mus': "음악적 형식미와 정교한 구조를 추구하는 완벽주의자의 면모를 보입니다. 단 한 치의 오차도 허용하지 않는 정밀한 연주와 사운드 디자인을 지향하며, 불필요한 장식을 걷어낸 본질적인 가치를 추구합니다. 작품의 퀄리티를 최상으로 유지하며 밴드의 앙상블을 조율하고 기강을 잡는 마스터로서의 역량이 탁월합니다. 믹싱이나 마스터링 과정에서 집중력을 발휘하며, 차가운 톤 속에 숨겨진 투명한 진심은 청중의 이성을 자극합니다. 타협을 모르는 예술가의 정수가 담긴 사운드 아카이브를 구축하게 될 것입니다.",
        'pos_title': "🎯 밴드 마스터 & 베이시스트",
        'pos_desc': "앙상블의 기강을 잡고 사운드의 규격화된 완성도를 이끄는 리더에 적합합니다. 고도의 집중력을 요하는 소리 편집 및 시스템 설계에 강점이 있으며, 본인의 철저한 관리 하에 완성된 음악은 독보적인 품격을 지니게 됩니다.",
        'instrument': "정밀함과 규율을 중시하는 귀하에게는 **키보드**와 **베이스**가 적합합니다. 키보드는 화성학적 기초가 탄탄해야 하며 정교한 터치가 요구되기에 귀하의 기질을 투영하기 좋고, 베이스 연주 시에도 메트로놈 같은 정확성을 보여주어 밴드의 음악적 품격을 높입니다. 보컬 스타일은 정석적인 발성과 정갈한 창법을 선호합니다. 정해진 약속(Score)을 완벽하게 이행하는 모습에서 아티스트로서의 독보적 권위가 세워지며, 소리의 설계자로서 기능하게 됩니다."
    },
    '인성': {
        'gen': "본인은 깊은 통찰력과 지혜로운 사유를 바탕으로 본질을 탐구하는 지혜로운 명식입니다. 지식의 습득 능력이 뛰어나고 이를 본인만의 철학으로 재해석하는 능력이 탁월합니다. 수용성이 좋아 타인의 감정과 주변 에너지를 민감하게 읽어내며, 갈등을 치유하고 정서적 안정감을 주는 중재자 역할을 수행합니다. 내면의 충만함을 중시하며 인문학적 소양이 깊습니다. 사회적으로 정신적 지주나 전문 지식을 다루는 분야에서 큰 빛을 발하게 되며, 삶의 이치를 관조하며 평온을 유지하는 지혜로운 운명을 개척하게 됩니다.",
        'mus': "음악 속에 심오한 철학적 메시지와 무의식의 영역을 담아내는 능력이 탁월합니다. 완벽한 세계관을 창조하는 과정을 즐기며, 보이지 않는 정서를 유려한 선율로 치환하는 지혜가 대단합니다. 화성학적 구성이 치밀하고 가사 하나에도 문학적인 깊이가 느껴지는 지적인 음악을 선호하며, 청중을 현실 너머의 깊은 곳으로 안내합니다. 유행에 휩쓸리지 않는 독자적인 예술 세계를 구축하며, 음악을 통한 정서적 치유를 선사하는 아티스트로 추앙받습니다. 지혜로운 사유가 담긴 선율은 사람들의 영혼에 긴 여운을 남깁니다.",
        'pos_title': "🎼 수석 편곡가 & 키보디스트",
        'pos_desc': "곡의 내러티브를 설계하고 세련된 화성으로 사운드를 풍성하게 만드는 편곡 분야에서 독보적입니다. 보이지 않는 감정을 선율로 치환하는 능력을 갖추고 있으며, 음악적 이론을 바탕으로 새로운 예술적 해석을 제시합니다.",
        'instrument': "깊은 사유를 추구하는 귀하에게는 **기타(어쿠스틱)**와 **키보드(피아노)**가 어울립니다. 풍부한 울림을 가진 악기를 통해 내면세계를 확장하며, 여운이 긴 선율을 직조할 때 영감이 극대화됩니다. 보컬은 이야기를 들려주는 스토리텔링형 보컬이나 몽환적인 창법이 공명합니다. 기술적 화려함보다는 감정의 밀도를 중시하여 무의식을 건드리는 지혜로운 선율을 구사합니다. 귀하가 연주하는 소리들은 단순한 음악을 넘어 영혼을 치유하는 특별한 힘을 발휘하게 될 것입니다."
    }
}

# 3️⃣ 연도별 운세(세운) DB 복구
yearly_luck_db = {
    '비겁': "올해는 본인의 주체성과 독립심이 극대화되는 시기입니다. 외부의 압력이나 유행에 타협하기보다는 본인이 추구해온 정체성을 사운드에 녹여내어 독보적인 존재감을 드러내기에 최적인 해입니다. 주변의 간섭에서 벗어나 독자적인 솔로 프로젝트를 추진하거나 밴드의 리더로서 강력한 카리스마를 발휘하게 됩니다.",
    '식상': "창작의 마르지 않는 샘물을 만난 듯 영감이 쏟아지는 해입니다. 멜로디와 가사를 직조하는 감각이 본능적으로 발달하며, 본인의 감정을 소리로 투영하여 예술적 카타르시스를 느끼게 해주는 재능이 빛을 발합니다. 정형화된 틀에 얽매이지 않고 즉흥적인 영감을 소리로 표현하는 데 능해집니다.",
    '재성': "음악을 하나의 거대한 건축물처럼 이해하고 설계하는 현실적인 안목과 성취가 따르는 해입니다. 단순히 연주하는 단계를 넘어 사운드의 전체적인 밸런스와 대중적 성공 가능성을 냉철하게 판단하게 됩니다. 그동안 준비해온 프로젝트가 실제적인 '결실'로 돌아오는 보상의 해입니다.",
    '관성': "명예와 규율을 중요시하며 음악적 위상이 공적으로 인정받는 해입니다. 자신에게 엄격한 기준을 적용하는 만큼 단 한 치의 오차도 허용하지 않는 정밀한 연주와 사운드 디자인을 지향하게 됩니다. 완벽주의적인 태도는 작품의 퀄리티를 최상으로 유지하게 만듭니다.",
    '인성': "깊은 통찰력과 지혜로운 사유를 바탕으로 음악 속에 심오한 철학적 메시지를 담아내는 해입니다. 음악 철학이 심오해지고, 보이지 않는 정서적 깊이를 선율에 녹여내는 능력이 발달합니다. 공부와 수양에 유리한 시기라 새로운 화성학이나 음악 이론을 습득하기 좋습니다."
}

# 4️⃣ 핵심 계산 함수 (사용자 로직 준수)
def get_ohaeng(gan):
    return {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}.get(gan, '목')

def get_sibsung_name(my_gan, target_gan):
    order = ['목', '화', '토', '금', '수']
    my_oh = get_ohaeng(my_gan)
    target_oh = get_ohaeng(target_gan)
    idx_diff = (order.index(target_oh) - order.index(my_oh)) % 5
    return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[idx_diff]

def get_ohaeng_max(ba_zi):
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    return max(counts, key=counts.get)

# 5️⃣ 사용자 입력 UI (복구 완료)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="임환백")
    col1, col2, col3 = st.columns(3)
    y = col1.number_input("출생년", 1900, 2100, value=1981)
    m = col2.number_input("출생월", 1, 12, value=2)
    d = col3.number_input("출생일", 1, 31, value=7)
    # 복구: 출생 시간 리스트
    h_str = st.selectbox("출생 시간", ["05~07 묘시", "23~01 자시", "01~03 축시", "03~05 인시", "07~09 진시", "09~11 사시", "11~13 오시", "13~15 미시", "15~17 신시", "17~19 유시", "19~21 술시", "21~23 해시"], index=0)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    # 사주 산출
    solar = Solar.fromYmd(int(y), int(m), int(d))
    lunar = solar.getLunar()
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "辛卯"] # 고유 시주 적용
    d_gan = lunar.getDayGan()
    
    # 분석 데이터 매칭
    max_oh = get_ohaeng_max(ba_zi)
    origin_sib = get_sibsung_name(d_gan, max_oh)
    origin_data = analysis_db[origin_sib]

    # 세운 산출
    target_lunar = Solar.fromYmd(int(target_y), 1, 1).getLunar()
    target_gan = target_lunar.getYearGan()
    target_gz = target_lunar.getYearInGanZhi()
    target_sib = get_sibsung_name(d_gan, target_gan)
    target_luck_text = yearly_luck_db[target_sib]

    # 결과 출력 (레이아웃 복구)
    st.markdown(f"### 🍀 {user_name}님의 심층 리포트")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)

    # 섹션 1: 타고난 명식
    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 운명적 기질</h2><div class='content-text'>{origin_data['gen']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주와 예술성</h2><div class='content-text'>{origin_data['mus']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='inst-card'><h2>🎻 운명적 악기 및 보컬 스타일</h2><div class='content-text'>{origin_data['instrument']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='position-card'><h2>✨ 추천 포지션 및 전문 역량</h2><div class='content-text'><span class='pos-title'>{origin_data['pos_title']}</span>{origin_data['pos_desc']}</div></div>", unsafe_allow_html=True)

    # 섹션 2: 연도별 운세
    st.markdown(f"""
    <div class='target-year-card'>
        <h2>🏙️ {target_y}년({target_gz}) 종합 운세 리포트</h2>
        <div class='content-text'>
            <b>{target_y}년은 귀하의 {d_gan} 일간이 세운의 천간 {target_gan}을(를) 만나 '{target_sib}'의 기운이 지배하는 해입니다.</b><br><br>
            {target_luck_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 복구: 음악적 흐름 섹션
    st.markdown(f"""
    <div class='music-card' style='background-color:#FFF5F7;'>
        <h2>🎹 {target_y}년 음악적 흐름과 창작 운세</h2>
        <div class='content-text'>
            올해 도래하는 <b>{target_sib}</b>의 기운은 귀하의 창작 세계에 새로운 활력을 불어넣을 것입니다. 
            이미 확립된 본인의 음악적 색채 위에 올해의 운이 제공하는 특수한 에너지가 더해져, 이전과는 다른 차원의 사운드 메이킹이 가능해집니다. 
            {target_y}년에 발표하거나 기획하는 프로젝트는 장기적으로 귀하의 음악 커리어에서 중요한 포트폴리오가 될 것입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
