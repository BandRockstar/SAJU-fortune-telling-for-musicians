import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

# CSS: 디자인 레이아웃 및 폰트 설정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card { background-color: #ffffff; padding: 25px; border-radius: 18px; border-left: 6px solid #4A5568; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .music-card { background-color: #FDF2F8; padding: 25px; border-radius: 18px; border-left: 6px solid #D53F8C; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(213,63,140,0.1); }
    .position-card { background-color: #FFFBEB; padding: 25px; border-radius: 18px; border-left: 6px solid #D97706; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(217,119,6,0.1); }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 20px; gap: 5px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 15px; border-radius: 15px; margin-bottom: 20px; }
    .ohaeng-item { text-align: center; flex: 1; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 15px; display: flex; align-items: center; }
    .content-text { line-height: 1.9; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.2rem; font-weight: bold; color: #B45309; margin-bottom: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변</h1></div>", unsafe_allow_html=True)

hour_time_map = {
    "시간 선택": None, "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

# 2️⃣ 입력 영역
with st.expander("📝 사주 정보 및 분석 연도 입력", expanded=True):
    name = st.text_input("성함", value="", placeholder="이름을 입력하세요")
    c1, c2 = st.columns(2)
    year = c1.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    month = c2.number_input("출생월", 1, 12, value=None, placeholder="MM")
    day = c1.number_input("출생일", 1, 31, value=None, placeholder="DD")
    hour_str = c2.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    
    cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    is_leap = st.checkbox("윤달 여부") if cal_type == "음력" else False
    target_year = st.number_input("분석하고 싶은 연도 선택", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 분석 리포트 생성", use_container_width=True)

# 3️⃣ 포지션 추천 로직 엔진
def get_music_position(max_elem):
    pos_data = {
        '목': {
            'title': "🎻 보컬 & 서정적 인스트루멘탈",
            'desc': "목(木)의 기운은 생명력과 성장을 상징하며, 사람의 목소리와 가장 닮아 있습니다. 풍부한 감수성을 바탕으로 대중의 마음을 어루만지는 보컬이나, 어쿠스틱 기타, 현악기 파트에서 뛰어난 역량을 발휘합니다. 따뜻한 멜로디를 만드는 작곡 분야에서도 두각을 나타냅니다."
        },
        '화': {
            'title': "🎤 프론트맨 & 퍼포머 (보컬/리드기타)",
            'desc': "화(火)의 기운은 발산과 화려함을 의미합니다. 무대 위에서 시선을 집중시키는 카리스마 있는 보컬이나 화려한 속주를 선보이는 리드 기타리스트에 적합합니다. 청중의 에너지를 끌어올리는 퍼포먼스 기획이나 직관적인 작곡 스타일에 강점이 있습니다."
        },
        '토': {
            'title': "🎧 프로듀서 & 사운드 엔지니어 (작곡/편곡)",
            'desc': "토(土)의 기운은 조율과 중재, 그리고 중심을 지키는 힘입니다. 여러 악기의 소리를 하나로 묶어주는 프로듀싱이나 편곡, 전체적인 사운드 밸런스를 잡는 엔지니어링에 탁월합니다. 묵직하게 팀의 중심을 잡아주는 베이스 파트와도 궁합이 좋습니다."
        },
        '금': {
            'title': "🎸 테크니션 (일렉기타/드럼)",
            'desc': "금(金)의 기운은 결단력과 정교함을 상징합니다. 정확한 타격감이 필요한 드럼이나 금속성 사운드가 매력적인 일렉 기타 테크니션으로서 독보적인 존재감을 보입니다. 한 치의 오차도 없는 미디(MIDI) 프로그래밍이나 날카로운 비판적 시각을 가진 작사 분야에서도 능력을 발휘합니다."
        },
        '수': {
            'title': "🎹 키보드 & 예술적 작곡가",
            'desc': "수(水)의 기운은 유연함과 깊은 사유를 의미합니다. 변화무쌍한 선율을 그려내는 키보드(신디사이저)나 철학적이고 깊이 있는 가사를 쓰는 작사가에 어울립니다. 장르를 넘나드는 유연한 작곡 능력과 전체적인 음악적 흐름을 설계하는 기획자로서의 자질이 충분합니다."
        }
    }
    return pos_data.get(max_elem, {"title": "All-Rounder", "desc": "다양한 오행이 조화를 이루어 모든 포지션에서 활약이 가능합니다."})

# 4️⃣ 분석 및 결과 출력
if submitted:
    if not (year and month and day and hour_time_map[hour_str] is not None):
        st.warning("분석을 위해 모든 정보를 입력해주세요.")
    else:
        h = hour_time_map[hour_str]
        lunar = Solar.fromYmdHms(int(year), int(month), int(day), h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(year), (int(month) * -1) if is_leap else int(month), int(day), h, 0, 0)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), lunar.getTimeInGanZhi()]
        
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        counts = {k: sum(1 for c in "".join(ba_zi) if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        pos_info = get_music_position(max_elem)

        st.markdown(f"### 🍀 {name if name else '아티스트'}님의 사주 분석 결과")
        
        # 명식 및 오행 시각화 (이미지 스타일 유지)
        st.markdown(f"""<div class='saju-grid'>
            <div class='saju-box'><small>년주</small><br>{ba_zi[0]}</div>
            <div class='saju-box'><small>월주</small><br>{ba_zi[1]}</div>
            <div class='saju-box'><small>일주</small><br>{ba_zi[2]}</div>
            <div class='saju-box'><small>시주</small><br>{ba_zi[3]}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        # 🌟 포지션 추천 섹션 (새로 추가된 란)
        st.markdown(f"""
            <div class='position-card'>
                <h2>✨ 추천 음악 포지션</h2>
                <span class='pos-title'>{pos_info['title']}</span>
                <div class='content-text'>{pos_info['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

        # 기존 리포트 섹션
        st.markdown(f"<div class='section-card'><h2>👤 일반 인생 통변</h2><div class='content-text'>타고난 예술적 영감이 풍부한 명조입니다. 본인만의 독창적인 색채를 믿고 나아가십시오.</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 음악적 사주 통변</h2><div class='content-text'>{max_elem}의 기운이 강하여 해당 속성의 악기나 작업 방식에서 가장 큰 창의성이 발현됩니다.</div></div>", unsafe_allow_html=True)
