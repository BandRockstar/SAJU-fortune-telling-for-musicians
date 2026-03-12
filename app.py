import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 CSS (레이아웃 틀 100% 보존)
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

# 2️⃣ [에러 해결] 필수 함수 정의 (최상단 배치)

def get_samjae_status(year_ganzhi, target_year):
    """삼재 여부를 판단하는 함수"""
    zodiac = year_ganzhi[-1]
    samjae_map = {'申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'], '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']}
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    # 타겟 연도의 띠 추출
    target_lunar = Solar.fromYmd(target_year, 1, 1).getLunar()
    target_zodiac = target_lunar.getYearInGanZhi()[-1]
    
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

def get_ten_god_info(d_gan, target_y):
    """일간과 연도 천간의 관계(십신)를 계산하는 함수"""
    target_lunar = Solar.fromYmd(target_y, 1, 1).getLunar()
    t_gan = target_lunar.getYearGan()
    gan_list = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    try:
        idx_diff = (gan_list.index(t_gan) - gan_list.index(d_gan)) % 10
        fortune_db = {
            0: ("비견(比肩)", "동료와의 협업과 주체성이 강해지는 시기입니다. 밴드 활동이나 공동 작업에서 본인의 목소리가 커지며 자신감이 넘칩니다."),
            1: ("겁재(劫財)", "경쟁심이 고취되고 에너지의 소모가 큽니다. 강렬한 록 사운드나 에너지를 발산하는 무대에 유리한 운입니다."),
            2: ("식신(食神)", "창의성이 폭발하며 새로운 곡이 술술 써지는 해입니다. 본인만의 독창적인 사운드를 구축하기 가장 좋은 때입니다."),
            3: ("상관(傷官)", "기교와 테크닉이 화려해지는 시기입니다. 대중의 시선을 사로잡는 퍼포먼스와 파격적인 시도가 성공을 거둡니다."),
            4: ("편재(偏財)", "활동 영역이 넓어집니다. 큰 무대나 프로젝트 기회가 찾아오며 비즈니스적으로 큰 성취가 따르는 해입니다."),
            5: ("정재(正財)", "노력의 결과가 안정적인 보상으로 돌아옵니다. 고정적인 공연 수입이나 앨범 계약 등 안정이 따릅니다."),
            6: ("편관(偏官)", "강한 압박감이 오지만 이를 예술적 에너지로 승화하면 명반이 탄생합니다. 카리스마가 극대화됩니다."),
            7: ("정관(正관)", "사회적 명예가 오르고 공신력 있는 기관과 인연이 닿습니다. 상을 받거나 공식적인 직함이 생길 수 있습니다."),
            8: ("편인(偏印)", "독특하고 신비로운 예술적 영감이 깃듭니다. 실험적인 음악이나 깊은 사운드에 몰입하게 됩니다."),
            9: ("정인(正印)", "귀인의 도움과 학습의 운입니다. 대가로부터 가르침을 받거나 음악적 이론이 정립되는 시기입니다.")
        }
        return fortune_db.get(idx_diff, ("운세", "새로운 여정이 시작됩니다."))
    except:
        return ("운세", "평온한 흐름이 예상됩니다.")

def get_dynamic_report(d_gan, max_elem, name, target_y):
    """연도별로 다른 통변 문구를 생성하는 함수"""
    ten_god, god_desc = get_ten_god_info(d_gan, target_y)
    t_lunar = Solar.fromYmd(target_y, 1, 1).getLunar()
    t_ganzhi = t_lunar.getYearInGanZhi()
    
    gen_text = f"본인은 {d_gan}의 정기를 타고나 예술적 고집과 정교한 기술력을 동시에 갖춘 명식입니다. {max_elem}의 기운이 발달하여 디테일한 부분까지 집요하게 파고드는 완벽주의가 돋보이며, {name}님만의 원칙을 고수할 때 비로소 큰 성취를 맛보는 구조입니다. 주변과 소통하며 본인의 재능을 현실화할 때 독보적인 위치에 오르게 될 것입니다."
    mus_text = f"{name}님의 음악 세계는 {max_elem} 기운의 명징함과 {d_gan} 특유의 감성이 어우러진 결과물입니다. 사운드 마스터링과 편곡에 있어 타협하지 않는 퀄리티를 추구하며, 대중에게 신뢰감을 주는 시그니처 사운드를 완성해 나가는 과정이 매우 인상적입니다."
    year_gen = f"{target_y}년({t_ganzhi})은 {name}님에게 {ten_god}의 기운이 강하게 작용하는 해입니다. {god_desc} 올해는 묵묵히 쌓아온 내공이 사회적인 환경과 만나 강력한 결실을 맺는 시기이니 자신감 있게 추진하십시오."
    year_mus = f"예술가로서 {target_y}년은 본인의 음악적 정체성이 {ten_god}의 특성과 결합하여 대중에게 가장 강렬하게 각인되는 시기입니다. 이 시기에 제작되는 음악은 평소보다 깊은 서사를 담아낼 것이며, 중요한 발표를 통해 아티스트로서의 커리어에 큰 마디를 형성하게 될 것입니다."
    
    return gen_text, mus_text, year_gen, year_mus

# 3️⃣ 메인 UI 및 로직
st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

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
        
        display_name = user_name if user_name else "아티스트"
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)
        gen_text, mus_text, y_gen, y_mus = get_dynamic_report(d_gan, max_elem, display_name, target_y)

        # UI 출력 (레이아웃 보존)
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)

        st.markdown(f"### 📅 {target_y}년 심층 운세")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ 일반 운세 흐름</h2><div class='content-text'>{y_gen}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 음악적 흐름 이야기</h2><div class='content-text'>{y_mus}</div></div>", unsafe_allow_html=True)
