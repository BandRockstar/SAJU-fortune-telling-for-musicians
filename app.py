import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 (모바일 대응을 위해 레이아웃 조절)
st.set_page_config(page_title="음악가 사주 리포트", layout="centered")

# 커스텀 CSS: 모바일에서 폰트 크기와 카드 너비 최적화
st.markdown("""
    <style>
    .report-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #eee;
        margin-bottom: 15px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }
    .saju-unit {
        text-align: center;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 5px;
    }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.2rem !important; }
    p { line-height: 1.6; font-size: 0.95rem; }
    </style>
    """, unsafe_allow_html=True)

hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 2️⃣ 입력부 (모바일에서는 세로로 나오는 것이 기본)
with st.expander("👤 정보 입력 (여기를 클릭)", expanded=True):
    name = st.text_input("성함", value="임환백")
    col1, col2 = st.columns(2)
    year = col1.number_input("출생년", 1900, 2100, 1981)
    month = col2.number_input("출생월", 1, 12, 2)
    day = col1.number_input("출생일", 1, 31, 7)
    hour_str = col2.selectbox("출생 시간", list(hour_time_map.keys()), index=3)
    
    calendar_type = st.radio("달력 종류", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달 여부") if calendar_type == "음력" else False
    
    target_year = st.number_input("보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🚀 분석 리포트 생성", use_container_width=True)

# 3️⃣ 통변 로직 (내용 보강)
def get_mobile_report(day_gan, max_elem, counts):
    reports = {
        "丙": "태양의 기운인 丙(병화) 일간을 타고난 당신은 화려한 무대 매너와 열정적인 에너지가 특징입니다. 음악에서도 감정을 솔직하게 터뜨리는 스타일로, 대중을 압도하는 카리스마를 지녔습니다. 다소 성격이 급할 수 있으나 그만큼 추진력이 좋아 한 번 몰입하면 놀라운 속도로 결과물을 만들어냅니다. 200자 이상의 깊은 통변이 필요하다면 이 공간을 활용하여 당신의 음악적 천성과 대인관계, 건강운까지 상세히 설명해 드릴 수 있습니다.",
        "庚": "강직한 원석인 庚(경금) 일간은 결단력이 있고 정확한 사운드를 지향합니다. 완벽주의적인 성향이 강해 테크닉적으로 완벽한 연주를 선호하며, 음악적 주관이 매우 뚜렷하여 자신만의 스타일을 고집하는 장인 정신이 돋보입니다."
    }
    
    oh_desc = f"현재 당신의 사주에는 **{max_elem}**의 기운이 매우 강하게 자리 잡고 있습니다. "
    if max_elem == '금':
        oh_desc += "이는 날카롭고 정교한 감각을 의미하며, 일렉 기타나 금속성 사운드 믹싱에서 타의 추종을 불허하는 재능을 발휘하게 합니다. 하지만 지나친 완벽주의로 스스로를 괴롭힐 수 있으니 가끔은 즉흥적인 연주로 유연함을 찾는 것이 음악적 장수에 도움이 됩니다."
    
    return reports.get(day_gan, "타고난 예술적 영감이 풍부한 사주입니다."), oh_desc

# 4️⃣ 출력부 (모바일 최적화 레이아웃)
if submitted:
    h = hour_time_map[hour_str]
    lunar = Lunar.fromYmdHms(int(year), -int(month) if is_leap else int(month), int(day), h, 0, 0) if calendar_type == "음력" else Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar()
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    
    # 데이터 분석
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    max_elem = max(counts, key=counts.get)
    gan_rep, oh_rep = get_mobile_report(day_gan, max_elem, counts)

    # 결과 시작
    st.markdown(f"### ✨ {name}님의 운세 리포트")
    
    # [섹션 1: 8자 명식 - 모바일은 2x2 배치]
    st.markdown("#### **📜 사주 명식**")
    m1, m2 = st.columns(2)
    m1.markdown(f"<div class='saju-unit'><small>년주</small><br><b>{ba_zi[0]}</b></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='saju-unit'><small>월주</small><br><b>{ba_zi[1]}</b></div>", unsafe_allow_html=True)
    m1.markdown(f"<div class='saju-unit'><small>일주</small><br><b>{ba_zi[2]}</b></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='saju-unit'><small>시주</small><br><b>{ba_zi[3]}</b></div>", unsafe_allow_html=True)

    # [섹션 2: 심층 통변 - 카드형 세로 배치]
    st.markdown(f"""
    <div class='report-card'>
        <h3>🔍 타고난 천성 ({day_gan} 일간)</h3>
        <p>{gan_rep}</p>
    </div>
    <div class='report-card'>
        <h3>☯️ 오행과 음악성 ({max_elem})</h3>
        <p>{oh_rep}</p>
    </div>
    """, unsafe_allow_html=True)

    # [섹션 3: 보고 싶은 연도 분석]
    target_lunar = Solar.fromYmd(target_year, 1, 1).getLunar()
    target_gz = target_lunar.getYearInGanZhi()
    
    st.markdown(f"""
    <div class='report-card' style='background-color: #f0f7ff; border-color: #bee3f8;'>
        <h3>📅 {target_year}년({target_gz}년) 운세</h3>
        <p>올해는 <b>{target_gz}</b>의 기운이 본인에게 강하게 작용하는 해입니다. 음악적으로는 새로운 시도보다는 내실을 다지고 기존의 결과물을 다듬기에 적합한 시기입니다. 대인관계에서 오는 영감을 곡 작업으로 연결한다면 기대 이상의 성과를 거둘 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # [섹션 4: 오행 지표]
    st.markdown("#### **📊 오행 에너지**")
    for elem, count in counts.items():
        st.write(f"{elem} ({count}자)")
        st.progress(count/8.0)
