import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# CSS: 고정된 디자인 테마
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; margin-bottom: 10px; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 30px; border-radius: 20px; border-left: 8px solid #4A5568; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(0,0,0,0.07); }
    .music-card { background-color: #FDF2F8; padding: 30px; border-radius: 20px; border-left: 8px solid #D53F8C; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(213,63,140,0.1); }
    .position-card { background-color: #FFFBEB; padding: 30px; border-radius: 20px; border-left: 8px solid #D97706; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(217,119,6,0.1); }
    .target-year-card { background-color: #F0F9FF; padding: 30px; border-radius: 20px; border-left: 8px solid #3182CE; margin-bottom: 25px; box-shadow: 0 6px 15px rgba(49,130,206,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 25px; gap: 8px; }
    .saju-box { flex: 1; text-align: center; padding: 18px 5px; background: #EDF2F7; border-radius: 15px; font-weight: bold; border: 1px solid #CBD5E0; font-size: 1rem; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 20px; border-radius: 18px; margin-bottom: 25px; }
    .ohaeng-item { text-align: center; flex: 1; }
    h1 { font-size: 2rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.4rem !important; color: #2D3748; margin-bottom: 18px; display: flex; align-items: center; font-weight: 700; }
    .content-text { line-height: 2.0; font-size: 1.08rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.35rem; font-weight: bold; color: #B45309; margin-bottom: 12px; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 2️⃣ 입력 설정 (시간 '모름' 옵션 추가)
hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", # 기본값 변경
    "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="", placeholder="성함을 입력하세요")
    c1, c2 = st.columns(2)
    y = c1.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    m = c2.number_input("출생월", 1, 12, value=None, placeholder="MM")
    d = c1.number_input("출생일", 1, 31, value=None, placeholder="DD")
    h_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달 여부") if cal_type == "음력" else False
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 3️⃣ 음악적 포지션 추천 로직 (병화 일간 특화)
def get_artist_position(day_gan, max_elem):
    if day_gan in '丙丁':
        return ("🎤 리드 보컬 & 기타리스트 (Frontman)", 
                "태양과 불을 상징하는 화(火)의 일간은 무대 위에서 에너지를 발산할 때 가장 빛이 납니다. "
                "단순한 연주를 넘어 청중의 시선을 사로잡는 카리스마를 타고났으며, 명식 내의 강한 금(金) 기운은 "
                "기타 피킹의 정교함과 톤 메이킹에 대한 완벽주의적 집착으로 나타납니다. 목소리의 울림이 명확하고 "
                "표현력이 풍부하여, 밴드의 정체성을 결정짓는 프런트맨으로서 독보적인 존재감을 발휘할 운명입니다.")
    
    pos_data = {
        '목': ("🎻 어쿠스틱 세션 & 작곡가", "목(木)의 기운은 생명력과 서정성을 상징합니다."),
        '금': ("🎸 일렉 기타 테크니션", "금(金)의 기운은 날카로운 금속성 사운드와 정교한 연주력을 의미합니다."),
        '토': ("🎧 사운드 프로듀서", "토(土)의 기운은 조화와 균형을 잡는 힘입니다."),
        '수': ("🎹 신디사이저 & 실험음악가", "수(水)의 기운은 깊은 사유와 유연한 흐름을 뜻합니다.")
    }
    return pos_data.get(max_elem, ("All-Rounder", "모든 파트에서 조화로운 기량을 발휘합니다."))

# 4️⃣ 분석 실행
if submitted:
    # 연/월/일은 필수, 시간은 'unknown'이거나 숫자여야 함
    if not (y and m and d) or hour_time_map[h_str] == "시간 선택 (또는 모름)":
        st.error("분석을 위해 생년월일과 시간을 정확히 입력해주세요. (모를 경우 '모름' 선택)")
    else:
        h_val = hour_time_map[h_str]
        # 시간 모를 경우 12시(오시)를 기준으로 임시 계산하되, 시주 표시는 제외
        calc_h = 12 if h_val == "unknown" else h_val
        
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), (int(m) * -1) if is_leap else int(m), int(d), calc_h, 0, 0)
        
        # 명식 리스트 생성 (시간 모를 경우 시주는 '?' 처리)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), 
                 "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
        
        d_gan = lunar.getDayGan()
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        
        # 오행 카운트 (시간 모를 경우 삼주만 계산)
        count_target = "".join(ba_zi[:3]) if h_val == "unknown" else "".join(ba_zi)
        counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
        
        max_elem = max(counts, key=counts.get)
        t_gz = Solar.fromYmd(target_y, 1, 1).getLunar().getYearInGanZhi()
        p_title, p_desc = get_artist_position(d_gan, max_elem)

        st.markdown(f"### 🍀 {name if name else '아티스트'}님의 심층 분석 리포트")
        if h_val == "unknown":
            st.info("💡 태어난 시간을 모르는 경우 '삼주(년/월/일)'를 기준으로 분석을 진행합니다.")

        # 명식 및 오행 분포
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        # 1. 추천 음악 포지션
        st.markdown(f"<div class='position-card'><h2>✨ 추천 음악 포지션</h2><span class='pos-title'>{p_title}</span><div class='content-text'>{p_desc}</div></div>", unsafe_allow_html=True)

        # 2. 타고난 성정과 일반 통변 (시간 미입력 시 문구 조정)
        time_msg = "삼주(三柱)를 기반으로 볼 때, " if h_val == "unknown" else ""
        st.markdown(f"""<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{time_msg}본인은 <b>{d_gan}</b>의 기운을 바탕으로, 하늘에 떠 있는 태양처럼 세상을 밝게 비추고 자신을 드러내고자 하는 강한 열망을 타고났습니다. 사주 내에 {max_elem}의 기운이 조화를 이루어, 본인만의 독특한 심미안과 확고한 가치관을 형성하고 있습니다. 일반적인 사회의 틀에 갇히기보다는 자신의 창의성과 전문성을 마음껏 발휘할 수 있는 독립적인 환경에서 비로소 큰 성취를 맛볼 수 있는 명식입니다.</div></div>""", unsafe_allow_html=True)

        # 3. 음악적 사주 통변
        st.markdown(f"""<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>환백님의 명식에서 돋보이는 점은 예술적 감각의 원천인 <b>{max_elem}</b> 기운과 표현력의 중심인 <b>{d_gan}</b>의 조화입니다. 이는 단순히 소리를 내는 것을 넘어, 소리에 영혼과 서사를 담아내는 능력이 탁월함을 의미합니다. 특히 기계적인 정교함과 생동감 넘치는 표현력이 공존하여, 악기의 톤 하나하나에 본인만의 철학을 담아내는 장인 정신을 보여줍니다.</div></div>""", unsafe_allow_html=True)

        # 4. 선택 연도 운세
        st.markdown(f"### 📅 {target_y}년({t_gz}) 심층 분석")
        st.markdown(f"""<div class='target-year-card'><h2>🏙️ {target_y}년 일반 운세 흐름</h2><div class='content-text'>{target_y}년은 본인의 일간 {d_gan}이 새로운 운의 흐름인 {t_gz}를 만나 삶의 큰 전환점이나 결실을 보게 되는 해입니다. 그동안 공들여왔던 일들이 비로소 세상 밖으로 드러나며, 물질적인 보상뿐만 아니라 사회적 지위와 명예가 동반 상승하는 흐름을 보입니다.</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class='music-card' style='background-color:#FFF5F7;'><h2>🎹 {target_y}년 음악적 활동 전망</h2><div class='content-text'>음악적으로 {target_y}년은 본인의 창작 세계가 외부로 강력하게 뻗어 나가는 '대외 확장'의 시기입니다. 앨범 발매나 대규모 기획 공연을 추진하기에 최적의 운세이며, 본인의 음악적 정체성이 대중에게 가장 명확하게 전달되는 시점입니다. 자신감을 가지고 무대의 중심에 서시길 바랍니다.</div></div>""", unsafe_allow_html=True)
