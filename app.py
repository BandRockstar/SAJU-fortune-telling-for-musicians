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
    stems = ["경", "신", "임", "계", "갑", "을", "병", "정", "무", "기"]
    return stems[year_num % 10]

def get_saju_relation(me, target):
    relations = {
        "丙": {"갑": "편인", "을": "정인", "병": "비견", "정": "겁재", "무": "식신", "기": "상관", "경": "편재", "신": "정재", "임": "편관", "계": "정관"}
    }
    return relations.get(me, {}).get(target, "운세")

# 3️⃣ 입력부 (모든 위젯에 key를 부여하여 상태 변화를 감지)
st.title("🔮 음악인을 위한 사주통변")
with st.expander("📝 정보 입력", expanded=True):
    u_name = st.text_input("이름", value="임환백")
    c1, c2, c3 = st.columns(3)
    # key 설정을 통해 값이 변할 때마다 Streamlit이 이를 인지하게 합니다.
    with c1: u_y = st.number_input("년", 1900, 2100, 1981, key="input_y")
    with c2: u_m = st.number_input("월", 1, 12, 2, key="input_m")
    with c3: u_d = st.number_input("일", 1, 31, 7, key="input_d")
    u_h = st.slider("시간 (0~23시)", 0, 23, 6, key="input_h")
    u_cal = st.radio("달력", ["양력", "음력"], horizontal=True, key="input_cal")
    
    # 이 부분이 바뀌면 아래 결과도 즉시 바뀌어야 함
    target_y = st.number_input("조회 연도", 1900, 2100, 2026, key="target_y_val")

# 4️⃣ 결과 출력부 (입력 연도 및 달력 정보 실시간 연동)
if st.button("사주 분석 실행"):
    # 입력받은 위젯의 최신 값(key)을 사용하여 사주 명식 추출
    if u_cal == "양력":
        lunar = Solar.fromYmdHms(u_y, u_m, u_d, u_h, 0, 0).getLunar()
    else:
        # 음력 선택 시 윤달 여부 등 입력된 최신 상태 반영
        lunar = Lunar.fromYmdHms(u_y, u_m, u_d, u_h, 0, 0, False)
    
    eight = lunar.getEightChar()
    d_gan = eight.getDay()[0]

    # 🎯 핵심: 사용자가 입력한 target_y_val을 직접 연산에 사용
    t_gan = get_year_gan(target_y)
    t_god = get_saju_relation(d_gan, t_gan)

    st.markdown(f"""
    <div class='saju-grid'>
        <div class='saju-box'><div class='saju-label'>년주</div><div class='saju-ganji'>{eight.getYear()}</div></div>
        <div class='saju-box'><div class='saju-label'>월주</div><div class='saju-ganji'>{eight.getMonth()}</div></div>
        <div class='saju-box'><div class='saju-label'>일주</div><div class='saju-ganji'>{eight.getDay()}</div></div>
        <div class='saju-box'><div class='saju-label'>시주</div><div class='saju-ganji'>{eight.getTime()}</div></div>
    </div>
    
    <div class='target-year-card'>
        <h3>🏙️ {target_y}년 ({t_gan}년) 심층 운세 - {t_god}운</h3>
        <div class='content-text'>
            <b>{target_y}년은 귀하에게 {t_god}의 기운이 작용하는 해입니다.</b><br>
            선택하신 {u_cal} 생년월일을 바탕으로 분석한 결과, {target_y}년의 {t_gan}기운은 귀하의 {d_gan}화와 상호작용하여...
            (여기에 {t_god}에 최적화된 300자 이상의 데이터를 매칭합니다)
        </div>
    </div>
    """, unsafe_allow_html=True)
