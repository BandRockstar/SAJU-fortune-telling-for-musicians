import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 디자인 (모바일 최적화)
st.set_page_config(page_title="음악가 운세 리포트", layout="centered")

st.markdown("""
    <style>
    .main-header { text-align: center; padding: 20px; background: #1a202c; color: white; border-radius: 15px; margin-bottom: 25px; }
    .samjae-box { text-align: center; padding: 15px; border-radius: 12px; margin-bottom: 20px; font-weight: bold; }
    .card { background: white; padding: 25px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #edf2f7; }
    .music-theme { background: #fff5f7; border-left: 6px solid #d53f8c; }
    h2 { font-size: 1.2rem !important; margin-bottom: 12px; color: #2d3748; }
    p { line-height: 1.8; font-size: 1rem; color: #4a5568; text-align: justify; }
    .footer { text-align: center; font-size: 0.8rem; color: #a0aec0; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>🎸 음악인을 위한 사주통변</h1><p>당신의 리듬과 운명을 읽어드립니다</p></div>", unsafe_allow_html=True)

# 시간 매핑 데이터
hour_map = {
    "05~07 묘시": 6, "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12,
    "13~15 미시": 14, "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20,
    "21~23 해시": 22, "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4
}

# 2️⃣ 정보 입력창
with st.expander("👤 정보 입력하기", expanded=True):
    name = st.text_input("이름 또는 닉네임", value="아티스트")
    c1, c2 = st.columns(2)
    y = c1.number_input("태어난 연도", 1950, 2026, 1981)
    m = c2.number_input("월", 1, 12, 2)
    d = c1.number_input("일", 1, 31, 7)
    h_label = c2.selectbox("태어난 시간", list(hour_map.keys()), index=0)
    
    cal = st.radio("양력/음력", ["양력", "음력"], horizontal=True)
    target_y = st.number_input("궁금한 운세 연도", 1900, 2100, 2026)
    btn = st.button("✨ 나의 음악 운세 확인", use_container_width=True)

# 3️⃣ 로직 및 출력
if btn:
    # 사주 계산
    h_val = hour_map[h_label]
    lunar = Solar.fromYmdHms(int(y), int(m), int(d), h_val, 0, 0).getLunar() if cal == "양력" else Lunar.fromYmdHms(int(y), int(m), int(d), h_val, 0, 0)
    
    gz = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
    day_gan = lunar.getDayGan()
    
    # 삼재 체크
    animal = gz[0][-1]
    sam_groups = {'申子辰': '寅卯辰', '亥卯未': '巳午未', '寅午戌': '申酉戌', '巳酉丑': '亥子丑'}
    target_ani = Solar.fromYmd(target_y, 1, 1).getLunar().getYearInGanZhi()[-1]
    sam_years = next((v for k, v in sam_groups.items() if animal in k), "")
    
    # 결과 화면
    st.markdown(f"### 🍀 {name}님을 위한 {target_y}년 분석 결과")
    
    # 삼재 알림
    if target_ani in sam_years:
        st.markdown(f"<div class='samjae-box' style='background:#fff5f5; color:#c53030; border:1px solid #feb2b2;'>⚠️ 올해는 삼재({['들','눌','날'][sam_years.index(target_ani)]}삼재) 기간입니다. 돌다리도 두드려가는 지혜가 필요합니다!</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='samjae-box' style='background:#f0fff4; color:#2f855a; border:1px solid #9ae6b4;'>✅ 올해는 삼재의 영향이 없는 평온한 해입니다.</div>", unsafe_allow_html=True)

    # 일반 통변
    st.markdown(f"""
    <div class='card'>
        <h2>👤 올해의 전반적인 삶</h2>
        <p>올해는 당신에게 <b>주변 환경이 새롭게 정리되는 해</b>입니다. 과거의 복잡했던 문제들이 하나둘 해결되며, 마음의 여유를 찾게 될 것입니다. 특히 {target_y}년 하반기에는 금전적인 흐름이 좋아지니 계획했던 소비나 저축을 실행하기에 적합합니다. 서두르지 말고 천천히 흐름을 타는 것이 길운을 불러오는 열쇠입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 음악 통변
    st.markdown(f"""
    <div class='card music-theme'>
        <h2>🎸 아티스트로서의 운명</h2>
        <p>음악가로서 올해는 <b>'표현의 확장'</b>이 일어나는 해입니다. 본인이 가진 색깔에 새로운 악기나 사운드를 얹었을 때 대중의 반응이 뜨거울 것입니다. 특히 영감이 풍부해지는 시기라 작곡이나 편곡 활동에 몰입하기 좋으며, 작은 공연이라도 무대에 설 기회가 생긴다면 주저하지 말고 잡으세요. 당신의 에너지가 사람들에게 위로와 전율을 동시에 줄 수 있는 해입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='footer'>※ 본 분석은 재미로 보는 리포트이며, 당신의 음악적 열정이 곧 최고의 운세입니다!</div>", unsafe_allow_html=True)
