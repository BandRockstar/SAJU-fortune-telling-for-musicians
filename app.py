import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 원본 CSS (레이아웃 및 디자인 100% 고수)
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

# 2️⃣ 핵심 분석 엔진 (함수 최상단 배치)

def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {'申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'], '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']}
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

def get_ten_god(d_gan, t_gan):
    gan_list = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    idx_diff = (gan_list.index(t_gan) - gan_list.index(d_gan)) % 10
    ten_god_map = {0:'비견', 1:'겁재', 2:'식신', 3:'상관', 4:'편재', 5:'정재', 6:'편관', 7:'정관', 8:'편인', 9:'정인'}
    return ten_god_map.get(idx_diff)

def generate_full_report(d_gan, max_elem, name, target_y):
    # 1. 일반 통변 (사주 중심 - 300자 이상)
    gan_desc = {
        '甲': "천간의 우두머리인 갑목의 기운을 타고나 추진력과 강직함이 돋보입니다. 어떠한 시련에도 굴하지 않고 하늘을 향해 뻗어가는 거목처럼 본인의 신념이 확고하며, 리더십을 발휘하여 주변을 이끄는 힘이 강합니다.",
        '乙': "유연하면서도 끈질긴 생명력을 지닌 을목의 기운을 지녔습니다. 환경에 적응하는 능력이 탁월하며 내면의 강인함을 바탕으로 외유내강의 전형을 보여줍니다. 세밀한 분석력과 주밀한 기획력이 강점입니다.",
        '丙': "태양과 같은 정열을 지닌 병화의 기운으로 화려하고 명랑한 기질을 소유하고 있습니다. 숨김없는 솔직함과 공정한 판단력을 갖추었으며, 자신을 드러내어 세상을 밝히려는 의지가 강해 공동체의 중심 역할을 수행합니다.",
        '丁': "따뜻한 등불과 같은 정화의 기운으로 섬세하고 헌신적인 성품을 지녔습니다. 겉으로는 조용해 보일 수 있으나 내면에는 뜨거운 열정을 품고 있으며, 예의가 바르고 타인을 배려하는 마음이 깊어 덕망이 높습니다.",
        '戊': "넓은 대지와 같은 무토의 기운으로 묵직하고 포용력 있는 성정입니다. 신의를 중요하게 여기며 한 번 정한 목표는 끝까지 완수하는 책임감이 강합니다. 주변 사람들에게 든든한 버팀목이 되어주는 존재입니다.",
        '己': "만물을 키워내는 문전옥답과 같은 기토의 기운으로 주밀하고 다정한 성품입니다. 현실적인 감각이 뛰어나며 자기 관리가 철저합니다. 타인의 마음을 잘 헤아려 대인관계가 원만하며 안정적인 삶을 추구합니다.",
        '庚': "강인한 바위와 칼의 기운인 경금의 성정으로 결단력과 의리가 남다릅니다. 시비지심이 분명하여 옳고 그름을 가리는 데 주저함이 없으며, 강력한 실행력을 바탕으로 난관을 돌파하는 카리스마를 지녔습니다.",
        '辛': "세밀하게 세공된 보석과 같은 신금의 기운으로 예민하면서도 고귀한 성품입니다. 자기 기준이 엄격하고 깔끔하며, 날카로운 통찰력을 지녔습니다. 독창적인 사고방식으로 본인만의 영역을 확고히 구축합니다.",
        '壬': "깊은 바다와 같은 임수의 기운으로 지혜롭고 유연한 사고방식을 가졌습니다. 모든 것을 포용하는 넓은 도량과 앞을 내다보는 통찰력이 뛰어나며, 변화에 대처하는 능력이 능수능란하여 사회적 성취가 빠릅니다.",
        '癸': "만물을 적시는 단비와 같은 계수의 기운으로 세밀하고 명민한 두뇌를 소유하고 있습니다. 조용히 스며드는 친화력과 무궁무진한 상상력을 지녔으며, 직관력이 뛰어나 타인이 보지 못하는 이면을 읽어내는 힘이 있습니다."
    }
    elem_desc = {
        '목': "인자함과 창의성이 풍부하여 새로운 분야를 개척하는 데 두각을 나타냅니다.",
        '화': "정열적이고 사교적이며 본인의 에너지를 외부로 발산하여 대중을 압도하는 힘이 있습니다.",
        '토': "신의와 안정을 중시하며 중재자 역할과 기반을 닦는 작업에 탁월한 재능이 있습니다.",
        '금': "냉철한 판단력과 정교한 기술력을 바탕으로 완벽한 결과물을 만들어내는 힘이 있습니다.",
        '수': "지혜와 유연함으로 보이지 않는 곳에서 전략을 짜고 깊이 있는 사유를 즐깁니다."
    }
    gen_text = f"본인은 {d_gan}일간으로서 {gan_desc.get(d_gan, '')} 특히 사주 명식에 {max_elem}의 기운이 강하게 자리 잡고 있어 {elem_desc.get(max_elem, '')} {name}님은 단순히 주어진 길을 가기보다 본인의 명확한 주관을 바탕으로 인생의 경로를 개척해 나가는 힘이 남다릅니다. 이러한 기질은 조직 내에서 핵심적인 위치를 차지하게 만들며, 시간이 흐를수록 경험이 축적되어 견고한 성공의 기틀을 마련하게 될 것입니다. 자기 성찰이 깊고 원칙을 준수하려는 마음이 강해 사회적으로 신뢰받는 아티스트 혹은 리더로서의 면모를 유감없이 발휘하게 될 사주 구성입니다."

    # 2. 음악 통변 (음악 중심 - 300자 이상)
    mus_ohaeng = {
        '목': "어쿠스틱한 공간감과 서사적인 멜로디 라인이 강점입니다. 자연스러운 소리의 질감을 살리는 데 탁월하며, 곡 전체의 스토리텔링을 중시합니다.",
        '화': "폭발적인 무대 장악력과 화려한 톤이 특징입니다. 청중의 감정을 단숨에 고조시키는 강렬한 에너지를 지녔으며 하이파이한 사운드를 선호합니다.",
        '토': "사운드의 중심을 잡는 안정적인 밸런스가 돋보입니다. 전체적인 프로듀싱 능력과 악기 간의 조화를 이루는 믹싱 감각이 천부적입니다.",
        '금': "명징하고 날카로운 테크닉, 정교한 하이엔드 엔지니어링 능력을 갖췄습니다. 불필요한 소리를 걷어내고 본질적인 사운드를 찾아내는 데 능합니다.",
        '수': "몽환적이고 깊은 잔향, 무의식을 자극하는 선율이 매력입니다. 깊이 있는 사운드 디자인과 감성적인 리듬감을 통해 독보적인 아우라를 형성합니다."
    }
    mus_text = f"{name}님의 음악적 재능은 {d_gan}의 일간적 감수성과 {max_elem}의 발달된 기운이 만나 독창적인 사운드 세계를 구축합니다. {mus_ohaeng.get(max_elem, '')} 특히 악기를 다루거나 곡을 쓸 때 보여주는 집요한 완벽주의는 결과물의 완성도를 극상으로 끌어올리는 원동력이 됩니다. 남들이 발견하지 못하는 세밀한 주파수의 변화나 리듬의 미묘한 뉘앙스를 캐치하는 능력이 뛰어나며, 이는 장르를 불문하고 {name}님만의 시그니처 사운드를 대중에게 각인시키는 강력한 무기가 됩니다. 무대 위에서는 본인의 에너지를 정제하여 전달하는 힘이 있어 관객에게 깊은 예술적 카타르시스를 선사하는 천부적인 음악가입니다."

    # 3. 연도별 동적 운세 (연도별 변화 확실히 적용)
    t_lunar = Solar.fromYmd(target_y, 1, 1).getLunar()
    t_gan = t_lunar.getYearGan()
    t_ganzhi = t_lunar.getYearInGanZhi()
    ten_god = get_ten_god(d_gan, t_gan)
    
    god_desc = {
        '비견': "동료와의 협업이 활발해지고 본인의 주체성이 강해지는 시기입니다. 밴드 활동이나 공동 작업에서 중심적인 역할을 수행하게 됩니다.",
        '겁재': "강한 경쟁심과 에너지가 발동하는 해입니다. 파격적인 음악적 시도나 대담한 무대 퍼포먼스가 대중의 시선을 사로잡을 것입니다.",
        '식신': "창의적인 영감이 폭발하는 해입니다. 새로운 곡이 술술 써지고 본인만의 독특한 음악적 표현력이 극대화되는 황금기입니다.",
        '상관': "기교와 테크닉이 화려하게 빛을 발하는 시기입니다. 세련된 편곡과 실험적인 사운드 디자인으로 평단의 주목을 받게 됩니다.",
        '편재': "활동 영역이 비약적으로 넓어지고 큰 무대와 인연이 닿습니다. 비즈니스적인 성과와 예술적 명성을 동시에 거머쥘 기회가 찾아옵니다.",
        '정재': "성실한 노력의 결실이 안정적인 보상으로 이어집니다. 앨범 계약이나 고정적인 공연 활동 등 기반이 단단해지는 해입니다.",
        '편관': "강한 카리스마와 압박감이 공존하는 시기입니다. 이를 창작 에너지로 승화한다면 인생에서 가장 묵직한 명반을 탄생시킬 수 있습니다.",
        '정관': "사회적인 명예와 공신력이 높아지는 해입니다. 공신력 있는 상을 받거나 중요한 직함을 맡아 커리어의 정점에 서게 됩니다.",
        '편인': "철학적이고 신비로운 영감이 깃드는 시기입니다. 깊이 있는 가사와 실험적인 사운드로 본인만의 매니아층을 확고히 굳히게 됩니다.",
        '정인': "귀인의 도움과 학구적인 깊이가 더해지는 해입니다. 거장으로부터의 가르침이나 이론적 정립을 통해 음악적 격조가 한 단계 상승합니다."
    }
    
    y_gen = f"{target_y}년({t_ganzhi})은 {name}님에게 {ten_god}의 기운이 강력하게 작용하는 해입니다. {god_desc.get(ten_god, '')} 올해는 본인이 그동안 묵묵히 쌓아온 내공이 외부 환경과 공명하며 강력한 시너지를 내는 변곡점이 될 것입니다. 특히 중요한 결정이나 계약에 있어 운의 흐름이 본인을 적극적으로 지원하니 자신감을 갖고 추진하십시오. 사회적 입지가 굳건해지며 주변의 인정을 한 몸에 받는 보람찬 한 해가 될 것입니다."
    y_mus = f"예술가로서 {target_y}년은 {ten_god}의 기질이 본인의 선율에 투영되어 독창적인 지평을 여는 시기입니다. {t_ganzhi}의 기운은 {name}님의 창의적인 에너지를 더욱 정교하게 다듬어줄 것이며, 이 시기에 탄생하는 결과물은 평소보다 깊은 서사와 예술적 완성도를 담게 될 것입니다. 특히 대규모 라이브나 중요한 신곡 발표를 통해 아티스트로서의 이름값이 비약적으로 상승하며, 본인만의 사운드 정체성이 대중의 가슴속에 깊이 각인되는 기념비적인 해가 될 것입니다."

    return gen_text, mus_text, y_gen, y_mus

# 3️⃣ 메인 앱 로직

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", placeholder="성함을 입력하세요")
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
        gen_text, mus_text, y_gen, y_mus = generate_full_report(d_gan, max_elem, display_name, target_y)

        # 🍀 리포트 출력 (사용자 원본 디자인 유지)
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b></div>", unsafe_allow_html=True)

        # 메뉴명 토씨 하나 안 틀리게 복구
        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 메인 보컬 및 프론트맨</span>
                귀하의 명식은 무대 중심에서 에너지를 발산할 때 가장 빛납니다. 관객과의 정서적 교감을 주도하는 천부적인 자질을 갖추고 있습니다.
                <br><br>
                <span class='pos-title'>🎚️ 사운드 마스터링 및 디자인</span>
                발달된 {max_elem}의 기운은 주파수의 미묘한 차이를 읽어내고 최상의 톤을 찾아내는 엔지니어링 영역에서 독보적인 전문성을 발휘하게 합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 📅 {target_y}년 심층 운세")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ 일반 운세 흐름</h2><div class='content-text'>{y_gen}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 음악적 흐름 이야기</h2><div class='content-text'>{y_mus}</div></div>", unsafe_allow_html=True)
