import streamlit as st
from lunar_python import Solar, Lunar
import random

# 1️⃣ 페이지 설정 및 모바일 최적화 UI 디자인 (반응형 유지)
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    html { font-size: 14px; }
    @media (min-width: 600px) { html { font-size: 16px; } }

    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card, .samjae-card { 
        padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
    }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 8px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    .samjae-card { background-color: #FEF2F2; border-left: 8px solid #EF4444; }

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

# 2️⃣ 입력 설정 (년-월-일-시 순서 유지)
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

# 3️⃣ 삼재 계산 로직
def get_samjae_info(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {
        '申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'],
        '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']
    }
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다. ", True
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다. ", False

# 4️⃣ 300자 이상 초장문 통변 생성 함수
def get_ultra_report(d_gan, max_elem, name):
    # 일반 성정 (300자 이상)
    gen_data = {
        '목': f"본인은 {d_gan}의 정기를 품고 태어나 만물을 소생시키는 생명력과 서정적 감수성이 조화롭게 어우러진 예술가입니다. {max_elem}의 기운이 발달한 명식은 온화하고 자애로운 성품을 지니고 있으면서도, 내면에는 거친 비바람을 견디며 하늘로 뻗어 나가는 나무처럼 강인한 생명력과 꺾이지 않는 신념이 자리 잡고 있습니다. 타인과의 관계에서는 따뜻한 포용력으로 주변을 아우르지만, 자신이 정한 예술적 가치관이나 도덕적 기준에 있어서는 타협을 거부하는 강직함을 동시에 보여줍니다. 이러한 성정은 단순한 창작 활동을 넘어 주변 사람들에게 긍정적인 삶의 동기를 부여하는 지도자적 영감으로 발현될 것입니다. 시간이 흐를수록 본인의 내면세계는 더욱 깊어질 것이며, 이는 세상을 향한 독보적인 메시지를 지닌 인격적 완성으로 이어져 많은 이들의 존경과 신뢰를 받는 아티스트로 거듭나게 될 것입니다.",
        '화': f"본인은 {d_gan}의 에너지를 지녀 태양처럼 뜨거운 열정과 자신을 세상에 화려하게 드러내는 발산의 기운이 매우 강한 명식입니다. {max_elem}의 기운이 풍부한 덕분에 사물의 본질을 단숨에 꿰뚫어 보는 직관력이 매우 뛰어나며, 상황 판단이 빠르고 화려한 표현력으로 대중의 시선을 사로잡는 카리스마가 돋보입니다. 새로운 환경에 대한 적응력이 뛰어나고 실패를 두려워하지 않는 추진력은 남들이 감히 시도하지 못하는 창의적인 영역에서 큰 성취를 이뤄내는 핵심 엔진이 됩니다. 때로는 감정의 기복이 강하게 나타날 수 있으나, 이러한 뜨거운 에너지를 예술적 창작으로 승화시킬 때 비로소 진정한 내면의 평화와 삶의 희열을 느끼게 될 것입니다. 본인이 가진 그 열정은 주변 사람들의 차가운 마음을 녹이고 세상에 밝은 빛을 전하는 아티스트로서의 천명을 완수하는 힘이 될 것입니다.",
        '토': f"본인은 {d_gan}의 기운을 품어 드넓은 대지처럼 모든 것을 수용하고 조화롭게 융합하는 듬직한 포용력과 신중함을 지니고 있습니다. {max_elem}의 성분이 강한 명식은 매사에 정직하고 신의가 두터우며, 안정적인 토대 위에서 서서히 성과를 쌓아가는 만성형의 기질이 뚜렷하게 나타납니다. 급격한 변화보다는 지속 가능한 성장을 추구하며, 주변 사람들의 갈등을 조율하고 전체의 균형을 잡는 능력이 탁월하여 어떤 조직에서든 없어서는 안 될 든든한 기둥 같은 존재가 됩니다. 이러한 묵직한 내공은 당장의 화려함보다는 시간이 흐를수록 깊어지는 진국 같은 매력으로 발현되며, 많은 이들이 본인의 말과 행동에서 정신적인 위안과 신뢰를 얻게 될 것입니다. 본인이 구축한 견고한 예술적 토대는 흔들리지 않는 뿌리가 되어, 세월이 흘러도 변치 않는 가치를 지닌 묵직한 작품 세계를 완성하는 밑거름이 될 것입니다.",
        '금': f"본인은 {d_gan}의 정기를 받아 차가운 금속처럼 예리한 분석력과 완벽을 기하는 장인 정신을 소유한 명식입니다. {max_elem}의 기운이 주도하는 사주는 시비지심이 명확하고 불의와 타협하지 않는 강직함이 돋보이며, 자신이 맡은 일에 대해서는 끝까지 책임을 지는 결벽에 가까운 성실함을 보여줍니다. 겉으로는 냉철하고 이성적으로 보일 수 있으나 내면에는 그 누구보다 뜨거운 정의감과 순수한 열정이 자리 잡고 있습니다. 본인만의 엄격한 기준을 예술이나 전문 분야에 투영한다면, 그 누구도 넘볼 수 없는 최고 수준의 완성과 미학적 경지에 도달하여 사회적 존경을 한 몸에 받게 될 운명입니다. 이러한 절제된 기운은 혼란스러운 세상 속에서 질서를 부여하고 본질적인 가치를 찾아내는 탁월한 능력이 되며, 이는 아티스트로서 본인만의 명확한 색채를 지탱하는 강력한 무기가 될 것입니다.",
        '수': f"본인은 {d_gan}의 성정을 타고나 깊은 바다와 같이 유연하고 지혜로우며, 현상의 이면에 숨겨진 감정의 흐름을 읽어내는 통찰력이 매우 남다른 명식입니다. {max_elem}의 기운이 깊은 사주는 겉으로 드러나는 일시적인 현상보다는 그 본질적인 가치와 무의식의 세계에 집중하며, 타인의 아픔을 어루만지는 공감 능력이 매우 뛰어납니다. 고정된 형식이나 사회적 통념에 얽매이지 않는 자유로운 사고를 지향하며, 때로는 명상적이고 철학적인 면모를 보여주어 주변에 신비로운 분위기를 자아내기도 합니다. 이러한 깊은 사유와 유연함은 사람들의 영혼을 건드리는 고차원적인 창작이나 전략적인 기획력으로 연결되어 세상에 깊고 긴 여운을 남기는 성과를 남기게 될 것입니다. 본인이 창조하는 예술은 단순히 듣고 보는 것을 넘어, 사람들을 무의식의 깊은 바다로 안내하여 내면의 진실을 마주하게 하는 고귀한 치유의 과정이 될 것입니다."
    }
    
    # 음악적 통변 (300자 이상)
    mus_data = {
        '목': f"{name}님의 음악 세계는 서사적인 선율과 자연의 생동감이 완벽하게 조화를 이루며 청중의 마음을 어루만지는 따뜻한 치유의 힘을 지니고 있습니다. {max_elem} 기운이 풍부하여 현악기의 울림이나 어쿠스틱한 공간감에서 독보적인 심미안을 발휘하며, 단순히 소리를 나열하기보다 곡 전체의 흐름과 생명력을 중시하는 서정적 깊이를 보여줍니다. 가사 한 줄에도 본인만의 철학적 사유를 담아내는 능력이 탁월하며, 이는 듣는 이에게 한 편의 시를 읽는 듯한 감동을 선사합니다. 본인의 음악은 시간이 지날수록 대중의 정서와 깊게 교감하게 될 것이며, 지친 영혼들에게 안식처를 제공하는 독보적인 아티스트로 자리매김할 것입니다. 본인이 연주하는 선율은 성장의 에너지를 품고 있어, 음악적 경력이 쌓일수록 더욱 울창한 숲과 같은 거대한 음악 세계를 완성하게 될 것이며 이는 후대 음악인들에게도 큰 영감을 주는 자산이 될 것입니다.",
        '화': f"{name}님의 음악은 무대 위에서 폭발하는 압도적인 카리스마와 화려한 퍼포먼스가 결합한 열정의 결정체라 할 수 있습니다. {max_elem} 기운이 주도하는 명식 덕분에 보컬의 성량이 풍부하거나 연주의 색채가 매우 화려하며, 청중의 감정을 단숨에 최고조로 끌어올리는 극적인 곡 구성에 천부적인 재능을 보입니다. 직관적으로 사운드의 핵심 톤을 잡아내고 대중을 매료시키는 멜로디를 직조하는 능력이 뛰어나, 장르에 구애받지 않고 강력한 흡인력을 발휘합니다. 본인의 열정을 소리로 치환할 때 발생하는 에너지는 그 누구도 흉내 낼 수 없는 본인만의 독창적인 '오라'를 형성하며, 무대의 가장 밝은 곳에서 비로소 아티스트로서의 완전한 자아를 실현하게 됩니다. 끊임없이 타오르는 창작의 불꽃은 대중에게 강렬한 에너지를 전파하며, 시대의 감성을 이끄는 트렌드세터이자 무대의 지배자로서 오래도록 기억될 강력한 사운드적 족적을 남기게 될 것입니다.",
        '토': f"{name}님의 음악적 기반은 사운드의 완벽한 밸런스와 안정적인 구조미, 그리고 모든 소리를 하나로 아우르는 묵직한 통찰력에 있습니다. {max_elem} 기운이 중심을 잡아주어 저음부의 무게감을 탁월하게 활용하며, 복잡한 밴드 세션이나 오케스트레이션 속에서도 사운드를 하나로 융합하여 음악적 완성도를 극대화하는 프로듀싱 능력이 탁월합니다. 자극적이고 일시적인 유행을 쫓기보다는 클래식하고 깊이 있는 사운드를 지향하며, 탄탄한 기본기 위에서 세월이 흘러도 변하지 않는 가치를 전하는 데 주력합니다. 본인의 음악은 듣는 이에게 정서적인 안정감과 묵직한 감동을 동시에 선사하며, 이는 아티스트로서의 명성을 견고하게 지탱해 주는 핵심적인 힘이 됩니다. 소리 사이의 빈 공간까지도 본인의 의도로 채워 넣는 신중함은 곡의 전체적인 품격을 높여주며, 결국 대중의 마음속에 가장 신뢰받는 장인이자 음악적 기둥으로 우뚝 서게 만들 것입니다.",
        '금': f"{name}님의 연주는 차가운 금속처럼 명징한 사운드와 단 한 치의 오차도 허용하지 않는 정교한 테크닉이 돋보이는 고도의 미학적 성취를 보여줍니다. {max_elem} 기운이 강한 덕분에 불필요한 장식을 걷어낸 세련된 미니멀리즘이나 날카롭게 정제된 사운드 디자인에서 본인만의 날카로운 개성을 발산합니다. 특히 하이엔드 음향 장비에 대한 깊은 이해와 사운드 엔지니어링 측면에서의 완벽주의는 본인의 결과물을 항상 최상의 퀄리티로 유지하게 만드는 원동력입니다. 차가운 톤 속에 숨겨진 투명하고 순수한 진심은 청중의 감정을 마비시키기보다 이성을 자극하고 소리 자체의 질감에 완벽히 집중하게 만드는 강력한 흡입력을 발휘합니다. 본인이 추구하는 완벽한 사운드의 조각들은 시간이 흐를수록 하나의 거대한 금속 조형물처럼 단단하게 완성될 것이며, 이는 타협을 모르는 예술가의 정수가 담긴 명반으로 역사에 기록될 수준 높은 음악적 성취가 될 것입니다.",
        '수': f"{name}님의 음악적 지평은 현실을 넘어 몽환적이면서도 깊은 공간감을 지닌 신비로운 무의식의 영역에 닿아 있습니다. {max_elem} 기운이 깊어 고정된 형식보다는 즉흥적이고 유연한 흐름 속에서 영감을 얻으며, 보이지 않는 정서를 유려한 선율과 신비로운 사운드 텍스처로 치환하는 능력이 대단히 뛰어납니다. 풍부한 화성적 변화나 리버브를 활용한 공간 연출에 능하며, 청중을 현실 너머의 깊은 곳으로 안내하는 철학적 사유를 음악에 담아냅니다. 본인의 음악은 단순한 청각적 경험을 넘어 하나의 완벽한 세계관을 창조하는 과정이며, 지혜로운 사유가 담긴 선율은 사람들의 영혼에 깊고 긴 여운을 남기게 될 것입니다. 변화무쌍한 물의 흐름처럼 장르를 자유롭게 넘나드는 본인의 유연함은 시대의 변화 속에서도 도태되지 않고 끊임없이 새로운 음악적 생명력을 얻게 할 것이며, 결국 세상의 모든 감정을 하나로 연결하는 깊고 푸른 예술의 바다를 완성하게 될 것입니다."
    }
    return gen_data.get(max_elem, ""), mus_data.get(max_elem, "")

