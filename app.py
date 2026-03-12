import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 CSS (원본 디자인 유지)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #2D3748; text-align: justify; word-break: keep-all; }
    .section-card, .music-card, .target-year-card { padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FFF5F7; border-left: 8px solid #D53F8C; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 2rem; gap: 10px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #F7FAFC; border-radius: 15px; border: 1px solid #E2E8F0; font-weight: bold; }
    .saju-label { font-size: 0.8rem; color: #718096; margin-bottom: 5px; }
    .saju-ganji { font-size: 1.2rem; color: #1A202C; }
    </style>
    """, unsafe_allow_html=True)

# 2️⃣ 데이터 로직 (연도 변동 계산기)
def get_year_gan(year_num):
    # 입력된 연도를 십간으로 변환 (정확한 사실 기반)
    stems = ["경", "신", "임", "계", "갑", "을", "병", "정", "무", "기"]
    return stems[year_num % 10]

def get_saju_relation(me, target):
    # 일간(병화) 기준 십신 매칭
    relations = {
        "丙": {"갑": "편인", "을": "정인", "병": "비견", "정": "겁재", "무": "식신", "기": "상관", "경": "편재", "신": "정재", "임": "편관", "계": "정관"}
    }
    return relations.get(me, {}).get(target, "운세")

# 3️⃣ 입력부 (캡처 화면의 입력창 구조)
st.title("🔮 음악인을 위한 사주통변")
with st.expander("📝 정보 입력", expanded=True):
    u_name = st.text_input("이름", value="임환백")
    c1, c2, c3 = st.columns(3)
    with c1: u_y = st.number_input("년", 1900, 2100, 1981)
    with c2: u_m = st.number_input("월", 1, 12, 2)
    with c3: u_d = st.number_input("일", 1, 31, 7)
    u_h = st.slider("시간 (0~23시)", 0, 23, 6)
    u_cal = st.radio("달력", ["양력", "음력"], horizontal=True)
    
    # 🎯 핵심: 이 변수가 아래 결과창의 연도를 결정합니다.
    selected_year = st.number_input("조회 연도", 1900, 2100, 2026)

# 4️⃣ 결과 출력부 (입력 연도 연동 수정)
if st.button("사주 분석 실행"):
    if u_cal == "양력":
        lunar = Solar.fromYmdHms(u_y, u_m, u_d, u_h, 0, 0).getLunar()
    else:
        lunar = Lunar.fromYmdHms(u_y, u_m, u_d, u_h, 0, 0, False)
    
    eight = lunar.getEightChar()
    d_gan = eight.getDay()[0] # 일간 추출

    # 🎯 변동 로직 적용
    target_gan = get_year_gan(selected_year)
    target_god = get_saju_relation(d_gan, target_gan)

    # 사주 명식 그리드 디자인 유지
    st.markdown(f"""
    <div class='saju-grid'>
        <div class='saju-box'><div class='saju-label'>년주</div><div class='saju-ganji'>{eight.getYear()}</div></div>
        <div class='saju-box'><div class='saju-label'>월주</div><div class='saju-ganji'>{eight.getMonth()}</div></div>
        <div class='saju-box'><div class='saju-label'>일주</div><div class='saju-ganji'>{eight.getDay()}</div></div>
        <div class='saju-box'><div class='saju-label'>시주</div><div class='saju-ganji'>{eight.getTime()}</div></div>
    </div>
    
    <div class='target-year-card'>
        <h3>🏙️ {selected_year}년 ({target_gan}년) 심층 운세 - {target_god}운</h3>
        <div class='content-text'>
            <b>{selected_year}년은 귀하에게 {target_god}의 기운이 작용하는 해입니다.</b><br>
            입력하신 {selected_year}년에 해당하는 {target_gan}년의 기운은 귀하의 {d_gan}화와 만나... 
            (이 부분에 {target_god}에 맞는 300자 이상의 데이터를 매칭하십시오)
        </div>
    </div>
    """, unsafe_allow_html=True)
