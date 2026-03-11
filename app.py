import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인
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
# (기존 analysis_db의 'gen', 'mus', 'pos' 데이터는 타고난 사주 분석용으로 유지)
analysis_db = {
    '비겁': {
        'gen': "본인은 주체성과 독립심이 대단히 강한 명식으로, 외부의 압력이나 타인의 시선에 굴하지 않고 자신만의 뚜렷한 가치관을 관철하는 강직한 성품을 지니고 있습니다...",
        'mus': "음악적으로는 그 누구와도 비교할 수 없는 독창적인 사운드를 구축하는 솔로 아티스트의 기질이 매우 농후합니다...",
        'pos_title': "🎤 독보적 아우라의 솔로 싱어송라이터",
        'pos_desc': "귀하의 명식에서 가장 빛나는 포지션은 본인의 강력한 자아를 무대 위에서 가감 없이 표출하는 프런트맨이자 리드 보컬입니다..."
    },
    '식상': {
        'gen': "본인은 천재적인 영감과 표현의 수려함을 타고난 명식으로, 일상의 모든 경험을 예술적 가치로 치환하는 비범한 재능을 지니고 있습니다...",
        'mus': "창작의 마르지 않는 샘물을 가진 아티스트로서, 멜로디와 가사를 직조하는 감각이 본능적으로 발달해 있습니다...",
        'pos_title': "🎹 천재적 영감의 퍼포머 & 메인 작곡가",
        'pos_desc': "관객을 사로잡는 화려한 연주자이자 창의적인 작곡가로서 가장 큰 빛을 발합니다..."
    },
    '재성': {
        'gen': "본인은 현실을 꿰뚫어 보는 안목과 공간을 장악하는 능력이 남다른 명식으로, 매사에 실리적이고 결과 중심적인 사고를 통해 목표를 성취하는 대단히 유능한 성품의 소유자입니다...",
        'mus': "음악을 하나의 거대한 건축물처럼 이해하고 설계하는 프로듀싱 능력이 탁월합니다...",
        'pos_title': "🎚️ 사운드 디렉터 & 총괄 프로듀서",
        'pos_desc': "전체 사운드를 조율하고 앨범의 상업적·예술적 가치를 책임지는 프로듀서 역할에 최적입니다..."
    },
    '관성': {
        'gen': "본인은 명예와 규율을 목숨처럼 중요하게 여기는 강직한 성품과 완벽주의를 소유한 명식입니다...",
        'mus': "음악적 형식미와 정교한 구조를 추구하는 완벽주의자의 면모를 보여줍니다...",
        'pos_title': "🎯 완벽주의 밴드 마스터 & 마스터링 엔지니어",
        'pos_desc': "앙상블의 기강을 잡고 사운드의 규격화된 완성도를 이끄는 리더나 기술적 정점에 서 있는 엔지니어에 적합합니다..."
    },
    '인성': {
        'gen': "본인은 깊은 통찰력과 지혜로운 사유를 바탕으로 현상의 본질을 탐구하는 선비와 같은 기질을 지닌 명식입니다...",
        'mus': "음악 속에 심오한 철학적 메시지와 신비로운 무의식의 영역을 담아내는 능력이 탁월합니다...",
        'pos_title': "🎼 심오한 음악 철학자 & 수석 편곡가",
        'pos_desc': "곡의 내러티브를 설계하고 세련된 화성으로 사운드를 풍성하게 만드는 편곡 분야에서 독보적입니다..."
    }
}

