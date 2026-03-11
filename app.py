import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="정통 명리 & 음악가 운세 분석", layout="wide")

# 1️⃣ 데이터 설정
hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

ohaeng_info = {
    '목': {'chars': '甲乙寅卯', 'desc': '곡직(曲直) - 창조적 감성, 선율, 새로운 시도'},
    '화': {'chars': '丙丁巳午', 'desc': '염상(炎上) - 열정적 에너지, 표현력, 무대 장악력'},
    '토': {'chars': '戊己辰戌丑未', 'color': '#ffc107', 'desc': '가색(稼穡) - 안정감, 리듬의 기초, 프로듀싱'},
    '금': {'chars': '庚辛申酉', 'desc': '종혁(從革) - 결단력, 정교한 테크닉, 금속성 사운드'},
    '수': {'chars': '壬癸亥子', 'desc': '윤하(潤下) - 깊은 사색, 유연성, 잼/즉흥연주'}
}

# 2️⃣ 사이드바 입력창 (보고 싶은 연도 추가)
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
    submitted = st.button("운명 및 음악 운세 분석")

# 3️⃣ 분석 함수 정의
def get_interpretation(day_gan, max_elem):
    # 일간별 기본 기질 통변 (예시)
    gan_desc = {
        "甲": "우두머리 기질과 솟구치는 창의성을 가졌습니다.", "乙": "유연하고 섬세하며 표현력이 뛰어납니다.",
        "丙": "태양처럼 밝고 화려하며 주목받는 에너지가 강합니다.", "丁": "감수성이 예민하고 내면의 집중력이 훌륭합니다.",
        "戊": "포용력이 있고 중심을 지키는 묵직함이 있습니다.", "己": "자기 관리에 철저하며 조화로운 조율에 능합니다.",
        "庚": "의리가 있고 날카로운 카리스마와 절제미를 갖췄습니다.", "辛": "보석처럼 정교하고 깔끔한 기교를 추구합니다.",
        "壬": "지혜가 깊고 거침없는 추진력을 보유했습니다.", "癸": "생각이 깊고 변화무쌍하며 영감이 풍부합니다."
    }
    return gan_desc.get(day_gan, "독특한 예술적 기질을 보유하셨습니다.")

# 4️⃣ 메인 로직
if submitted:
    # 원국 분석
    h = hour_time_map[hour_str]
    lunar = Lunar.fromYmdHms(int(year), -int(month) if is_leap else int(month), int(day), h, 0, 0) if calendar_type == "음력" else Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar()
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    counts = {k: sum(1 for c in "".join(ba_zi) if c in v['chars']) for k, v in ohaeng_info.items()}
    max_elem = max(counts, key=counts.get)

    # 보고 싶은 연도(세운) 분석
    target_solar = Solar.fromYmd(target_year, 1, 1) # 해당 연도의 천간지지를 위해
    year_gan_zhi = target_solar.getLunar().getYearInGanZhi()
    target_gan = year_gan_zhi[0]

    # --- 출력 섹션 ---
    st.subheader(f"📑 {name}님의 사주 본질 및 {target_year}년 음악 운세")
    
    # [섹션 1: 사주 원국 통변]
    with st.expander("🔍 타고난 사주 기질 통변 (본질 풀이)", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**명식: {ba_zi[2]} 일주**")
            st.info(f"핵심 기운: {max_elem}")
        with col2:
            st.write(f"**[{day_gan}화(火) 일간의 예술성]**")
            st.write(get_interpretation(day_gan, max_elem))
            st.write(f"현재 사주에 **{max_elem}**의 기운이 강하여, 전체적으로 {ohaeng_info[max_elem]['desc']}의 성향이 음악적 색채를 결정짓습니다.")

    # [섹션 2: 보고 싶은 연도 분석]
    st.divider()
    st.write(f"### 📅 {target_year}년({year_gan_zhi}년)의 흐름 분석")
    
    col_flow, col_music = st.columns(2)
    with col_flow:
        st.markdown(f"**[ {target_year}년 총운 ]**")
        # 간단한 생극제화 로직 기반 통변 (예시)
        flow_msg = "새로운 기운이 들어와 변화가 많은 시기입니다."
        if target_gan in '甲乙': flow_msg = "활동 반경이 넓어지고 창작 욕구가 샘솟는 해입니다."
        elif target_gan in '丙丁': flow_msg = "자신의 존재감이 드러나고 대외적인 활동이 활발해지는 시기입니다."
        st.success(flow_msg)

    with col_music:
        st.markdown(f"**[ {target_year}년 음악적 운세 ]**")
        music_flow = "기존의 틀을 깨고 과감한 사운드를 시도하기에 적기입니다. 공연이나 앨범 발표 시 좋은 결과가 예상됩니다."
        st.warning(music_flow)

    # [섹션 3: 8자 명식 및 오행 지표 (기존 유지)]
    st.divider()
    cols = st.columns(4)
    for i, label in enumerate(["년주", "월주", "일주", "시주"]):
        cols[i].markdown(f"<div style='text-align:center; padding:10px; border:1px solid #ddd; border-radius:5px;'><b>{label}</b><br><h2>{ba_zi[i]}</h2></div>", unsafe_allow_html=True)

    st.write("### ☯️ 오행 균형 지표")
    o_cols = st.columns(5)
    for i, (elem, count) in enumerate(counts.items()):
        o_cols[i].metric(elem, f"{count}자")
        o_cols[i].progress(count/8.0)
