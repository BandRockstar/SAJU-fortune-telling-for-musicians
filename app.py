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
        # 데이터 계산부 시작
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

        # 결과 화면 출력
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

        # 삼재 분석
        st.divider()
        my_year_zi = eight_char.getYear()[1]
        samjae_groups = {
            "申": ["寅", "卯", "辰"], "子": ["寅", "卯", "辰"], "辰": ["寅", "卯", "辰"],
            "寅": ["申", "酉", "戌"], "午": ["申", "酉", "戌"], "戌": ["申", "酉", "戌"],
            "巳": ["亥", "자", "丑"], "酉": ["亥", "子", "丑"], "丑": ["亥", "子", "丑"],
            "亥": ["巳", "午", "未"]
        }
        my_samjae_zis = samjae_groups.get(my_year_zi, [])
        target_solar = Solar.fromYmd(target_year, 1, 1)
        target_year_zi = target_solar.getLunar().getEightChar().getYear()[1]
        
        if target_year_zi in my_samjae_zis:
            samjae_idx = my_samjae_zis.index(target_year_zi)
            current_status = ["들삼재", "눌삼재", "날삼재"][samjae_idx]
            st.error(f"🚫 **삼재: {target_year}년은 귀하의 삼재 기간({current_status})입니다.**\n\n삼재는 9년 주기로 돌아와 3년 동안 머무는 에너지의 정체기를 의미합니다. 현재 귀하는 기운이 내면으로 응축되고 외부의 변화에 민감하게 반응하는 시기에 놓여 있습니다.")
        else:
            st.success(f"✅ **삼재: {target_year}년은 삼재에 해당하지 않습니다.**\n\n축하드립니다. 현재 귀하는 삼재의 영향권에서 완전히 벗어나 기운이 비교적 맑고 순탄하게 흐르는 운세의 흐름 속에 있습니다.")

        # 심층 통변 리포트 섹션 시작
        st.divider()
        st.subheader(f"📜 {name}님 심층 통변 리포트")
        gan_elements = {"甲":"木", "乙":"木", "丙":"火", "丁":"火", "戊":"土", "己":"土", "庚":"金", "辛":"金", "壬":"水", "癸":"水"}
        zi_elements = {"寅":"木", "卯":"木", "巳":"火", "午":"火", "申":"金", "酉":"金", "亥":"水", "자":"水", "辰":"土", "戌":"土", "丑":"土", "未":"土", "子":"水"}
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

        # 1) 오행 기질
        p1_text = f"**1) 오행의 균형 및 기질 분석:** {name}님의 사주 구성을 심층 분석한 결과, 전체 8글자 중 {max_ele}의 기운이 {counts[max_ele]}개로 강력하게 작용하고 있습니다. "
        if counts[max_ele] >= 3:
            p1_text += "명리학적으로 특정 오행이 이토록 강성한 명조는 기질이 매우 선명하고 주관이 뚜렷하여 자신만의 독자적인 영역을 구축하는 데 탁월한 능력을 보입니다."
        else:
            p1_text += "오행의 분포가 어느 한쪽으로 치우치지 않고 비교적 고르게 분포되어 있어 성품이 원만하고 매사에 균형 감각이 대단히 뛰어난 명조입니다."
        st.info(p1_text)

        # 2) 본신 성정
        p2_text = f"**2) 본신의 성정과 심리적 특징:** 본신(自身)을 상징하는 일간 {my_day_gan}은 오행상 {my_element}의 근본적인 성질을 내포하고 있습니다. "
        # (생략: 기존 일간별 성정 텍스트 유지)
        st.info(p2_text)

        # 음악적 사주 통변
        st.markdown('<div class="section-header">🎵 음악적 사주 통변 (밴드 페르소나 분석)</div>', unsafe_allow_html=True)
        # (생략: 기존 음악 포지션 분석 텍스트 유지)

        # 📅 [개편된] 세운 분석 엔진 통합 지점
        st.markdown(f'<div class="section-header">📅 {target_year}년도 명리학적 세운(歲運) 분석</div>', unsafe_allow_html=True)
        
        t_solar = Solar.fromYmd(target_year, 1, 1)
        t_lunar = t_solar.getLunar()
        t_ganzi_year = t_lunar.getEightChar().getYear()
        tg, tz = t_ganzi_year[0], t_ganzi_year[1]
        
        ele_order = ["木", "火", "土", "金", "水"]
        tg_element = gan_elements.get(tg, "木")
        diff = (ele_order.index(tg_element) - ele_order.index(my_element)) % 5
        
        ten_god_db = {
            0: f"올해 {tg}({tg_element})년은 '비겁(比劫)'의 해입니다. 본인만의 독보적인 톤을 확립하고 주도적으로 프로젝트를 이끌기에 최적입니다.",
            1: f"올해 {tg}({tg_element})년은 '식상(食傷)'의 해입니다. 창의력이 폭발하고 표현력이 빛을 발합니다. 즉흥 연주와 작곡에서 큰 호응을 얻을 것입니다.",
            2: f"올해 {tg}({tg_element})년은 '재성(財星)'의 해입니다. 실질적인 보상이 따르며 철저한 기획에 기반한 활동이 큰 성취를 가져옵니다.",
            3: f"올해 {tg}({tg_element})년은 '관성(官星)'의 해입니다. 명예와 사회적 질서를 상징하며, 공신력 있는 무대의 제안이 예상됩니다.",
            4: f"올해 {tg}({tg_element})년은 '인성(印星)'의 해입니다. 내실을 다지고 전문 지식을 습득하기 좋으며 귀인의 도움을 얻는 운세입니다."
        }

        zi_action_db = {
            "子": "자수(子水)는 깊은 심해의 소리처럼 오묘한 감성을 깨웁니다. 저음역대 작업이 길합니다.",
            "丑": "축토(丑土)는 묵묵한 연습의 시간입니다. 정교한 수정 작업이 향후 결실의 밑바탕이 됩니다.",
            "寅": "인목(寅木)은 새로운 시작의 기운입니다. 공격적인 확장과 생동감 넘치는 사운드가 주효합니다.",
            "卯": "묘목(卯木)은 예민한 감각이 돋보입니다. 어쿠스틱한 질감을 살리는 작업이 유리합니다.",
            "辰": "진토(辰토)는 변화무쌍한 에너지가 흐릅니다. 기존 스타일을 탈피한 실험적 시도를 해보십시오.",
            "巳": "사화(巳火)는 자신을 화려하게 드러내는 시기입니다. 퍼포먼스와 조명을 적극 활용하십시오.",
            "午": "오화(午火)는 폭발적인 열정이 가득합니다. 강렬한 비트와 연주가 행운을 부릅니다.",
            "未": "미토(未土)는 열기를 조율하는 시간입니다. 앙상블의 조화와 미니멀리즘이 효과적입니다.",
            "申": "신금(申金)은 날카로운 감각이 살아납니다. 정교한 믹싱이나 장비 업그레이드에 적기입니다.",
            "酉": "유금(酉金)은 청명한 기운이 돕습니다. 보컬이나 메인 악기의 맑은 톤을 살려 녹음해 보십시오.",
            "戌": "술토(戌土)는 성과를 지키는 시기입니다. 오랜 팬과의 유대나 클래식한 재해석이 길합니다.",
            "亥": "해수(亥水)는 화합의 시간입니다. 협업 프로젝트에서 중심적인 역할을 수행하게 됩니다."
        }

        summary_db = {
            0: f"올해는 당신의 '자아'가 투영된 해입니다. 주변에 흔들리지 말고 가장 {name}님다운 소리를 세상에 각인시키는 데 집중하십시오.",
            1: f"발산의 에너지가 최고조에 달하는 해입니다. 머릿속의 악상을 미루지 말고 즉시 기록하고 연주하십시오.",
            2: f"결과를 수확하는 시기입니다. 예술적 완성도만큼이나 현실적인 성과를 어떻게 관리할지에 대한 전략이 필요합니다.",
            3: f"사회적 위치와 책임이 강조되는 해입니다. 개인의 만족을 넘어 당신의 음악이 조직 내에서 갖는 가치를 고민하십시오.",
            4: f"깊이를 더하는 해입니다. 화려한 무대 뒤에서 내실을 다지고 축적한 에너지는 향후 가장 큰 자산이 됩니다."
        }

        ten_god_names = ["비겁", "식상", "재성", "관성", "인성"]
        ten_god = ten_god_names[diff]
        main_text = ten_god_db.get(diff, "운세를 분석 중입니다.")
        footer_text = zi_action_db.get(tz, "지지의 기운이 당신의 활동을 지원합니다.")
        final_summary = summary_db.get(diff, "하늘의 기운을 믿고 당신의 리듬에 맞춰 나아가십시오.")

        combined_report = f"""
**[{tg}{tz}년 연간 운세 핵심 요약]**
올해는 천간의 '{ten_god}' 기운과 지지의 '{tz}({zi_ko.get(tz)})' 기운이 결합하여 {name}님의 예술적 연대기에 새로운 장을 엽니다. 

**1. 환경과 심리 흐름:** {main_text}

**2. 구체적 음악 가이드:** {footer_text} 

**3. 종합 제언:** {name}님, {target_year}년은 당신의 사주 원국과 세운이 만나 거대한 파동을 만드는 시기입니다. **{final_summary}** 당신이 내딛는 한 걸음이 명리학적 흐름과 일치할 때 가장 큰 공명을 일으킬 것입니다. {tz}년의 기운을 당신의 악기에 담아 후회 없는 연주를 이어가시길 바랍니다.
"""
        st.info(combined_report)

    else:
        st.warning("성함을 입력해 주세요.")
