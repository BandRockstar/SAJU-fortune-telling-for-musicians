import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정 (모바일 최적화 레이아웃)
st.set_page_config(
    page_title="밴드맨을 위한 사주통변", 
    page_icon="☯️",
    layout="centered"
)

# 모바일 대응 커스텀 CSS (기존 유지 및 가독성 강화 추가)
st.markdown("""
    <style>
    /* 기본 폰트 및 배경 최적화 */
    .main {
        background-color: #ffffff;
    }
    .stAlert p {
        font-size: 0.9rem !important;
        line-height: 1.7;
        word-break: keep-all;
    }
    /* 메트릭 및 컬럼 간격 조정 */
    div[data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }
    [data-testid="column"] {
        padding: 0 3px !important;
    }
    /* 섹션 헤더 디자인 강화 */
    .section-header {
        background-color: #1E1E1E;
        color: #FFFFFF;
        padding: 12px;
        border-radius: 8px;
        border-left: 8px solid #ff4b4b;
        margin: 25px 0 15px 0;
        font-size: 1.05rem;
        font-weight: bold;
    }
    /* 카드형 결과창 스타일 */
    .stInfo {
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        background-color: #fafafa !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* 모바일 텍스트 정렬 */
    .report-text {
        text-align: justify;
        letter-spacing: -0.02em;
    }
    /* 버튼 스타일 확장 */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 방문 횟수 표시
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 1
else:
    st.session_state.visit_count += 1

col_title, col_visit = st.columns([4, 1])
with col_title:
    st.title("☯️ 밴드맨을 위한 사주통변")
with col_visit:
    st.write(f"방문: {st.session_state.visit_count}")

# 2. 사주 정보 입력 섹션 (기존 코드 유지)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("출생년", 1900, 2026, value=1981)
    with col2:
        month = st.number_input("출생월", 1, 12, value=2)
    with col3:
        day = st.number_input("출생일", 1, 31, value=7)

    time_options = [
        "모름",
        "23:30~01:30 자시 (子)", "01:30~03:30 축시 (丑)", "03:30~05:30 인시 (寅)",
        "05:30~07:30 묘시 (卯)", "07:30~09:30 진시 (辰)", "09:30~11:30 사시 (巳)",
        "11:30~13:30 오시 (午)", "13:30~15:30 미시 (未)", "15:30~17:30 신시 (申)",
        "17:30~19:30 유시 (酉)", "19:30~21:30 술시 (戌)", "21:30~23:30 해시 (亥)"
    ]
    birth_time = st.selectbox("출생 시간", time_options, index=4)
    
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달인가요?")

    target_year = st.number_input("운세를 보고 싶은 연도", min_value=1900, max_value=2100, value=2026)
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

# 3. 분석 버튼 및 결과 도출
if st.button("🎭 심층 이원 통변 리포트 생성"):
    if name:
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_text = f"양력 {year}년 {month}월 {day}일"
        else:
            if is_leap_month:
                lunar_obj = Lunar.fromYmd(year, month, day, True)
            else:
                lunar_obj = Lunar.fromYmd(year, month, day)
            display_text = f"음력 {year}년 {month}월 {day}일" + (" (윤달)" if is_leap_month else " (평달)")

        eight_char = lunar_obj.getEightChar()
        
        gan_ko = {"甲":"갑", "乙":"을", "丙":"병", "丁":"정", "戊":"무", "己":"기", "庚":"경", "辛":"신", "壬":"임", "癸":"계"}
        zi_ko = {"子":"자", "丑":"축", "寅":"인", "卯":"묘", "辰":"진", "巳":"사", "午":"오", "未":"미", "申":"신", "酉":"유", "戌":"술", "亥":"해"}

        def format_ganzi(ganzi_str):
            if not ganzi_str or len(ganzi_str) < 2: return "?", "?"
            gan, zi = ganzi_str[0], ganzi_str[1]
            return f"{gan}({gan_ko.get(gan, '')})", f"{zi}({zi_ko.get(zi, '')})"

        y_gan, y_zi = format_ganzi(eight_char.getYear())
        m_gan, m_zi = format_ganzi(eight_char.getMonth())
        d_gan, d_zi = format_ganzi(eight_char.getDay())
        
        if birth_time == "모름":
            t_gan, t_zi = "?", "?"
        else:
            selected_zi = ""
            for char in birth_time:
                if char in zi_ko: selected_zi = char; break
            hour_map = {"子":0, "丑":2, "寅":4, "卯":6, "辰":8, "巳":10, "午":12, "未":14, "申":16, "酉":18, "戌":20, "亥":22}
            target_hour = hour_map.get(selected_zi, 0)
            if calendar_type == "양력":
                precise_solar = Solar.fromYmdHms(year, month, day, target_hour, 30, 0)
                precise_eight_char = precise_solar.getLunar().getEightChar()
                t_gan, t_zi = format_ganzi(precise_eight_char.getTime())
            else:
                precise_lunar = Lunar.fromYmdHms(year, month, day, target_hour, 30, 0, is_leap_month)
                precise_eight_char = precise_lunar.getEightChar()
                t_gan, t_zi = format_ganzi(precise_eight_char.getTime())

        st.divider()
        st.subheader(f"📊 {name}님 사주 원국")
        col_t, col_d, col_m, col_y = st.columns(4)
        with col_y: st.caption("년주"); st.info(f"{y_gan}\n{y_zi}")
        with col_m: st.caption("월주"); st.info(f"{m_gan}\n{m_zi}")
        with col_d: st.caption("일주"); st.info(f"{d_gan}\n{d_zi}")
        with col_t: st.caption("시주"); st.info(f"{t_gan}\n{t_zi}")
        st.write(f"**정보:** {display_text} | {gender}")

        # [삼재 분석] 수정된 명리학 판별식
        st.divider()
        my_year_zi = eight_char.getYear()[1]
        samjae_groups = {
            "申": ["寅", "卯", "辰"], "子": ["寅", "卯", "辰"], "辰": ["寅", "卯", "辰"],
            "寅": ["申", "酉", "戌"], "午": ["申", "酉", "戌"], "戌": ["申", "酉", "戌"],
            "巳": ["亥", "子", "丑"], "酉": ["亥", "子", "丑"], "丑": ["亥", "子", "丑"],
            "亥": ["巳", "午", "未"], "卯": ["巳", "午", "未"], "未": ["巳", "午", "未"]
        }
        my_samjae_zis = samjae_groups.get(my_year_zi, [])
        target_solar = Solar.fromYmd(target_year, 1, 1)
        target_year_zi = target_solar.getLunar().getEightChar().getYear()[1]
        
        if target_year_zi in my_samjae_zis:
            samjae_idx = my_samjae_zis.index(target_year_zi)
            current_status = ["들삼재", "눌삼재", "날삼재"][samjae_idx]
            st.error(f"🚫 **삼재: {target_year}년은 귀하의 삼재 기간({current_status})입니다.**\n\n삼재는 9년 주기로 돌아와 3년 동안 머무는 에너지의 정체기를 의미합니다. 현재 귀하는 기운이 내면으로 응축되고 외부의 변화에 민감하게 반응하는 시기에 놓여 있습니다. 이 시기에는 새로운 확장보다는 내실을 기하고, 대인 관계에서의 구설이나 예기치 못한 사고를 미연에 방지하기 위해 평소보다 신중한 태도를 유지하는 것이 좋습니다. 특히 감정적인 결단보다는 객관적인 데이터와 주변의 조언을 수용하며 자중자애하는 자세가 액운을 복으로 바꾸는 열쇠가 될 것입니다. 인내를 가지고 현재의 자산을 지키는 데 집중한다면 삼재의 풍파를 무사히 넘길 수 있을 것입니다. 삼재를 지혜롭게 보낸다면 다가올 길운을 더욱 크게 누릴 수 있는 법입니다. 인고의 시간을 견디며 내공을 쌓는다면 삼재가 끝난 뒤 비약적인 발전을 이룰 수 있을 것입니다.")
        else:
            st.success(f"✅ **삼재: {target_year}년은 삼재에 해당하지 않습니다.**\n\n축하드립니다. 현재 귀하는 삼재의 영향권에서 완전히 벗어나 기운이 비교적 맑고 순탄하게 흐르는 운세의 흐름 속에 있습니다. 무거운 기운이 물러가고 본연의 역량을 온전히 발휘할 수 있는 환경이 조성되는 시기이므로, 그동안 계획해왔던 일들을 적극적으로 추진하거나 새로운 도전을 시작하기에 매우 적합한 타이밍입니다. 자신감을 가지고 활동하신다면 길운을 더욱 길게 유지할 수 있을 것입니다. 긍정적인 에너지를 주변과 나누며 목표를 향해 매진하기에 가장 좋은 시기임을 잊지 마십시오. 운세의 맑은 흐름을 타서 큰 성취를 거두시길 바랍니다. 지금의 활발한 에너지를 바탕으로 인생의 새로운 전환점을 만드시길 응원합니다.")

        # 심층 통변 리포트 섹션
        st.divider()
        st.subheader(f"📜 {name}님 심층 통변 리포트")
        gan_elements = {"甲":"木", "乙":"木", "丙":"火", "丁":"火", "戊":"土", "己":"土", "庚":"金", "辛":"金", "壬":"水", "癸":"水"}
        zi_elements = {"寅":"木", "卯":"木", "巳":"火", "午":"火", "申":"金", "酉":"金", "亥":"水", "子":"水", "辰":"土", "戌":"土", "丑":"土", "未":"土"}
        all_chars = [y_gan[0], y_zi[0], m_gan[0], m_zi[0], d_gan[0], d_zi[0], t_gan[0], t_zi[0]]
        counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for c in all_chars:
            if c in gan_elements: counts[gan_elements[c]] += 1
            elif c in zi_elements: counts[zi_elements[c]] += 1
        my_day_gan = d_gan[0]
        my_element = gan_elements.get(my_day_gan, "알수없음")
        max_ele = max(counts, key=counts.get)

        st.markdown('<div class="section-header">🔍 일반 역학 통변 (기질 및 성정 분석)</div>', unsafe_allow_html=True)
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.write("**[오행 분포]**")
            res_list = [f"{k}({counts[k]})" for k in ["木", "火", "土", "金", "水"]]
            st.code(" | ".join(res_list))
        with col_res2:
            st.write("**[일간 속성]**")
            st.code(f"{my_day_gan} ({my_element})")

        # 1) 오행 기질 (전문 복구)
        p1_text = f"**1) 오행의 균형 및 기질 분석:** {name}님의 사주 구성을 심층 분석한 결과, 전체 8글자 중 {max_ele}의 기운이 {counts[max_ele]}개로 강력하게 작용하고 있습니다. "
        if counts[max_ele] >= 3:
            p1_text += "명리학적으로 특정 오행이 이토록 강성한 명조는 기질이 매우 선명하고 주관이 뚜렷하여 자신만의 독자적인 영역을 구축하는 데 탁월한 능력을 보입니다. 외부의 거센 풍파나 주변의 간섭에도 불구하고 자신의 신념과 원칙을 관철해 나가는 강인한 추진력을 소유하고 계십니다. 다만, 이러한 강한 에너지는 때로 타인에게 독단적으로 비춰질 수 있으므로, 자신의 강점인 에너지를 부드럽게 표출하는 유연함을 갖춘다면 사회적 성취의 크기는 더욱 거대해질 것입니다. 본인의 에너지가 집중된 만큼 전문 분야에서의 성취는 보장되어 있으며, 부족한 오행의 기운을 보강하기 위해 일상에서 균형을 맞추려는 노력이 병행된다면 대운의 흐름을 더욱 유리하게 이끌 수 있을 것입니다. 자신의 개성을 무기로 삼아 독보적인 위치를 점하기에 최적화된 기운이며, 이는 예술적 성취뿐만 아니라 삶의 전반적인 방향성에서 강력한 자아가 원동력이 됨을 의미합니다."
        else:
            p1_text += "오행의 분포가 어느 한쪽으로 치우치지 않고 비교적 고르게 분포되어 있어 성품이 원만하고 매사에 균형 감각이 대단히 뛰어난 명조입니다. 편중되지 않은 객관적인 시각으로 사물의 본질을 바라볼 줄 알며, 어떠한 환경에서도 빠르게 적응하고 주변 사람들과 조화롭게 융화되는 유연한 처세술이 강점입니다. 이러한 중용의 기질은 대인 관계에서 높은 신망을 얻게 하며, 위기 상황에서도 극단에 치우치지 않고 합리적인 해결책을 찾아내는 중재자로서의 면모를 돋보이게 합니다. 자신의 내면에 잠재된 다양한 오행의 역량을 때에 맞춰 꺼내 쓸 수 있는 다재다능함을 갖추고 있으므로 안정적이면서도 지속적인 발전을 이룩할 수 있는 귀한 명조라 할 수 있습니다."
        st.info(p1_text)

        # 2) 본신 성정 (전문 복구)
        p2_text = f"**2) 본신의 성정과 심리적 특징:** 본신(自身)을 상징하는 일간 {my_day_gan}은 오행상 {my_element}의 근본적인 성질을 내포하고 있습니다. "
        if my_element == "木": p2_text += "오상 중 인(仁)을 상징하는 나무처럼 위로 뻗어 나가려는 향상심과 창의적인 기획력이 돋보입니다. 타인을 배려하는 어진 마음씨와 생동감 넘치는 생명력을 지녔으나, 때로는 굽히지 않는 고집으로 인해 갈등을 빚을 수 있습니다. 당신의 지적 호기심과 성장에 대한 열망은 주변을 정화하고 함께 상생하게 만드는 힘이 있으며, 척박한 땅에서도 뿌리를 내리는 끈질긴 생명력은 시련을 극복하는 강력한 무기가 됩니다."
        elif my_element == "火": p2_text += "오상 중 예(禮)를 상징하는 불꽃처럼 열정적이고 화려하며, 자신을 세상에 드러내어 소통하려는 표현력이 대단히 강력합니다. 감수성이 풍부하고 명확한 것을 선호하며 주변을 밝게 만드는 긍정적인 에너지를 전파합니다. 다만 감정의 기복을 다스리는 절제력을 보강한다면, 본연의 불꽃은 타인을 태우는 열기가 아닌 모두를 비추는 따뜻한 빛으로 승화될 것이며 명예로운 삶을 영위할 것입니다. 당신은 군중 속에서도 빛나는 아우라를 지녔으며, 자신의 감정을 소리와 빛으로 치환하여 타인의 가슴에 감동을 새기는 예술적 본능이 매우 발달한 명조입니다."
        elif my_element == "土": p2_text += "오상 중 신(信)을 상징하는 대지처럼 묵직하고 신의가 두터우며, 만물을 품는 포용력을 갖추고 있습니다. 매사에 신중하고 원칙을 변함없이 지켜나가는 중용의 덕이 있어 주변 사람들에게 깊은 신뢰를 얻습니다. 변화보다는 안정을 추구하는 경향이 있으나 그 내면에는 무엇이든 수용하고 길러낼 수 있는 무한한 잠재력과 끈기 있는 생명력이 잠재되어 있는 아주 든든하고 믿음직한 명조입니다."
        elif my_element == "金": p2_text += "오상 중 의(義)를 상징하는 금속의 날카로운 결단력처럼 시비지심이 분명하고 일 처리에 있어 완벽을 기하는 냉철한 성정을 지니고 있습니다. 불필요한 것을 과감히 쳐내는 과단성과 강직한 의리는 귀하를 지도자적 위치로 이끄는 핵심 동력입니다. 시련을 통해 더욱 견고해지는 성취형 인간의 표본이라 할 수 있으며, 한번 맺은 인연은 끝까지 책임지는 의리파의 면모를 보여줍니다."
        else: p2_text += "오상 중 지(智)를 상징하는 물처럼 유연하고 지혜로우며, 깊은 감수성과 영감을 바탕으로 내면의 통찰을 이뤄내는 명조입니다. 어떤 그릇에도 담길 수 있는 적응력과 보이지 않는 곳에서 흐르며 세상을 적시는 헌신적인 면모가 돋보입니다. 당신은 낮은 곳으로 흘러 바다를 이루는 수의 덕성을 지니고 있어, 음악적으로도 가장 깊고 오묘한 감성의 영역을 탐구하고 이를 타인과 유연하게 공유하는 능력이 탁월한 명조입니다."
        st.info(p2_text)

        # 음악적 사주 통변 (모든 오행별 전문 복구)
        st.markdown('<div class="section-header">🎵 음악적 사주 통변 (밴드 페르소나 분석)</div>', unsafe_allow_html=True)
        if my_element == "木":
            p_pos = "**1) 추천 음악 포지션: 기타 (Guitar)**\n\n귀하의 목(木) 기운은 생동감 있게 뻗어 나가는 현의 울림과 완벽하게 공명합니다. 멜로디를 생성해내는 창의적인 '리프 메이킹' 능력이 탁월하며, 복잡한 이론보다는 직관적인 감각으로 새로운 선율을 찾아내는 재능이 있습니다."
            p_style = "**2) 음악적 성향:** 끊임없이 성장하고 변화하는 나무처럼, 한 장르에 머물기보다는 다양한 실험적 요소를 도입하려는 경향이 강합니다. 포크의 따뜻함부터 블루스의 즉흥성까지 폭넓은 스펙트럼을 지향하며, 인위적인 가공보다는 악기 본연의 소리를 살린 유기적인 사운드를 선호합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 귀하는 밴드의 '성장을 주도하는 아이디어 뱅크'입니다. 팀이 매너리즘에 빠질 때 새로운 방향성을 제시하며 창작의 활력을 불어넣는 역할을 맡습니다. 리더십이 강해 곡의 전체적인 테마를 설정하는 데 주도적인 목소리를 낼 것입니다."
        elif my_element == "火":
            p_pos = "**1) 추천 음악 포지션: 보컬 (Vocal)**\n\n발산하는 화(火)의 기운은 청중의 감정을 단번에 사로잡는 보이스의 힘과 연결됩니다. 풍부한 성량과 화려한 테크닉을 구사하는 재능이 있으며, 곡의 감정적 절정을 압도적으로 표현해내는 능력이 탁월합니다."
            p_style = "**2) 음악적 성향:** 뜨겁게 타오르는 불꽃처럼 강렬하고 명확한 사운드를 지향합니다. 록, 메탈, 혹은 팝의 화려한 사운드 디자인을 선호하며 자신의 존재감을 확실히 드러낼 수 있는 구성을 추구합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 귀하는 밴드의 상징인 '프론트맨이자 에너지 메이커'입니다. 공연의 전체 분위기를 주도하며 관객과의 접점을 책임지는 가장 중요한 역할을 수행합니다."
        elif my_element == "土":
            p_pos = "**1) 추천 음악 포지션: 드럼 (Drum)**\n\n모든 오행을 조율하는 토(土)의 기운은 밴드의 심장인 드럼의 리듬과 일치합니다. 흔들리지 않는 정확한 타이밍 감각과 묵직한 타격감을 구현하는 재능이 있으며 사운드의 균형을 유지하는 전문성이 돋보입니다."
            p_style = "**2) 음악적 성향:** 화려한 기교보다는 사운드의 질감과 안정적인 그루브를 중시합니다. 묵직한 록 비트나 안정감 있는 팝 리듬을 선호하며 전체를 포용하는 음악 스타일을 지향합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 귀하는 밴드의 토대인 '안정적인 중재자이자 정신적 지주'입니다. 멤버들의 서로 다른 개성이 충돌할 때 이를 리듬으로 묶어 조화를 이루게 하는 중심축 역할을 합니다."
        elif my_element == "金":
            p_pos = "**1) 추천 음악 포지션: 키보드 (Keyboard)**\n\n정교하고 세밀한 금(金)의 기운은 디지털과 아날로그를 넘나드는 키보드의 사운드 디자인과 맞닿아 있습니다. 복잡한 화성학적 이론을 연주에 녹여내는 분석적인 재능이 탁월합니다."
            p_style = "**2) 음악적 성향:** 차갑고 명료하면서도 세련된 도시적 감성을 지향합니다. 사운드의 불순물을 걸러내고 가장 정제된 예술의 미를 구현하는 데 탁월하며 완벽하게 정제된 소리를 선호합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 귀하는 밴드의 '사운드 디렉터이자 완벽주의자'입니다. 합주 시 사운드의 균형과 편곡의 완성도를 최종적으로 점검하는 품질 보증자 역할을 수행합니다."
        else:
            p_pos = "**1) 추천 음악 포지션: 베이스 (Bass)**\n\n유연하게 흐르며 모든 소리를 감싸는 수(水)의 기운은 저음역대의 하모니를 책임지는 베이스와 완벽히 일치합니다. 드럼과 멜로디 사이를 연결하는 유기적 인터플레이 능력이 탁월합니다."
            p_style = "**2) 음악적 성향:** 강요하지 않으면서도 깊이 스며드는 음악 스타일을 선호합니다. 유연한 리듬이 돋보이는 펑크(Funk)나 몽환적인 엠비언트, 깊은 감성을 자극하는 블루지한 성향을 보입니다."
            p_place = "**3) 밴드 내 자신의 위치:** 귀하는 밴드의 '보이지 않는 설계자이자 유연한 전략가'입니다. 멤버들의 개성이 과할 때는 이를 부드럽게 감싸 안고, 부족할 때는 빈 자리를 소리 없이 채우는 헌신적인 서포터입니다."
        
        st.info(p_pos); st.info(p_style); st.info(p_place)

        # 4) 종합 의견 (복구)
        st.info(f"**4) 종합:** 결론적으로 {name}님은 사주 원국에 내재된 {max_ele}의 강성한 기운을 음악적 페르소나로 치환했을 때 독보적인 전문성을 발휘하는 명조입니다. 자신의 타고난 오행적 기질을 음악적 도구와 일치시켜 나갈 때, 단순한 기술적 연주를 넘어 청중의 영혼을 울리는 깊은 예술적 아우라를 뿜어낼 수 있을 것입니다.")

        # 📅 세운 분석 엔진 (전문 복구)
        st.markdown(f'<div class="section-header">📅 {target_year}년도 명리학적 세운(歲運) 분석</div>', unsafe_allow_html=True)
        t_solar = Solar.fromYmd(target_year, 1, 1); t_lunar = t_solar.getLunar()
        t_ganzi_year = t_lunar.getEightChar().getYear(); tg, tz = t_ganzi_year[0], t_ganzi_year[1]
        
        ten_god_db = {
            0: f"올해 {tg}년은 '비겁'의 해입니다. 본인만의 독보적인 톤을 확립하고 주도적으로 프로젝트를 이끌기에 최적입니다. 자신의 예술적 고집을 결과물로 증명하십시오.",
            1: f"올해 {tg}년은 '식상'의 해입니다. 창의력이 폭발하고 표현력이 빛을 발합니다. 기술적 연습보다 감각적인 즉흥 연주와 작곡에서 큰 호응을 얻을 것입니다.",
            2: f"올해 {tg}년은 '재성'의 해입니다. 공연 수익이나 저작권료 등 실질적인 보상이 따릅니다. 철저한 기획과 데이터에 기반한 활동이 큰 성취를 가져옵니다.",
            3: f"올해 {tg}년은 '관성'의 해입니다. 명예와 사회적 질서를 상징하며, 공신력 있는 무대의 제안이 예상됩니다. 프로페셔널한 책임감 있는 사운드가 필요한 때입니다.",
            4: f"올해 {tg}년은 '인성'의 해입니다. 내실을 다지고 전문 지식을 습득하기 좋습니다. 귀인의 도움이나 좋은 장비를 얻는 운세이니 깊이를 다지는 데 집중하십시오."
        }
        
        # 십신 계산 로직 (간략)
        ele_order = ["木", "火", "土", "金", "水"]
        tg_element = gan_elements.get(tg, "木")
        try: diff = (ele_order.index(tg_element) - ele_order.index(my_element)) % 5
        except: diff = 0
        
        main_text = ten_god_db.get(diff, "운세를 분석 중입니다.")
        st.info(f"**[{tg}{tz}년 연간 운세 핵심 요약]**\n\n**1. 환경과 심리 흐름:** {main_text}\n\n**2. 구체적 음악 가이드:** {tz}의 기운을 당신의 악기에 담아 후회 없는 연주를 이어가시길 바랍니다. 이 운세의 흐름을 지혜롭게 활용한다면 당신의 음악은 더욱 깊은 울림을 가질 것입니다.")
        
        st.success("✨ 모든 분석이 완료되었습니다. 음악과 사주의 지혜를 결합하여 최고의 한 해를 만드시길 바랍니다.")
