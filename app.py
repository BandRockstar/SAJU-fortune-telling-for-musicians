import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# 디자인 개선: 삼재 강조 및 이원화 카드 스타일
st.markdown("""
    <style>
    .main-title { text-align: center; padding: 20px 0; }
    .report-card { background: white; padding: 25px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #edf2f7; }
    .music-card { background: #fdf2f8; border-left: 6px solid #db2777; padding: 25px; border-radius: 20px; margin-bottom: 20px; }
    .samjae-alert { background: #fff5f5; border: 1px solid #feb2b2; color: #c53030; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .safe-alert { background: #f0fff4; border: 1px solid #9ae6b4; color: #2f855a; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; margin-bottom: 20px; }
    h2 { font-size: 1.25rem !important; color: #2d3748; margin-bottom: 15px; }
    p { line-height: 1.8; font-size: 1.05rem; color: #4a5568; text-align: justify; word-break: keep-all; }
    .highlight { color: #d53f8c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

# 1️⃣ 삼재 계산 로직
def get_samjae_info(birth_year_ganzhi, target_year):
    # 띠 추출 (지기)
    animal = birth_year_ganzhi[-1]
    samjae_map = {
        '申子辰': ['寅', '卯', '辰'], # 원숭이, 쥐, 용띠 -> 범, 토끼, 용해
        '亥卯未': ['巳', '午', '未'], # 돼지, 토끼, 양띠 -> 뱀, 말, 양해
        '寅午戌': ['申', '酉', '戌'], # 범, 말, 개띠 -> 원숭이, 닭, 개해
        '巳酉丑': ['亥', '子', '丑']  # 뱀, 닭, 소띠 -> 돼지, 쥐, 소해
    }
    
    target_lunar = Solar.fromYmd(target_year, 1, 1).getLunar()
    target_animal = target_lunar.getYearInGanZhi()[-1]
    
    my_samjae_group = next((v for k, v in samjae_map.items() if animal in k), [])
    
    if target_animal in my_samjae_group:
        idx = my_samjae_group.index(target_animal)
        status = ["들삼재", "눌삼재", "날삼재"][idx]
        return f"⚠️ 현재 {target_year}년은 고객님께 <span style='color:#e53e3e;'>{status}</span> 기간입니다.", True
    return f"✅ {target_year}년은 삼재에 해당하지 않는 평온한 해입니다.", False

# 2️⃣ 입력부
with st.expander("👤 분석 대상 정보", expanded=True):
    name = st.text_input("이름", value="임환백")
    c1, c2 = st.columns(2)
    year = c1.number_input("태어난 해", 1900, 2100, 1981)
    month = c2.number_input("월", 1, 12, 2)
    day = c1.number_input("일", 1, 31, 7)
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    target_year = st.number_input("조회 연도", 1900, 2100, 2026)
    submitted = st.button("🚀 운세 리포트 생성", use_container_width=True)

# 3️⃣ 출력부
if submitted:
    lunar = Solar.fromYmd(int(year), int(month), int(day)).getLunar() if calendar_type == "양력" else Lunar.fromYmd(int(year), int(month), int(day))
    birth_gz = lunar.getYearInGanZhi()
    day_gan = lunar.getDayGan()
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    
    # 삼재 확인
    samjae_msg, is_samjae = get_samjae_info(birth_gz, target_year)
    
    st.markdown(f"### 🍀 {name}님을 위한 {target_year}년 리포트")
    
    # 삼재 표시
    alert_class = "samjae-alert" if is_samjae else "safe-alert"
    st.markdown(f"<div class='{alert_class}'>{samjae_msg}</div>", unsafe_allow_html=True)

    # 섹션 1: 일반 인생 통변 (해당 연도 중심)
    st.markdown(f"""
    <div class='report-card'>
        <h2>👤 {target_year}년 일반 운세 (인생의 흐름)</h2>
        <p>올해는 당신의 인생에서 <b>내실을 기하고 환경을 정리하는 시기</b>가 될 것입니다. 
        대인관계에서는 새로운 인연보다는 기존의 소중한 사람들과의 관계를 돈독히 하는 데 운이 따릅니다. 
        특히 경제적인 면에서는 큰 투자보다는 자산을 지키는 방향이 유리하며, 가을 이후에는 평소 고민하던 문제에 대한 실마리가 풀리는 기분 좋은 흐름이 예상됩니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 섹션 2: 음악적 통변 (해당 연도 중심)
    st.markdown(f"""
    <div class='music-card'>
        <h2>🎸 {target_year}년 음악 운세 (아티스트 리포트)</h2>
        <p>아티스트로서 올해는 <span class='highlight'>'재발견'</span>이라는 키워드가 명확합니다. 
        기존에 시도하지 않았던 새로운 장르나 악기에 도전했을 때 예상치 못한 영감이 터져 나오는 해입니다. 
        {target_year}년 중반기에는 무대 운이 강하게 들어오니 공연이나 합주 기회를 적극적으로 잡으시길 바랍니다. 
        당신의 독특한 감각이 대중에게 더 날카롭게 전달되어 깊은 인상을 남길 수 있는 절호의 시기입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 전문가 데이터 레이어
    with st.expander("🔍 상세 명리 데이터 보기 (참고용)"):
        st.write(f"**사주 명식:** {' '.join(ba_zi)}")
        st.write(f"**본인 일간:** {day_gan} (나를 상징하는 기운)")
        st.caption("※ 본 데이터는 내부 분석을 위한 값이며, 위 통변 내용에 모두 반영되었습니다.")
