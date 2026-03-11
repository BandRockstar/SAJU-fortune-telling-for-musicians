import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# 모바일 최적화 스타일
st.markdown("""
    <style>
    .report-card { background: white; padding: 22px; border-radius: 18px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f2f6; }
    .music-card { background: #fdf2f8; border-left: 6px solid #db2777; padding: 22px; border-radius: 18px; margin-bottom: 20px; }
    .samjae-badge { display: inline-block; padding: 5px 12px; border-radius: 50px; font-weight: bold; font-size: 0.9rem; margin-bottom: 10px; }
    .samjae-on { background: #fff5f5; color: #c53030; border: 1px solid #feb2b2; }
    .samjae-off { background: #f0fff4; color: #2f855a; border: 1px solid #9ae6b4; }
    h2 { font-size: 1.2rem !important; color: #2d3748; margin-bottom: 10px; }
    p { line-height: 1.8; font-size: 1rem; color: #4a5568; text-align: justify; word-break: keep-all; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🎸 음악인을 위한 사주통변</h1>", unsafe_allow_html=True)

# 시간 매핑
hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 1️⃣ 입력부
with st.expander("📝 사주 정보 및 분석 연도 설정", expanded=True):
    name = st.text_input("성함", value="임환백")
    c1, c2 = st.columns(2)
    year = c1.number_input("출생년", 1900, 2100, 1981)
    month = c2.number_input("출생월", 1, 12, 2)
    day = c1.number_input("출생일", 1, 31, 7)
    hour_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=3) # 시간 입력 부활
    
    cal_type = st.radio("달력 종류", ["양력", "음력"], horizontal=True)
    target_year = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🚀 심층 리포트 생성", use_container_width=True)

# 2️⃣ 삼재 계산기
def check_samjae(birth_year_gz, target_year):
    animal = birth_year_gz[-1]
    groups = {'申子辰': '寅卯辰', '亥卯未': '巳午未', '寅午戌': '申酉戌', '巳酉丑': '亥子丑'}
    target_animal = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    
    samjae_years = next((v for k, v in groups.items() if animal in k), "")
    if target_animal in samjae_years:
        status = ["들삼재", "눌삼재", "날삼재"][samjae_years.index(target_animal)]
        return f"⚠️ {target_year}년은 {status} 기간입니다.", True
    return f"✅ {target_year}년은 삼재에 해당하지 않습니다.", False

# 3️⃣ 출력부
if submitted:
    h = hour_time_map[hour_str]
    lunar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    
    samjae_text, is_samjae = check_samjae(ba_zi[0], target_year)
    badge_class = "samjae-on" if is_samjae else "samjae-off"

    st.markdown(f"### 🍀 {name}님의 {target_year}년 분석")
    st.markdown(f"<div class='samjae-badge {badge_class}'>{samjae_text}</div>", unsafe_allow_html=True)

    # 섹션 1: 일반 인생 통변 (150자 이상)
    st.markdown(f"""
    <div class='report-card'>
        <h2>👤 {target_year}년 일반 인생 운세</h2>
        <p>올해는 당신의 삶에서 <b>안정적인 기반을 다지고 주변의 신뢰를 얻는 해</b>입니다. 
        직장이나 사회적 관계에서 본인의 노력이 인정받기 시작하며, 특히 금전적인 흐름이 작년에 비해 유연해지는 기운이 들어옵니다. 
        무리한 확장보다는 현재 가진 것을 지키고 내실을 기할 때 뜻밖의 기회가 찾아올 것입니다. 
        대인관계에서는 소통의 실수가 발생할 수 있으니 언행에 신중을 기한다면 평탄하고 복된 한 해가 될 것입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 섹션 2: 음악 사주 통변 (150자 이상)
    st.markdown(f"""
    <div class='music-card'>
        <h2 style='color:#db2777;'>🎸 {target_year}년 음악적 활동 운세</h2>
        <p>아티스트로서 {target_year}년은 <b>당신만의 독창적인 색깔이 대중에게 각인되는 중요한 시기</b>입니다. 
        작곡이나 연주에서 기존의 틀을 깨는 파격적인 시도가 의외의 호평을 이끌어낼 가능성이 큽니다. 
        그동안 정체되어 있던 프로젝트가 있다면 올해 중반기를 기점으로 활기를 띨 것이며, 
        특히 공연이나 합주 활동에서 주도적인 역할을 맡게 될 운세입니다. 
        당신의 에너지가 무대 위에서 가장 빛나는 해이니 자신감을 가지고 창작물에 임하시길 권장합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 데이터 확인 (선택 사항)
    with st.expander("🔍 전문 명리 데이터 (명식)"):
        st.write(f"**사주 8자:** {' '.join(ba_zi)}")
        st.write(f"**일간:** {day_gan} / **시간:** {hour_str}")
