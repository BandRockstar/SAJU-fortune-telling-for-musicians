import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인 (원본 스타일 완벽 복구)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.6", layout="centered")
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

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.6</h1></div>", unsafe_allow_html=True)

# 2️⃣ 복구된 핵심 계산 함수 (삼재 로직 포함)
def get_samjae(year_zhi):
    samjae_map = {
        '申': ['寅', '卯', '辰'], '子': ['寅', '卯', '辰'], '辰': ['寅', '卯', '辰'],
        '亥': ['巳', '午', '未'], '卯': ['巳', '午', '未'], '未': ['巳', '午', '未'],
        '寅': ['申', '酉', '戌'], '午': ['申', '酉', '戌'], '戌': ['申', '酉', '戌'],
        '巳': ['亥', '子', '丑'], '酉': ['亥', '子', '丑'], '丑': ['亥', '子', '丑']
    }
    return samjae_map.get(year_zhi, [])

def get_ohaeng(gan):
    return {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}.get(gan, '목')

def get_sibsung_name(my_gan, target_gan):
    order = ['목', '화', '토', '금', '수']
    my_oh, target_oh = get_ohaeng(my_gan), get_ohaeng(target_gan)
    idx_diff = (order.index(target_oh) - order.index(my_oh)) % 5
    return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[idx_diff]

def get_ohaeng_max(ba_zi):
    # 년월일시 8글자 전체 분석
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    full_str = "".join(ba_zi)
    counts = {k: sum(1 for c in full_str if c in v) for k, v in ohaeng_map.items()}
    return max(counts, key=counts.get)

