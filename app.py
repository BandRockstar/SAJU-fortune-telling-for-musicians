import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# CSS: 디자인 레이아웃 및 폰트 설정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 25px; border-radius: 18px; border-left: 6px solid #4A5568; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .music-card { background-color: #FDF2F8; padding: 25px; border-radius: 18px; border-left: 6px solid #D53F8C; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(213,63,140,0.1); }
    .target-year-card { background-color: #F0F9FF; padding: 25px; border-radius: 18px; border-left: 6px solid #3182CE; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(49,130,206,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 20px; gap: 5px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 15px; border-radius: 15px; margin-bottom: 20px; }
    .ohaeng-item { text-align: center; flex: 1; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 15px; display: flex; align-items: center; }
    .content-text { line-height: 1.9; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .highlight { color: #D53F8C; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 시간 매핑
hour_time_map = {
    "시간 선택": None, "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 2️⃣ 입력 영역
with st.expander("📝 사주 정보 및 분석 연도 입력", expanded=True):
    name = st.text_input("성함", value="", placeholder="이름을 입력하세요")
    c1, c2 = st.columns(2)
    year = c1.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    month = c2.number_input("출생월", 1, 12, value=None, placeholder="MM")
    day = c1.number_input("출생일", 1, 31, value=None, placeholder="DD")
    hour_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달 여부") if cal_type == "음력" else False
    
    # 보고 싶은 연도 입력 복원
    target_year = st.number_input("분석하고 싶은 연도 선택", 1900, 2100, value=2026)
    
    submitted = st.button("🎭 심층 이원 분석 리포트 생성", use_container_width=True)

# 3️⃣ 심층 통변 엔진 (분량 및 연도별 분석 강화)
def get_reports(day_gan, max_elem, counts, t_year, t_gz):
    # 1. 전체 사주 통변
    gen_total = f"본인은 <b>{day_gan}</b> 일간의 기운을 바탕으로, 하늘의 에너지가 지상으로 투영되는 독특한 예술적 명조를 지녔습니다. 전체적인 사주의 흐름이 창의적인 자기표현에 집중되어 있어, 일반적인 조직 생활보다는 본인만의 전문 영역에서 빛을 발하는 스타일입니다. 특히 대인관계에서 본인만의 확고한 주관을 가지고 있으면서도 타인에게 영감을 주는 능력이 탁월하여, 시간이 흐를수록 주변의 신뢰와 명성을 동시에 얻을 수 있는 복된 기운을 지니고 있습니다."
    mus_total = f"명식 내에 <b>{max_elem}</b>의 에너지가 {counts[max_elem]}자로 가장 강하게 작용하고 있습니다. 이는 음악적으로 매우 강렬한 흡입력을 의미하며, 특히 사운드의 질감을 정교하게 다루거나 무대 위에서 대중을 압도하는 카리스마로 표출됩니다. 단순히 연주 기술에 머무는 것이 아니라, 감정의 깊은 곳을 건드리는 선율을 만들어내는 데 천부적인 소질이 있습니다. {max_elem} 기운의 특성을 살려 본인만의 장르를 개척한다면 대체 불가능한 아티스트로 자리매김할 것입니다."
    
    # 2. 선택 연도 운세 (일반/음악 이원화)
    gen_year = f"{t_year}년({t_gz}년)은 본인의 일간인 {day_gan}과 새로운 운의 흐름이 교차하며 삶의 활력이 더해지는 시기입니다. 그동안 정체되었던 문제들이 주변 조력자의 도움으로 해결의 실마리를 찾게 되며, 사회적으로 자신의 입지를 공고히 다질 수 있는 중요한 기회가 찾아옵니다. 무리한 확장보다는 내실을 기하며 다가오는 변화를 차분히 준비한다면, 연말에는 기대 이상의 성취감과 안정을 동시에 누릴 수 있는 아주 긍정적인 한 해가 될 것입니다."
    mus_year = f"음악가로서 {t_year}년은 창작의 영감이 최고조에 달하는 <span class='highlight'>'개화(開花)'</span>의 해입니다. 본인이 가진 {max_elem}의 에너지가 세운의 기운과 조화를 이루어 대중에게 깊은 인상을 남길 수 있는 결과물을 발표하기에 최적의 시기입니다. 특히 새로운 악기나 기술적 시도가 큰 성과를 거둘 것이며, 공연이나 협업을 통해 아티스트로서의 명예운이 크게 상승합니다. 자신의 감각을 믿고 적극적으로 활동 영역을 넓혀보시길 권장합니다."
    
    return gen_total, mus_total, gen_year, mus_year

# 4️⃣ 분석 및 결과 출력
if submitted:
    if not (year and month and day and hour_time_map[hour_str] is not None):
        st.warning("분석을 위해 모든 정보를 입력해주세요.")
    else:
        h = hour_time_map[hour_str]
        lunar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(year), (int(month) * -1) if is_leap else int(month), int(day), h, 0, 0)

        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
        day_gan = lunar.getDayGan()
        
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        # 타겟 연도 간지 계산
        t_lunar = Solar.fromYmd(target_year, 1, 1).getLunar()
        target_gz = t_lunar.getYearInGanZhi()
        
        g_total, m_total, g_year, m_year = get_reports(day_gan, max_elem, counts, target_year, target_gz)

        st.markdown(f"### 🍀 {name if name else '아티스트'}님의 사주 분석 및 {target_year}년 운세")
        
        # 1. 사주 명식 및 오행 분포 (이미지 스타일 준수)
        st.markdown(f"""
            <div class='saju-grid'>
                <div class='saju-box'><small>년주</small><br>{ba_zi[0]}</div>
                <div class='saju-box'><small>월주</small><br>{ba_zi[1]}</div>
                <div class='saju-box'><small>일주</small><br>{ba_zi[2]}</div>
                <div class='saju-box'><small>시주</small><br>{ba_zi[3]}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        # 2. 전체 사주 리포트
        st.markdown(f"<div class='section-card'><h2>👤 타고난 천성 및 일반 통변</h2><div class='content-text'>{g_total}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{m_total}</div></div>", unsafe_allow_html=True)
        
        # 3. 선택 연도 이원화 리포트 (추가된 부분)
        st.markdown(f"### 📅 {target_year}년({target_gz}) 심층 분석")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_year}년 일반 운세 흐름</h2><div class='content-text'>{g_year}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 {target_year}년 음악적 활동 전망</h2><div class='content-text'>{m_year}</div></div>", unsafe_allow_html=True)
