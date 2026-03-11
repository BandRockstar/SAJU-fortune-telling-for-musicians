import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 기본 설정
st.set_page_config(page_title="정통 사주 & 음악 분석", layout="wide")

# 2️⃣ 데이터 매핑 및 설정
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

# 3️⃣ 사이드바 입력창
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

# 4️⃣ 메인 분석 및 출력 로직
if submitted:
    # 사주 계산 (lunar-python 라이브러리 활용)
    h = hour_time_map[hour_str]
    if calendar_type == "음력":
        # 윤달일 경우 월 값에 마이너스(-)를 붙여 라이브러리에 전달
        m_val = -int(month) if is_leap else int(month)
        lunar = Lunar.fromYmdHms(int(year), m_val, int(day), h, 0, 0)
    else:
        solar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
        lunar = solar.getLunar()

    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    all_chars = "".join(ba_zi)
    day_gan = lunar.getDayGan()
    
    # 오행 계산
    counts = {k: sum(1 for c in all_chars if c in v['chars']) for k, v in ohaeng_info.items()}
    max_elem = max(counts, key=counts.get)

    # --- 결과 화면 렌더링 ---
    st.subheader(f"📑 {name}님의 사주 분석 결과")
    leap_txt = " (윤달)" if is_leap else ""
    st.caption(f"기준: {calendar_type} {year}-{month}-{day}{leap_txt} / 변환된 음력: {lunar.toString()}")
    
    # 섹션 1: 8자 명식 (HTML/CSS 활용)
    cols = st.columns(4)
    labels = ["년주(年)", "월주(月)", "일주(日)", "시주(時)"]
    for i, col in enumerate(cols):
        col.markdown(f"""
        <div style="text-align:center; padding:15px; border:2px solid #f0f2f6; border-radius:10px; background-color:#ffffff; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
            <small style="color:#666; font-weight:bold;">{labels[i]}</small>
            <h2 style="margin:10px 0; color:#31333F; font-family: 'Nanum Gothic', sans-serif;">{ba_zi[i]}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 섹션 2: 오행 에너지 분포 지표
    st.write("### ☯️ 오행 에너지 분포")
    o_cols = st.columns(5)
    for i, (elem, count) in enumerate(counts.items()):
        with o_cols[i]:
            st.metric(label=elem, value=f"{count}자")
            # 8자 중 비중을 시각적으로 표시
            st.progress(count / 8.0)

    st.divider()

    # 섹션 3: 상세 분석 (정통 명리 + 음악 특화)
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("### 🔍 사주 본질 분석")
        st.markdown(f"""
        * **일주(日柱)의 기운:** 본인은 **{ba_zi[2]}** 일주로, 타고난 성정은 하늘의 기운인 **'{day_gan}'**의 성질을 강하게 띱니다.
        * **오행의 형상:** 현재 사주 명식에서 가장 두드러지는 에너지는 **'{max_elem}'**입니다. 
        * **종합 평:** 전체적으로 기운이 {('안정적이고 조화로운' if counts[max_elem] < 4 else '한 분야에 매우 집중된')} 흐름을 보여주고 있습니다.
        """)

    with col_right:
        st.write("### 🎸 음악적 특화 해석")
        music_map = {
            "목": "선율 중심의 서정적 사운드, 어쿠스틱/현악기, 섬세한 보컬",
            "화": "폭발적인 에너지와 퍼포먼스, 하드록/메탈, 금관악기",
            "토": "중심을 잡는 묵직한 리듬, 베이스/타악기, 음악 프로듀싱",
            "금": "날카롭고 정교한 테크닉, 일렉 기타, 정확한 비트감",
            "수": "유연한 즉흥성, 재즈/엠비언트, 깊은 감성의 건반 악기"
        }
        st.success(f"**권장 음악 스타일:** {music_map.get(max_elem, '다양한 장르의 조화')}")
        st.write(f"본인의 핵심 에너지인 **'{max_elem}'**의 기운을 악기 선택이나 작곡 스타일에 투영할 때 가장 독창적인 결과물이 나옵니다.")

    st.divider()
    st.caption("※ 본 분석은 명리학적 통계에 기반한 해석이며, 참고용으로 활용하시기 바랍니다.")
