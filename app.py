import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 설정 및 데이터 매핑
st.set_page_config(page_title="정통 사주 & 음악 분석", layout="wide")
st.title("⚖️ 정통 명리 & 음악가 사주 분석 시스템")

hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 2️⃣ 입력 폼
with st.sidebar:
    st.header("👤 사주 입력")
    name = st.text_input("성함", value="홍길동")
    year = st.number_input("생년", 1900, 2100, 1981)
    month = st.number_input("월", 1, 12, 2)
    day = st.number_input("일", 1, 31, 7)
    hour_str = st.selectbox("시간", list(hour_time_map.keys()), index=3)
    calendar_type = st.radio("달력", ["양력", "음력"])
    submitted = st.button("운명 분석 실행")

# 3️⃣ 분석 핵심 로직
def get_detailed_saju(year, month, day, hour_str, cal_type):
    h = hour_time_map[hour_str]
    lunar = Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0) if cal_type == "음력" else Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar()
    
    ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    all_chars = "".join(ba_zi)
    
    # 오행 및 색상 매핑
    ohaeng_info = {
        '목': {'chars': '甲乙寅卯', 'color': '#28a745', 'desc': '창조, 시작, 인자함'},
        '화': {'chars': '丙丁巳午', 'color': '#dc3545', 'desc': '열정, 확산, 예의'},
        '토': {'chars': '戊己辰戌丑未', 'color': '#ffc107', 'desc': '중재, 신용, 안정'},
        '금': {'chars': '庚辛申酉', 'color': '#6c757d', 'desc': '결단, 의리, 숙살'},
        '수': {'chars': '壬癸亥子', 'color': '#007bff', 'desc': '지혜, 흐름, 유연'}
    }
    
    counts = {k: sum(1 for c in all_chars if c in v['chars']) for k, v in ohaeng_info.items()}
    return {"ba_zi": ba_zi, "counts": counts, "day_gan": lunar.getDayGan(), "day_zhi": lunar.getDayZhi(), "info": ohaeng_info}

# 4️⃣ 결과 출력
if submitted:
    data = get_detailed_saju(year, month, day, hour_str, calendar_type)
    
    # --- 섹션 1: 정통 사주 명식 ---
    st.subheader(f"📑 {name}님의 정통 사주 명식")
    cols = st.columns(4)
    titles = ["年 (년주)", "月 (월주)", "日 (일주)", "時 (시주)"]
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:10px; border:1px solid #ddd; border-radius:10px;">
                <p style="color:gray;">{titles[i]}</p>
                <h2 style="margin:0;">{data['ba_zi'][i]}</h2>
            </div>
            """, unsafe_allow_safe_allow_html=True)

    # --- 섹션 2: 오행 에너지 균형 (한눈에 보기) ---
    st.divider()
    st.subheader("☯️ 오행 에너지 분포")
    o_cols = st.columns(5)
    for i, (elem, count) in enumerate(data['counts'].items()):
        with o_cols[i]:
            st.metric(label=elem, value=f"{count}자")
            st.progress(count / 4.0 if count <= 4 else 1.0) # 8자 중 비중 시각화

    # --- 섹션 3: 일주론 기반 성향 분석 (본질) ---
    st.divider()
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("🔍 사주 본질 분석")
        day_gan = data['day_gan']
        # 실제 일주론 데이터를 가져오는 로직 (예시)
        st.write(f"**본인은 '{day_gan}'의 기운을 타고난 {data['ba_zi'][2]} 일주입니다.**")
        st.info(f"이 사주는 전체적으로 **{max(data['counts'], key=data['counts'].get)}** 기운이 강하여 성격이 곧고 추진력이 강한 편입니다.")
    
    # --- 섹션 4: 음악적 사주 풀이 (추가 서비스) ---
    with col_b:
        st.subheader("🎸 음악적 특화 해석")
        music_logic = {
            "목": "선율 위주의 클래식, 어쿠스틱 사운드",
            "화": "폭발적인 록, 화려한 퍼포먼스, 금관악기",
            "토": "안정적인 베이스, 리듬 섹션, 프로듀싱",
            "금": "정교한 비트, 일렉 기타, 금속 타악기",
            "수": "깊이 있는 재즈, 엠비언트, 신디사이저"
        }
        main_elem = data['info'][ '목' if day_gan in '甲乙' else '화' if day_gan in '丙丁' else '토' if day_gan in '戊己' else '금' if day_gan in '庚辛' else '수' ]
        st.success(f"**추천 장르/사운드**\n\n{music_logic.get(max(data['counts'], key=data['counts'].get))}")

    st.caption("※ 본 분석은 명리학적 통계를 바탕으로 하며, 실제 운명은 개인의 노력에 따라 변화할 수 있습니다.")
