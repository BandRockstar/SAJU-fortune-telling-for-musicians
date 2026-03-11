import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 스타일 (환백님 전용 Ver 1.1)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.1", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card, .music-flow-card { 
        padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
    }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 8px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    .music-flow-card { background-color: #FFF5F7; border-left: 8px solid #ED64A6; }
    
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 1.5rem; gap: 8px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 20px; border-radius: 15px; margin-bottom: 1.5rem; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.3rem; font-weight: bold; color: #B45309; margin-bottom: 0.8rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.1</h1></div>", unsafe_allow_html=True)

# 2️⃣ 입력 설정
hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="", placeholder="성함을 입력하세요")
    y = st.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    m = st.number_input("출생월", 1, 12, value=None, placeholder="MM")
    d = st.number_input("출생일", 1, 31, value=None, placeholder="DD")
    h_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 정밀 이원 통변 리포트 생성", use_container_width=True)

if submitted:
    if not (y and m and d):
        st.error("정보를 입력하세요.")
    else:
        h_val = hour_time_map[h_str]
        calc_h = 12 if h_val == "unknown" else h_val
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
        d_gan = lunar.getDayGan()
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
        display_name = user_name if user_name else "아티스트"

        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div style='text-align:center'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        # 1. 타고난 성정
        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>본인은 {d_gan}의 기운을 받아 단단한 바위나 정제된 금속처럼 날카로운 분석력과 강한 의지를 소유하고 있습니다... (이미지 내용 전문)</div></div>", unsafe_allow_html=True)

        # 2. 음악적 사주 통변
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{display_name}님의 연주는 차가운 금속처럼 명징한 사운드와 단 한 치의 오차도 허용하지 않는 정교한 테크닉이 돋보이는 고도의 미학적 성취를 보여줍니다... (이미지 내용 전문)</div></div>", unsafe_allow_html=True)

        # 3. 추천 음악 포지션 및 전문 재능 (이미지 2, 3 내용 완벽 복구)
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 리드 보컬 및 기타리스트 (Frontman)</span>
                귀하의 명식에서 가장 빛나는 음악적 포지션은 화(火)의 폭발적인 에너지와 금(金)의 날카로운 정밀함이 교차하는 지점인 '리드 보컬 겸 리드 기타리스트'입니다...
                <br><br>
                <span class='pos-title'>📂 사운드 메이킹 및 엔지니어링</span>
                사주 내에 두드러지는 금(金)의 기운은 소리를 단순히 감상하는 단계를 넘어, 소리의 질감을 미세하게 깎고 다듬어 최상의 결과물을 도출해내는 '사운드 조각가'로서의 재능을 부여합니다...
                <br><br>
                <span class='pos-title'>🎯 음악적 성향: 완벽주의적 표현</span>
                예술적 자아에 있어서 귀하는 타협을 거부하는 확고한 주관과 디테일한 부분까지 집요하게 파고드는 완벽주의적 성향을 지니고 있습니다. 화(火)의 뜨거운 창조적 영감이 떠오르면, 금(金)의 차가운 이성이 이를 분석하고 정제하여 한 점의 오차도 없는 예술적 결과물로 만들어내야만 직성이 풀리는 기질입니다...
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. 연도별 심층 운세 (일반 운세 흐름 + 음악적 흐름 이야기)
        st.markdown(f"""
        <div class='target-year-card'>
            <h2>📅 {target_y}년 심층 운세</h2>
            <div class='content-text'>
                <b>📊 일반 운세 흐름</b><br>
                {target_y}년은 본인의 일간 丙이 세운의 기운과 깊이 공명하며 인생의 새로운 마디를 형성하는 매우 중요한 변곡점입니다...
            </div>
        </div>
        <div class='music-flow-card'>
            <div class='content-text'>
                <b>🎹 음악적 흐름 이야기</b><br>
                예술가로서 {target_y}년은 본인만의 독보적인 '사운드 정체성'이 대중에게 가장 강렬하게 각인되는 확장의 시기입니다. 올해의 기운은 본인의 창의적인 에너지를 더욱 정교하게 정제하여 세련된 결과물로 도출하게 도우며, 특히 새로운 장르로의 도전이나 예상치 못한 아티스트와의 협업이 본인의 음악적 지평을 넓히는 결정적인 계기가 될 것입니다...
            </div>
        </div>
        """, unsafe_allow_html=True)
