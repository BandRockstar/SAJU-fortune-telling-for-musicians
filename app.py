import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 CSS 디자인 (원본 유지)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #2D3748; text-align: justify; word-break: keep-all; }
    .section-card, .music-card, .position-card, .target-year-card { padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FFF5F7; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #F0FFF4; border-left: 8px solid #38A169; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 2rem; gap: 10px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #F7FAFC; border-radius: 15px; border: 1px solid #E2E8F0; font-weight: bold; }
    .saju-label { font-size: 0.8rem; color: #718096; margin-bottom: 5px; }
    .saju-ganji { font-size: 1.2rem; color: #1A202C; }
    </style>
    """, unsafe_allow_html=True)

# 2️⃣ 데이터 로직 (연도 변동 수식만 정확히 추가)
def get_target_year_gan(t_year):
    # 연도 숫자를 천간으로 변환하는 정확한 수식
    stems = ["경", "신", "임", "계", "갑", "을", "병", "정", "무", "기"]
    return stems[t_year % 10]

def get_ten_god_data(day_gan, target_gan):
    # 일간(나)과 연도 기운의 관계를 계산
    relations = {
        "丙": {"갑": "편인", "을": "정인", "병": "비견", "정": "겁재", "무": "식신", "기": "상관", "경": "편재", "신": "정재", "임": "편관", "계": "정관"}
    }
    return relations.get(day_gan, {}).get(target_gan, "운세")

# 3️⃣ 입력부 (원본 그대로 유지)
st.title("🔮 음악인을 위한 사주통변")
with st.expander("📝 정보 입력", expanded=True):
    u_name = st.text_input("이름", value="임환백")
    c1, c2, c3 = st.columns(3)
    with c1: u_y = st.number_input("년", 1900, 2100, 1981)
    with c2: u_m = st.number_input("월", 1, 12, 2)
    with c3: u_d = st.number_input("일", 1, 31, 7)
    u_h = st.slider("시간 (0~23시)", 0, 23, 6)
    u_cal = st.radio("달력", ["양력", "음력"], horizontal=True)
    target_y = st.number_input("조회 연도", 1900, 2100, 2026)

# 4️⃣ 분석 및 결과 (변동 로직 적용)
if st.button("사주 분석 실행"):
    if u_cal == "양력":
        lunar = Solar.fromYmdHms(u_y, u_m, u_d, u_h, 0, 0).getLunar()
    else:
        lunar = Lunar.fromYmdHms(u_y, u_m, u_d, u_h, 0, 0, False)
    
    eight = lunar.getEightChar()
    y_gz, m_gz, d_gz, t_gz = eight.getYear(), eight.getMonth(), eight.getDay(), eight.getTime()
    d_gan = d_gz[0]

    # 🎯 핵심 수정: 조회 연도(target_y)에 따라 변동되도록 설정
    t_gan = get_target_year_gan(target_y)
    t_god = get_ten_god_data(d_gan, t_gan)

    st.markdown(f"""
    <div class='saju-grid'>
        <div class='saju-box'><div class='saju-label'>년주</div><div class='saju-ganji'>{y_gz}</div></div>
        <div class='saju-box'><div class='saju-label'>월주</div><div class='saju-ganji'>{m_gz}</div></div>
        <div class='saju-box'><div class='saju-label'>일주</div><div class='saju-ganji'>{d_gz}</div></div>
        <div class='saju-box'><div class='saju-label'>시주</div><div class='saju-ganji'>{t_gz}</div></div>
    </div>

    <div class='section-card'>
        <h3>👤 타고난 성정과 일반 통변</h3>
        <div class='content-text'>
            귀하는 {d_gan}화의 기운을 바탕으로 예술적 열정을 지닌 아티스트입니다. {d_gz}의 특성은...
        </div>
    </div>
    
    <div class='target-year-card'>
        <h3>🏙️ {target_y}년 ({t_gan}년) 심층 운세 - {t_god}운</h3>
        <div class='content-text'>
            <b>{target_y}년은 귀하에게 {t_god}의 기운이 작용하는 해입니다.</b><br>
            이 해에는 {t_god}의 특성에 따라 음악적 환경과 사회적 관계에서 뚜렷한 변화가 나타납니다. 
            (여기에 {t_god}별 300자 이상의 고정 데이터를 매칭하여 출력합니다.)
        </div>
    </div>
    """, unsafe_allow_html=True)
