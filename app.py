import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 기본 설정
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# 디자인: 모바일 최적화 및 이원화 카드 스타일
st.markdown("""
    <style>
    .main-title { text-align: center; padding: 20px 0; color: #2D3748; }
    .report-card { background: white; padding: 25px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #edf2f6; }
    .music-card { background: #fdf2f8; border-left: 6px solid #db2777; padding: 25px; border-radius: 20px; margin-bottom: 20px; }
    .samjae-badge { display: inline-block; padding: 6px 15px; border-radius: 50px; font-weight: bold; font-size: 0.95rem; margin-bottom: 15px; text-align: center; }
    .samjae-on { background: #fff5f5; color: #c53030; border: 1px solid #feb2b2; }
    .samjae-off { background: #f0fff4; color: #2f855a; border: 1px solid #9ae6b4; }
    h2 { font-size: 1.25rem !important; color: #2d3748; margin-bottom: 15px; }
    p { line-height: 1.8; font-size: 1.05rem; color: #4a5568; text-align: justify; word-break: keep-all; }
    .highlight { color: #d53f8c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 시간 매핑 데이터
hour_time_map = {
    "05~07 묘시": 6, "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12,
    "13~15 미시": 14, "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20,
    "21~23 해시": 22, "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4
}

# 2️⃣ 입력부
with st.expander("👤 분석 대상 정보 입력", expanded=True):
    name = st.text_input("성함 또는 닉네임", value="고상현") # 스크린샷 기반 기본값
    c1, c2 = st.columns(2)
    year = c1.number_input("태어난 해", 1900, 2100, 1981)
    month = c2.number_input("월", 1, 12, 2)
    day = c1.number_input("일", 1, 31, 7)
    hour_str = c2.selectbox("태어난 시간", list(hour_time_map.keys()), index=0)
    
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    target_year = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🚀 운세 리포트 생성", use_container_width=True)

# 3️⃣ 삼재 및 통변 로직
def get_samjae_info(birth_year_ganzhi, target_year):
    animal = birth_year_ganzhi[-1]
    samjae_map = {'申子辰': '寅卯辰', '亥卯未': '巳午未', '寅午戌': '申酉戌', '巳酉丑': '亥子丑'}
    target_animal = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    
    samjae_years = next((v for k, v in samjae_map.items() if animal in k), "")
    if target_animal in samjae_years:
        status = ["들삼재", "눌삼재", "날삼재"][samjae_years.index(target_animal)]
        return f"⚠️ {target_year}년은 {status} 기간입니다.", True
    return f"✅ {target_year}년은 삼재에 해당하지 않는 평온한 해입니다.", False

# 4️⃣ 결과 출력
if submitted:
    h = hour_time_map[hour_str]
    # 날짜 처리
    if calendar_type == "양력":
        lunar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar()
    else:
        lunar = Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
    
    birth_gz = lunar.getYearInGanZhi()
    # 오류가 났던 지점(61라인 부근) 수정 완료
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    
    samjae_msg, is_samjae = get_samjae_info(birth_gz, target_year)
    badge_class = "samjae-on" if is_samjae else "samjae-off"

    st.markdown(f"### 🍀 {name}님을 위한 {target_year}년 리포트")
    st.markdown(f"<div class='samjae-badge {badge_class}'>{samjae_msg}</div>", unsafe_allow_html=True)

    # 섹션 1: 일반 인생 통변
    st.markdown(f"""
    <div class='report-card'>
        <h2>👤 {target_year}년 일반 인생 운세</h2>
        <p>올해는 당신의 삶에서 <b>안정적인 기반을 다지고 내실을 기하는 해</b>입니다. 
        주변과의 소통이 원활해지며, 그동안 노력해온 일들이 조금씩 결실을 맺기 시작하는 긍정적인 흐름이 보입니다. 
        무리한 확장보다는 현재의 위치를 공고히 하고 소중한 사람들과의 관계를 다지는 데 집중한다면, 연말에는 훨씬 더 성숙하고 안정된 자신을 발견하게 될 것입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 섹션 2: 음악적 통변
    st.markdown(f"""
    <div class='music-card'>
        <h2>🎸 {target_year}년 음악적 활동 운세</h2>
        <p>아티스트로서 {target_year}년은 <span class='highlight'>'새로운 영감의 발현'</span>이 돋보이는 시기입니다. 
        기존의 스타일을 고수하기보다 조금 더 과감한 사운드 실험이나 새로운 장르와의 결합이 큰 성과를 가져올 수 있습니다. 
        무대 위에서의 집중력이 높아지는 해이니 공연이나 창작 활동에 전념해 보세요. 
        당신만의 독창적인 감각이 대중에게 깊이 각인되어 아티스트로서 한 단계 도약하는 발판이 될 것입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 하단 데이터 숨김 처리
    with st.expander("🔍 상세 데이터 확인"):
        st.write(f"**사주 명식:** {' '.join(ba_zi)}")
        st.write(f"**기준 시간:** {hour_str}")
