import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악가 전용 사주 분석기", layout="centered")

# 모바일 최적화 스타일 시트
st.markdown("""
    <style>
    .section-card { background-color: #ffffff; padding: 22px; border-radius: 18px; border-left: 6px solid #4A5568; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .music-card { background-color: #F7FAFC; padding: 22px; border-radius: 18px; border-left: 6px solid #805AD5; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(128,90,213,0.15); }
    .saju-box { text-align: center; padding: 12px; background: #EDF2F7; border-radius: 12px; margin: 4px; font-weight: bold; border: 1px solid #CBD5E0; }
    h2 { font-size: 1.4rem !important; color: #2D3748; margin-bottom: 12px; }
    .content-text { line-height: 1.8; font-size: 1rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .label-tag { background: #805AD5; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; vertical-align: middle; }
    </style>
    """, unsafe_allow_html=True)

hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 1️⃣ 입력 영역
with st.expander("📝 사주 및 분석 연도 설정", expanded=True):
    name = st.text_input("성함", value="임환백")
    c1, c2 = st.columns(2)
    year = c1.number_input("출생년", 1900, 2100, 1981)
    month = c2.number_input("출생월", 1, 12, 2)
    day = c1.number_input("출생일", 1, 31, 7)
    hour_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=3)
    calendar_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    target_year = st.number_input("분석 희망 연도", 1900, 2100, 2026)
    submitted = st.button("🎭 심층 이원 통변 실행", use_container_width=True)

# 2️⃣ 심층 통변 데이터베이스 엔진
def get_dual_interpretation(day_gan, max_elem, counts):
    # [일반 사주 통변] - 성격, 삶의 태도, 대인관계
    general_base = {
        "丙": f"본인은 만물을 비추는 태양인 丙(병화)의 기운을 타고났습니다. 성품이 대단히 명랑하고 숨김이 없으며, 매사에 열정적이고 자신감이 넘치는 타입입니다. 타인의 시선을 즐기며 리더십이 뛰어나 어딜 가나 주인공 역할을 자처하는 경향이 있습니다. 하지만 태양이 너무 뜨거우면 스스로를 소진하기 쉽듯, 감정 조절에 유의하고 내면의 고요함을 찾는 노력이 병행될 때 삶의 균형이 완성됩니다.",
        "庚": f"본인은 강직한 원석이자 예리한 칼날인 庚(경금)의 기운을 지녔습니다. 한번 결심한 일은 끝까지 밀고 나가는 강한 추진력과 의리가 돋보이는 성품입니다. 옳고 그름이 명확하여 대인관계에서도 맺고 끊음이 확실하지만, 때로는 지나친 직설적 화법이 오해를 살 수 있습니다. 스스로를 제련하는 과정을 즐긴다면 사회적으로 큰 성취를 이룰 수 있는 힘이 있는 사주입니다."
    }
    
    # [음악 사주 통변] - 예술성, 연주 스타일, 창작 성향
    music_base = {
        "금": f"사주에 '금(金)' 기운이 {counts['금']}자로 매우 강하게 나타납니다. 이는 음악적으로 매우 정교하고 날카로운 '금속성 감각'을 의미합니다. 일렉 기타의 디스토션 사운드나 정밀하게 계산된 미디 작업, 혹은 아주 타이트한 박자감을 요구하는 장르에서 타의 추종을 불허하는 재능을 보입니다. 완벽주의적 성향 때문에 한 음 한 음에 집착하는 경향이 있는데, 이는 곧 장인 정신으로 이어져 고퀄리티의 결과물을 만들어내는 원동력이 됩니다.",
        "목": f"사주에 '목(木)' 기운이 {counts['목']}자로 가득합니다. 이는 끝없이 샘솟는 서정적 선율과 어쿠스틱한 감수성을 뜻합니다. 나무가 자라듯 자연스러운 흐름의 작곡에 능하며, 현악기나 인간의 목소리를 가장 아름답게 표현할 줄 압니다. 계산된 음악보다는 즉흥적인 잼(Jam)이나 감정에 충실한 연주에서 본연의 빛이 나며, 따뜻하고 희망적인 가사나 멜로디로 대중의 마음을 치유하는 힘을 가졌습니다."
    }

    gen_text = general_base.get(day_gan, "타고난 기운이 강건하여 스스로의 길을 개척하는 독립적인 삶의 궤적을 그리게 될 사주입니다.")
    mus_text = music_base.get(max_elem, "다양한 오행이 조화를 이루어 장르에 국한되지 않는 넓은 음악적 스펙트럼을 보유한 올라운더 타입입니다.")
    
    return gen_text, mus_text

# 3️⃣ 출력 로직
if submitted:
    h = hour_time_map[hour_str]
    lunar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar() if calendar_type == "양력" else Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    max_elem = max(counts, key=counts.get)

    gen_rep, mus_rep = get_dual_interpretation(day_gan, max_elem, counts)

    st.markdown(f"### 🛡️ {name}님 심층 분석 결과")
    
    # 명식 표시
    cols = st.columns(4)
    for i, label in enumerate(["년주", "월주", "일주", "시주"]):
        cols[i].markdown(f"<div class='saju-box'><small>{label}</small><br>{ba_zi[i]}</div>", unsafe_allow_html=True)

    # 섹션 1: 일반 사주
    st.markdown(f"""
    <div class='section-card'>
        <h2>👤 일반 인생 통변 (성격 및 삶의 흐름)</h2>
        <div class='content-text'>{gen_rep}</div>
    </div>
    """, unsafe_allow_html=True)

    # 섹션 2: 음악 사주
    st.markdown(f"""
    <div class='music-card'>
        <h2>🎸 음악 특화 통변 <span class='label-tag'>ARTIST</span></h2>
        <div class='content-text'>{mus_rep}</div>
        <p style='margin-top:15px; font-size:0.85rem; color:#805AD5;'><b>※ 추천 악기/포지션:</b> { '기타/테크니션' if max_elem=='금' else '보컬/프론트맨' if max_elem=='화' else '작곡/건반' if max_elem=='수' else '드럼/베이스' }</p>
    </div>
    """, unsafe_allow_html=True)

    # 섹션 3: 지정 연도 운세
    target_gz = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()
    st.markdown(f"""
    <div class='section-card' style='border-left-color:#3182CE; background-color:#EBF8FF;'>
        <h2>📅 {target_year}년({target_gz}년) 종합 흐름</h2>
        <div class='content-text'>올해는 <b>{target_gz}</b>의 기운이 들어와 본인의 <b>{day_gan}</b> 일간과 반응하는 해입니다. 
        일반적으로는 사회적 지위나 명예가 오르는 구간이며, 음악적으로는 그동안 쌓아온 실력을 대중에게 검증받는 '데뷔' 혹은 '재발견'의 시기가 될 것입니다. 
        상반기에는 내실을 다지고 하반기에는 과감한 대외 활동을 추천합니다.</div>
    </div>
    """, unsafe_allow_html=True)

    # 오행 그래프
    st.markdown("#### **📊 오행 에너지 밸런스**")
    for elem, count in counts.items():
        st.write(f"{elem} ({count}자)")
        st.progress(count / 8.0)