# 3️⃣ 통합 데이터 엔진: 원본 기질 + 음악적 5대 악기 상세 분석
analysis_db = {
    '비겁': {
        'gen': "주체성과 독립심이 강하며 자신만의 뚜렷한 가치관을 관철하는 강직한 성품입니다. 외부의 압력에 굴하지 않고 스스로를 일으켜 세우는 불굴의 의지가 돋보입니다.",
        'mus': "독창적인 사운드를 구축하는 솔로 아티스트 기질이 강합니다. '나 자신이 장르'가 되는 예술적 경지를 지향하며, 무대 위에서 압도적인 존재감을 발휘합니다.",
        'pos_title': "🎤 독보적 아우라의 리드 보컬",
        'pos_desc': "곡의 기획부터 연주까지 본인의 의도대로 끌고 나갈 때 최고의 시너지가 발생합니다. 청중을 단숨에 사로잡는 강력한 무대 장악력을 타고났습니다.",
        'instrument': """귀하에게 운명적인 악기는 **보컬**과 **기타**입니다. 비겁의 강렬한 에너지는 무대 중앙에서 대중을 압도하는 에너지를 필요로 합니다. 보컬로서는 기교보다 목소리의 톤과 힘으로 청중을 관통하는 스타일이 적합하며, 직선적인 벨팅 창법이 기질과 잘 맞습니다. 기타를 잡는다면 섬세한 연주보다 화려하고 공격적인 리드 기타가 어울립니다. 전체 사운드의 중심을 뚫고 나오는 선명한 존재감을 드러낼 때 예술적 갈증이 해소될 것입니다. 밴드 내에서도 다른 악기에 묻히기보다 사운드의 주인공으로서 기능할 때 가장 큰 음악적 성취를 거둘 수 있습니다."""
    },
    '식상': {
        'gen': "천재적인 영감과 표현의 수려함을 타고난 명식으로, 일상의 모든 경험을 예술적 가치로 치환하는 비범한 재능을 지니고 있습니다.",
        'mus': "창작의 마르지 않는 샘물을 가진 아티스트로서, 멜로디와 가사를 직조하는 감각이 본능적으로 발달해 있습니다. 즉흥적인 영감을 소리로 표현하는 데 능합니다.",
        'pos_title': "🎹 천재적 영감의 키보디스트",
        'pos_desc': "순발력이 요구되는 즉흥 연주나 대중의 심리를 꿰뚫는 멜로디 메이킹에 강점이 있습니다. 화려한 연주자로 가장 큰 빛을 발합니다.",
        'instrument': """다채로운 표현력을 지닌 귀하에게는 **키보드(신디사이저)**와 **기타**가 최적입니다. 식상의 창의성은 무한한 소리의 변화를 추구하므로, 수만 가지 음색을 디자인할 수 있는 키보드를 통해 상상력을 현실화할 때 최고의 희열을 느낍니다. 기타 연주 시에도 이펙터를 적극 활용하여 자신만의 사운드 텍스처를 직조하는 능력이 탁월합니다. 보컬로서는 화려한 애드리브와 넓은 음역대를 활용하는 스타일이 귀하의 기질과 공명합니다. 귀하의 연주는 단순히 음을 나열하는 것이 아니라, 매 순간 변화하는 감정의 물결을 소리로 치환하는 과정이기에 관객들에게 강렬한 퍼포먼스적 쾌감을 선사하게 될 것입니다."""
    },
    '재성': {
        'gen': "현실을 꿰뚫어 보는 안목과 공간 장악 능력이 남다릅니다. 실리적이고 결과 중심적인 사고를 통해 목표를 성취하는 유능한 성품의 소유자입니다.",
        'mus': "음악을 거대한 건축물처럼 이해하고 설계하는 프로듀싱 능력이 탁월합니다. 사운드 밸런스와 대중적 성공 가능성을 냉철하게 판단하는 안목을 지녔습니다.",
        'pos_title': "🥁 사운드 디렉터 & 드러머",
        'pos_desc': "전체 사운드를 조율하고 앨범의 가치를 책임지는 프로듀서 역할에 최적입니다. 세션 뮤지션들을 적재적소에 배치하는 관리 능력이 돋보입니다.",
        'instrument': """음악의 뼈대를 형성하는 귀하에게는 **드럼**과 **베이스**가 운명적입니다. 재성의 현실 장악력은 무대 뒤편에서 전체 앙상블의 리듬을 완벽하게 통제할 때 빛납니다. 드럼은 곡의 구조를 결정짓는 설계도이며, 베이스는 화성과 리듬을 연결하는 가교이기에 본인의 관리자적 기질과 일치합니다. 화려하게 전면에 나서기보다 전체 사운드가 비지 않도록 채워주는 견고한 플레이에서 깊은 만족감을 느낄 것입니다. 동료 뮤지션들이 마음 놓고 연주할 수 있는 가장 든든한 기반이 될 것이며, 보컬을 한다면 안정적인 호흡을 바탕으로 곡의 서사를 이끄는 스타일이 적합합니다."""
    },
    '관성': {
        'gen': "명예와 규율을 중요하게 여기는 강직한 성품과 완벽주의를 소유한 명식입니다. 자신에게 엄격한 기준을 적용하며 조직의 질서를 유지합니다.",
        'mus': "음악적 형식미와 정교한 구조를 추구합니다. 단 한 치의 오차도 허용하지 않는 정밀한 연주와 사운드 디자인을 지향하며 본질적인 가치를 추구합니다.",
        'pos_title': "🎯 완벽주의 밴드 마스터",
        'pos_desc': "앙상블의 기강을 잡고 사운드의 완성도를 이끄는 리더에 적합합니다. 시스템 설계 및 정밀한 소리 편집 분야에서 독보적입니다.",
        'instrument': """정밀함을 중시하는 귀하에게는 **키보드**와 **베이스**가 가장 적합합니다. 키보드는 화성학적 기초와 정교한 터치가 요구되기에 귀하의 완벽주의를 투영하기 좋고, 베이스 연주 시에도 정확한 박자로 밴드의 품격을 높입니다. 보컬 스타일은 정석적인 발성과 정갈한 창법을 선호합니다. 정해진 약속(Score)을 완벽하게 이행하는 모습에서 아티스트로서의 독보적 권위가 세워지게 될 것입니다. 귀하의 소리는 청중에게 깊은 신뢰감을 주며, 정교하게 세공된 사운드의 정수를 보여줄 것입니다."""
    },
    '인성': {
        'gen': "깊은 통찰력과 지혜로운 사유를 바탕으로 본질을 탐구합니다. 지식 습득 능력이 뛰어나며 이를 자신만의 철학으로 재해석하는 능력이 탁월합니다.",
        'mus': "음악 속에 심오한 철학적 메시지와 무의식의 영역을 담아냅니다. 세계관을 창조하는 과정을 즐기며 보이지 않는 정서를 유려한 선율로 치환합니다.",
        'pos_title': "🎼 수석 편곡가 & 키보디스트",
        'pos_desc': "곡의 내러티브를 설계하고 세련된 화성으로 사운드를 풍성하게 만드는 편곡 분야에서 독보적입니다. 예술적 해석력이 매우 뛰어납니다.",
        'instrument': """깊은 사유를 추구하는 귀하에게는 **기타(어쿠스틱)**와 **키보드(피아노)**가 가장 잘 어울립니다. 풍부한 울림을 가진 악기를 통해 내면세계를 확장하며, 여운이 긴 선율을 직조할 때 영감이 극대화됩니다. 보컬은 이야기를 들려주는 스토리텔링형 보컬이 적합하며, 기술적 화려함보다 감정의 밀도를 중시하여 청중의 무의식을 건드리는 지혜로운 선율을 구사하게 될 것입니다. 귀하가 연주하는 소리들은 단순한 음악을 넘어 영혼을 치유하는 특별한 힘을 발휘하게 될 것입니다."""
    }
}