# 3️⃣ 동적 세운(연도별) 통변 데이터베이스
yearly_luck_db = {
    '비겁': "올해는 본인의 주체적인 에너지가 대외적인 결과물로 강력하게 표출되는 시기입니다. 주변의 시선에 구애받지 않고 예술적 영감을 소신껏 펼칠 때 청중으로부터 경외심에 가까운 반응을 이끌어낼 수 있습니다. 독립적인 프로젝트를 추진하기에 최적의 해입니다.",
    '식상': "창의적인 에너지가 정점에 달하여 곡 작업의 속도가 붙고, 예상치 못한 협업을 통해 본인의 음악적 지평이 획기적으로 넓어지는 경험을 하게 될 것입니다. 새로운 장르로의 도전이나 파격적인 퍼포먼스가 대중의 열광적인 반응을 이끌어낼 것입니다.",
    '재성': "그동안 정교하게 준비해 온 프로젝트가 세상의 빛을 보며 실제적인 '결실'로 돌아오는 보상의 해입니다. 경제적인 이익과 명예를 동시에 거머쥐게 될 확률이 높으며, 본인의 디렉팅 능력이 업계의 인정을 받아 중요한 계약이 성사될 운세입니다.",
    '관성': "음악적 위상이 공적으로 인정받는 권위의 해입니다. 자신에게 엄격한 기준을 적용한 결과물이 평단의 극찬을 받게 되며, 책임감 있는 리더십을 발휘하여 밴드나 프로젝트를 성공적인 궤도에 올려놓게 됩니다. 공적인 수상이나 명예로운 소식이 따릅니다.",
    '인성': "깊이 있는 사유와 내공이 음악에 녹아들어 대중적인 감동을 자아내는 해입니다. 창작 활동에서 오는 정신적 고뇌가 오히려 예술적 깊이를 더해주는 자양분이 되며, 본인이 정립한 음악적 스타일이 업계에 커다란 영감을 주는 등 영향력이 확대될 것입니다."
}

# 4️⃣ 로직 함수들
hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

def get_ohaeng(gan):
    return {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}.get(gan, '목')

def get_sibsung_name(my_gan, target_gan):
    order = ['목', '화', '토', '금', '수']
    my_oh = get_ohaeng(my_gan)
    target_oh = get_ohaeng(target_gan)
    idx_diff = (order.index(target_oh) - order.index(my_oh)) % 5
    return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[idx_diff]

def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {'申|子|辰': ['寅', '卯', '辰'], '亥|卯|未': ['巳', '午', '미'], '寅|午|戌': ['申', '酉', '戌'], '巳|酉|丑': ['亥', '子', '丑']}
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

# 5️⃣ 입력 및 메인 실행부
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="", placeholder="성함을 입력하세요")
    col1, col2, col3 = st.columns(3)
    y = col1.number_input("출생년", 1900, 2100, value=1981)
    m = col2.number_input("출생월", 1, 12, value=2)
    d = col3.number_input("출생일", 1, 31, value=7)
    h_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=4) # 묘시 기본값
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    h_val = hour_time_map[h_str]
    calc_h = 12 if h_val == "unknown" else h_val
    lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0)
    
    # 사주 원국 및 오행 계산
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
    d_gan = lunar.getDayGan()
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    max_elem = max(counts, key=counts.get)
    
    # 목표 연도(세운) 계산
    target_lunar = Solar.fromYmd(int(target_y), 1, 1).getLunar()
    target_gan = target_lunar.getYearGan()
    target_gz = target_lunar.getYearInGanZhi()
    
    # 연도별 십성 및 운세 텍스트 매칭
    target_sibsung = get_sibsung_name(d_gan, target_gan)
    target_luck_text = yearly_luck_db[target_sibsung]
    
    # 원국 분석 데이터 매칭
    sib_key = get_sibsung_name(d_gan, max_elem)
    data = analysis_db[sib_key]
    samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

    # 출력 화면 구성
    st.markdown(f"### 🍀 {user_name if user_name else '아티스트'}님의 심층 리포트")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b></div>", unsafe_allow_html=True)

    # 섹션 1: 타고난 분석
    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정</h2><div class='content-text'>{data['gen']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주</h2><div class='content-text'>{data['mus']}</div></div>", unsafe_allow_html=True)
    
    # 섹션 2: {target_y}년 동적 운세
    st.markdown(f"""
    <div class='target-year-card'>
        <h2>🏙️ {target_y}년({target_gz}) 일반 운세 흐름</h2>
        <div class='content-text'>
            {target_y}년은 귀하의 <b>{d_gan}</b> 일간이 세운의 천간 <b>{target_gan}</b>을 만나 <b>{target_sibsung}</b>의 기운이 강하게 작용하는 해입니다. 
            이는 인생의 마디를 형성하는 매우 중요한 변곡점으로, 그동안 묵묵히 쌓아온 내공이 사회적인 환경과 조우하여 강력한 결실을 맺는 시기가 될 것입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='music-card' style='background-color:#FFF5F7;'>
        <h2>🎹 {target_y}년 음악적 흐름 이야기</h2>
        <div class='content-text'>
            <b>[연도별 십성: {target_sibsung}]</b><br>
            {target_luck_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