def get_refined_position(d_gan):
    positions = {
        '丙丁': ("🎤 리드 보컬 & 프런트맨 (Frontman)", "화(火)의 기운은 발산과 확장의 에너지입니다. 무대 중앙에서 목소리로 대중의 시선과 감정을 장악하는 카리스마를 상징하며, 본인의 정체성을 가장 직접적으로 투영할 수 있는 포지션입니다."),
        '甲乙': ("🎸 리드 기타리스트 (Lead Guitar)", "목(木)의 기운은 선율과 유연성을 상징합니다. 곡의 서사를 이끄는 멜로디 라인을 직조하고, 정교한 핑거링과 섬세한 톤 변화로 곡의 온도를 결정하는 핵심 연주자입니다."),
        '庚辛': ("🥁 드러머 (Percussionist)", "금(金)의 기운은 명확한 타격과 정확한 분별을 뜻합니다. 밴드의 심장박동과 같은 리듬을 일정한 간격으로 유지하며 단단한 금속성 타격음으로 사운드의 뼈대를 세우는 역할입니다."),
        '壬癸': ("🎹 키보디스트 & 작곡가", "수(水)의 기운은 깊이와 흐름, 그리고 화성을 상징합니다. 사운드의 빈틈을 감성으로 채우고 유려한 화성 변화를 통해 곡의 전반적인 분위기를 신비롭게 주조하는 마술사와 같은 역할입니다.")
    }
    for k, v in positions.items():
        if d_gan in k: return v
    return ("🎸 베이시스트 & 프로듀서", "토(土)의 기운은 조화와 토대입니다. 고음과 저음을 연결하고 모든 악기가 제 소리를 낼 수 있도록 밑바탕을 지탱해 주는 안정적인 역할이자 사운드의 총지배인입니다.")

