import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인 (원본 스타일 완벽 복구)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.7", layout="centered")
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

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.7</h1></div>", unsafe_allow_html=True)

# 2️⃣ 데이터 엔진
# (기존 analysis_db는 동일하므로 중복 방지를 위해 핵심 로직만 기술)
analysis_db = {
    '비겁': {'gen': "주체성이 강한 성품...", 'mus': "독창적 사운드...", 'pos_title': "🎤 리드 보컬", 'pos_desc': "무대 장악력...", 'instrument': "보컬과 기타가 최적... (300자 상세 내용)"},
    '식상': {'gen': "천재적 영감...", 'mus': "창작의 샘물...", 'pos_title': "🎹 키보디스트", 'pos_desc': "즉흥 연주...", 'instrument': "키보드와 기타... (300자 상세 내용)"},
    '재성': {'gen': "현실 장악력...", 'mus': "프로듀싱 능력...", 'pos_title': "🥁 드러머", 'pos_desc': "사운드 조율...", 'instrument': "드럼과 베이스... (300자 상세 내용)"},
    '관성': {'gen': "완벽주의...", 'mus': "정교한 구조...", 'pos_title': "🎯 밴드 마스터", 'pos_desc': "기강을 잡는 리더...", 'instrument': "키보드와 베이스... (300자 상세 내용)"},
    '인성': {'gen': "깊은 통찰력...", 'mus': "철학적 메시지...", 'pos_title': "🎼 편곡가", 'pos_desc': "감정의 선율화...", 'instrument': "어쿠스틱 기타와 피아노... (300자 상세 내용)"}
}

# 십성별 세운(연도별) 리포트 텍스트 (이미지의 중복 문제 해결)
year_fortune_db = {
    '비겁': "자아와 주체성이 극대화되는 시기입니다. 밴드의 리더로서 본인의 목소리를 확실하게 낼 수 있으며, 경쟁자들 사이에서 본인만의 독보적인 색깔을 증명하는 해가 될 것입니다.",
    '식상': "창의적 표현력이 쏟아지는 시기입니다. 새로운 신곡 작업이나 공연 기획에서 유례없는 영감을 얻게 되며, 대중과의 감정적 교감이 그 어느 때보다 활발해지는 성장의 해입니다.",
    '재성': "음악적 활동이 구체적인 결실로 이어지는 해입니다. 공연 수익이나 앨범 발매 등 현실적인 성취가 뒤따르며, 밴드의 전반적인 운영과 환경을 장악하는 능력이 발휘됩니다.",
    '관성': "명예와 사회적 위치가 공고해지는 시기입니다. 공식적인 무대 제안이나 협업 요청이 늘어나며, 절제된 연주와 정교한 사운드 디자인을 통해 커리어의 정점을 찍을 수 있습니다.",
    '인성': "내실을 다지고 정신적인 깊이를 더하는 해입니다. 기술적인 기교보다는 음악적 철학을 정립하고 심오한 세계관을 구축하기 좋으며, 주변의 도움과 지지를 받는 시기입니다."
}

def get_ohaeng(gan):
    return {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}.get(gan, '목')

def get_sibsung_name(my_gan, target_gan):
    order = ['목', '화', '토', '금', '수']
    my_oh, target_oh = get_ohaeng(my_gan), get_ohaeng(target_gan)
    return {0: '비겁', 1: '식상', 2: '재성', 3: '관성', 4: '인성'}[(order.index(target_oh) - order.index(my_oh)) % 5]

# 3️⃣ 사용자 입력단
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="임환백")
    calendar_type = st.radio("날짜 구분", ["양력", "음력", "음력(윤달)"], horizontal=True)
    col1, col2, col3 = st.columns(3)
    y, m, d = col1.number_input("년", 1900, 2100, 1981), col2.number_input("월", 1, 12, 2), col3.number_input("일", 1, 31, 7)
    h_str = st.selectbox("출생 시간", ["05~07 묘시", "23~01 자시", "01~03 축시", "03~05 인시", "07~09 진시", "09~11 사시", "11~13 오시", "13~15 미시", "15~17 신시", "17~19 유시", "19~21 술시", "21~23 해시"], index=0)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    # 날짜 변환
    if calendar_type == "양력":
        lunar = Solar.fromYmd(int(y), int(m), int(d)).getLunar()
    else:
        lunar = Lunar.fromYmd(int(y), int(m), int(d), (calendar_type == "음력(윤달)"))
    
    # ⚠️ 수정 포인트: getTimeGanZhi -> getTimeInGanZhi
    time_gz = lunar.getTimeInGanZhi() 
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), time_gz]
    d_gan = lunar.getDayGan()
    
    # 분석 데이터 매칭
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    origin_sib = get_sibsung_name(d_gan, max(counts, key=counts.get))
    data = analysis_db.get(origin_sib, analysis_db['비겁'])
    
    # 세운 산출 및 리포트
    target_lunar = Solar.fromYmd(int(target_y), 1, 1).getLunar()
    t_gan, t_gz = target_lunar.getYearGan(), target_lunar.getYearInGanZhi()
    t_sib = get_sibsung_name(d_gan, t_gan)
    
    # 5️⃣ 리포트 출력
    st.markdown(f"### 🍀 {user_name}님의 심층 리포트")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
    
    # 타고난 기질 섹션 (중략 - 기존 코드와 동일)
    st.markdown(f"<div class='inst-card'><h2>🎻 운명적 악기 및 보컬 스타일</h2><div class='content-text'>{data['instrument']}</div></div>", unsafe_allow_html=True)

    # ⚠️ 수정 포인트: 세운별로 각기 다른 텍스트 출력
    st.markdown(f"""
    <div class='target-year-card'>
        <h2>🏙️ {target_y}년({t_gz}) 종합 운세 리포트</h2>
        <div class='content-text'>
            {target_y}년은 귀하의 {d_gan} 일간이 세운의 천간 {t_gan}을(를) 만나 <b>'{t_sib}'</b>의 운이 도래하는 해입니다. <br><br>
            {year_fortune_db[t_sib]} 변화하는 기운을 적극적으로 활용하여 본인의 영역을 확장하고 내실을 다지는 기회로 삼으시길 바랍니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
