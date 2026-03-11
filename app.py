import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# CSS: 스타일 및 레이아웃 설정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; margin-bottom: 10px; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 25px; border-radius: 18px; border-left: 6px solid #4A5568; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .music-card { background-color: #FDF2F8; padding: 25px; border-radius: 18px; border-left: 6px solid #D53F8C; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(213,63,140,0.1); }
    .position-card { background-color: #FFFBEB; padding: 25px; border-radius: 18px; border-left: 6px solid #D97706; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(217,119,6,0.1); }
    .target-year-card { background-color: #F0F9FF; padding: 25px; border-radius: 18px; border-left: 6px solid #3182CE; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(49,130,206,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 20px; gap: 5px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; font-size: 0.95rem; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 15px; border-radius: 15px; margin-bottom: 20px; }
    .ohaeng-item { text-align: center; flex: 1; }
    h1 { font-size: 1.8rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 15px; display: flex; align-items: center; }
    .content-text { line-height: 1.9; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.25rem; font-weight: bold; color: #B45309; margin-bottom: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 2️⃣ 시간 매핑 (이미지상의 SyntaxError 해결: 모든 따옴표 종결 확인)
hour_time_map = {
    "시간 선택": None,
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="", placeholder="성함을 입력하세요")
    c1, c2 = st.columns(2)
    year = c1.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    month = c2.number_input("출생월", 1, 12, value=None, placeholder="MM")
    day = c1.number_input("출생일", 1, 31, value=None, placeholder="DD")
    hour_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    
    col_cal, col_leap = st.columns([2, 1])
    calendar_type = col_cal.radio("달력", ["양력", "음력"], horizontal=True)
    is_leap = col_leap.checkbox("윤달 여부") if calendar_type == "음력" else False
    
    target_year = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 포지션 추천 데이터
def get_music_position(max_elem):
    pos_data = {
        '목': ("🎻 보컬 & 서정적 인스트루멘탈", "목(木)의 기운은 생명력과 성장을 의미하며 인간의 음색과 가장 닮아 있습니다. 따뜻한 울림을 주는 보컬이나 현악기 연주에서 천부적인 감각을 보이며, 서정적인 멜로디 위주의 작곡에서도 두각을 나타냅니다."),
        '화': ("🎤 프론트맨 & 퍼포머", "화(火)의 기운은 화려한 열정과 에너지의 발산을 의미합니다. 무대를 장악하는 카리스마 있는 보컬이나 화려한 리드 기타리스트에 적합하며, 대중의 시선을 사로잡는 퍼포먼스 기획에 재능이 있습니다."),
        '토': ("🎧 프로듀서 & 베이시스트", "토(土)의 기운은 전체를 조율하고 중심을 잡는 포용력입니다. 사운드 밸런스를 잡는 프로듀싱이나 편곡에 능하며, 팀의 리듬을 묵직하게 지탱하는 베이스 파트와 최상의 궁합을 자랑합니다."),
        '금': ("🎸 테크니션 & 드러머", "금(金)의 기운은 정교하고 단단한 타격감을 상징합니다. 날카로운 일렉 기타 사운드나 정확한 박자감이 요구되는 드럼 파트에서 독보적이며, 기술적인 믹싱 작업에서도 완벽주의적 면모를 보입니다."),
        '수': ("🎹 키보드 & 예술적 기획자", "수(水)의 기운은 유연한 흐름과 깊은 사유를 의미합니다. 변화무쌍한 선율을 다루는 키보드나 신디사이징에 강하며, 철학적인 작사가나 장르를 넘나드는 실험적 기획자로서 깊은 결과물을 냅니다.")
    }
    return pos_data.get(max_elem, ("All-Rounder", "모든 파트에서 조화로운 기량을 발휘하는 다재다능한 뮤지션입니다."))

# 3️⃣ 분석 실행
if submitted:
    if not (year and month and day and hour_time_map[hour_str] is not None):
        st.error("분석을 위해 모든 정보를 정확히 입력해주세요.")
    else:
        h = hour_time_map[hour_str]
        if calendar_type == "양력":
            lunar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar()
        else:
            lunar = Lunar.fromYmdHms(int(year), (int(month) * -1) if is_leap else int(month), int(day), h, 0, 0)

        # 이미지상의 ba_zi SyntaxError 해결: 리스트 괄호 종결 확인 완료
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
        day_gan = lunar.getDayGan()
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        t_gz = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()
        pos_title, pos_desc = get_music_position(max_elem)

        st.markdown(f"### 🍀 {name if name else '아티스트'}님의 심층 분석 리포트")

        # 명식 그리드
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{label}</small><br>{val}</div>" for label, val in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        # 결과 섹션 출력
        st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><span class='pos-title'>{pos_title}</span><div class='content-text'>{pos_desc}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>본인은 <b>{day_gan}</b> 일간의 기운을 바탕으로, 자신만의 확고한 예술적 심미안을 지닌 분입니다. 사주 전체의 흐름이 창의적인 자기표현에 집중되어 있어, 조직 생활보다는 전문성을 발휘할 수 있는 환경에서 큰 성취를 이룰 사주입니다.</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>명식 내에 <b>{max_elem}</b>의 기운이 강하게 자리 잡아 사운드를 다루는 감각이 매우 직관적이고 날카롭습니다. 단순히 연주 기술에 머무는 것이 아니라 감정의 심연을 건드리는 선율을 창조하는 데 천부적인 소질이 있습니다.</div></div>", unsafe_allow_html=True)

        # 선택 연도 운세 (일반/음악 이원화)
        st.markdown(f"### 📅 {target_year}년({t_gz}) 심층 분석")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ {target_year}년 일반 운세 흐름</h2><div class='content-text'>{target_year}년은 조력자의 도움으로 정체되었던 문제들이 해결의 실마리를 찾는 시기입니다. 내실을 다지며 변화를 준비한다면 연말에는 기대 이상의 성취감과 안정을 동시에 누릴 수 있는 아주 긍정적인 한 해가 될 것입니다.</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 {target_year}년 음악적 활동 전망</h2><div class='content-text'>음악적으로 {target_year}년은 창작물이 널리 퍼져나가는 '확장'의 해입니다. 앨범 발매나 대규모 공연을 기획하기에 매우 길한 운세이며, 새로운 기술적 시도가 뜻밖의 큰 성과를 거두어 아티스트로서의 명예가 상승할 것입니다.</div></div>", unsafe_allow_html=True)
