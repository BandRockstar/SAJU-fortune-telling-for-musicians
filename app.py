import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# CSS: 가독성 및 디자인 최적화
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; margin-bottom: 10px; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 25px; border-radius: 18px; border-left: 6px solid #4A5568; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .music-card { background-color: #FDF2F8; padding: 25px; border-radius: 18px; border-left: 6px solid #D53F8C; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(213,63,140,0.1); }
    .position-card { background-color: #FFFBEB; padding: 25px; border-radius: 18px; border-left: 6px solid #D97706; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(217,119,6,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 20px; gap: 5px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; font-size: 0.95rem; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 15px; border-radius: 15px; margin-bottom: 20px; }
    .ohaeng-item { text-align: center; flex: 1; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 15px; display: flex; align-items: center; }
    .content-text { line-height: 1.9; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.25rem; font-weight: bold; color: #B45309; margin-bottom: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 2️⃣ 입력 설정 (Syntax 검수 완료)
hour_time_map = {
    "시간 선택": None, "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 입력", expanded=True):
    name = st.text_input("성함", value="", placeholder="성함을 입력하세요")
    c1, c2 = st.columns(2)
    y = c1.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    m = c2.number_input("출생월", 1, 12, value=None, placeholder="MM")
    d = c1.number_input("출생일", 1, 31, value=None, placeholder="DD")
    h_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달") if cal_type == "음력" else False
    target_y = st.number_input("분석 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 분석 시작", use_container_width=True)

# 3️⃣ 정교화된 파트 추천 엔진 (일간 중심)
def get_refined_position(day_gan, max_elem):
    # 화(火) 일간은 기본적으로 보컬/프런트맨 기질이 강함
    if day_gan in '丙丁':
        return ("🎤 리드 보컬 & 프런트맨", "화(火) 일간은 무대 위에서 스스로를 발산하며 에너지를 전파하는 능력이 탁월합니다. 명식 내 강한 금(金) 기운은 목소리의 명징함과 정교한 톤 제어 능력을 더해주어, 관객의 귀를 사로잡는 압도적인 보컬리스트로서의 자질을 부여합니다.")
    
    # 그 외 오행 기반 추천
    pos_map = {
        '목': ("🎸 기타리스트 (어쿠스틱/일렉)", "목(木)의 유연함은 현악기의 선율을 다루는 감각으로 발현됩니다."),
        '금': ("🎸 테크니션 (일렉기타/드럼)", "금(金)의 정교함은 정확한 타격과 금속성 사운드를 다루는 데 최적입니다."),
        '토': ("🎧 프로듀서 & 베이시스트", "토(土)의 중재력은 사운드의 중심을 잡는 능력을 의미합니다."),
        '수': ("🎹 키보디스트 & 작곡가", "수(水)의 유연함은 풍부한 건반 선율과 깊은 서사를 만들어냅니다.")
    }
    return pos_map.get(max_elem, ("All-Rounder", "다재다능한 예술가입니다."))

# 4️⃣ 분석 및 출력
if submitted:
    if not (y and m and d and hour_time_map[h_str] is not None):
        st.error("모든 정보를 입력해주세요.")
    else:
        h = hour_time_map[h_str]
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), (int(m) * -1) if is_leap else int(m), int(d), h, 0, 0)
        
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
        d_gan = lunar.getDayGan()
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
        max_e = max(counts, key=counts.get)
        p_title, p_desc = get_refined_position(d_gan, max_e)

        st.markdown(f"### 🍀 {name if name else '아티스트'}님의 리포트")
        st.markdown(f"<div class='saju-grid'>" + "".join([f"<div class='saju-box'>{b}</div>" for b in ba_zi]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><span class='pos-title'>{p_title}</span><div class='content-text'>{p_desc}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-card'><h2>👤 일반 통변</h2><div class='content-text'>{d_gan}일간으로 태어나 예술적 자기표현 욕구가 강합니다.</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 음악적 통변</h2><div class='content-text'>{max_e}의 기운을 활용한 독창적인 작업 방식이 길합니다.</div></div>", unsafe_allow_html=True)
