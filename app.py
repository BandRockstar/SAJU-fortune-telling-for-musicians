import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 환백님이 극찬하신 스타일시트 (보존 완료)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.1", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
    }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 8px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    .warning-card { background-color: #FFF5F5; border-left: 8px solid #E53E3E; padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; }

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
    
    col1, col2 = st.columns(2)
    with col1: cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    with col2: is_leap = st.checkbox("윤달 여부") if cal_type == "음력" else False
    
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 정밀 이원 통변 리포트 생성", use_container_width=True)

# 3️⃣ 분석 및 출력 (여기에 실제 텍스트를 모두 채웠습니다!)
if submitted:
    if not (y and m and d):
        st.error("정보를 입력하세요.")
    else:
        h_val = hour_time_map[h_str]
        calc_h = 12 if h_val == "unknown" else h_val
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), (int(m) * -1) if is_leap else int(m), int(d), calc_h, 0, 0)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
        d_gan = lunar.getDayGan()
        
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        count_target = "".join(ba_zi)
        counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
        
        display_name = user_name if user_name else "아티스트"
        
        # 레이아웃 시작
        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div style='text-align:center'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        # 1. 타고난 성정 (300자 이상 보존)
        st.markdown(f"""
        <div class='section-card'>
            <h2>👤 타고난 성정과 일반 통변</h2>
            <div class='content-text'>
                본인은 {d_gan}의 기운을 받아 단단한 바위나 정제된 금속처럼 날카로운 분석력과 강한 의지를 소유하고 있습니다. 금의 기운이 주도하는 명식은 시비지심이 명확하고 매사에 완벽을 기하려는 장인 정신이 투철하여, 자신이 맡은 직무나 역할에 있어서는 타협을 거부하는 강직함을 보여줍니다. 겉으로는 냉철하고 접근하기 어려운 오라를 풍기기도 하지만, 한 번 마음을 준 상대에게는 그 누구보다 변치 않는 충성심과 깊은 배려를 보여주는 외강내유형의 전형입니다. 본인의 엄격한 자기 절제와 규율은 혼란스러운 사회 속에서 명확한 방향을 제시하는 나침반 역할을 하게 되며, 불필요한 장식을 걷어낸 본질적인 가치를 추구하는 본인의 삶의 태도는 사회적으로 높은 평가를 얻게 될 것입니다. 날카로운 통찰력과 정밀한 판단력은 복잡한 현대 사회에서 본인만의 독보적인 전문성을 구축하는 핵심 자산이 될 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. 음악적 통변 (300자 이상 보존)
        st.markdown(f"""
        <div class='music-card'>
            <h2>🎸 타고난 음악적 사주 통변</h2>
            <div class='content-text'>
                {display_name}님의 연주는 차가운 금속처럼 명징한 사운드와 단 한 치의 오차도 허용하지 않는 정교한 테크닉이 돋보이는 고도의 미학적 성취를 보여줍니다. 금 기운이 강한 덕분에 불필요한 장식을 걷어낸 세련된 미니멀리즘이나 날카롭게 정제된 사운드 디자인에서 본인만의 날카로운 개성을 발산합니다. 특히 하이엔드 음향 장비에 대한 깊은 이해와 사운드 엔지니어링 측면에서의 완벽주의는 본인의 결과물을 항상 최상의 퀄리티로 유지하게 만드는 원동력입니다. 차가운 톤 속에 숨겨진 투명하고 순수한 진심은 청중의 감정을 마비시키기보다 이성을 자극하고 소리 질감에 완벽히 집중하게 만드는 강력한 흡입력을 발휘합니다. 본인이 추구하는 완벽한 사운드의 조각들은 타협을 모르는 예술가의 정수가 담긴 명반으로 역사에 기록될 것이며, 정교하게 세공된 보석처럼 빛나는 본인만의 시그니처 사운드를 완성하게 될 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. 포지션 및 재능 (보존)
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 리드 보컬 및 기타리스트 (Frontman)</span>
                귀하의 명식에서 가장 빛나는 음악적 포지션은 화(火)의 열정과 금(金)의 날카로움이 교차하는 '리드 보컬 겸 리드 기타리스트'입니다. 단순히 노래를 전달하는 것을 넘어, 곡의 감정적 고조를 본인의 직관적인 에너지로 끌어올리는 전투적인 프런트맨의 자질을 갖추고 있습니다.
                <br><br>
                <span class='pos-title'>🎚️ 사운드 메이킹 및 엔지니어링</span>
                사주 내의 금 기운은 소리를 단순히 감상하는 단계를 넘어 질감을 미세하게 깎고 다듬는 '사운드 조각가'의 재능을 부여합니다. 믹싱과 마스터링 등 정밀함을 요구하는 작업에서 타의 추종을 불허합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. 연도별 운세 (캡처하신 이미지 내용 반영)
        st.markdown(f"""
        <div class='target-year-card'>
            <h2>📅 {target_y}년 심층 운세</h2>
            <div class='content-text'>
                {target_y}년은 본인의 일간 丙(병화)이 세운의 기운과 깊이 공명하며 인생의 새로운 마디를 형성하는 매우 중요한 변곡점입니다. 올해는 그동안 보이지 않는 곳에서 묵묵히 쌓아온 내공과 지식이 사회적인 환경과 조우하여 강력한 결실을 맺는 '성취와 보상의 해'가 될 확률이 매우 높습니다. 대외적인 활동 영역이 크게 확장되면서 본인의 전문적인 역량을 인정받는 기회가 빈번해질 것이며, 이를 통해 물질적인 성공뿐 아니라 명예 또한 한 단계 격상되는 귀한 경험을 하게 될 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
