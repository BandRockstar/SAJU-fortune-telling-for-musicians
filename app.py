import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악가 심층 사주 리포트", layout="centered")

# 모바일 가독성을 위한 디자인 설정
st.markdown("""
    <style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 15px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); }
    .saju-unit { text-align: center; padding: 10px; background: #f8f9fa; border-radius: 10px; margin: 5px; border: 1px solid #dee2e6; }
    .highlight { color: #2d3748; font-weight: bold; }
    h2 { font-size: 1.4rem !important; margin-bottom: 10px; }
    h3 { font-size: 1.1rem !important; color: #4a5568; }
    p { line-height: 1.7; font-size: 0.95rem; color: #4a5568; text-align: justify; }
    </style>
    """, unsafe_allow_html=True)

hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 1️⃣ 입력부
with st.expander("👤 정보 입력 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="임환백")
    c1, c2 = st.columns(2)
    year = c1.number_input("출생년", 1900, 2100, 1981)
    month = c2.number_input("출생월", 1, 12, 2)
    day = c1.number_input("출생일", 1, 31, 7)
    hour_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=3)
    calendar_type = st.radio("달력 종류", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달 여부") if calendar_type == "음력" else False
    target_year = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("🚀 심층 리포트 생성 (진짜 통변)", use_container_width=True)

# 2️⃣ 진짜 통변 로직 엔진 (조건별로 문장을 조립함)
def generate_real_interpretation(day_gan, max_elem, counts):
    # (1) 일간별 심층 풀이 (최소 150자 이상 조합)
    gan_data = {
        "丙": "본인은 하늘의 태양과 같은 丙(병화)의 기운을 타고났습니다. 성격이 밝고 정열적이며, 자신의 감정을 숨기지 않고 음악을 통해 폭발시키듯 표현하는 스타일입니다. 무대 위에서 주목받을 때 가장 큰 에너지를 얻으며, 독창적인 창의성보다는 대중을 압도하는 화려한 퍼포먼스와 전달력에 강점이 있습니다. 다만 태양이 너무 뜨거우면 주변을 태울 수 있듯, 감정 기복을 조절하는 것이 장기적인 창작 활동의 핵심입니다.",
        "庚": "본인은 단단한 원석이나 잘 제련된 칼과 같은 庚(경금)의 기운을 가졌습니다. 의리가 있고 결단력이 강하며, 음악 작업에 있어서도 타협하지 않는 자신만의 철학이 뚜렷합니다. 사운드의 질감이나 테크닉적인 완벽함을 추구하는 경향이 강해 엔지니어링이나 정교한 연주에서 빛을 발합니다. 때로는 너무 날카로운 비판 의식이 본인을 힘들게 할 수 있으니, 여백의 미를 즐기는 태도가 필요합니다."
    }
    
    # (2) 오행 과다에 따른 풀이
    oh_data = {
        "금": f"현재 사주에 '금'의 기운이 {counts['금']}자로 매우 강합니다. 이는 명리학적으로 '숙살지기'라 하여, 맺고 끊음이 확실한 에너지를 뜻합니다. 음악적으로는 정확한 박자감, 금속성 악기(일렉 기타, 브라스), 혹은 차갑고 세련된 도시적 감성의 곡들과 인연이 깊습니다. 금이 강하면 완벽주의 때문에 곡 마무리가 늦어질 수 있으니, 수(水)의 기운을 활용해 유연하게 흘려보내는 연습이 길운을 부릅니다.",
        "목": f"사주에 '목'의 기운이 {counts['목']}자로 강하게 자리 잡았습니다. 이는 솟구치는 생명력과 서정적인 감성을 의미합니다. 멜로디 위주의 작곡이나 어쿠스틱한 사운드, 현악기와의 조화가 뛰어납니다. 새로운 것을 시작하는 기획력은 좋으나 마무리가 아쉬울 수 있으니, 금(金)의 기운을 가진 동료와 협업하거나 본인의 연주에 절제미를 더하면 세계적인 명곡을 탄생시킬 수 있습니다."
    }

    # (3) 부족한 부분 보완점
    advice = "전체적으로 기운이 한쪽으로 쏠려 있어 개성이 매우 뚜렷한 예술가적 면모를 보입니다. "
    if counts['수'] == 0:
        advice += "특히 '수(물)'의 기운이 부족하여 감정의 유연한 흐름이나 깊은 사색의 시간이 필요할 수 있습니다. 차분한 앰비언트 음악을 듣거나 물가에서 명상을 하는 것이 창작 영감을 얻는 데 큰 도움이 됩니다."

    main_text = gan_data.get(day_gan, "타고난 기질이 비범하며, 자신만의 독특한 예술적 감각을 바탕으로 세상을 놀라게 할 에너지를 지니셨습니다.")
    sub_text = oh_data.get(max_elem, "오행이 고루 분포되어 있어 다양한 장르를 섭렵할 수 있는 올라운더 아티스트입니다.")
    
    return main_text + "\n\n" + sub_text + "\n\n" + advice

# 3️⃣ 출력부
if submitted:
    h = hour_time_map[hour_str]
    lunar = Lunar.fromYmdHms(int(year), -int(month) if is_leap else int(month), int(day), h, 0, 0) if calendar_type == "음력" else Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar()
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan, max_elem = lunar.getDayGan(), ""
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    max_elem = max(counts, key=counts.get)

    # 진짜 통변 생성
    full_interpretation = generate_real_interpretation(day_gan, max_elem, counts)

    st.markdown(f"### ✨ {name}님의 예술가 운세 리포트")
    
    # 명식 (모바일용 2x2)
    m1, m2 = st.columns(2)
    for i, label in enumerate(["년주", "월주", "일주", "시주"]):
        target = m1 if i % 2 == 0 else m2
        target.markdown(f"<div class='saju-unit'><small>{label}</small><br><b>{ba_zi[i]}</b></div>", unsafe_allow_html=True)

    # 심층 통변 카드
    st.markdown(f"""
    <div class='report-card'>
        <h2 style='color:#2d3748;'>🔍 타고난 명리 통변 (심층 분석)</h2>
        <p>{full_interpretation.replace('\n', '<br>')}</p>
    </div>
    """, unsafe_allow_html=True)

    # 보고 싶은 연도 운세
    target_gz = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()
    st.markdown(f"""
    <div class='report-card' style='background-color: #f7fafc; border-left: 5px solid #4299e1;'>
        <h2>📅 {target_year}년({target_gz}년) 음악적 흐름</h2>
        <p>올해는 <b>{target_gz}</b>의 기운이 본인에게 들어오는 시기입니다. {day_gan} 일간인 본인에게 이 시기는 새로운 음반 작업보다는 공연 활동이나 대외적인 인지도를 높이는 데 매우 유리한 해입니다. 특히 하반기로 갈수록 명예운이 상승하니 자신감을 갖고 무대에 서시길 권장합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 오행 프로그레스
    st.markdown("#### **📊 오행 에너지 균형 지표**")
    for elem, count in counts.items():
        st.write(f"{elem} ({count}자)")
        st.progress(count / 8.0)
