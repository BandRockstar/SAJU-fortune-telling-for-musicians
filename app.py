import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악인 맞춤 사주 분석", layout="wide")
st.title("🎵 음악인 맞춤 사주 분석기 (정밀, Lunar Python)")

# -------------------------
# 1️⃣ 입력 폼 및 시간 매핑
# -------------------------
hour_time_map = {
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.form("saju_input_form"):
    st.subheader("기본 정보 입력")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름")
        year = st.number_input("생년", min_value=1900, max_value=2100, step=1, value=1981)
        month = st.number_input("월", min_value=1, max_value=12, step=1, value=2)
        day = st.number_input("일", min_value=1, max_value=31, step=1, value=7)
    with col2:
        gender = st.selectbox("성별", ["남", "여"])
        calendar_type = st.radio("양력 / 음력", ["양력", "음력"])
        hour_str = st.selectbox("시간 (2시간 단위)", list(hour_time_map.keys()))
        target_year = st.number_input("보고 싶은 연도", min_value=1900, max_value=2100, step=1, value=2026)

    submitted = st.form_submit_button("사주 분석 시작")

# -------------------------
# 2️⃣ 사주 계산 및 오행 분석 로직
# -------------------------
def calculate_full_saju(year, month, day, hour_str, calendar_type):
    h = hour_time_map[hour_str]
    
    if calendar_type == "양력":
        solar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)
        lunar = solar.getLunar()
    else:
        lunar = Lunar.fromYmdHms(int(year), int(month), int(day), h, 0, 0)

    # 8자 정보 가져오기 (시두법 자동 적용)
    ba_zi = [
        lunar.getYearInGanZhi(),  # 년주
        lunar.getMonthInGanZhi(), # 월주
        lunar.getDayInGanZhi(),   # 일주
        lunar.getTimeInGanZhi()   # 시주
    ]
    
    # 오행 매핑 (천간 + 지지 합산)
    ohaeng_map = {
        '甲': '목', '乙': '목', '寅': '목', '卯': '목',
        '丙': '화', '丁': '화', '巳': '화', '午': '화',
        '戊': '토', '己': '토', '辰': '토', '戌': '토', '丑': '토', '未': '토',
        '庚': '금', '辛': '금', '申': '금', '酉': '금',
        '壬': '수', '癸': '수', '亥': '수', '子': '수'
    }
    
    all_chars = "".join(ba_zi)
    ohaeng_counts = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
    for char in all_chars:
        elem = ohaeng_map.get(char)
        if elem:
            ohaeng_counts[elem] += 1
            
    return {
        "ba_zi": ba_zi,
        "ohaeng": ohaeng_counts,
        "day_gan": lunar.getDayGan()
    }

# -------------------------
# 3️⃣ 결과 출력부
# -------------------------
if submitted:
    res = calculate_full_saju(year, month, day, hour_str, calendar_type)
    ba_zi = res["ba_zi"]
    ohaeng = res["ohaeng"]
    
    st.divider()
    st.subheader(f"📜 {name}님의 사주 분석 결과")
    
    # 8자 사주팔자 시각화
    cols = st.columns(4)
    labels = ["년주", "월주", "일주", "시주"]
    for i, col in enumerate(cols):
        col.metric(labels[i], ba_zi[i])

    # 오행 분석
    st.write("### ☯️ 오행 분포 (총 8자 기준)")
    o_cols = st.columns(5)
    for i, (key, val) in enumerate(ohaeng.items()):
        o_cols[i].write(f"**{key}**: {val}개")

    # 음악 성향 (일간 기준 간략화 예시)
    st.subheader("🎵 음악적 특징")
    music_traits = {
        "甲": "웅장하고 클래식한 선율, 리더십 있는 지휘 스타일",
        "乙": "섬세하고 화려한 연주, 현악기나 보컬에 강점",
        "丙": "열정적이고 폭발적인 무대 매너, 금관악기나 록 음악",
        "丁": "감성적이고 따뜻한 작곡 실력, 재즈나 발라드",
        "戊": "안정감 있는 베이스, 묵직한 타악기 리듬",
        "己": "조화로운 화음 중시, 편곡 및 프로듀싱 능력",
        "庚": "날카롭고 정확한 비트, 일렉 기타나 금속성 사운드",
        "辛": "정교하고 깔끔한 기교, 피아노나 정밀한 사운드 디자인",
        "壬": "유연하고 깊이 있는 음악성, 즉흥 연주(잼) 능력",
        "癸": "변화무쌍하고 몽환적인 분위기, 신디사이저나 엠비언트"
    }
    
    trait = music_traits.get(res["day_gan"], "다양한 음악적 재능 보유")
    st.info(f"**{name}님의 핵심 음악 성향:** {trait}")
