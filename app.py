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

    # 지시사항 반영: 2026년부터 2080년까지 범위 설정
    target_year = st.number_input("운세를 보고 싶은 연도", min_value=2026, max_value=2080, value=2026)
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

# 3. 분석 버튼 및 결과 도출
if st.button("🎭 심층 이원 통변 리포트 생성"):
    if name:
        # [생략 불가] 데이터 계산 로직
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

        # 사주 원국 출력부
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

        # 삼재 분석부
        st.divider()
        my_year_zi = eight_char.getYear()[1]
        samjae_groups = {
            "申": ["寅", "卯", "辰"], "子": ["寅", "卯", "辰"], "辰": ["寅", "卯", "辰"],
            "寅": ["申", "酉", "戌"], "午": ["申", "酉", "戌"], "戌": ["申", "酉", "戌"],
            "巳": ["亥", "子", "丑"], "酉": ["亥", "子", "丑"], "丑": ["亥", "子", "丑"],
            "亥": ["巳", "午", "未"], "卯": ["巳", "午", "미"], "未": ["巳", "午", "미"]
        }
        my_samjae_zis = samjae_groups.get(my_year_zi, [])
        target_solar_temp = Solar.fromYmd(target_year, 1, 1)
        target_year_zi_temp = target_solar_temp.getLunar().getEightChar().getYear()[1]
        
        if target_year_zi_temp in my_samjae_zis:
            samjae_idx = my_samjae_zis.index(target_year_zi_temp)
            current_status = ["들삼재", "눌삼재", "날삼재"][samjae_idx]
            st.error(f"🚫 **삼재: {target_year}년은 귀하의 삼재 기간({current_status})입니다.**\n\n삼재는 기운의 정체기를 의미하며 이 시기에는 내실을 기하고 신중한 태도를 유지하는 것이 중요합니다. 예기치 못한 변화에 흔들리지 않도록 자중자애하는 자세가 필요합니다.")
        else:
            st.success(f"✅ **삼재: {target_year}년은 삼재에 해당하지 않습니다.**\n\n현재 귀하는 삼재의 영향권 밖에서 비교적 맑은 기운을 유지하고 있습니다. 계획해온 일들을 적극적으로 추진하기에 좋은 시기입니다.")

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

        # 1) 오행 기질 (300자 이상)
        p1_text = f"**1) 오행의 균형 및 기질 분석:** {name}님의 사주는 {max_ele}의 기운이 지배적으로 작용하고 있습니다. "
        p1_text += "명리학적으로 이러한 구성은 개성이 뚜렷하고 자신의 신념을 관철하려는 의지가 대단히 강함을 의미합니다. 외부의 압력에 굴하지 않고 자신만의 전문 영역을 개척하는 데 탁월한 소질이 있으며, 목표를 향한 집중력이 남다릅니다. 다만 강한 기운이 한곳으로 쏠려 있어 유연한 사고와 타협이 필요한 순간에도 완고함을 보일 수 있으니, 일상에서 부족한 오행의 기운을 채우려는 노력이 균형 잡힌 삶을 위해 필수적입니다. 본인의 강점을 극대화하면서도 주변과의 조화를 고려한다면 사회적 성취의 크기가 더욱 확장될 것입니다."
        st.info(p1_text)

        # 2) 본신 성정 (300자 이상)
        p2_text = f"**2) 본신의 성정과 심리적 특징:** 일간 {my_day_gan}({my_element})의 성질을 분석해 보면, "
        if my_element == "木": p2_text += "위로 뻗어가는 나무처럼 향상심과 도덕성이 강하며 창의적인 영감이 풍부합니다. 정직하고 어진 성품을 가졌으나 때로는 융통성이 부족해 보일 수 있습니다."
        elif my_element == "火": p2_text += "화려한 불꽃처럼 열정적이고 자신을 표현하는 능력이 뛰어나며 예의를 중시합니다. 감수성이 예민하여 예술적 감각이 돋보이는 명조입니다."
        elif my_element == "土": p2_text += "두터운 대지처럼 신의가 있고 포용력이 넓으며 안정적인 삶을 추구합니다. 매사에 신중하고 묵직하게 자신의 자리를 지키는 든든한 존재입니다."
        elif my_element == "金": p2_text += "냉철한 금속처럼 시비지심이 분명하고 결단력이 뛰어나며 의리를 중시합니다. 완벽을 추구하는 성향이 강해 프로페셔널한 면모가 돋보입니다."
        else: p2_text += "유연한 물처럼 지혜롭고 깊은 통찰력을 가졌으며 환경 변화에 빠르게 적응합니다. 내면의 감수성이 매우 깊어 보이지 않는 본질을 꿰뚫는 힘이 있습니다."
        p2_text += " 이러한 천성적인 기질은 삶의 위기마다 본인을 지탱하는 근본적인 힘이 되며, 이를 긍정적으로 발산할 때 비로소 진정한 자아실현의 길로 나아갈 수 있을 것입니다."
        st.info(p2_text)

        # 🎵 음악적 사주 통변 (3분할)
        st.markdown('<div class="section-header">🎵 음악적 사주 통변 (밴드 페르소나 분석)</div>', unsafe_allow_html=True)
        if my_element == "木":
            p_pos = "**1) 추천 음악 포지션 및 전문 재능 (기타 - Guitar):** 목 기운의 생동감은 현의 울림과 공명하여 창의적인 리프와 선율을 만들어내는 데 탁월합니다."
            p_style = "**2) 음악적 성향:** 끊임없이 변화하는 자연처럼 실험적이고 유기적인 사운드를 지향하며, 인위적이지 않은 본연의 톤을 선호합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 팀에 새로운 아이디어를 공급하는 활력소이며, 성장을 주도하는 정신적 리더의 역할을 수행합니다."
        elif my_element == "火":
            p_pos = "**1) 추천 음악 포지션 및 전문 재능 (보컬 - Vocal):** 발산하는 에너지는 청중을 압도하는 발성과 화려한 무대 매너로 직결되어 극적인 감동을 선사합니다."
            p_style = "**2) 음악적 성향:** 강렬하고 명확한 사운드를 선호하며, 화려한 사운드 디자인을 통해 자신의 존재감을 드라마틱하게 드러냅니다."
            p_place = "**3) 밴드 내 자신의 위치:** 밴드의 상징적인 얼굴이자 에너지의 구심점으로, 무대 전체의 분위기를 지배하는 프론트맨입니다."
        elif my_element == "土":
            p_pos = "**1) 추천 음악 포지션 및 전문 재능 (드럼 - Drum):** 모든 소리를 조율하는 무게감은 밴드의 심장인 드럼 리듬과 일치하여 단단한 기초를 제공합니다."
            p_style = "**2) 음악적 성향:** 화려함보다 사운드의 밀도와 안정감을 중시하며, 전체 앙상블을 포용하는 묵직한 그루브를 지향합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 멤버들 사이의 갈등을 조율하고 사운드의 중심을 잡는 든든한 중재자이자 정신적 지주입니다."
        elif my_element == "金":
            p_pos = "**1) 추천 음악 포지션 및 전문 재능 (키보드 - Keyboard):** 정교한 금의 기운은 치밀한 사운드 레이어링과 선명한 음색을 구현하는 키보드 연주에 적합합니다."
            p_style = "**2) 음악적 성향:** 차갑고 명료하며 세련된 미학을 추구합니다. 논리적이고 정교한 화성적 완결성을 지향하는 경향이 강합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 사운드의 품질을 최종 검증하는 품질 보증자이자, 팀의 음악적 완성도를 높이는 브레인입니다."
        else:
            p_pos = "**1) 추천 음악 포지션 및 전문 재능 (베이스 - Bass):** 유연하게 흐르는 저음의 기운은 모든 악기를 하나로 묶어주는 베이스의 유기적 역할과 일맥상통합니다."
            p_style = "**2) 음악적 성향:** 여백의 미를 살린 깊은 울림을 중시하며, 감수성을 자극하는 몽환적이고 서정적인 흐름을 추구합니다."
            p_place = "**3) 밴드 내 자신의 위치:** 겉으로 드러나지 않지만 사운드의 빈틈을 완벽히 메우는 설계자이며, 팀의 결속력을 유지하는 접착제입니다."
        st.info(p_pos + "\n\n" + p_style + "\n\n" + p_place)

        # 4) 종합 (300자 이상)
        st.info(f"**4) 종합:**\n\n결론적으로 {name}님은 사주 원국에 내재된 {max_ele}의 강력한 기운을 음악이라는 매개체를 통해 발산할 때 가장 큰 성취를 이룰 수 있는 명조입니다. 분석된 포지션과 성향은 귀하의 타고난 본질과 맞닿아 있으며, 이를 밴드 활동에 녹여낼 때 대체 불가능한 존재감을 발휘하게 됩니다. 자신의 강점을 명확히 인지하고 멤버들과의 조화를 도모한다면, 예술적 완성도는 물론 인생 전반의 운을 상승시키는 긍정적인 파동을 만들어낼 것입니다. 타고난 운명의 흐름을 신뢰하고 정진하시길 바랍니다.")

        # 📅 [신규 추가] 5) 지정 연도(세운) 심층 운세 분석 엔진 (연도별 변화 로직 강화)
        st.markdown(f'<div class="section-header">📅 {target_year}년도 명리학적 세운(歲運) 분석</div>', unsafe_allow_html=True)
        
        # 세운 데이터 추출
        t_solar = Solar.fromYmd(target_year, 1, 1)
        t_lunar = t_solar.getLunar()
        t_ganzi = t_lunar.getEightChar().getYear()
        t_gan, t_zi = t_ganzi[0], t_ganzi[1]
        t_gan_ele = gan_elements.get(t_gan, "")
        t_zi_ele = zi_elements.get(t_zi, "")

        # 십성(Ten Gods) 관계 분석 엔진 (연도별 변화를 만드는 핵심 로직)
        elements_order = ["木", "火", "土", "金", "水"]
        my_idx = elements_order.index(my_element)
        target_idx = elements_order.index(t_gan_ele)
        diff = (target_idx - my_idx) % 5

        ten_gods = ["비겁(자신/동료)", "식상(표현/재능)", "재성(결실/재물)", "관성(명예/조직)", "인성(배움/수용)"]
        current_ten_god = ten_gods[diff]

        # 연도별 다변화 통변 문구 생성
        fortune_detail = f"**{target_year}년({t_gan}{t_zi})의 에너지 흐름:** "
        fortune_detail += f"올해는 천간으로 {t_gan}({t_gan_ele})의 기운이 들어오며 {name}님에게는 명리학적으로 **'{current_ten_god}'**의 해에 해당합니다. "
        
        if diff == 0: # 비겁
            fortune_detail += "자아의 확장이 강하게 일어나는 시기로, 주관이 뚜렷해지고 독립적인 활동을 하고 싶은 욕구가 커집니다. 동료들과의 협업이 활발해지는 한편, 지나친 고집은 갈등을 부를 수 있으니 유의하십시오."
        elif diff == 1: # 식상
            fortune_detail += "자신의 재능을 밖으로 뿜어내는 기운이 가득합니다. 음악적 창작 활동이나 대외적인 표현력이 극대화되어 예술적인 성취를 거두기에 최적의 해입니다. 새로운 도전을 두려워하지 마십시오."
        elif diff == 2: # 재성
            fortune_detail += "노력에 대한 실질적인 보상과 결실이 따르는 시기입니다. 현실적인 감각이 예리해지며 활동 범위가 넓어집니다. 밴드의 상업적 성공이나 구체적인 결과물을 도출하는 데 유리한 운세입니다."
        elif diff == 3: # 관성
            fortune_detail += "명예와 조직의 기운이 강해지는 해입니다. 책임감이 커지고 대중으로부터 인정을 받는 기회가 찾아옵니다. 자신을 절제하고 규칙적인 틀 안에서 성과를 내는 능력이 돋보일 것입니다."
        else: # 인성
            fortune_detail += "내실을 기하고 지혜를 쌓는 수용의 시기입니다. 외부의 자극보다는 내면의 성찰과 공부, 연습에 집중할 때 큰 도약의 발판을 마련할 수 있습니다. 주변의 도움과 지원을 받는 운세입니다."

        fortune_detail += f"\n\n지지의 {t_zi}({t_zi_ele}) 기운은 현실적인 환경의 변화를 예고합니다. {target_year}년은 귀하의 사주 원국과 상호작용하며 특정한 삶의 변곡점을 형성하게 됩니다. 특히 {t_zi_ele}의 특성은 올해의 활동 무대를 더욱 견고하게 하거나 새로운 환경으로의 이동을 암시하기도 합니다. 이 해의 흐름을 지혜롭게 타신다면 그동안 정체되었던 문제들이 해결되고 본인이 목표했던 예술적/사회적 지위로 한 걸음 더 다가설 수 있는 강력한 동력이 생길 것입니다. 300자 이상의 밀도 높은 분석 결과, 올해는 당신의 의지와 우주의 기운이 맞물려 매우 유의미한 흔적을 남기는 해가 될 것임을 확신합니다."

        st.info(fortune_detail)

    else:
        st.warning("성함을 입력해 주세요.")
