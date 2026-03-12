import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 CSS (사용자님이 주신 HTML 레이아웃 100% 고수)
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

# 2️⃣ 입력 설정 (기존 입력창 구성 유지)
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

# 3️⃣ [핵심] 연도별 십신 및 음악적 운세 동적 생성 함수
def get_dynamic_fortune(d_gan, target_y, name):
    # 대상 연도의 천간 추출
    target_lunar = Solar.fromYmd(target_y, 1, 1).getLunar()
    t_gan = target_lunar.getYearGan()
    t_ganzhi = target_lunar.getYearInGanZhi()
    
    gan_list = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    idx_diff = (gan_list.index(t_gan) - gan_list.index(d_gan)) % 10
    
    # 연도별 십신 관계에 따른 장문 통변 데이터베이스
    fortune_db = {
        0: ("비견(比肩)", "동료들과의 강한 유대감이 형성되는 시기입니다. 밴드 내에서 본인의 영향력이 커지며, 주관이 뚜렷한 사운드를 세상에 내놓게 됩니다."),
        1: ("겁재(劫財)", "경쟁적 에너지가 폭발하여 파격적인 시도가 돋보이는 해입니다. 라이브 무대에서 압도적인 카리스마를 발산할 수 있는 절호의 시기입니다."),
        2: ("식신(食神)", "창조적인 영감이 샘솟는 해로, 본인만의 독창적인 곡을 쓰기에 최적입니다. 사운드의 질감이 풍성해지고 음악적 즐거움이 극대화됩니다."),
        3: ("상관(傷官)", "기교와 테크닉이 화려해지는 시기입니다. 대중의 시선을 사로잡는 세련된 편곡과 실험적인 사운드 디자인이 빛을 발하게 됩니다."),
        4: ("편재(偏財)", "활동 영역이 비약적으로 확장됩니다. 대규모 공연 기회나 예상치 못한 음반 계약 등 비즈니스적으로 큰 성취가 따르는 해입니다."),
        5: ("정재(정재)", "노력해온 결실이 안정적인 수익과 명예로 돌아오는 해입니다. 앨범의 완성도가 높아지며 꾸준한 팬덤의 지지를 확보하게 됩니다."),
        6: ("편관(偏官)", "강한 책임감과 압박이 따르지만, 이를 예술적 투지로 승화시키면 본인의 커리어에서 가장 묵직하고 깊이 있는 명반이 탄생합니다."),
        7: ("정관(正官)", "사회적 인정과 명예가 따르는 시기입니다. 공신력 있는 상을 받거나 대형 레이블과의 협업 등 공식적인 성과가 뚜렷해집니다."),
        8: ("편인(偏印)", "무의식을 자극하는 독특한 예술성이 깃듭니다. 철학적 깊이가 담긴 가사와 신비로운 사운드로 매니아층을 열광시킬 수 있습니다."),
        9: ("정인(正印)", "귀인의 도움과 학구적인 깊이가 더해집니다. 음악적 이론이 정립되고 거장으로부터의 영감을 통해 한 단계 도약하는 시기입니다.")
    }
    
    rel_name, rel_desc = fortune_db.get(idx_diff, ("운세", "평온한 흐름이 예상됩니다."))
    
    gen_text = f"{target_y}년({t_ganzhi})은 {name}님에게 {rel_name}의 기운이 머무는 해입니다. {rel_desc} 특히 올해는 본인의 잠재력이 외부의 환경과 맞물려 강력한 시너지를 내는 시기로, 망설였던 프로젝트를 과감하게 실행에 옮길 때 우주의 기운이 본인을 지원할 것입니다."
    mus_text = f"음악적으로 {target_y}년은 {rel_name}의 특성이 선율과 리듬에 깊게 투영됩니다. 올해 제작되는 사운드는 평소보다 더욱 선명한 목적 의식을 갖게 되며, 특히 대중과의 소통 방식에 있어 {name}님만의 독보적인 정체성이 가장 강력하게 각인되는 기념비적인 해가 될 것입니다."
    
    return gen_text, mus_text

# 4️⃣ 타고난 성정과 음악 통변 생성 함수
def get_natal_report(d_gan, max_elem, name):
    # (내용 생략 없이 풍성하게 구성 - 기존 로직 고도화)
    gen_text = f"본인은 {d_gan}의 정기를 타고나 만물을 아우르는 깊은 내면과 예술적 통찰력을 지닌 성품을 소유하고 있습니다. {max_elem}의 기운이 풍부한 명식은 한 분야에서 장인의 경지에 오르는 집중력이 돋보이며, {name}님만의 원칙을 고수하는 강직함은 시간이 흐를수록 주변의 신뢰를 얻는 근간이 됩니다. 인생의 중반부로 접어들수록 본인의 지혜가 세상과 공명하여 견고한 성공의 기틀을 마련하게 될 것입니다."
    mus_text = f"{name}님의 음악 세계는 {max_elem}의 명징함과 {d_gan}의 감수성이 조화롭게 어우러진 결정체입니다. 특히 사운드 엔지니어링과 작법에 있어 타협하지 않는 완벽주의는 본인의 창작물을 하이엔드 퀄리티로 유지하게 만드는 핵심 원동력입니다. 단순히 유행을 쫓기보다 시대의 흐름을 관통하는 본인만의 시그니처 사운드는 청중에게 깊은 여운을 남기게 될 것입니다."
    return gen_text, mus_text

# 5️⃣ 결과 출력부 (레이아웃 및 메뉴 순서 절대 보존)
if submitted:
    if not (y and m and d) or h_str == "시간 선택 (또는 모름)":
        st.error("생년월일과 시간을 정확히 입력해주세요.")
    else:
        h_val = hour_time_map[h_str]
        calc_h = 12 if h_val == "unknown" else h_val
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), (int(m) * -1) if is_leap else int(m), int(d), calc_h, 0, 0)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
        d_gan = lunar.getDayGan()
        
        # 오행 카운트 로직
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        count_target = "".join(ba_zi[:3]) if h_val == "unknown" else "".join(ba_zi)
        counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        display_name = user_name if user_name else "아티스트"
        gen_text, mus_text = get_natal_report(d_gan, max_elem, display_name)
        year_gen, year_mus = get_dynamic_fortune(d_gan, target_y, display_name)
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y) # (기존 함수 동일)

        # UI 출력 시작
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)

        # ✨ 추천 음악 포지션 (고정된 텍스트 대신 세션 유지)
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 리드 보컬 및 메인 아티스트</span>
                귀하의 명식은 무대 중심에서 에너지를 발산할 때 가장 큰 빛을 발합니다. {d_gan}의 기운을 담아 소리를 전달하는 능력은 독보적입니다.
                <br><br>
                <span class='pos-title'>🎚️ 사운드 마스터링 및 디자인</span>
                {max_elem}의 기운이 주는 정밀함은 곡의 밸런스를 잡고 하이엔드 사운드를 창조하는 엔지니어링 영역에서 최고의 실력을 발휘하게 합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 📅 [가장 중요한 부분] 연도별 동적 운세 출력
        st.markdown(f"### 📅 {target_y}년 심층 운세")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ 일반 운세 흐름</h2><div class='content-text'>{year_gen}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 음악적 흐름 이야기</h2><div class='content-text'>{year_mus}</div></div>", unsafe_allow_html=True)
