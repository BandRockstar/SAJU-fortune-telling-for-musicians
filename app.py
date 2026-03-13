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

        # 2층: 사주 원국 출력
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

        st.write(f"**정보:** {display_text} | {gender}")

        # 3층: 삼재 분석
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
            samjae_types = ["들삼재", "눌삼재", "날삼재"]
            current_status = samjae_types[samjae_idx]
            st.error(f"🚫 **삼재: {target_year}년은 귀하의 삼재 기간({current_status})입니다.**\n\n삼재는 9년 주기로 돌아와 3년 동안 머무는 세 가지 재난을 의미합니다. 현재 귀하는 에너지가 응축되고 외부의 변화에 민감하게 반응하는 시기에 놓여 있습니다. 이 시기에는 새로운 확장보다는 내실을 기하고, 대인 관계에서의 구설이나 예기치 못한 사고를 미연에 방지하기 위해 평소보다 신중한 태도를 유지하는 것이 좋습니다. 특히 감정적인 결단보다는 객관적인 데이터와 주변의 조언을 수용하며 자중자애하는 자세가 액운을 복으로 바꾸는 열쇠가 될 것입니다.")
        else:
            st.success(f"✅ **삼재: {target_year}년은 삼재에 해당하지 않습니다.**\n\n축하드립니다. 현재 귀하는 삼재의 영향권에서 벗어나 에너지가 비교적 맑고 순탄하게 흐르는 운세의 흐름 속에 있습니다. 무거운 기운이 물러가고 본연의 역량을 온전히 발휘할 수 있는 환경이 조성되는 시기이므로, 그동안 계획해왔던 일들을 적극적으로 추진하거나 새로운 도전을 시작하기에 매우 적합한 타이밍입니다. 다만 운의 흐름이 좋다고 해서 무리한 과욕을 부리기보다는, 자신의 페이스를 유지하며 주변 사람들과 성과를 나누는 포용력을 발휘한다면 현재의 길운을 더욱 길게 유지할 수 있을 것입니다.")

        # 4층: 정통 명리 심층 통변
        st.divider()
        st.subheader(f"📜 심층 통변 리포트")

        gan_elements = {"甲":"木", "乙":"木", "丙":"火", "丁":"火", "戊":"土", "己":"土", "庚":"金", "辛":"金", "壬":"水", "癸":"水"}
        zi_elements = {"寅":"木", "卯":"木", "巳":"火", "午":"火", "申":"金", "酉":"金", "亥":"水", "子":"水", "辰":"土", "戌":"土", "丑":"土", "未":"土"}
        all_chars = [y_gan[0], y_zi[0], m_gan[0], m_zi[0], d_gan[0], d_zi[0], t_gan[0], t_zi[0]]
        
        counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for c in all_chars:
            if c in gan_elements: counts[gan_elements[c]] += 1
            elif c in zi_elements: counts[zi_elements[c]] += 1

        my_day_gan = d_gan[0]
        my_element = gan_elements.get(my_day_gan, "알수없음")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.write("**[오행 분포]**")
            res_list = [f"{k}({counts[k]})" for k in ["木", "火", "土", "金", "水"]]
            st.code(" | ".join(res_list))
        with col_res2:
            st.write("**[일간 속성]**")
            st.code(f"{my_day_gan} ({my_element})")

        max_ele = max(counts, key=counts.get)
        # 1. 오행 구성 분석
        part1 = f"**1. 오행의 균형 및 기질 분석:** {name}님의 사주 구성을 심층 분석한 결과, 전체 8글자 중 {max_ele}의 기운이 {counts[max_ele]}개로 가장 강력한 세력을 형성하고 있습니다. "
        if counts[max_ele] >= 3:
            part1 += f"명리학적으로 특정 오행이 이토록 강성한 명조는 기질이 매우 선명하고 주관이 뚜렷하여 자신만의 독자적인 영역을 구축하는 데 탁월한 능력을 보입니다. 외부의 거센 풍파나 주변의 간섭에도 불구하고 자신의 신념과 원칙을 관철해 나가는 강인한 추진력을 소유하고 계십니다. 다만, 이러한 강한 에너지는 때로 타인에게 독단적으로 비춰질 수 있으므로, 자신의 강점인 에너지를 부드럽게 표출하는 유연함을 갖춘다면 사회적 성취의 크기는 더욱 거대해질 것입니다. 본인의 에너지가 집중된 만큼 전문 분야에서의 성취는 보장되어 있으나, 부족한 오행의 기운을 보강하기 위해 일상에서 색상이나 음식, 혹은 사람과의 인연을 통해 균형을 맞추려는 노력이 병행된다면 대운의 흐름을 더욱 유리하게 이끌 수 있습니다."
        else:
            part1 += f"오행의 분포가 어느 한쪽으로 치우치지 않고 비교적 고르게 분포되어 있어 성품이 원만하고 매사에 균형 감각이 대단히 뛰어난 명조입니다. 편중되지 않은 객관적인 시각으로 사물의 본질을 바라볼 줄 알며, 어떠한 환경에서도 빠르게 적응하고 주변 사람들과 조화롭게 융화되는 유연한 처세술이 강점입니다. 이러한 중용의 기질은 대인 관계에서 높은 신망을 얻게 하며, 위기 상황에서도 극단에 치우치지 않고 합리적인 해결책을 찾아내는 중재자로서의 면모를 돋보이게 합니다. 자신의 내면에 잠재된 다양한 오행의 역량을 때에 맞춰 꺼내 쓸 수 있는 다재다능함을 갖추고 있으므로, 이를 구체적인 목표와 결합한다면 안정적이면서도 지속적인 발전을 이룩할 수 있는 귀한 명조라 할 수 있습니다."

        # 2. 본질 분석
        part2 = f"**2. 본신의 성정과 심리적 특징:** 본신(自身)을 상징하는 일간 {my_day_gan}은 오행상 {my_element}의 근본적인 성질을 내포하고 있습니다. "
        if my_element == "木": part2 += "오상 중 인(仁)을 상징하는 나무처럼 위로 뻗어 나가려는 향상심과 창의적인 기획력이 돋보입니다. 타인을 배려하는 어진 마음씨와 생동감 넘치는 생명력을 지녔으나, 때로는 굽히지 않는 고집으로 인해 갈등을 빚을 수 있습니다. 그러나 근본적으로 성장을 지향하는 성품이기에 배움에 능하고 새로운 가치를 창조하는 일에서 영혼의 만족감을 얻는 유형입니다."
        elif my_element == "火": part2 += "오상 중 예(禮)를 상징하는 불꽃처럼 열정적이고 화려하며, 자신을 세상에 드러내어 소통하려는 표현력이 대단히 강력합니다. 감수성이 풍부하고 명확한 것을 선호하며 주변을 밝게 만드는 긍정적인 에너지를 전파합니다. 다만 감정의 기복을 다스리는 절제력을 보강한다면, 본연의 불꽃은 타인을 태우는 열기가 아닌 모두를 비추는 따뜻한 빛으로 승화될 것입니다."
        elif my_element == "土": part2 += "오상 중 신(信)을 상징하는 대지처럼 묵직하고 신의가 두터우며, 만물을 품는 포용력을 갖추고 있습니다. 매사에 신중하고 원칙을 변함없이 지켜나가는 중용의 덕이 있어 주변 사람들에게 깊은 신뢰를 얻습니다. 변화보다는 안정을 추구하는 경향이 있으나, 그 내면에는 무엇이든 수용하고 길러낼 수 있는 무한한 잠재력과 끈기 있는 생명력이 잠재되어 있는 든든한 명조입니다."
        elif my_element == "金": part2 += "오상 중 의(義)를 상징하는 금속의 날카로운 결단력처럼 시비지심이 분명하고 일 처리에 있어 완벽을 기하는 냉철한 성정을 지니고 있습니다. 불필요한 것을 과감히 쳐내는 과단성과 강직한 의리는 귀하를 지도자적 위치로 이끄는 핵심 동력입니다. 차가운 금속이 뜨거운 담금질을 거쳐 보검이 되듯, 시련을 통해 더욱 견고해지는 성취형 인간의 표본이라 할 수 있습니다."
        else: part2 += "오상 중 지(智)를 상징하는 물처럼 유연하고 지혜로우며, 깊은 감수성과 영감을 바탕으로 내면의 통찰을 이뤄내는 명조입니다. 어떤 그릇에도 담길 수 있는 적응력과 보이지 않는 곳에서 흐르며 세상을 적시는 헌신적인 면모가 돋보입니다. 바다와 같은 넓은 마음으로 정보를 수집하고 지식을 탐구하는 지적 욕구가 강하며, 이를 통해 세상을 이롭게 하는 지혜를 전하는 역할을 수행합니다."
        
        part2 += " 이러한 본신의 기질은 사주 전체의 흐름과 결합하여 귀하만의 독특한 아우라를 형성합니다. 자신의 타고난 기운을 억제하기보다는 순리대로 활용하되, 부족한 부분을 인지하고 채워나가는 지혜를 발휘한다면 삶의 질은 더욱 풍요로워질 것입니다."

        # 3. 음악적 사주 통변 (신규 신설 메뉴 - 300자 이상)
        music_part = f"**3. 음악적 사주 통변 (페르소나 분석):** {name}님의 사주 에너지를 음악적 요소로 치환해 보면, 귀하는 "
        if my_element == "木":
            music_part += "생동감 넘치는 '어쿠스틱 선율'과 닮아 있습니다. 목(木) 기운의 성장 에너지는 현악기의 울림처럼 유기적이며 따뜻한 정서를 자아냅니다. 장르적으로는 포크(Folk)나 실내악 같은 편안하면서도 생명력이 느껴지는 곡조가 귀하의 본질과 공명합니다. 곡의 도입부에서 점진적으로 고조되는 크레셴도(Crescendo)처럼, 시간이 흐를수록 깊이를 더해가는 음악적 서사를 지녔습니다. 이러한 에너지는 사람들의 마음속에 새로운 영감을 심어주는 치유의 선율이 됩니다."
        elif my_element == "火":
            music_part += "강렬한 에너지를 발산하는 '오케스트라의 금관악기' 또는 '화려한 일렉트로닉 사운드'와 공명합니다. 화(火)의 기운은 무대를 압도하는 솔로 연주자처럼 자신을 표현하는 데 거침이 없으며, 장르적으로는 열정적인 재즈(Jazz)나 웅장한 교향곡의 클라이맥스와 닮아 있습니다. 귀하의 삶은 화려한 화음과 빠른 템포가 어우러진 비르투오소(Virtuoso)의 연주와 같아, 대중에게 강렬한 인상을 남기고 감정을 동화시키는 강력한 흡입력을 발휘하는 음악적 명조입니다."
        elif my_element == "土":
            music_part += "모든 소리를 안정적으로 받쳐주는 '콘트라베이스' 또는 '대지를 울리는 타악기'의 낮은 공명과 닮아 있습니다. 토(土)의 기운은 음악 전체의 중심을 잡는 베이스 라인처럼 묵직하고 변함없는 신뢰감을 줍니다. 장르적으로는 명상 음악이나 장중한 합창곡처럼 영혼을 안정시키는 깊이 있는 울림이 귀하의 기질과 일치합니다. 화려한 기교보다는 정박자의 정직함과 깊은 배음(Harmonics)을 통해 세상에 안식과 토대를 제공하는, 삶의 근간이 되는 음악적 에너지를 보유하고 계십니다."
        elif my_element == "金":
            music_part += "명징하고 날카로운 '피아노의 고음역대' 또는 '정교하게 벼려진 금속 악기'의 소리와 닮아 있습니다. 금(金)의 기운은 흐트러짐 없는 완벽한 조율과 정교한 리듬감을 상징하며, 장르적으로는 구조적 미학이 극대화된 바로크 음악이나 현대적인 미니멀리즘 음악과 공명합니다. 귀하의 에너지는 불필요한 잡음이 섞이지 않은 순수한 사인파(Sine Wave)처럼 명확하고 결단력이 있어, 삶의 서사 속에서 군더더기 없는 완벽한 마무리를 지향하는 고결한 소나타와 같습니다."
        else:
            music_part += "끝없이 깊고 유연한 '플루트의 선율' 또는 '신비로운 앰비언트 사운드'와 공명합니다. 수(水)의 기운은 정해진 형태 없이 흐르는 물처럼 즉흥 연주(Improvisation)에 능하며, 청각적 상상력을 자극하는 몽환적인 화성학과 닮아 있습니다. 장르적으로는 경계가 없는 뉴에이지나 깊은 사유를 유도하는 블루스(Blues)와 일맥상통합니다. 귀하의 삶은 잔잔한 파도에서 폭포수까지 아우르는 넓은 스펙트럼의 다이내믹을 지니고 있어, 듣는 이의 무의식을 어루만지는 깊은 영성의 음악을 연주합니다."

        music_part += f" 종합적으로 볼 때, {name}님은 사주에 흐르는 오행의 배합을 통해 자신만의 고유한 심포니를 작곡해 나가는 연주자와 같습니다. 강성한 {max_ele}의 기운을 곡의 메인 테마로 삼되, 다른 오행의 기운을 다채로운 변주(Variation)로 활용하신다면 더욱 완성도 높은 인생의 대곡을 완성하실 수 있을 것입니다."

        st.info(part1)
        st.info(part2)
        st.info(music_part)

    else:
        st.warning("성함을 입력해 주세요.")
