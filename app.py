import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 제목 배치
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# 모바일 최적화 및 세련된 디자인을 위한 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; margin-bottom: 10px; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 22px; border-radius: 18px; border-left: 6px solid #4A5568; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .music-card { background-color: #FDF2F8; padding: 22px; border-radius: 18px; border-left: 6px solid #D53F8C; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(213,63,140,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 20px; gap: 5px; }
    .saju-box { flex: 1; text-align: center; padding: 12px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; font-size: 0.9rem; }
    h1 { font-size: 1.8rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 12px; display: flex; align-items: center; }
    .content-text { line-height: 1.8; font-size: 1rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    </style>
    """, unsafe_allow_html=True)

# 최상단 제목 배치
st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 2️⃣ 입력 영역
with st.expander("📝 사주 정보 입력 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="임환백")
    c1, c2 = st.columns(2)
    year = c1.number_input("출생년", 1900, 2100, 1981)
    month = c2.number_input("출생월", 1, 12, 2)
    day = c1.number_input("출생일", 1, 31, 7)
    hour_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=3)
    calendar_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    target_year = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 3️⃣ 심층 통변 엔진 (서술형 데이터 강화)
def get_dual_report(day_gan, max_elem, counts):
    # 일반 인생 통변 (최소 150자 이상)
    general_dict = {
        "丙": f"본인은 만물을 비추는 태양의 기운인 丙(병화) 일간을 타고났습니다. 타고난 성품이 대단히 명랑하고 숨김이 없으며, 매사에 정열적이고 자신감이 넘치는 스타일입니다. 타인의 시선을 즐기며 리더십이 뛰어나 어딜 가나 주인공 역할을 하는 경향이 강합니다. 다만 태양이 너무 뜨거우면 주변을 메마르게 하듯, 감정의 기복을 다스리고 내면의 고요함을 찾는 노력이 병행될 때 비로소 삶의 균형과 평온이 완성될 사주입니다.",
        "庚": f"본인은 단단한 원석이자 예리한 칼날의 기운인 庚(경금) 일간을 타고났습니다. 한번 결심한 일은 끝까지 밀고 나가는 강한 추진력과 의리가 돋보이는 성품의 소유자입니다. 옳고 그름이 명확하여 대인관계에서도 맺고 끊음이 확실하지만, 때로는 지나치게 직설적인 화법이 주변에 오해를 살 수도 있습니다. 스스로를 끊임없이 제련하고 수련하는 과정을 즐긴다면 사회적으로 큰 성취를 이룰 수 있는 묵직한 힘이 있는 사주입니다."
    }
    
    # 음악적 사주 통변 (최소 150자 이상)
    music_dict = {
        "금": f"사주 원국에 '금(金)'의 기운이 {counts['금']}자로 매우 강하게 자리 잡고 있습니다. 이는 음악적으로 매우 정교하고 날카로운 '금속성 감각'을 의미하며, 일렉 기타의 디스토션 사운드나 정밀하게 계산된 미디(MIDI) 작업에서 독보적인 재능을 발휘합니다. 완벽주의적 성향 때문에 한 음 한 음에 집착하는 경향이 있는데, 이는 곧 아티스트로서의 장인 정신으로 승화되어 고퀄리티의 결과물을 만들어내는 핵심 동력이 됩니다.",
        "목": f"본인의 사주에는 '목(木)'의 기운이 {counts['목']}자로 가득하여 서정적인 선율과 풍부한 감수성이 돋보입니다. 나무가 자라듯 자연스러운 흐름의 작곡에 능하며, 현악기나 보컬의 감성을 극대화하여 표현하는 데 천부적인 소질이 있습니다. 계산된 기교보다는 즉흥적인 연주나 영감에 충실한 창작 활동에서 본연의 빛이 나며, 따뜻하고 희망적인 멜로디로 대중의 마음을 어루만지는 힐러(Healer)의 자질을 갖춘 아티스트입니다."
    }

    gen = general_dict.get(day_gan, "타고난 예술적 영감이 풍부하여 어떤 장르에서도 자신만의 독창적인 색채를 드러내는 비범한 사주를 지니셨습니다. 본인만의 독특한 감각을 믿고 나아가십시오.")
    mus = music_dict.get(max_elem, "다양한 오행이 조화를 이루어 특정 장르에 국한되지 않는 넓은 음악적 스펙트럼을 보유한 올라운더 타입의 뮤지션입니다.")
    
    return gen, mus

# 4️⃣ 분석 및 결과 출력
if submitted:
    h = hour_time_map[hour_str]
    # 날짜 변환 로직
    if calendar_type == "양력":
        solar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
        lunar = solar.getLunar()
    else:
        lunar = Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)

    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    max_elem = max(counts, key=counts.get)

    gen_rep, mus_rep = get_dual_report(day_gan, max_elem, counts)

    # 8자 명식 그리드 (모바일 2x2 대응 가능하도록 설계)
    st.markdown("### 📜 나의 사주 명식")
    st.markdown(f"""
        <div class='saju-grid'>
            <div class='saju-box'><small>년주</small><br>{ba_zi[0]}</div>
            <div class='saju-box'><small>월주</small><br>{ba_zi[1]}</div>
            <div class='saju-box'><small>일주</small><br>{ba_zi[2]}</div>
            <div class='saju-box'><small>시주</small><br>{ba_zi[3]}</div>
        </div>
    """, unsafe_allow_html=True)

    # 일반 인생 리포트
    st.markdown(f"""
        <div class='section-card'>
            <h2>👤 일반 인생 통변</h2>
            <div class='content-text'>{gen_rep}</div>
        </div>
    """, unsafe_allow_html=True)

    # 음악 특화 리포트
    st.markdown(f"""
        <div class='music-card'>
            <h2>🎸 음악적 사주 통변</h2>
            <div class='content-text'>{mus_rep}</div>
            <p style='margin-top:15px; font-size:0.9rem; color:#D53F8C;'>
                <b>🎹 추천 포지션:</b> { '일렉기타/테크니션' if max_elem=='금' else '보컬/퍼포머' if max_elem=='화' else '작곡/편곡/건반' if max_elem=='수' else '리듬파트/프로듀서' }
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 선택 연도 운세
    target_gz = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()
    st.markdown(f"""
        <div class='section-card' style='border-left-color:#3182CE; background-color:#EBF8FF;'>
            <h2>📅 {target_year}년({target_gz}년) 운세 흐름</h2>
            <div class='content-text'>올해는 <b>{target_gz}</b>의 기운이 본인의 <b>{day_gan}</b> 일간과 조우하는 해입니다. 
            음악적으로는 그동안 쌓아온 내실이 대외적으로 빛을 발하는 시기로, 특히 하반기에 명예운이 강하게 들어옵니다. 
            앨범 발표나 공연 기획이 있다면 과감하게 추진해 보셔도 좋은 운의 흐름입니다.</div>
        </div>
    """, unsafe_allow_html=True)

    # 오행 지표
    st.markdown("#### **📊 오행 에너지 분포**")
    for elem, count in counts.items():
        st.write(f"{elem} ({count}자)")
        st.progress(count / 8.0)
