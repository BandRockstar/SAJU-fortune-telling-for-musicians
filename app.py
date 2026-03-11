import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="정통 명리 & 음악가 운세 분석 리포트", layout="wide")

# 1️⃣ 기본 데이터 설정
hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 2️⃣ 사이드바 입력창
with st.sidebar:
    st.header("👤 사주 정보 및 운세 설정")
    name = st.text_input("성함", value="고상현")
    year = st.number_input("출생년", 1900, 2100, 1981)
    month = st.number_input("출생월", 1, 12, 2)
    day = st.number_input("출생일", 1, 31, 7)
    calendar_type = st.radio("달력 종류", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달 여부", value=False) if calendar_type == "음력" else False
    hour_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=3)
    
    st.divider()
    target_year = st.number_input("운세를 보고 싶은 연도", 1900, 2100, 2026)
    submitted = st.button("심층 운명 리포트 생성")

# 3️⃣ 심층 통변 엔진 (100자 이상의 서술형 데이터베이스)
def get_detailed_report(day_gan, max_elem, counts):
    # 일간별 심층 성향 통변 (최소 100자 이상)
    gan_interpretations = {
        "丙": f"하늘의 태양과 같은 丙(병화) 일간을 타고난 당신은 타고난 예술적 카리스마와 대중을 압도하는 화려한 에너지를 지니고 있습니다. 성격이 밝고 명랑하며 감정을 숨기지 못하는 솔직함이 음악에서도 그대로 투영되어, 듣는 이로 하여금 폭발적인 카리스마와 생동감을 느끼게 합니다. 무대 위에서 조명을 받을 때 가장 빛나는 존재이며, 다소 급한 성미를 잘 조절하여 음악적 디테일에 집중한다면 대중의 사랑을 한 몸에 받는 독보적인 아티스트로 거듭날 운명입니다.",
        "辛": f"다듬어진 보석과 같은 辛(신금) 일간인 당신은 날카롭고 섬세하며 완벽주의적인 예술가적 기질이 매우 강합니다. 사운드 메이킹이나 편곡 과정에서 단 하나의 결점도 허용하지 않으려는 집요함이 당신의 음악을 명품의 반열에 올립니다. 자존심이 매우 강하고 내면이 예민하여 혼자만의 작업 공간에서 깊은 사색을 통해 영감을 얻는 스타일이며, 때로는 지나친 완벽주의가 스스로를 힘들게 할 수 있으니 유연한 마음가짐이 창작의 장수를 돕습니다.",
        "甲": f"하늘로 솟구치는 거목인 甲(갑목) 일간의 당신은 음악계의 리더이자 개척자적인 기질을 타고났습니다. 남을 따라 하기보다 자신만의 독창적인 장르를 구축하려는 의지가 강하며, 곡의 구성이 웅장하고 진취적인 색채를 띠는 경우가 많습니다. 인자한 성품 속에 강한 승부욕을 감추고 있어 장기적인 프로젝트나 앨범 제작에서 지치지 않는 추진력을 발휘하지만, 지나친 독단은 협업 시 장애가 될 수 있으니 화음을 중시하는 태도가 길운을 불러옵니다."
        # (다른 일간들도 동일한 분량으로 구현 가능)
    }

    # 오행 편중에 따른 심층 통변
    ohaeng_detail = ""
    if max_elem == '금':
        ohaeng_detail = f"현재 사주에서 '금(金)'의 기운이 {counts['금']}자로 매우 강하게 자리 잡고 있습니다. 이는 명리학적으로 숙살지기(肅殺之氣)라 하여 결단력과 날카로움을 의미합니다. 음악적으로는 정확한 비트감과 금속성 사운드, 혹은 일렉 기타와 같이 차갑고 세련된 음색을 선호하게 됩니다. 특히 {counts['금']}자의 강력한 금 기운은 당신의 연주 테크닉을 정교하게 만들지만, 때로는 감성보다 기술에 치우칠 우려가 있으니 수(水)의 유연함을 보충하여 음악에 깊이를 더하시기 바랍니다."
    elif max_elem == '목':
        ohaeng_detail = f"사주 원국에 '목(木)'의 기운이 지배적입니다. 이는 생동감 넘치는 선율과 서정적인 감수성을 의미합니다. 어쿠스틱한 사운드나 현악기, 보컬 위주의 곡에서 강점을 보이며 인간미 넘치는 가사 전달력이 뛰어납니다. 다만 목 기운이 너무 강하면 생각이 많아져 마무리가 약할 수 있으니, 금(金)의 기운을 빌려 곡의 완성도를 높이는 작업이 필요합니다."
    
    main_gan_text = gan_interpretations.get(day_gan, "타고난 예술적 영감이 풍부하여 어떤 장르에서도 자신만의 색채를 드러내는 비범한 사주를 지니셨습니다. 본인만의 독특한 감각을 믿고 나아가십시오.")
    return main_gan_text, ohaeng_detail

# 4️⃣ 메인 로직
if submitted:
    h = hour_time_map[hour_str]
    lunar = Lunar.fromYmdHms(int(year), -int(month) if is_leap else int(month), int(day), h, 0, 0) if calendar_type == "음력" else Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar()
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    
    ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
    max_elem = max(counts, key=counts.get)

    # 통변 생성
    gan_report, oh_report = get_detailed_report(day_gan, max_elem, counts)

    # --- 화면 출력 ---
    st.header(f"✨ {name}님의 사주 본질 및 {target_year}년 음악 운세 리포트")

    # [섹션 1: 타고난 기질 심층 통변]
    st.subheader("🔍 사주 원국 심층 통변 (본질적 예술성)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### **[{day_gan} 일간의 타고난 천성]**")
        st.write(gan_report)
    with col2:
        st.markdown(f"#### **[오행 분포에 따른 음악적 색채]**")
        st.write(oh_report)

    st.divider()

    # [섹션 2: 보고 싶은 연도(세운) 분석]
    st.subheader(f"📅 {target_year}년 음악 활동 운세 분석")
    target_lunar = Solar.fromYmd(target_year, 1, 1).getLunar()
    target_gz = target_lunar.getYearInGanZhi()
    
    flow_col1, flow_col2 = st.columns([1, 2])
    flow_col1.metric("올해의 기운", target_gz)
    
    with flow_col2:
        st.info(f"**{target_year}년 총평:** 올해는 {target_gz}의 기운이 들어오는 해로, {day_gan} 일간인 본인에게는 매우 역동적인 변화가 예상됩니다. 음악적으로는 그동안 준비해온 결과물을 대중에 공개하거나, 새로운 협업을 통해 자신의 영역을 확장하기에 더할 나위 없이 좋은 시기입니다. 특히 재물운과 명예운이 함께 상승하는 구간이니 과감한 도전을 추천합니다.")

    st.divider()

    # [섹션 3: 8자 명식 및 지표 (전문성 강화)]
    st.write("### 📊 명리 데이터 지표")
    cols = st.columns(4)
    labels = ["년주", "월주", "일주", "시주"]
    for i, col in enumerate(cols):
        col.markdown(f"<div style='text-align:center; padding:15px; border:1px solid #ddd; border-radius:10px; background:#f9f9f9;'><b>{labels[i]}</b><br><h2>{ba_zi[i]}</h2></div>", unsafe_allow_html=True)

    o_cols = st.columns(5)
    for i, (elem, count) in enumerate(counts.items()):
        o_cols[i].metric(elem, f"{count}자")
        o_cols[i].progress(count/8.0)
