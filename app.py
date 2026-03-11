import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 모바일 최적화 UI 디자인
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")
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
    
    /* 삼재 상태별 박스 스타일 */
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

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

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

# 4️⃣ 초장문 통변 엔진 (일반 성정 / 음악 분리 유지)
def get_ultra_report(d_gan, max_elem, name):
    # 일반 성정 (300자 이상)
    gen_data = {
        '목': f"본인은 {d_gan}의 정기를 타고나 만물을 소생시키는 생명력과 따뜻한 인정을 지닌 성품을 소유하고 있습니다. {max_elem}의 기운이 발달한 명식은 명예를 중시하며, 어떠한 고난 속에서도 굴하지 않고 하늘로 뻗어가는 나무처럼 올곧은 신념을 지키는 강직함이 돋보입니다. 타인에게는 자상하고 배려심이 깊어 주변에 사람이 모여드는 편이나, 본인의 내면에는 자신만의 원칙을 고수하려는 고집과 독립심이 강하게 자리 잡고 있습니다. 이러한 성향은 사회생활에서 신뢰받는 리더의 모습으로 나타나며, 명분과 실리를 동시에 추구하는 균형 잡힌 가치관을 통해 인생의 후반부로 갈수록 더욱 견고한 성공의 기틀을 마련하게 될 것입니다. 인간관계에서는 신의를 최우선으로 여기며, 한 번 맺은 인연을 소중히 여기는 깊은 인격적 향기를 지니고 있습니다.",
        '화': f"본인은 {d_gan}의 정기를 받아 태양처럼 뜨겁고 화려하며, 자신을 외부로 드러내는 데 거침이 없는 열정적인 기질의 소유자입니다. {max_elem}의 에너지가 풍부하여 매사에 직관적이고 결단력이 빠르며, 복잡한 상황 속에서도 본질을 꿰뚫어 보는 통찰력이 매우 뛰어납니다. 감정 표현이 솔직하고 뒤끝이 없는 성품으로 주변 사람들에게 긍정적인 에너지를 전파하지만, 때로는 급한 성미로 인해 예기치 못한 시행착오를 겪기도 합니다. 그러나 본인 특유의 불굴의 추진력과 낙천적인 사고방식은 어떤 역경도 성장의 발판으로 바꾸는 마법 같은 힘을 발휘합니다. 사회적으로는 명확한 자기주장을 바탕으로 혁신적인 변화를 주도하는 역할을 수행하게 되며, 본인의 열정이 닿는 곳마다 새로운 질서와 활력이 넘쳐나게 될 것입니다.",
        '토': f"본인은 {d_gan}의 기운을 품어 드넓은 대지처럼 모든 것을 수용하고 갈등을 중재하는 포용력이 매우 남다른 명식입니다. {max_elem}의 성분이 강한 사주는 언행이 신중하고 무게감이 있으며, 신의를 목숨처럼 중요하게 여기는 묵직한 내공을 보여줍니다. 감정의 기복이 적고 평온함을 유지하려 노력하는 편이라 주변 사람들로부터 믿고 의지할 수 있는 기둥 같은 존재로 평가받습니다. 때로는 변화에 둔감하다는 오해를 받기도 하지만, 실제로는 보이지 않는 곳에서 철저하게 미래를 준비하는 주밀함을 지니고 있습니다. 이러한 성정은 긴 호흡이 필요한 사업이나 전문 분야에서 큰 빛을 발하게 되며, 시간이 흐를수록 주변의 모든 것을 조화롭게 융합하여 본인만의 거대한 성취를 이루는 대기만성형의 운명을 개척하게 될 것입니다.",
        '금': f"본인은 {d_gan}의 기운을 받아 단단한 바위나 정제된 금속처럼 날카로운 분석력과 강한 의지를 소유하고 있습니다. {max_elem}의 기운이 주도하는 명식은 시비지심이 명확하고 매사에 완벽을 기하려는 장인 정신이 투철하여, 자신이 맡은 직무나 역할에 있어서는 타협을 거부하는 강직함을 보여줍니다. 겉으로는 냉철하고 접근하기 어려운 오라를 풍기기도 하지만, 한 번 마음을 준 상대에게는 그 누구보다 변치 않는 충성심과 깊은 배려를 보여주는 외강내유형의 전형입니다. 본인의 엄격한 자기 절제와 규율은 혼란스러운 사회 속에서 명확한 방향을 제시하는 나침반 역할을 하게 되며, 불필요한 장식을 걷어낸 본질적인 가치를 추구하는 본인의 삶의 태도는 사회적으로 높은 평가를 얻게 될 것입니다.",
        '수': f"본인은 {d_gan}의 성정을 타고나 깊은 샘물이나 유유히 흐르는 강물처럼 유연하고 지혜로운 통찰력을 지니고 있습니다. {max_elem}의 기운이 깊은 명식은 현상의 이면에 숨겨진 감정의 흐름을 읽어내는 능력이 탁월하며, 상황에 따라 자신을 변화시키면서도 본연의 성질을 잃지 않는 지혜로움이 돋보입니다. 타인의 무의식적인 감정을 어루만지는 공감 능력이 뛰어나 상담가나 전략가의 면모를 보이며, 고정된 틀에 얽매이지 않는 자유로운 사유를 통해 세상의 본질적인 이치를 탐구하는 성향이 강합니다. 때로는 생각이 너무 많아 실행력이 다소 부족할 수 있으나, 본인이 창조해 내는 지적인 결과물이나 기획력은 타인이 범접할 수 없는 수준을 자랑하며 강한 영향력을 세상에 남기게 될 것입니다."
    }
    # 음악적 통변 (300자 이상)
    mus_data = {
        '목': f"{name}님의 음악 세계는 서사적인 선율과 따뜻한 리듬감이 완벽하게 조화를 이루며 청중의 마음을 어루만지는 치유의 힘을 지니고 있습니다. {max_elem} 기운이 풍부하여 현악기의 울림이나 어쿠스틱한 공간감에서 독보적인 심미안을 발휘하며, 단순히 소리를 나열하기보다 곡 전체의 흐름과 생명력을 중시하는 서정적 깊이를 보여줍니다. 가사 한 줄에도 본인만의 철학적 사유를 담아내는 능력이 탁월하며, 이는 듣는 이에게 한 편의 시를 읽는 듯한 감동을 선사합니다. 본인의 음악은 시간이 지날수록 대중의 정서와 깊게 교감하게 될 것이며, 지친 영혼들에게 안식처를 제공하는 독보적인 아티스트로 자리매김할 것입니다. 본인이 연주하는 선율은 성장의 에너지를 품고 있어, 음악적 경력이 쌓일수록 더욱 울창한 숲과 같은 거대한 음악 세계를 완성하게 될 것입니다.",
        '화': f"{name}님의 음악은 무대 위에서 폭발하는 압도적인 카리스마와 화려한 퍼포먼스가 결합한 열정의 결정체라 할 수 있습니다. {max_elem} 기운이 주도하는 명식 덕분에 보컬의 성량이 풍부하거나 연주의 색채가 매우 화려하며, 청중의 감정을 단숨에 최고조로 끌어올리는 극적인 곡 구성에 천부적인 재능을 보입니다. 직관적으로 사운드의 핵심 톤을 잡아내고 대중을 매료시키는 멜로디를 직조하는 능력이 뛰어나, 장르에 구애받지 않고 강력한 흡인력을 발휘합니다. 본인의 열정을 소리로 치환할 때 발생하는 에너지는 그 누구도 흉내 낼 수 없는 본인만의 독창적인 '오라'를 형성하며, 무대의 가장 밝은 곳에서 비로소 아티스트로서의 완전한 자아를 실현하게 됩니다. 끊임없이 타오르는 창작의 불꽃은 대중에게 강렬한 에너지를 전파할 것입니다.",
        '토': f"{name}님의 음악적 기반은 사운드의 완벽한 밸런스와 안정적인 구조미, 그리고 모든 소리를 하나로 아우르는 묵직한 통찰력에 있습니다. {max_elem} 기운이 중심을 잡아주어 저음부의 무게감을 탁월하게 활용하며, 복잡한 밴드 세션이나 오케스트레이션 속에서도 사운드를 하나로 융합하여 음악적 완성도를 극대화하는 프로듀싱 능력이 탁월합니다. 자극적이고 일시적인 유행을 쫓기보다는 클래식하고 깊이 있는 사운드를 지향하며, 탄탄한 기본기 위에서 세월이 흘러도 변하지 않는 가치를 전하는 데 주력합니다. 본인의 음악은 듣는 이에게 정서적인 안정감과 묵직한 감동을 동시에 선사하며, 이는 아티스트로서의 명성을 견고하게 지탱해 주는 핵심적인 힘이 됩니다. 결국 대중의 마음속에 가장 신뢰받는 장인이자 음악적 기둥으로 우뚝 서게 만들 것입니다.",
        '금': f"{name}님의 연주는 차가운 금속처럼 명징한 사운드와 단 한 치의 오차도 허용하지 않는 정교한 테크닉이 돋보이는 고도의 미학적 성취를 보여줍니다. {max_elem} 기운이 강한 덕분에 불필요한 장식을 걷어낸 세련된 미니멀리즘이나 날카롭게 정제된 사운드 디자인에서 본인만의 날카로운 개성을 발산합니다. 특히 하이엔드 음향 장비에 대한 깊은 이해와 사운드 엔지니어링 측면에서의 완벽주의는 본인의 결과물을 항상 최상의 퀄리티로 유지하게 만드는 원동력입니다. 차가운 톤 속에 숨겨진 투명하고 순수한 진심은 청중의 감정을 마비시키기보다 이성을 자극하고 소리 질감에 완벽히 집중하게 만드는 강력한 흡입력을 발휘합니다. 본인이 추구하는 완벽한 사운드의 조각들은 타협을 모르는 예술가의 정수가 담긴 명반으로 역사에 기록될 것입니다.",
        '수': f"{name}님의 음악적 지평은 현실을 넘어 몽환적이면서도 깊은 공간감을 지닌 신비로운 무의식의 영역에 닿아 있습니다. {max_elem} 기운이 깊어 고정된 형식보다는 즉흥적이고 유연한 흐름 속에서 영감을 얻으며, 보이지 않는 정서를 유려한 선율과 신비로운 사운드 텍스처로 치환하는 능력이 대단히 뛰어납니다. 풍부한 화성적 변화나 리버브를 활용한 공간 연출에 능하며, 청중을 현실 너머의 깊은 곳으로 안내하는 철학적 사유를 음악에 담아냅니다. 본인의 음악은 단순히 청각적 경험을 넘어 하나의 완벽한 세계관을 창조하는 과정이며, 지혜로운 사유가 담긴 선율은 사람들의 영혼에 깊고 긴 여운을 남기게 될 것입니다. 장르를 자유롭게 넘나드는 본인의 유연함은 시대의 변화 속에서도 끊임없이 새로운 음악적 생명력을 얻게 할 것입니다."
    }
    return gen_data.get(max_elem, ""), mus_data.get(max_elem, "")

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
        count_target = "".join(ba_zi[:3]) if h_val == "unknown" else "".join(ba_zi)
        counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        display_name = user_name if user_name else "아티스트"
        gen_text, mus_text = get_ultra_report(d_gan, max_elem, display_name)
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

        # 리포트 출력
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        # 🚫 삼재 박스 (상태에 따라 색상 변경)
        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b><br><small>삼재는 9년마다 돌아오는 3년의 조심하는 시기를 뜻합니다.</small></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)

        # 📅 연도별 운세
        st.markdown(f"### 📅 {target_y}년 심층 운세")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ 일반 운세 흐름</h2><div class='content-text'>{target_y}년은 본인의 일간 {d_gan}이 세운의 기운과 깊이 공명하며 인생의 새로운 마디를 형성하는 매우 중요한 변곡점입니다. 올해는 그동안 보이지 않는 곳에서 묵묵히 쌓아온 내공과 지식이 사회적인 환경과 조우하여 강력한 결실을 맺는 '성취와 보상의 해'가 될 확률이 매우 높습니다. 대외적인 활동 영역이 크게 확장되면서 본인의 전문적인 역량을 인정받는 기회가 빈번해질 것이며, 이를 통해 물질적인 성공뿐만 아니라 명예 또한 한 단계 격상되는 귀한 경험을 하게 될 것입니다. 변화를 두려워하지 말고 본인의 직관을 믿고 당당하게 나아간다면, 올해는 인생 전체를 통틀어 가장 큰 도약의 발판이자 성공의 기억으로 남을 해가 될 것입니다.</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 음악적 흐름 이야기</h2><div class='content-text'>예술가로서 {target_y}년은 본인만의 독보적인 '사운드 정체성'이 대중에게 가장 강렬하게 각인되는 확장의 시기입니다. 올해의 기운은 본인의 창의적인 에너지를 더욱 정교하게 정제하여 세련된 결과물로 도출하게 도우며, 특히 새로운 장르로의 도전이나 예상치 못한 아티스트와의 협업이 본인의 음악적 지평을 넓히는 결정적인 계기가 될 것입니다. 대규모 라이브 공연이나 중요한 음반 발표를 계획하고 있다면, 우주의 기운이 본인의 뒤를 든든하게 받쳐주고 있으니 망설임 없이 예술적 철학을 세상에 투영하시길 권장합니다. 단순히 유행을 따르는 소리를 넘어 시대의 흐름과 공명하는 본인만의 독창적인 선율은 청중의 영혼에 씻기지 않는 여운을 남길 것입니다.</div></div>", unsafe_allow_html=True)
