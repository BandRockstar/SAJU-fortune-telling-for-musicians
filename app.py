import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정 (모바일 최적화 레이아웃)
st.set_page_config(
    page_title="정통 사주 명리 분석", 
    page_icon="☯️",
    layout="centered"
)

# 모바일 대응 커스텀 CSS
st.markdown("""
    <style>
    .stAlert p {
        font-size: 0.95rem !important;
        line-height: 1.6;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
    }
    [data-testid="column"] {
        padding: 0 5px !important;
    }
    .report-text {
        text-align: justify;
    }
    .section-header {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ff4b4b;
        margin: 20px 0 10px 0;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("☯️ 정통 사주 명리 분석")

# 2. 사주 정보 입력 섹션 (1층: 고정)
with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("출생년", 1900, 2026, value=2000)
    with col2:
        month = st.number_input("출생월", 1, 12, value=1)
    with col3:
        day = st.number_input("출생일", 1, 31, value=1)

    time_options = [
        "모름",
        "23:30~01:30 자시 (子)", "01:30~03:30 축시 (丑)", "03:30~05:30 인시 (寅)",
        "05:30~07:30 묘시 (卯)", "07:30~09:30 진시 (辰)", "09:30~11:30 사시 (巳)",
        "11:30~13:30 오시 (午)", "13:30~15:30 미시 (未)", "15:30~17:30 신시 (申)",
        "17:30~19:30 유시 (酉)", "19:30~21:30 술시 (戌)", "21:30~23:30 해시 (亥)"
    ]
    birth_time = st.selectbox("출생 시간", time_options, index=0)
    
    calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달인가요?")

    target_year = st.number_input("운세를 보고 싶은 연도", min_value=1900, max_value=2100, value=2026)
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

# 3. 분석 버튼 및 결과 출력
if st.button("🎭 심층 이원 통변 리포트 생성"):
    if name:
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_text = f"양력 {year}년 {month}월 {day}일"
        else:
            lunar_obj = Lunar.fromYmd(year, month, day, is_leap_month)
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
                if char in zi_ko:
                    selected_zi = char
                    break

            hour_map = {"子":0, "丑":2, "寅":4, "卯":6, "辰":8, "巳":10, "午":12, "未":14, "申":16, "酉":18, "戌":20, "亥":22}
            target_hour = hour_map.get(selected_zi, 0)
            
            if calendar_type == "양력":
                precise_solar = Solar.fromYmdHms(year, month, day, target_hour, 30, 0)
                precise_eight_char = precise_solar.getLunar().getEightChar()
            else:
                precise_lunar = Lunar.fromYmdHms(year, month, day, target_hour, 30, 0, is_leap_month)
                precise_eight_char = precise_lunar.getEightChar()
            
            t_gan, t_zi = format_ganzi(precise_eight_char.getTime())

        # 사주 원국 출력
        st.divider()
        st.subheader(f"📊 {name}님 사주 원국")
        col_t, col_d, col_m, col_y = st.columns(4)
        with col_y:
            st.caption("년주")
            st.info(f"{y_gan}\n{y_zi}")
        with col_m:
            st.caption("월주")
            st.info(f"{m_gan}\n{m_zi}")
        with col_d:
            st.caption("일주")
            st.info(f"{d_gan}\n{d_zi}")
        with col_t:
            st.caption("시주")
            st.info(f"{t_gan}\n{t_zi}")

        # 삼재 분석
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
            st.error(f"🚫 **삼재: {target_year}년은 귀하의 삼재 기간({current_status})입니다.**\n\n현재 귀하는 기운이 내면으로 응축되고 주변 환경의 변화에 민감하게 반응하는 시기입니다. 밴드나 팀 활동 시 독단적인 결정보다는 멤버들의 의견을 경청하며 화합을 도모하는 지혜가 필요합니다. 무리한 확장보다는 내실을 다지는 자세가 액운을 복으로 바꾸는 열쇠가 될 것입니다.")
        else:
            st.success(f"✅ **삼재: {target_year}년은 삼재에 해당하지 않습니다.**\n\n축하드립니다. 현재 기운이 순탄하게 흐르는 시기이므로 계획해왔던 창작 활동이나 공연 등을 적극적으로 추진하기에 매우 적합합니다. 본연의 역량을 온전히 발휘하여 주변의 지지를 이끌어낼 수 있는 길운의 흐름 속에 있습니다.")

        # 심층 통변 리포트
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

        # [일반 역학 통변 단락]
        st.markdown('<div class="section-header">🔍 일반 역학 통변 (기질 및 성정 분석)</div>', unsafe_allow_html=True)
        part1 = f"**1) 오행 구성 분석:** {name}님의 사주는 {max_ele}의 기운이 {counts[max_ele]}개로 가장 강력합니다. "
        if counts[max_ele] >= 3:
            part1 += "특정 기운이 강성한 명조는 주관이 뚜렷하고 신념을 관철하는 힘이 대단합니다. 전문 분야에서의 성취도는 매우 높으나 자칫 독단적으로 흐를 수 있으니 유연함을 기르는 것이 성취의 크기를 결정할 것입니다. "
        else:
            part1 += "오행이 고루 분포되어 원만하고 균형 감각이 뛰어납니다. 중재 능력이 탁월하여 어떤 조직에서도 조화롭게 융화되며 합리적인 해결책을 찾아내는 지혜를 지니고 계십니다. "
        part1 += "이러한 오행의 배합은 삶의 전반에서 안정적인 토대를 제공하며, 대운의 흐름에 따라 자신의 역량을 다각도로 펼칠 수 있는 잠재력을 의미합니다."

        part2 = f"**2) 본질 성정 분석:** 일간 {my_day_gan}은 {my_element}의 성질을 내포합니다. "
        if my_element == "木": part2 += "인(仁)을 상징하며 진취적이고 창의적입니다. 나무처럼 성장하려는 욕구가 강해 늘 배움을 멈추지 않습니다. "
        elif my_element == "火": part2 += "예(禮)를 상징하며 열정적이고 자신을 드러내는 표현력이 강력합니다. 주변을 밝히는 긍정적 에너지를 전파합니다. "
        elif my_element == "土": part2 += "신(信)을 상징하며 묵직하고 신의가 두텁습니다. 만물을 품는 대지처럼 신중하게 원칙을 지켜나가는 덕이 있습니다. "
        elif my_element == "金": part2 += "의(義)를 상징하며 결단력이 날카롭고 완벽을 기합니다. 시비지심이 분명하여 일 처리가 냉철하고 견고합니다. "
        else: part2 += "지(智)를 상징하며 유연하고 지혜롭습니다. 깊은 감수성과 영감을 통해 내면의 통찰을 이뤄내는 지적인 명조입니다. "
        part2 += "자신의 타고난 기질을 긍정적으로 수용하고 부족한 기운을 보완한다면 삶의 질은 더욱 풍요로워질 것입니다."
        
        st.info(part1)
        st.info(part2)

        # [음악적 사주 통변 단락 - 악기 한정 및 밴드 활동 성향]
        st.markdown('<div class="section-header">🎵 음악적 사주 통변 (밴드 페르소나 분석)</div>', unsafe_allow_html=True)
        
        music_text = f"**{name}님의 사주 기운에 최적화된 악기와 밴드 활동 성향 분석:**\n\n"
        if my_element == "木":
            music_text += "귀하의 에너지는 생동감 넘치는 **'기타(Guitar)'**와 가장 잘 공명합니다. 나무의 성질인 목(木) 기운은 현의 울림을 통해 생명력을 발산하는 어쿠스틱/일렉 기타의 특성과 일치합니다. 밴드 내에서는 **'아이디어 뱅크이자 창의적인 리더'**로서 활동합니다. 곡의 테마를 설정하고 새로운 리프를 제안하는 등 성장을 주도하는 역할을 맡습니다. 다만, 때로는 자신의 음악적 고집을 앞세울 수 있으므로 멤버들과의 조화로운 합주를 위해 호흡을 맞추는 노력이 더해진다면 밴드의 사운드는 더욱 풍성해질 것입니다."
        elif my_element == "火":
            music_text += "귀하의 에너지는 무대를 장악하는 **'보컬(Vocal)'**에 최적화되어 있습니다. 화(火)의 발산하는 기운은 청중의 감정을 자극하고 에너지를 전파하는 보이스의 특성과 닮아 있습니다. 밴드 내에서는 **'화려한 프론트맨이자 분위기 메이커'**로 활동합니다. 관객과의 소통을 주도하고 공연의 에너지를 최고조로 끌어올리는 역할을 수행합니다. 감수성이 풍부하여 곡의 해석력이 뛰어나지만, 컨디션에 따른 기복을 잘 다스린다면 어떤 무대에서도 빛나는 압도적인 존재감을 발휘할 것입니다."
        elif my_element == "土":
            music_text += "귀하의 에너지는 중심을 잡아주는 **'드럼(Drum)'**과 깊은 인연이 있습니다. 모든 소리를 수용하고 박자를 지탱하는 토(土)의 기운은 밴드의 뼈대인 드럼의 특성과 일치합니다. 밴드 내에서는 **'든든한 조력자이자 중재자'**로서 활동합니다. 멤버들이 흔들리지 않게 안정적인 리듬을 제공하며, 팀 내 갈등이 생길 때 묵묵히 중심을 지키며 화합을 이끄는 정신적 지주 역할을 합니다. 화려한 기교보다는 정직하고 묵직한 비트를 통해 밴드 사운드의 완성도를 책임지는 핵심 멤버입니다."
        elif my_element == "金":
            music_text += "귀하의 에너지는 명징한 소리를 내는 **'키보드(Keyboard)'**와 닮아 있습니다. 구조적이고 정교한 조율을 상징하는 금(金) 기운은 전자 악기의 세밀한 사운드 디자인과 피아노의 명료한 터치와 공명합니다. 밴드 내에서는 **'사운드 디렉터이자 완벽주의자'**로 활동합니다. 전체적인 편곡의 완성도를 점검하고 사운드의 빈틈을 채우는 치밀함을 보여줍니다. 차가운 듯하지만 감각적인 텐션 코드를 사용하여 곡에 세련미를 더하며, 연습 과정에서도 원칙을 준수하여 밴드의 실력을 향상시키는 역할을 합니다."
        else:
            music_text += "귀하의 에너지는 깊은 울림을 주는 **'베이스(Bass)'**와 공명합니다. 유연하게 흐르며 저음을 채우는 수(水) 기운은 밴드의 하모니를 하나로 묶어주는 베이스 기타의 성질과 같습니다. 밴드 내에서는 **'보이지 않는 곳의 설계자이자 전략가'**로서 활동합니다. 드럼과 멜로디 악기 사이를 연결하는 지혜로운 플레이를 보여주며, 팀 전체의 흐름을 읽고 완급을 조절하는 탁월한 능력을 지녔습니다. 겉으로 드러나기보다 내실 있는 연주를 통해 팀의 깊이를 더하는 유연한 사유의 음악가입니다."

        music_text += f"\n\n종합적으로 {name}님은 강성한 {max_ele}의 기운을 바탕으로 밴드 내에서 독보적인 위치를 점합니다. 자신의 악기가 가진 특성을 명리학적 기질과 결합하여 활용한다면, 단순한 연주를 넘어 멤버들과 영혼으로 교감하는 진정한 앙상블을 이뤄낼 수 있을 것입니다."
        
        st.info(music_text)

    else:
        st.warning("성함을 입력해 주세요.")
