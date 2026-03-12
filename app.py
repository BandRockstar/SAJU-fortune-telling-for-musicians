import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 모바일 최적화 UI 디자인
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

# 2️⃣ 입력 설정
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

# 3️⃣ 삼재 계산 함수
def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {
        '申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'],
        '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']
    }
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

# 4️⃣ 동적 심층 통변 엔진 (입력 데이터에 따라 300자 이상 생성)
def get_dynamic_report(d_gan, max_elem, name, target_y):
    # 1. 일반 운세 데이터 (오행별 300자급)
    gen_db = {
        '목': f"{name}님은 {d_gan}일간의 특성을 지니며 만물을 소생시키는 목(木)의 기운이 강하십니다. 이는 본능적으로 성장을 지향하며 어떠한 역경 속에서도 굴하지 않고 하늘로 뻗어가는 나무처럼 올곧은 신념을 의미합니다. {target_y}년에는 이러한 목의 생명력이 사회적 환경과 만나 새로운 기회를 창출하게 됩니다. 특히 주변 사람들과의 인화력을 바탕으로 본인의 아이디어가 구체적인 성과로 연결되는 시기이며, 명예를 중시하는 성품 덕분에 조직 내에서 정신적 지주 역할을 수행하게 될 것입니다. 내면의 고집을 유연함으로 승화시킨다면 인생의 후반부로 갈수록 더욱 견고한 성공의 기틀을 마련하게 될 운명입니다.",
        '화': f"{name}님은 태양처럼 뜨거운 화(火)의 정기를 타고나 자신을 외부로 드러내는 데 거침이 없는 열정적인 기질을 소유하고 계십니다. {d_gan}일간의 특성과 결합하여 매사에 직관적이고 결단력이 빠르며, 복잡한 상황 속에서도 본질을 꿰뚫어 보는 통찰력이 뛰어납니다. {target_y}년은 본인의 에너지가 만천하에 공개되는 확산의 시기입니다. 때로는 급한 성미로 인해 시행착오를 겪을 수 있으나, 특유의 불굴의 추진력과 낙천적인 사고방식은 어떤 역경도 성장의 발판으로 바꾸는 마법 같은 힘을 발휘합니다. 빛나는 카리스마로 대중을 리드하며 세상을 밝게 비추는 운명적 특징이 극대화될 것입니다.",
        '토': f"{name}님은 드넓은 대지인 토(土)의 기운을 품어 모든 것을 수용하고 갈등을 중재하는 포용력이 남다른 명식입니다. {d_gan}일간의 무게감이 더해져 언행이 신중하고 신의를 목숨처럼 중요하게 여기는 묵직한 내공을 보여줍니다. {target_y}년은 그동안 쌓아온 신뢰가 결실을 맺는 안정의 해입니다. 감정의 기복이 적고 평온함을 유지하는 성정은 주변 사람들로부터 '믿고 의지할 수 있는 기둥'이라는 평가를 이끌어낼 것입니다. 변화에 둔감하다는 오해를 받기도 하지만, 실제로는 보이지 않는 곳에서 철저하게 미래를 준비하는 주밀함을 지니고 있어 시간이 흐를수록 거대한 성취를 이루는 대기만성형의 운을 타게 됩니다.",
        '금': f"{name}님은 단단한 바위나 정제된 금속인 금(金)의 기운을 받아 날카로운 분석력과 강한 의지를 소유하고 계십니다. {d_gan}일간의 기운이 더해져 시비지심이 명확하고 매사에 완벽을 기하려는 장인 정신이 투철합니다. {target_y}년은 본인의 전문성이 가장 날카롭게 빛을 발하는 시기입니다. 겉으로는 냉철해 보이지만 한 번 마음을 준 상대에게는 변치 않는 충성심을 보여주는 외강내유형의 전형으로, 본인의 엄격한 자기 절제는 혼란스러운 상황 속에서 명확한 방향을 제시하는 나침반 역할을 하게 될 것입니다. 불필요한 장식을 걷어낸 본질적인 가치를 추구하는 자세가 사회적으로 높은 보상을 가져다줄 것입니다.",
        '수': f"{name}님은 유유히 흐르는 강물인 수(水)의 성정을 타고나 유연하고 지혜로운 통찰력을 지니고 계십니다. {d_gan}일간의 특성과 결합하여 현상의 이면에 숨겨진 흐름을 읽어내는 능력이 탁월하며, {target_y}년에는 이러한 지혜가 전략적인 성취로 이어지게 됩니다. 타인의 감정을 어루만지는 공감 능력이 뛰어나 상담가나 전략가의 면모를 보이며, 고정된 틀에 얽매이지 않는 자유로운 사유를 통해 세상의 이치를 탐구하는 성향이 강합니다. 생각이 많아 실행력이 부족할 수 있는 점을 올해의 강한 운세가 보완해주어, 본인이 창조해낸 지적인 결과물이 세상에 강한 영향력을 남기게 될 것입니다."
    }

    # 2. 음악적 운세 데이터 (오행별 300자급)
    mus_db = {
        '목': f"음악적으로 {name}님은 서사적인 선율과 따뜻한 리듬감을 조화시키는 치유의 힘을 가졌습니다. {target_y}년에는 현악기의 울림이나 어쿠스틱한 사운드에서 독보적인 영감을 얻게 될 것입니다. 단순히 소리를 나열하는 것이 아니라 곡 전체의 생명력을 중시하는 서정적 깊이는 듣는 이에게 한 편의 시를 읽는 듯한 감동을 선사합니다. 올해 발표하는 곡들은 시간이 지날수록 대중의 정서와 깊게 교감하게 될 것이며, 지친 영혼들에게 안식처를 제공하는 아티스트로서 입지를 굳히게 됩니다. 성장의 에너지가 가득한 해이므로 대작을 기획하기에 더할 나위 없이 좋은 시기입니다.",
        '화': f"{name}님의 음악은 무대 위에서 폭발하는 압도적인 카리스마와 화려한 퍼포먼스가 결합한 열정의 결정체입니다. {target_y}년의 운세는 보컬의 성량이나 연주의 색채를 더욱 화려하게 만들어줄 것입니다. 청중의 감정을 단숨에 최고조로 끌어올리는 극적인 곡 구성에 천부적인 재능을 발휘하는 시기이며, 직관적으로 사운드의 핵심 톤을 잡아내는 능력이 절정에 달합니다. 본인의 열정을 소리로 치환할 때 발생하는 에너지는 그 누구도 흉내 낼 수 없는 본인만의 '오라'를 형성하며, 라이브 현장에서 진정한 가치를 입증하게 될 기념비적인 해가 될 것입니다.",
        '토': f"{name}님의 음악적 기반은 사운드의 완벽한 밸런스와 안정적인 구조미에 있습니다. {target_y}년은 모든 소리를 하나로 아우르는 묵직한 프로듀싱 능력이 빛을 발하는 해입니다. 저음부의 무게감을 탁월하게 활용하며 복잡한 세션 속에서도 중심을 잡는 능력이 극대화됩니다. 자극적인 유행보다는 클래식하고 깊이 있는 사운드를 지향하는 본인의 철학이 올해 대중에게 '신뢰'로 다가갈 것입니다. 세월이 흘러도 변하지 않는 가치를 지닌 음악적 기둥으로서 본인의 명성을 견고하게 지탱해 줄 작품을 완성하게 될 것입니다.",
        '금': f"{name}님의 연주는 명징한 사운드와 오차 없는 정교한 테크닉이 돋보이는 고도의 미학적 성취를 보여줍니다. {target_y}년에는 불필요한 장식을 걷어낸 세련된 미니멀리즘과 하이엔드 음향 설계에서 본인만의 날카로운 개성이 발산될 것입니다. 특히 완벽주의적 속성은 믹싱과 마스터링 등 엔지니어링 작업에서 타의 추종을 불허하는 전문성으로 나타납니다. 차가운 톤 속에 숨겨진 투명한 진심은 청중의 이성을 자극하며 소리 질감에 완벽히 집중하게 만드는 강력한 흡입력을 발휘할 것이며, 이는 올해 최고의 퀄리티를 가진 명반 탄생의 밑거름이 됩니다.",
        '수': f"{name}님의 음악적 지평은 몽환적이면서도 깊은 공간감을 지닌 무의식의 영역에 닿아 있습니다. {target_y}년은 고정된 형식보다 즉흥적이고 유연한 흐름 속에서 위대한 영감을 얻는 해입니다. 보이지 않는 정서를 유려한 선율과 신비로운 사운드 텍스처로 치환하는 능력이 대단히 뛰어나며, 리버브나 딜레이를 활용한 공간 연출에서 독보적인 감각을 보여줄 것입니다. 올해는 단순히 곡을 만드는 것을 넘어 하나의 완벽한 세계관을 창조하게 되며, 지혜로운 사유가 담긴 선율은 청중의 영혼에 깊고 긴 여운을 남기게 될 것입니다."
    }

    return gen_db.get(max_elem, ""), mus_db.get(max_elem, "")

