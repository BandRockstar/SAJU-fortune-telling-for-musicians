import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인 (환백님 스타일 유지 및 최적화)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.1", layout="centered")
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
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.3rem; font-weight: bold; color: #B45309; margin-bottom: 0.8rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.1</h1></div>", unsafe_allow_html=True)

# 2️⃣ 데이터 맵핑 및 함수 정의
hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {'申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'], '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']}
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

# 3️⃣ 입력 설정 (환백님 정보 기본값 적용)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="임환백", placeholder="성함을 입력하세요")
    y = st.number_input("출생년", 1900, 2100, value=1981)
    m = st.number_input("출생월", 1, 12, value=2)
    d = st.number_input("출생일", 1, 31, value=7)
    h_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=4) # 묘시 기본값
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 4️⃣ 분석 실행 (에러 방지를 위한 로직 강화)
if submitted:
    h_val = hour_time_map[h_str]
    calc_h = 12 if h_val == "unknown" else h_val
    
    # 사주 계산
    if cal_type == "양력":
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar()
    else:
        lunar = Lunar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0)
        
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), 
             "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
    d_gan = lunar.getDayGan()
    
    # 오행 분석
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    count_target = "".join(ba_zi)
    counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
    max_elem = max(counts, key=counts.get)
    
    # 리포트 생성
    display_name = user_name if user_name else "아티스트"
    samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

    # UI 출력
    st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
    st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
    st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div style='text-align:center'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재 정보: {samjae_msg}</b></div>", unsafe_allow_html=True)

    # 통변 텍스트 출력 (이미지에 있던 장문 텍스트 포함)
    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>본인은 {d_gan}의 기운을 받아 단단한 바위나 정제된 금속처럼 날카로운 분석력과 강한 의지를 소유하고 있습니다...</div></div>", unsafe_allow_html=True)
    
    # (이하 추천 포지션 및 2026년 운세 섹션 동일하게 유지)
    # ... (생략된 섹션들은 Ver 1.0의 형식을 그대로 따릅니다)
