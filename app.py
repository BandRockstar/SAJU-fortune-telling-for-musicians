import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 모바일 최적화 UI 디자인 (기존 레이아웃 100% 유지)
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    html { font-size: 14px; }
    @media (min-width: 600px) { html { font-size: 16px; } }

    .main-title { text-align: center; color: #1A202C; padding: 20px 0; border-bottom: 2px solid #E2E8F0; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.06); 
    }
    .section-card { background-color: #ffffff; border-left: 8px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 8px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; }
    
    .samjae-active { background-color: #FEF2F2; border: 2px solid #EF4444; color: #991B1B; padding: 1.5rem; border-radius: 1.2rem; margin-bottom: 1.5rem; }
    .samjae-inactive { background-color: #F0FDF4; border: 2px solid #22C55E; color: #166534; padding: 1.5rem; border-radius: 1.2rem; margin-bottom: 1.5rem; }

    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 1.5rem; gap: 8px; }
    .saju-box { flex: 1; text-align: center; padding: 15px 5px; background: #EDF2F7; border-radius: 12px; font-weight: bold; border: 1px solid #CBD5E0; }
    .ohaeng-grid { display: flex; justify-content: space-between; background: #F8FAFC; padding: 20px; border-radius: 15px; margin-bottom: 1.5rem; }
    
    h1 { font-size: 1.8rem !important; font-weight: 700; color: #2D3748; }
    h2 { font-size: 1.3rem !important; color: #2D3748; margin-bottom: 1.2rem; font-weight: 700; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    .pos-title { font-size: 1.3rem; font-weight: bold; color: #B45309; margin-bottom: 0.8rem; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

# 2️⃣ 입력 설정 (기존 틀 유지)
hour_time_map = {
    "시간 선택 (또는 모름)": "unknown", "모름": "unknown",
    "23~01 자시": 0, "01~03 축시": 2, "03~05 인시": 4, "05~07 묘시": 6,
    "07~09 진시": 8, "09~11 사시": 10, "11~13 오시": 12, "13~15 미시": 14,
    "15~17 신시": 16, "17~19 유시": 18, "19~21 술시": 20, "21~23 해시": 22
}

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    user_name = st.text_input("성함", value="", placeholder="성함을 입력하세요")
    y = st.number_input("출생년", 1900, 2100, value=None, placeholder="YYYY")
    m = st.number_input("출생월", 1, 12, value=None, placeholder="MM")
    d = st.number_input("출생일", 1, 31, value=None, placeholder="DD")
    h_str = st.selectbox("출생 시간", list(hour_time_map.keys()), index=0)
    
    col1, col2 = st.columns(2)
    with col1: cal_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    with col2: is_leap = st.checkbox("윤달 여부") if cal_type == "음력" else False
    
    target_y = st.number_input("운세를 보고 싶은 연도", 1900, 2100, value=2026)
    submitted = st.button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 3️⃣ 로직 보완: 삼재 및 십신/운세 계산 함수 추가
def get_samjae_status(year_ganzhi, target_year):
    zodiac = year_ganzhi[-1]
    samjae_map = {'申子辰': ['寅', '卯', '辰'], '亥卯未': ['巳', '午', '未'], '寅午戌': ['申', '酉', '戌'], '巳酉丑': ['亥', '子', '丑']}
    my_group = next((v for k, v in samjae_map.items() if zodiac in k), [])
    target_zodiac = Solar.fromYmd(target_year, 1, 1).getLunar().getYearInGanZhi()[-1]
    if target_zodiac in my_group:
        status = ["들삼재", "눌삼재", "날삼재"][my_group.index(target_zodiac)]
        return f"현재 {target_year}년은 귀하의 **{status}** 기간입니다.", "samjae-active"
    return f"{target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.", "samjae-inactive"

# 4️⃣ 동적 통변 엔진 (개인화 로직으로 업그레이드)
def get_dynamic_report(d_gan, max_elem, name, target_y):
    # 일간별 성질 정의
    gan_nature = {
        '甲': "하늘로 뻗어가는 큰 나무처럼 강직하고 창의적인", '乙': "바람에 유연하게 대처하며 생명력이 끈질긴",
        '丙': "세상을 밝게 비추는 태양처럼 정열적이고 화려한", '丁': "밤하늘을 비추는 등불처럼 따뜻하고 섬세한",
        '戊': "드넓은 대지처럼 묵직하고 모든 것을 포용하는", '己': "만물을 키워내는 문전옥답처럼 주밀하고 다정한",
        '庚': "강인한 바위와 칼처럼 결단력 있고 명확한", '辛': "섬세하게 세공된 보석처럼 날카롭고 예민한",
        '壬': "깊은 바다와 강물처럼 지혜롭고 유연한 흐름을 지닌", '癸': "만물을 적시는 단비처럼 세밀하고 통찰력 있는"
    }
    
    # 오행별 음악적 키워드
    ohaeng_mus = {
        '목': "어쿠스틱한 공간감과 서사적인 멜로디 라인", '화': "폭발적인 에너지와 대중을 압도하는 화려한 톤",
        '토': "안정적인 밸런스와 사운드의 중심을 잡는 프로듀싱", '금': "명징하고 정교한 테크닉, 하이엔드 엔지니어링",
        '수': "몽환적이고 깊은 공간감, 무의식을 자극하는 선율"
    }

    # 개인별 종합 통변 생성 (300자 이상 조합)
    gen_text = f"본인은 {d_gan}의 정기를 타고나 {gan_nature.get(d_gan, '')} 성품을 소유하고 있습니다. 특히 {max_elem}의 기운이 발달한 명식은 자신의 신념을 예술적으로 승화시키는 힘이 남다릅니다. {name}님의 사주는 단순히 외부의 환경에 휘둘리기보다는 본인의 내면에서 솟구치는 창작의 욕구를 현실적인 결과물로 만들어낼 때 비로소 큰 성취를 맛보는 구조입니다. 주변 사람들과의 신의를 중요하게 여기며, 한 번 시작한 일은 끝까지 완수하려는 책임감이 돋보입니다. 이러한 기질은 인생의 후반부로 갈수록 더욱 견고한 성공의 기틀을 마련하게 될 것이며, 타인에게 영감을 주는 리더로서의 면모를 유감없이 발휘하게 될 것입니다."
    
    mus_text = f"{name}님의 음악 세계는 {ohaeng_mus.get(max_elem, '')}이 완벽하게 조화를 이루며 독보적인 아우라를 형성합니다. {d_gan}일간 특유의 감성이 {max_elem}의 발달된 감각과 만나면서, 단순히 듣기 좋은 소리를 넘어 청중의 영혼을 울리는 깊은 잔향을 남깁니다. 악기를 다루거나 곡을 쓸 때 디테일한 부분까지 집요하게 파고드는 완벽주의는 본인의 음악적 결과물을 항상 최상의 퀄리티로 유지하게 만드는 원동력입니다. 대중의 트렌드를 읽으면서도 그 안에 본인만의 고유한 사운드 정체성을 녹여내는 능력이 탁월하여, 시간이 흐를수록 대체 불가능한 아티스트로 평가받게 될 것입니다."

    # 연도별 동적 운세 로직
    target_lunar = Solar.fromYmd(target_y, 1, 1).getLunar()
    year_gan = target_lunar.getYearGan()
    year_desc = f"{target_y}년({target_lunar.getYearInGanZhi()})은 본인의 {d_gan} 기운이 {year_gan}의 흐름을 만나 새로운 변화를 맞이하는 해입니다."
    
    year_gen_text = f"{year_desc} 올해는 그동안 보이지 않는 곳에서 묵묵히 쌓아온 내공이 사회적인 환경과 조우하여 강력한 결실을 맺는 시기입니다. {target_y}년의 기운은 {name}님에게 명예와 실리를 동시에 안겨줄 수 있는 귀한 기회를 제공할 것이며, 특히 새로운 문서운이나 계약 관계에서 긍정적인 소식이 들려올 확률이 매우 높습니다. 주저하지 말고 본인의 직관을 믿고 추진하십시오."
    
    year_mus_text = f"예술가로서 {target_y}년은 본인만의 '사운드 정체성'이 대중에게 가장 강렬하게 각인되는 시기입니다. 올해의 천간 기운은 창의적인 영감을 현실적인 테크닉으로 치환하는 데 도움을 주며, 대규모 공연이나 중요한 음반 작업을 통해 아티스트로서의 커리어에서 기념비적인 작품을 탄생시킬 절호의 기회를 맞이하게 될 것입니다."

    return gen_text, mus_text, year_gen_text, year_mus_text

# 5️⃣ 결과 출력 (기존 레이아웃 엄수)
if submitted:
    if not (y and m and d) or h_str == "시간 선택 (또는 모름)":
        st.error("생년월일과 시간을 정확히 입력해주세요.")
    else:
        h_val = hour_time_map[h_str]
        calc_h = 12 if h_val == "unknown" else h_val
        lunar = Solar.fromYmdHms(int(y), int(m), int(d), calc_h, 0, 0).getLunar() if cal_type == "양력" else Lunar.fromYmdHms(int(y), (int(m) * -1) if is_leap else int(m), int(d), calc_h, 0, 0)
        ba_zi = [lunar.getYearInGanZhi(), lunar.getMonthInGanZhi(), lunar.getDayInGanZhi(), "?" if h_val == "unknown" else lunar.getTimeInGanZhi()]
        d_gan = lunar.getDayGan()
        
        ohaeng_map = {'목': '甲乙寅卯', '화': '丙丁巳午', '토': '戊己辰戌丑未', '금': '庚辛申酉', '수': '壬癸亥子'}
        count_target = "".join(ba_zi[:3]) if h_val == "unknown" else "".join(ba_zi)
        counts = {k: sum(1 for c in count_target if c in v) for k, v in ohaeng_map.items()}
        max_elem = max(counts, key=counts.get)
        
        display_name = user_name if user_name else "아티스트"
        # 동적 리포트 생성
        gen_text, mus_text, y_gen, y_mus = get_dynamic_report(d_gan, max_elem, display_name, target_y)
        samjae_msg, samjae_class = get_samjae_status(ba_zi[0], target_y)

        st.markdown(f"### 🍀 {display_name}님의 심층 리포트")
        st.markdown("<div class='saju-grid'>" + "".join([f"<div class='saju-box'><small>{l}</small><br>{v}</div>" for l, v in zip(['년주','월주','일주','시주'], ba_zi)]) + "</div>", unsafe_allow_html=True)
        st.markdown("<div class='ohaeng-grid'>" + "".join([f"<div class='ohaeng-item'><small>{k}</small><br><b>{v}자</b></div>" for k,v in counts.items()]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='{samjae_class}'><b>🚫 삼재(三災) 정보: {samjae_msg}</b><br><small>삼재는 9년마다 돌아오는 3년의 조심하는 시기를 뜻합니다.</small></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{gen_text}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>{mus_text}</div></div>", unsafe_allow_html=True)

        # 🎤 추천 포지션 (동적 구현)
        pos_title = "리드 보컬 및 기타리스트" if max_elem in ['화', '금'] else "작곡가 및 프로듀서"
        st.markdown(f"""
        <div class='position-card'>
            <h2>✨ 추천 음악 포지션 및 전문 재능</h2>
            <div class='content-text'>
                <span class='pos-title'>🎤 {pos_title}</span>
                귀하의 명식에서 가장 빛나는 음악적 포지션은 {max_elem}의 기운이 본인의 일간 {d_gan}과 만나는 지점에 있습니다. 
                강렬한 표출력은 무대 위에서 청중의 시선을 단숨에 사로잡는 무대 장악력으로 치환되며, 이는 단순히 기술적인 연주를 넘어 곡의 감정적 고조를 본인의 에너지를 통해 극적으로 끌어올리는 천부적인 자질을 갖추고 있음을 의미합니다.
                <br><br>
                <span class='pos-title'>🎚️ 사운드 메이킹 및 디자인</span>
                본인의 완벽주의적 속성은 사운드 엔지니어링 작업에서 타의 추종을 불허하는 전문성으로 나타납니다. 
                불필요한 요소를 걷어내고 악기 간의 조화를 본능적으로 조율하며, 곡의 의도에 가장 부합하는 세련된 톤을 찾아내는 데 탁월한 두각을 나타낼 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 📅 연도별 동적 운세 출력
        st.markdown(f"### 📅 {target_y}년 심층 운세")
        st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ 일반 운세 흐름</h2>
            <div class='content-text'>{y_gen}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='music-card' style='background-color:#FFF5F7;'>
            <h2>🎹 음악적 흐름 이야기</h2>
            <div class='content-text'>{y_mus}</div>
        </div>
        """, unsafe_allow_html=True)