# 5️⃣ 결과 출력 로직
if submitted:
    if not (y and m and d) or h_str == "시간 선택 (또는 모름)":
        st.error("생년월일과 시간을 정확히 입력해주세요.")
    else:
        # 데이터 계산 부분 (기존과 동일)
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
        
        # [핵심] 동적 엔진 호출 (입력된 target_y 반영)
        gen_text, mus_text = get_dynamic_report(d_gan, max_elem, display_name, target_y)
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

        # UI 출력 부분
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b><br><small>삼재는 9년마다 돌아오는 3년의 조심하는 시기를 뜻합니다.</small></div>", unsafe_allow_html=True)

        # 동적으로 생성된 300자 이상의 텍스트 출력
        st.markdown(f"<div class='section-card'><h2>👤 {display_name}님의 타고난 성정과 {target_y}년 운세</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 {target_y}년 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)

        # 추천 포지션 및 성향 (이 부분도 변수를 사용하여 출력)
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎯 핵심 분석: {max_elem}의 기운을 활용한 예술적 완성</span>
                {display_name}님의 사주에서 가장 두드러지는 {max_elem}의 기운은 {target_y}년의 흐름과 만나 본인만의 독창적인 음악적 문법을 완성하게 합니다. 
                특히 {d_gan}일간의 특성을 고려할 때, 감정에만 휩쓸리지 않고 기술적으로 완벽하게 제어된 사운드를 구현할 수 있는 능력이 돋보입니다. 
                이러한 이원적 재능의 결합은 밴드의 음악적 중심을 잡는 동시에 대중적 흡인력을 극대화하는 독보적인 존재감을 형성하며, 
                {target_y}년에는 무대의 가장 밝은 곳에서 비로소 아티스트로서의 완전한 자아를 실현하게 만들 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
