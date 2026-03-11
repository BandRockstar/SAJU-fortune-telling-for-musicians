import streamlit as st
from lunar_python import Solar, Lunar
import random

# 1️⃣ 페이지 설정 및 모바일 최적화 UI 디자인
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 모바일 반응형 폰트 및 레이아웃 */
    html { font-size: 14px; }
    @media (min-width: 600px) { html { font-size: 16px; } }

    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card, .samjae-card { 
        padding: 1.5rem; border-radius: 1.2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
    }
    .section-card { background-color: #ffffff; border-left: 6px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 6px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 6px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 6px solid #3182CE; }
    .samjae-card { background-color: #FEF2F2; border-left: 6px solid #EF4444; }

    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 1.5rem; gap: 5px; }
    .saju-box { flex: 1; text-align: center; padding: 12px 2px; background: #EDF2F7; border-radius: 10px; font-weight: bold; border: 1px solid #CBD5E0; font-size: 0.9rem; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 15px; border-radius: 12px; margin-bottom: 1.5rem; }
    .ohaeng-item { text-align: center; flex: 1; font-size: 0.85rem; }
    
    h1 { font-size: 1.8rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.2rem !important; color: #2D3748; margin-bottom: 1rem; font-weight: 700; }
    .content-text { line-height: 1.8; font-size: 1rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.2rem; font-weight: bold; color: #B45309; margin-bottom: 0.5rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 2️⃣ 입력 설정 (년-월-일-시 순서 교정)
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
    # 띠 계산 (지지)
    zodiac = year_ganzhi[-1]
    samjae_map = {
        '申': ['寅', '卯', '辰'], '子': ['寅', '卯', '辰'], '辰': ['寅', '卯', '辰'],
        '亥': ['巳', '午', '未'], '卯': ['巳', '午', '未'], '未': ['巳', '午', '未'],
        '寅': ['申', '酉', '戌'], '午': ['申', '酉', '戌'], '戌': ['申', '酉', '戌'],
        '巳': ['亥', '子', '丑'], '酉': ['亥', '子', '丑'], '丑': ['亥', '子', '丑']
    }
    
    target_lunar = Solar.fromYmd(target_year, 1, 1).getLunar()
    target_zodiac = target_lunar.getYearInGanZhi()[-1]
    
    my_samjae_years = samjae_map.get(zodiac, [])
    if target_zodiac in my_samjae_years:
        idx = my_samjae_years.index(target_zodiac)
        status = ["들삼재", "눌삼재", "날삼재"][idx]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다. ", True
    else:
        return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다. ", False

# 4️⃣ 통변 엔진 (기존 장문 로직 유지)
def get_final_report(d_gan, max_elem, name):
    gen_data = {
        '목': f"본인은 {d_gan}의 정기를 품고 태어나 만물을 소생시키는 생명력과 서정적 감수성이 조화를 이룬 예술가입니다. {max_elem}의 기운이 발달한 명식은 온화한 성품 뒤에 꺾이지 않는 대나무 같은 신념을 지니고 있으며, 끊임없이 위를 향해 성장하려는 학구열이 강합니다. 이러한 성정은 주변 사람들에게 긍정적인 영감을 주는 지도자적 자질로 나타나며, 시간이 흐를수록 본인만의 독보적인 가치관을 지키며 대중의 존경을 받는 인물로 거듭날 것입니다.",
        '화': f"본인은 {d_gan}의 에너지를 지녀 태양처럼 뜨겁고 열정적이며, 자신을 외부로 드러내는 데 최적화된 명식입니다. {max_elem}의 기운이 풍부하여 직관력이 매우 뛰어나고 상황 판단이 빠르며, 화려한 표현력과 카리스마로 무대를 장악하는 힘이 있습니다. 실패를 두려워하지 않는 추진력은 남들이 시도하지 못하는 창의적인 영역에서 큰 성취를 이뤄내는 원동력이 되며, 내면의 감정을 예술적으로 승화시킬 때 비로소 진정한 삶의 만족을 느끼게 될 것입니다.",
        '토': f"본인은 {d_gan}의 기운을 품어 대지처럼 넓은 포용력과 모든 사운드를 조화롭게 융합하는 중재 능력이 뛰어납니다. {max_elem}의 성분이 강한 명식은 매사에 신중하고 신의가 두터우며, 안정적인 토대 위에서 성과를 쌓아가는 만성형의 기질이 강합니다. 조직 내에서 기둥 같은 역할을 수행하며, 주변의 갈등을 조율하는 능력이 탁월하여 어떤 상황에서도 흔들리지 않는 내공을 보여줍니다. 이러한 묵직한 내공은 세월이 흐를수록 빛을 발하며 많은 이들이 믿고 의지할 수 있는 존재감을 완성합니다.",
        '금': f"본인은 {d_gan}의 정기를 받아 금속처럼 날카로운 분석력과 완벽을 기하는 장인 정신을 소유하고 있습니다. {max_elem}의 기운이 주도하는 명식은 시비지심이 명확하고 타협을 거부하는 강직함이 돋보이며, 자신이 맡은 일에 대해서는 끝까지 책임을 지는 성실함을 보여줍니다. 겉으로는 냉철해 보일 수 있으나 내면에는 누구보다 뜨거운 정의감이 자리 잡고 있습니다. 본인만의 엄격한 기준을 전문 분야에 적용한다면 그 누구도 넘볼 수 없는 경지에 도달하여 사회적 존경을 받게 될 것입니다.",
        '수': f"본인은 {d_gan}의 성정을 타고나 깊은 바다와 같이 유연하고 지혜로우며, 감정의 이면을 읽어내는 통찰력이 매우 남다릅니다. {max_elem}의 기운이 깊은 명식은 현상의 본질에 집중하며, 타인의 무의식을 건드리는 깊은 울림의 예술을 창조하는 공감 능력이 뛰어납니다. 고정된 형식에 얽매이지 않는 자유로운 사고를 지향하며, 때로는 철학적인 면모를 보여주기도 합니다. 이러한 유연함은 사람들의 마음을 움직이는 고차원적인 기획력이나 창작 활동으로 연결되어 세상에 깊은 흔적을 남기게 될 것입니다."
    }
    mus_data = {
        '목': f"{name}님의 음악 세계는 서사적인 선율과 따뜻한 리듬감이 완벽하게 조화를 이루고 있습니다. {max_elem} 기운이 풍부하여 어쿠스틱한 울림이나 서정적인 가사 전달에 탁월하며, 듣는 이의 마음을 위로하는 치유의 선율을 만들어냅니다. 단순히 기교를 뽐내기보다 곡 전체의 생명력과 정서적 교감을 중시하는 아티스트로서, 본인의 음악은 시간이 지날수록 대중의 마음에 깊이 스며들어 잊히지 않는 여운을 남기는 독보적인 스타일을 구축하게 될 것입니다.",
        '화': f"{name}님의 음악은 무대 위에서 폭발하는 카리스마와 화려한 퍼포먼스 그 자체입니다. {max_elem} 기운이 주도하는 덕분에 보컬의 성량이나 연주의 색채가 매우 화려하며, 청중의 감정을 한순간에 최고조로 이끄는 극적인 구성에 능합니다. 직관적으로 멜로디를 직조하는 능력이 뛰어나 대중적 흡인력이 매우 강하며, 본인의 뜨거운 열정을 소리로 치환할 때 발생하는 에너지는 누구도 흉내 낼 수 없는 개성이 되어 무대의 중심에서 가장 밝게 빛나게 될 것입니다.",
        '토': f"{name}님의 음악적 기반은 사운드의 완벽한 밸런스와 안정적인 구조미에 있습니다. {max_elem} 기운이 중심을 잡아주어 묵직한 베이스 톤이나 정교한 프로듀싱 능력이 탁월하며, 밴드 사운드를 하나로 융합하여 완성도를 높이는 데 핵심적인 역할을 합니다. 자극적인 소리보다는 깊이 있고 클래식한 사운드를 지향하며, 탄탄한 기본기 위에서 세월이 흘러도 변하지 않는 가치를 전합니다. 듣는 이에게 정서적 안정감과 묵직한 감동을 선사하는 아티스트로서의 입지를 굳건히 할 것입니다.",
        '금': f"{name}님의 연주는 명징한 사운드와 단 한 치의 오차도 허용하지 않는 정교한 테크닉이 돋보입니다. {max_elem} 기운이 강한 덕분에 날카롭게 정제된 톤 메이킹과 세련된 미니멀리즘에서 본인만의 매력을 발산합니다. 하이엔드 장비에 대한 이해도가 높고 사운드 엔지니어링 측면에서 완벽을 기하여 최상의 품질을 만들어냅니다. 날카로운 선율 속에 담긴 투명한 진심은 청중의 이성을 마비시키고 오로지 소리 자체에만 집중하게 만드는 강력한 흡입력을 발휘합니다.",
        '수': f"{name}님의 음악적 지평은 몽환적이면서도 신비로운 공간감에 닿아 있습니다. {max_elem} 기운이 깊어 유연한 흐름 속에서 영감을 얻으며, 보이지 않는 정서를 신비로운 사운드 텍스처로 치환하는 능력이 대단합니다. 앰비언트 사운드나 풍부한 화성적 변화를 활용한 연출에 능하며, 청중을 무의식의 깊은 곳으로 안내하는 철학적인 깊이를 제공합니다. 단순히 듣는 음악을 넘어 하나의 세계관을 창조하는 과정으로서, 본인의 선율은 영혼에 긴 여운을 남기는 지혜로운 예술이 될 것입니다."
    }
    return gen_data.get(max_elem, ""), mus_data.get(max_elem, "")

def get_refined_position(d_gan):
    positions = {
        '丙丁': ("🎤 리드 보컬 & 프런트맨", "화(火)의 기운은 발산의 에너지입니다. 무대 중앙에서 목소리로 대중을 장악하는 카리스마를 상징합니다."),
        '甲乙': ("🎸 리드 기타리스트", "목(木)의 기운은 선율과 유연성을 상징합니다. 곡의 온도를 결정하는 섬세한 연주자에 최적화되어 있습니다."),
        '庚辛': ("🥁 드러머", "금(金)의 기운은 정확한 분별을 뜻합니다. 밴드의 심장박동을 일정하게 유지하는 뼈대 역할을 합니다."),
        '壬癸': ("🎹 키보디스트 & 작곡가", "수(水)의 기운은 깊이와 흐름을 상징합니다. 분위기를 주조하는 마술사와 같은 역할입니다.")
    }
    for k, v in positions.items():
        if d_gan in k: return v
    return ("🎸 베이시스트 & 프로듀서", "토(土)의 기운은 조화와 토대입니다. 모든 악기를 밑바탕에서 지탱해 주는 총지배인입니다.")

# 5️⃣ 실행 및 결과 출력
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
        gen_text, mus_text = get_final_report(d_gan, max_elem, display_name)
        p_title, p_desc = get_refined_position(d_gan)
        samjae_msg, is_samjae = get_samjae_info(ba_zi[0], target_y)

        # 결과 리포트
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><span class='pos-title'>{p_title}</span><div class='content-text'>{p_desc}</div></div>", unsafe_allow_html=True)

        # 📅 운세 및 삼재 섹션
        st.markdown(f"### 📅 {target_y}년 심층 운세 및 삼재")
        
        # 삼재 카드
        samjae_desc = "삼재는 9년 주기로 돌아오는 3가지 재난의 시기를 뜻하지만, 예술가에게는 오히려 고통을 창작의 밑거름으로 삼아 명작을 남기는 시기가 되기도 합니다. "
        st.markdown(f"<div class='samjae-card'><h2>🚫 삼재(三災) 정보</h2><div class='content-text'><b>{samjae_msg}</b><br>{samjae_desc}</div></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_y}년 일반 운세 흐름</h2><div class='content-text'>{target_y}년은 본인의 일간 {d_gan}이 세운의 기운과 상호작용하며 인생의 새로운 마디를 형성하는 시기입니다. 그동안 묵묵히 쌓아온 내공이 드디어 사회적 명분과 결합하여 강력한 결실을 맺는 성취의 해가 될 것입니다. 대외 활동 영역이 넓어지며 전문성을 인정받는 기회가 잦아질 것이니, 본인의 직관을 믿고 나아간다면 큰 도약의 발판이 될 것입니다.</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 {target_y}년 음악적 흐름 이야기</h2><div class='content-text'>예술가로서 {target_y}년은 독보적인 사운드 정체성이 대중에게 각인되는 확장의 해입니다. 새로운 장르적 시도나 실험적인 협업이 의외의 큰 성공을 거두는 흐름을 보입니다. 대규모 공연이나 중요한 음원 발표를 앞두고 있다면 올해의 운이 든든하게 받쳐주고 있으니 망설임 없이 본인의 예술적 철학을 투영하시길 바랍니다. 시대의 흐름과 공명하는 선율은 아티스트로서의 명예를 한 단계 높여줄 것입니다.</div></div>", unsafe_allow_html=True)