# 4️⃣ 사용자 입력단 (원본 필드 완벽 복구)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="임환백")
    calendar_type = st.radio("날짜 구분", ["양력", "음력", "음력(윤달)"], horizontal=True)
    col1, col2, col3 = st.columns(3)
    y = col1.number_input("년", 1900, 2100, 1981)
    m = col2.number_input("월", 1, 12, 2)
    d = col3.number_input("일", 1, 31, 7)
    # 원본 인덱스 유지
    h_str = st.selectbox("출생 시간", ["05~07 묘시", "23~01 자시", "01~03 축시", "03~05 인시", "07~09 진시", "09~11 사시", "11~13 오시", "13~15 미시", "15~17 신시", "17~19 유시", "19~21 술시", "21~23 해시"], index=0)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    # 날짜 변환 및 사주 산출
    if calendar_type == "양력":
        solar = Solar.fromYmd(int(y), int(m), int(d))
        lunar = solar.getLunar()
    else:
        is_leap = (calendar_type == "음력(윤달)")
        lunar = Lunar.fromYmd(int(y), int(m), int(d), is_leap)
    
    # 시주(時柱) 정밀 산출
    h_idx = ["05~07 묘시", "23~01 자시", "01~03 축시", "03~05 인시", "07~09 진시", "09~11 사시", "11~13 오시", "13~15 미시", "15~17 신시", "17~19 유시", "19~21 술시", "21~23 해시"].index(h_str)
    hour_val = [6, 0, 2, 4, 8, 10, 12, 14, 16, 18, 20, 22][h_idx]
    
    # 8글자 산출
    year_gz = lunar.getYearInGanZhi()
    month_gz = lunar.getMonthInGanZhi()
    day_gz = lunar.getDayInGanZhi()
    time_gz = lunar.getTimeGanZhi() # lunar_python을 이용한 정확한 시주 산출
    ba_zi = [year_gz, month_gz, day_gz, time_gz]
    d_gan = lunar.getDayGan()
    
    # 삼재 계산
    year_zhi = year_gz[1]
    samjae_years = get_samjae(year_zhi)
    
    # 분석 데이터 매칭
    max_oh = get_ohaeng_max(ba_zi)
    origin_sib = get_sibsung_name(d_gan, max_oh)
    data = analysis_db[origin_sib]
    
    # 세운 산출 (이미지 d51fb5 로직 반영)
    target_lunar = Solar.fromYmd(int(target_y), 1, 1).getLunar()
    t_gan, t_gz = target_lunar.getYearGan(), target_lunar.getYearInGanZhi()
    t_sib = get_sibsung_name(d_gan, t_gan)
    is_target_samjae = t_gz[1] in samjae_years

    # 5️⃣ 리포트 출력
    st.markdown(f"### 🍀 {user_name}님의 심층 리포트")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)

    # 섹션 1: 타고난 명식
    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 운명적 기질</h2><div class='content-text'>{data['gen']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주와 예술성</h2><div class='content-text'>{data['mus']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='inst-card'><h2>🎻 운명적 악기 및 보컬 스타일</h2><div class='content-text'>{data['instrument']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='position-card'><h2>✨ 추천 포지션 및 전문 역량</h2><div class='content-text'><span class='pos-title'>{data['pos_title']}</span>{data['pos_desc']}</div></div>", unsafe_allow_html=True)

    # 섹션 2: 세운 리포트 (이미지 d51fb5 스타일)
    samjae_msg = f" (⚠️ {target_y}년은 귀하에게 삼재에 해당하는 해입니다)" if is_target_samjae else ""
    st.markdown(f"""
    <div class='target-year-card'>
        <h2>🏙️ {target_y}년({t_gz}) 종합 운세 리포트 {samjae_msg}</h2>
        <div class='content-text'>
            2026년은 귀하의 {d_gan} 일간이 세운의 천간 {t_gan}을(를) 만나 '{t_sib}'의 기운이 지배하는 해입니다.<br><br>
            이 시기에는 본인이 구축해온 음악적 기반이 외부 환경과 만나 큰 변화를 겪게 됩니다. 특히 {t_sib}의 특성에 맞춰 창작의 방향성을 설정한다면 보다 효율적인 예술적 성취를 거둘 수 있습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='music-card' style='background-color:#FFF5F7;'>
        <h2>🎹 {target_y}년 음악적 흐름과 창작 운세</h2>
        <div class='content-text'>
            올해 도래하는 <b>{t_sib}</b>의 기운은 귀하의 창작 세계에 새로운 활력을 불어넣을 것입니다. 본인의 음악적 색채 위에 올해의 운이 제공하는 에너지가 더해져, 이전과는 다른 차원의 사운드 메이킹이 가능해집니다. {target_y}년에 기획하는 프로젝트는 장기적으로 커리어에서 중요한 포트폴리오가 될 것입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
