import streamlit as st
from lunar_python import Solar, Lunar
import random

# 1️⃣ 페이지 설정 및 디자인 (기존 스타일 유지)
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

# 2️⃣ 입력 설정
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

# 3️⃣ 정교화된 음악 포지션 판별 함수
def get_refined_position(d_gan, max_elem):
    # 일간에 따른 기본 성향
    if d_gan in '丙丁': # 화(火) 일간: 발산의 기운
        return ("🎤 리드 보컬 & 프런트맨", "화(火)의 기운은 무대 위에서 에너지를 발산하고 관객을 압도하는 카리스마를 상징합니다. 밴드의 중심에서 목소리로 메시지를 전달할 때 가장 빛이 납니다.")
    elif d_gan in '甲乙': # 목(木) 일간: 선율과 곡조
        return ("🎸 리드 기타리스트", "목(木)의 기운은 유연하고 서정적인 선율을 다루는 능력을 의미합니다. 정교한 솔로 연주나 곡의 서사를 이끄는 멜로디 메이킹에 강점이 있습니다.")
    elif d_gan in '庚辛': # 금(金) 일간: 리듬과 타격
        return ("🥁 드러머 (Percussionist)", "금(金)의 기운은 정교한 타이밍과 단단한 타격감을 상징합니다. 정확한 비트를 유지하며 곡의 뼈대를 만드는 드럼 연주에서 탁월한 기량을 발휘합니다.")
    elif d_gan in '壬癸': # 수(水) 일간: 흐름과 깊이
        return ("🎹 키보디스트 & 작곡가", "수(水)의 기운은 곡의 흐름을 조절하고 깊이 있는 감성을 채워주는 역할을 합니다. 풍부한 화성과 몽환적인 사운드를 창조하는 데 최적화되어 있습니다.")
    else: # 토(土) 일간: 조화와 균형
        return ("🎸 베이시스트 & 프로듀서", "토(土)의 기운은 저음에서 사운드를 지탱하고 모든 악기를 조화롭게 묶어주는 안정감을 의미합니다. 곡의 중심을 잡는 베이스나 전체를 아우르는 프로듀싱이 길합니다.")

# 4️⃣ 풍성한 동적 통변 엔진
def get_dynamic_report(d_gan, counts, max_elem, name):
    general_intros = [
        f"본인은 {d_gan}의 기운을 바탕으로 태어난 예술가로서, 세상을 향해 자신만의 에너지를 발산하려는 강한 창의적 열망을 지니고 있습니다. ",
        f"사주의 핵심인 {d_gan}의 성정은 당신의 삶 전반에 걸쳐 명확한 주관과 독창적인 색채를 부여하며, 예술적 성취를 향한 나침반 역할을 합니다. "
    ]
    general_details = {
        '금': "명식 내 금(金)의 기운이 강하여 결단력이 있고 완벽주의적이며, 날카로운 분석력을 바탕으로 정교한 작업을 수행하는 능력이 뛰어납니다. ",
        '화': "화(火)의 기운이 발달하여 열정적이고 외향적이며, 자신의 감정을 예술적으로 표현할 때 최고의 카타르시스를 느끼는 타입입니다. ",
        '목': "목(木)의 기운이 풍부하여 서정적이고 인간미 넘치는 감수성을 지녔으며, 새로운 창작물을 기획하고 성장시키는 능력이 탁월합니다. ",
        '토': "토(土)의 기운이 중심을 잡아주어 신중하고 포용력이 있으며, 복잡한 상황 속에서도 흔들리지 않는 내면의 중심을 지키는 힘이 있습니다. ",
        '수': "수(水)의 기운이 깊어 유연하고 지혜로우며, 타인의 무의식을 건드리는 깊은 울림의 예술을 창조하는 통찰력이 남다릅니다. "
    }
    mus_intros = [f"예술적 원천인 {max_elem} 기운은 {name}님의 연주 스타일에서 가장 뚜렷한 개성을 형성합니다. ", f"명식의 {max_elem} 성분은 단순히 기량을 넘어 청중에게 전달되는 고유의 '톤'을 결정짓는 핵심입니다. "]
    
    gen_text = random.choice(general_intros) + general_details.get(max_elem, "") + "이 기질은 예술적 결과물을 완성할 때까지 멈추지 않는 끈기를 선사합니다."
    mus_text = random.choice(mus_intros) + "본인의 직관을 믿고 작업할 때 가장 독창적인 결과물이 나올 것이며, 이는 장르를 초월한 울림이 될 것입니다."
    
    return gen_text, mus_text

# 5️⃣ 분석 실행
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
        
        # 동적 문구 및 포지션 생성
        p_title, p_desc = get_refined_position(d_gan, max_elem)
        display_name = user_name if user_name else "아티스트"
        gen_text, mus_text = get_dynamic_report(d_gan, counts, max_elem, display_name)

        # 리포트 출력
        st.markdown(f"### 🍀 {display_name}님의 심층 분석 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><span class='pos-title'>{p_title}</span><div class='content-text'>{p_desc}</div></div>", unsafe_allow_html=True)

        st.markdown(f"### 📅 {target_y}년({t_gz}) 심층 분석")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_y}년 운세 흐름</h2><div class='content-text'>{target_y}년은 {d_gan} 일간이 {t_gz}를 만나 새로운 변화를 꾀하는 시기입니다. 명예와 결실이 따르는 긍정적인 운세이므로 자신감을 가지고 활동하시길 바랍니다.</div></div>", unsafe_allow_html=True)
