import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="정통 사주 & 음악 분석", layout="wide")

# 1️⃣ 시간 매핑 및 데이터 설정
hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

ohaeng_info = {
    '목': {'chars': '甲乙寅卯', 'color': '#28a745'},
    '화': {'chars': '丙丁巳午', 'color': '#dc3545'},
    '토': {'chars': '戊己辰戌丑未', 'color': '#ffc107'},
    '금': {'chars': '庚辛申酉', 'color': '#6c757d'},
    '수': {'chars': '壬癸亥子', 'color': '#007bff'}
}

# 2️⃣ 사이드바 입력
with st.sidebar:
    st.header("👤 사주 정보 입력")
    name = st.text_input("성함", value="고상현")
    year = st.number_input("년", 1900, 2100, 1955)
    month = st.number_input("월", 1, 12, 5)
    day = st.number_input("일", 1, 31, 4)
    calendar_type = st.radio("달력 종류", ["양력", "음력"], horizontal=True)
    
    is_leap = False
    if calendar_type == "음력":
        is_leap = st.checkbox("이 달은 윤달입니다", value=False)
    
    hour_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=2)
    submitted = st.button("사주 분석 시작")

# 3️⃣ 메인 분석 로직
if submitted:
    # 사주 계산
    h = hour_time_map[hour_str]
    if calendar_type == "음력":
        lunar = Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
        # 윤달 처리 강제 (lunar-python 특성 반영)
        if is_leap:
            lunar = Lunar.fromYmdHms(int(year), -int(month), int(day), h, 0, 0)
    else:
        solar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
        lunar = solar.getLunar()

    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    all_chars = "".join(ba_zi)
    day_gan = lunar.getDayGan()
    
    # 오행 계산
    counts = {k: sum(1 for c in all_chars if c in v['chars']) for k, v in ohaeng_info.items()}
    max_elem = max(counts, key=counts.get)

    # --- 화면 출력 시작 ---
    st.subheader(f"📑 {name}님의 사주 분석 결과")
    leap_txt = " (윤달)" if is_leap else ""
    st.caption(f"기준: {calendar_type} {year}-{month}-{day}{leap_txt} / 변환: {lunar.toString()}")
    
    # 섹션 1: 8자 명식
    cols = st.columns(4)
    labels = ["년주(年)", "월주(月)", "일주(日)", "시주(時)"]
    for i, col in enumerate(cols):
        col.markdown(f"""
        <div style="text-align:center; padding:15px; border:2px solid #f0f2f6; border-radius:10px; background-color:#ffffff;">
            <small style="color:#666;">{labels[i]}</small>
            <h2 style="margin:5px 0; color:#31333F;">{ba_zi[i]}</h2>
        </div>
        """, unsafe_allow_safe_allow_html=True)

    st.divider()

    # 섹션 2: 오행 에너지 분포 (한눈에 보기)
    st.write("### ☯️ 오행 에너지 분포")
    o_cols = st.columns(5)
    for i, (elem, count) in enumerate(counts.items()):
        with o_cols[i]:
            st.metric(label=elem, value=f"{count}자")
            st.progress(count / 8.0)

    st.divider()

    # 섹션 3: 정통 사주 및 음악 특화 풀이
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("### 🔍 사주 본질 분석")
        st.markdown(f"""
        - **일주 분석:** 본인은 **{ba_zi[2]}** 일주로, 하늘의 기운인 **{day_gan}**의 성질을 타고났습니다.
        - **에너지 균형:** 현재 사주에서 가장 강한 기운은 **'{max_elem}'**입니다. 
        - **성향:** 전체적으로 기운이 {('안정적' if counts[max_elem] < 4 else '한곳으로 집중된')} 형태를 띠고 있습니다.
        """)

    with col_right:
        st.write("### 🎸 음악적 특화 해석")
        music_map = {
            "목": "선율 위주의 서정적 사운드, 현악기, 보컬",
            "화": "폭발적인 에너지, 록/메탈, 화려한 무대매너",
            "토": "중심을 잡는 베이스, 리듬 섹션, 프로듀싱",
            "금": "날카로운 비트, 일렉 기타, 정확한 테크닉",
            "수": "유연한 재즈, 깊이 있는 감성, 건반 악기"
        }
        st.info(f"**추천 스타일:** {music_map.get(max_elem)}")
        st.write(f"본인의 주 기운인 **{max_elem}**의 에너지를 음악적으로 승화시킬 때 가장 큰 성취가 따릅니다.")