# 5️⃣ 실행 로직 및 결과 출력
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
        p_title, p_desc = get_refined_position(d_gan)
        samjae_msg, _ = get_samjae_info(ba_zi[0], target_y)

        # 결과 리포트 출력
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><span class='pos-title'>{p_title}</span><div class='content-text'>{p_desc}</div></div>", unsafe_allow_html=True)

        # 📅 운세 및 삼재 (300자 이상 확장)
        st.markdown(f"### 📅 {target_y}년 심층 운세 및 삼재")
        
        st.markdown(f"<div class='samjae-card'><h2>🚫 삼재(三災) 정보</h2><div class='content-text'><b>{samjae_msg}</b><br>삼재는 단순히 재난의 시기라기보다, 낡은 껍질을 벗고 새로운 자아로 거듭나기 위한 일종의 '성장통'의 시간입니다. 특히 예술가에게는 이러한 고통의 에너지가 창작의 강력한 촉매제가 되어 오히려 평소보다 훨씬 깊이 있고 울림이 큰 걸작을 만들어낼 수 있는 기회가 됩니다. 운의 흐름이 다소 정체된 듯 느껴질 때는 대외적인 확장보다는 내면의 사운드를 정교하게 다듬고 본인의 예술적 철학을 공고히 하는 '정진의 시간'으로 활용하신다면, 삼재가 끝난 후 비약적인 성장을 맞이하게 될 것입니다.</div></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_y}년 일반 운세 흐름</h2><div class='content-text'>{target_y}년은 본인의 일간 {d_gan}이 세운의 기운과 깊이 공명하며 인생의 새로운 마디를 형성하는 매우 중요한 변곡점입니다. 명리학적 관점에서 올해는 그동안 보이지 않는 곳에서 묵묵히 쌓아온 내공과 지식이 사회적인 환경과 조우하여 강력한 결실을 맺는 '성취와 보상의 해'가 될 확률이 매우 높습니다. 대외적인 활동 영역이 크게 확장되면서 본인의 전문적인 역량을 인정받는 기회가 빈번해질 것이며, 이를 통해 물질적인 성공뿐만 아니라 아티스트로서의 명예 또한 한 단계 격상되는 귀한 경험을 하게 될 것입니다. 변화를 두려워하지 말고 본인의 직관을 믿고 당당하게 나아간다면, 올해는 인생 전체를 통틀어 가장 큰 도약의 발판이자 성공의 기억으로 남을 해가 될 것입니다.</div></div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 {target_y}년 음악적 흐름 이야기</h2><div class='content-text'>예술가로서 {target_y}년은 본인만의 독보적인 '사운드 정체성'이 대중에게 가장 강렬하고 명확하게 각인되는 확장의 시기입니다. 올해의 기운은 본인의 창의적인 에너지를 더욱 정교하게 정제하여 세련된 결과물로 도출하게 도우며, 특히 새로운 장르로의 도전이나 예상치 못한 아티스트와의 협업이 본인의 음악적 지평을 넓히는 결정적인 계기가 될 것입니다. 대규모 라이브 공연이나 중요한 정규 음반 발표를 계획하고 있다면, 우주의 기운이 본인의 뒤를 든든하게 받쳐주고 있으니 망설임 없이 본인의 예술적 철학을 세상에 투영하시길 권장합니다. 단순히 유행을 따르는 소리를 넘어 시대의 흐름과 깊게 공명하는 본인만의 독창적인 선율은 청중의 영혼에 씻기지 않는 여운을 남길 것이며, 이는 아티스트로서 본인의 지위를 공고히 하는 역사적인 모멘텀이 될 것입니다.</div></div>", unsafe_allow_html=True)
