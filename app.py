import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 모바일 최적화 UI 디자인
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    html { font-size: 14px; }
    @media (min-width: 600px) { html { font-size: 16px; } }

    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
    }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 8px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    
    .samjae-active { background-color: #FEF2F2; border: 2px solid #EF4444; color: #991B1B; padding: 1.5rem; border-radius: 1.2rem; margin-bottom: 1.5rem; }
    .samjae-inactive { background-color: #F0FDF4; border: 2px solid #22C55E; color: #166534; padding: 1.5rem; border-radius: 1.2rem; margin-bottom: 1.5rem; }

    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 1.5rem; gap: 8px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 20px; border-radius: 15px; margin-bottom: 1.5rem; }
    
    h1 { font-size: 1.8rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 1.2rem; font-weight: 700; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.3rem; font-weight: bold; color: #B45309; margin-bottom: 0.8rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

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
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 3️⃣ 삼재 계산 함수
def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {
        '申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '미'],
        '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']
    }
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

# 4️⃣ 초장문 통변 엔진
def get_ultra_report(d_gan, max_elem, name):
    gen_data = {
        '목': f"본인은 {d_gan}의 정기를 타고나 만물을 소생시키는 생명력과 따뜻한 인정을 지닌 성품을 소유하고 있습니다...",
        '화': f"본인은 {d_gan}의 정기를 받아 태양처럼 뜨겁고 화려하며 열정적인 기질의 소유자입니다...",
        '토': f"본인은 {d_gan}의 기운을 품어 드넓은 대지처럼 모든 것을 수용하는 포용력이 남다른 명식입니다...",
        '금': f"본인은 {d_gan}의 기운을 받아 단단한 바위처럼 날카로운 분석력과 강한 의지를 소유하고 있습니다...",
        '수': f"본인은 {d_gan}의 성정을 타고나 깊은 샘물처럼 유연하고 지혜로운 통찰력을 지니고 있습니다..."
    }
    mus_data = {
        '목': f"{name}님의 음악 세계는 서사적인 선율과 따뜻한 리듬감이 완벽하게 조화를 이룹니다...",
        '화': f"{name}님의 음악은 무대 위에서 폭발하는 압도적인 카리스마가 결합한 열정의 결정체입니다...",
        '토': f"{name}님의 음악적 기반은 사운드의 완벽한 밸런스와 안정적인 구조미에 있습니다...",
        '금': f"{name}님의 연주는 차가운 금속처럼 명징한 사운드와 정교한 테크닉이 돋보입니다...",
        '수': f"{name}님의 음악적 지평은 현실을 넘어 몽환적이고 깊은 공간감을 지니고 있습니다..."
    }
    return gen_data.get(max_elem, ""), mus_data.get(max_elem, "")

# 5️⃣ 결과 출력
if submitted:
    if not (y and m and d) or h_str == "시간 선택 (또는 모름)":
        st.error("생년월일과 시간을 정확히 입력해주세요.")
    else:
        h_val = hour_time_map[h_str]
        calc_h = 12 if h_val == "unknown" else h_val
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), (int(m) * -1) if is_leap else int(m), int(d), calc_h, 0, 0)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
        d_gan = lunar.getDayGan()
        
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        count_target = "".join(ba_zi[:3]) if h_val == "unknown" else "".join(ba_zi)
        counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        display_name = user_name if user_name else "아티스트"
        gen_text, mus_text = get_ultra_report(d_gan, max_elem, display_name)
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b><br><small>삼재는 9년마다 돌아오는 3년의 조심하는 시기를 뜻합니다.</small></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)

        # -------------------------------------------------------------------
        # ✨ [초장문 업데이트] 추천 음악 포지션 및 전문 재능 섹션
        # -------------------------------------------------------------------
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 리드 보컬 및 기타리스트 (Frontman)</span>
                귀하의 명식에서 가장 빛나는 음악적 포지션은 화(火)의 폭발적인 에너지와 금(金)의 날카로운 정밀함이 교차하는 지점인 '리드 보컬 겸 리드 기타리스트'입니다. 
                화 기운은 태양처럼 자신을 만천하에 드러내고자 하는 강렬한 표출력을 상징하며, 이는 무대 위에서 청중의 시선을 단숨에 사로잡는 보컬의 성량과 무대 장악력으로 치환됩니다. 
                단순히 노래를 전달하는 것에 그치지 않고, 곡의 감정적 고조를 본인의 직관적인 에너지를 통해 극적으로 끌어올리는 천부적인 프런트맨의 자질을 갖추고 있습니다. 
                여기에 금 기운의 정교한 결단력이 더해져, 감정에만 휩쓸리지 않고 기술적으로 완벽하게 제어된 기타 연주를 동시에 수행할 수 있는 능력을 보여줍니다. 
                이러한 이원적 재능의 결합은 밴드의 음악적 중심을 잡는 동시에 대중적 흡인력을 극대화하는 독보적인 존재감을 형성하며, 무대의 가장 밝은 곳에서 비로소 아티스트로서의 완전한 자아를 실현하게 만들 것입니다.
                <br><br>
                <span class='pos-title'>🎚️ 사운드 메이킹 및 엔지니어링</span>
                사주 내에 두드러지는 금(金)의 기운은 소리를 단순히 감상하는 단계를 넘어, 소리의 질감을 미세하게 깎고 다듬어 최상의 결과물을 도출해내는 '사운드 조각가'로서의 재능을 부여합니다. 
                이러한 금 기운의 완벽주의적 속성은 믹싱, 마스터링, 이펙터 사운드 디자인 등 고도의 집중력과 청각적 예민함을 요구하는 엔지니어링 작업에서 타의 추종을 불허하는 전문성으로 나타납니다. 
                불필요한 노이즈를 걷어내고 악기 간의 주파수 간섭을 본능적으로 조율하며, 곡의 의도에 가장 부합하는 명징하고 세련된 톤을 찾아내는 데 탁월한 두각을 나타냅니다. 
                단순히 연주를 기록하는 차원을 넘어 소리의 공간감과 질감을 설계하는 프로듀싱 감각은 본인의 창작물을 상업적·예술적 완성도가 높은 하이엔드 퀄리티로 유지하게 만드는 핵심적인 원동력입니다. 
                이러한 기술적 정밀함은 아티스트로서 본인이 추구하는 예술적 이상향을 현실적인 소리로 완벽하게 구현해내는 강력한 무기가 되어줄 것입니다.
                <br><br>
                <span class='pos-title'>🎯 음악적 성향: 완벽주의적 표현</span>
                예술적 자아에 있어서 귀하는 타협을 거부하는 확고한 주관과 디테일한 부분까지 집요하게 파고드는 완벽주의적 성향을 지니고 있습니다. 
                화(火)의 뜨거운 창조적 영감이 떠오르면, 금(金)의 차가운 이성이 이를 분석하고 정제하여 한 점의 오차도 없는 예술적 결과물로 만들어내야만 직성이 풀리는 기질입니다. 
                연주에 있어서는 단 하나의 음표 처리나 소리의 잔향까지도 본인이 설계한 의도에 정확히 부합해야 하며, 이러한 철저함이 때로는 스스로를 고되게 할 수 있으나 결과적으로는 대중과 평단으로부터 높은 신뢰를 얻는 명반을 탄생시키는 근간이 됩니다. 
                자신만의 독창적인 음악적 문법을 고수하려는 독립심은 유행에 휩쓸리지 않는 독보적인 음악 세계를 구축하게 하며, 시간이 흘러도 가치가 변하지 않는 견고한 사운드 정체성을 확립하게 할 것입니다. 
                이러한 완벽주의는 본인이 추구하는 예술적 진실성을 담보하는 가장 중요한 가치이며, 이를 통해 누구도 흉내 낼 수 없는 본인만의 독창적인 예술적 지평을 넓혀가게 될 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 📅 연도별 운세
        st.markdown(f"### 📅 {target_y}년 심층 운세")
        st.markdown(f"<div class='target-year-card'><h2>🏙️ 일반 운세 흐름</h2><div class='content-text'>{target_y}년은 본인의 일간 {d_gan}이 세운의 기운과 깊이 공명하며 인생의 새로운 마디를 형성하는 매우 중요한 변곡점입니다...</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 음악적 흐름 이야기</h2><div class='content-text'>예술가로서 {target_y}년은 본인만의 독보적인 '사운드 정체성'이 대중에게 가장 강렬하게 각인되는 확장의 시기입니다...</div></div>", unsafe_allow_html=True)
