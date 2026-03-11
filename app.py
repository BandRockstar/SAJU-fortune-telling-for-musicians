import streamlit as st
from lunar_python import Solar, Lunar
import random

# 1️⃣ 페이지 설정 및 CSS (기존 디자인 테마 엄격 유지)
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; margin-bottom: 10px; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 30px; border-radius: 20px; border-left: 8px solid #4A5568; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(0,0,0,0.07); }
    .music-card { background-color: #FDF2F8; padding: 30px; border-radius: 20px; border-left: 8px solid #D53F8C; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(213,63,140,0.1); }
    .position-card { background-color: #FFFBEB; padding: 30px; border-radius: 20px; border-left: 8px solid #D97706; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(217,119,6,0.1); }
    .target-year-card { background-color: #F0F9FF; padding: 30px; border-radius: 20px; border-left: 8px solid #3182CE; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(49,130,206,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 25px; gap: 8px; }
    .saju-box { flex: 1; text-align: center; padding: 18px 5px; background: #EDF2F7; border-radius: 15px; font-weight: bold; border: 1px solid #CBD5E0; font-size: 1rem; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 20px; border-radius: 18px; margin-bottom: 25px; }
    .ohaeng-item { text-align: center; flex: 1; }
    h1 { font-size: 2rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.4rem !important; color: #2D3748; margin-bottom: 18px; display: flex; align-items: center; font-weight: 700; }
    .content-text { line-height: 2.0; font-size: 1.08rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.35rem; font-weight: bold; color: #B45309; margin-bottom: 12px; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 2️⃣ 입력 설정 (개인정보 보호 템플릿 준수)
hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="", placeholder="분석에 사용할 성함을 입력하세요")
    c1, c2 = st.columns(2)
    y = c1.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    m = c2.number_input("출생월", 1, 12, value=None, placeholder="MM")
    d = c2.number_input("출생일", 1, 31, value=None, placeholder="DD")
    h_str = c1.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달 여부") if cal_type == "음력" else False
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 3️⃣ 풍성한 동적 통변 엔진 (분량 및 다양성 확보)
def get_dynamic_report(d_gan, counts, max_elem, name):
    # 일반 통변: 200자 이상 확보용 데이터셋
    general_intros = [
        f"본인은 {d_gan}의 기운을 바탕으로 태어난 예술가로서, 세상을 향해 자신만의 에너지를 발산하려는 강한 창의적 열망을 지니고 있습니다. ",
        f"사주의 핵심인 {d_gan}의 성정은 당신의 삶 전반에 걸쳐 명확한 주관과 독창적인 색채를 부여하며, 남들과는 다른 길을 개척하게 만드는 원동력이 됩니다. "
    ]
    general_details = {
        '금': "명식 내 금(金)의 기운이 강하여 성격적으로 매우 정교하고 결단력이 있으며, 사물이나 상황을 한눈에 꿰뚫어 보는 통찰력이 남다릅니다. 이는 일상에서도 타협하지 않는 완벽주의로 나타나곤 합니다. ",
        '화': "불의 기운인 화(火)가 발달하여 감정의 폭이 깊고 열정적이며, 사람들 사이에서 분위기를 주도하는 에너지가 탁월합니다. 본인의 내면을 외부로 드러낼 때 가장 큰 행복을 느끼는 타입입니다. ",
        '목': "나무의 기운인 목(木)이 풍부하여 서정적이고 온화한 성품을 지녔으며, 끊임없이 배우고 성장하려는 이상향을 품고 있습니다. 따뜻한 인간미가 돋보이는 명식입니다. ",
        '토': "흙의 기운인 토(土)가 중심을 잡아주어 매우 듬직하고 신중하며, 주변의 갈등을 조율하고 하나로 묶어주는 포용력이 대단합니다. 어떤 상황에서도 흔들리지 않는 내공을 소유하고 있습니다. ",
        '수': "물의 기운인 수(水)가 깊어 유연하고 지혜로우며, 타인의 깊은 내면을 읽어내는 공감 능력이 뛰어납니다. 보이지 않는 가치에 대해 깊이 사유하는 철학적인 면모가 강합니다. "
    }
    
    # 음악적 통변: 200자 이상 확보용 데이터셋
    music_intros = [
        f"{name}님의 음악적 지평은 명식 내 {max_elem}의 기운을 어떻게 승화시키느냐에 따라 결정됩니다. 단순히 소리를 내는 것을 넘어 소리에 영혼을 담는 능력이 탁월합니다. ",
        f"예술적 감각의 원천인 {max_elem} 기운은 본인의 연주와 작곡 스타일에서 가장 뚜렷한 정체성을 형성하며, 청중에게 깊은 여운을 남기는 힘을 제공합니다. "
    ]
    music_details = {
        '금': "음악적으로는 금속성의 명징한 사운드와 정교한 연주 테크닉에 집착하는 경향이 있으며, 불필요한 음을 걷어낸 세련된 미니멀리즘이나 날카로운 톤 메이킹에서 본인만의 매력을 발산합니다. ",
        '화': "화려한 무대 매너와 폭발적인 감정 표현이 강점입니다. 특히 보컬이나 기타 솔로에서 감정을 최고조로 끌어올리는 극적인 구성에 능하며, 청중의 심장을 직접적으로 파고드는 직관적인 음악을 지향합니다. ",
        '목': "어쿠스틱한 울림이나 서사적인 멜로디 라인에 강점이 있습니다. 자연스러운 리듬감과 듣는 이의 마음을 편안하게 만드는 따뜻한 음색을 지니고 있어, 대중과 정서적으로 깊이 교감하는 음악에 최적화되어 있습니다. ",
        '토': "사운드의 밸런스를 잡는 능력이 탁월하여 밴드의 사운드를 하나로 묶어주는 역할을 완벽히 수행합니다. 묵직하고 안정적인 베이스 톤이나 정교한 미디 프로듀싱에서 본인만의 탄탄한 음악적 세계관을 보여줍니다. ",
        '수': "깊고 몽환적인 앰비언트 사운드나 유려한 즉흥 연주에 능합니다. 고정된 형식보다는 흐름에 몸을 맡기는 유연한 연주 스타일을 선호하며, 보이지 않는 정서를 소리로 치환하는 능력이 매우 신비롭습니다. "
    }

    gen_text = random.choice(general_intros) + general_details.get(max_elem, "") + "이러한 기질은 사회적 관계에서도 본인의 전문성을 인정받게 하며, 스스로 만족할 수 있는 예술적 결과물을 만들어낼 때까지 멈추지 않는 끈기를 선사합니다."
    mus_text = random.choice(music_intros) + music_details.get(max_elem, "") + "기존의 장르에 얽매이지 않고 본인의 감각이 이끄는 대로 소리를 직조해 나간다면, 그 누구도 흉내 낼 수 없는 {display_name}님만의 독보적인 음악적 지평이 열릴 것입니다."
    
    return gen_text, mus_text

# 4️⃣ 분석 실행 및 리포트 출력
if submitted:
    if not (y and m and d) or hour_time_map[h_str] == "시간 선택 (또는 모름)":
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
        t_gz = Solar.fromYmd(target_y, 1, 1).getLunar().getYearInGanZhi()
        
        # 병화 일간 정체성 고정 로직
        p_title = "🎤 리드 보컬 & 기타리스트 (Frontman)" if d_gan in '丙丁' else "🎸 아티스트 (All-Rounder)"
        p_desc = "태양과 불을 상징하는 화(火)의 일간은 무대 위에서 에너지를 발산할 때 비로소 완성됩니다. 단순한 연주를 넘어 청중의 시선을 사로잡는 카리스마를 타고났으며, 본인의 감성을 목소리와 선율에 담아 강력한 영감을 전달하는 독보적인 아티스트가 될 운명입니다."

        display_name = user_name if user_name else "아티스트"
        gen_text, mus_text = get_dynamic_report(d_gan, counts, max_elem, display_name)

        st.markdown(f"### 🍀 {display_name}님의 심층 분석 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><span class='pos-title'>{p_title}</span><div class='content-text'>{p_desc}</div></div>", unsafe_allow_html=True)

        st.markdown(f"### 📅 {target_y}년({t_gz}) 심층 분석")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_y}년 운세 흐름</h2><div class='content-text'>{target_y}년은 본인의 일간 {d_gan}이 {t_gz}의 흐름을 만나 삶의 새로운 전환점을 맞이하는 해입니다. 그동안의 노력이 외부로 드러나며 명예와 결실이 따르는 긍정적인 운세입니다. 자신감을 가지고 활동 영역을 넓히시길 바랍니다.</div></div>", unsafe_allow_html=True)
