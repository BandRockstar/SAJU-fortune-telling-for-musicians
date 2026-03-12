import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(page_title="사주 분석 서비스", page_icon="☯️")

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

    target_year = st.number_input("운세를 보고 싶은 연도", min_value=2024, max_value=2100, value=2026)
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

# 3. 분석 버튼 및 결과 출력
if st.button("🎭 심층 이원 통변 리포트 생성"):
    if name:
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_text = f"양력 {year}년 {month}월 {day}일"
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
            selected_zi = birth_time.split("(")[1][0] 
            hour_map = {"子":0, "丑":2, "寅":4, "卯":6, "辰":8, "巳":10, "午":12, "未":14, "申":16, "酉":18, "戌":20, "亥":22}
            target_hour = hour_map.get(selected_zi, 0)
            
            if calendar_type == "양력":
                precise_solar = Solar.fromYmdHms(year, month, day, target_hour, 0, 0)
                precise_eight_char = precise_solar.getLunar().getEightChar()
            else:
                precise_lunar = Lunar.fromYmdHms(year, month, day, target_hour, 0, 0)
                precise_eight_char = precise_lunar.getEightChar()
            
            t_gan, t_zi = format_ganzi(precise_eight_char.getTime())

        # 2층: 사주 원국 출력 (고정)
        st.divider()
        st.subheader(f"📊 {name}님의 사주 원국 (8글자)")

        col_t, col_d, col_m, col_y = st.columns(4)
        with col_y:
            st.markdown("### 년주")
            st.info(f"{y_gan}\n\n{y_zi}")
        with col_m:
            st.markdown("### 월주")
            st.info(f"{m_gan}\n\n{m_zi}")
        with col_d:
            st.markdown("### 일주")
            st.info(f"{d_gan}\n\n{d_zi}")
        with col_t:
            st.markdown("### 시주")
            st.info(f"{t_gan}\n\n{t_zi}")

        st.write(f"**입력 정보:** {display_text} | {gender} | {birth_time}")
        st.write(f"**분석 연도:** {target_year}년")

        # 3층: 삼재 분석 (고정)
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
        desc_text = "\n\n삼재는 9년마다 돌아오는 3년의 조심하는 시기를 뜻합니다."

        if target_year_zi in my_samjae_zis:
            samjae_idx = my_samjae_zis.index(target_year_zi)
            samjae_types = ["들삼재", "눌삼재", "날삼재"]
            current_status = samjae_types[samjae_idx]
            st.error(f"🚫 **삼재(三災) 정보: {target_year}년은 귀하의 삼재 기간({current_status})에 해당합니다.**{desc_text}")
        else:
            st.success(f"🚫 **삼재(三災) 정보: {target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.**{desc_text}")

        # --- [4층: 정통 명리 심층 통변] 음악적 내용 배제 ---
        st.divider()
        st.subheader(f"📜 {name}님 사주 원국 정밀 분석 리포트")

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
            res_list = [f"{k}({v})" for k, v in counts.items() if v > 0]
            st.code(" | ".join(res_list))
        with col_res2:
            st.write("**[일간 속성]**")
            st.code(f"{my_day_gan} ({my_element}의 기운)")

        max_ele = max(counts, key=counts.get)
        part1 = f"{name}님의 사주 구성을 분석한 결과, 현재 {max_ele}의 기운이 {counts[max_ele]}개로 가장 강성한 세력을 형성하고 있습니다. "
        if counts[max_ele] >= 3:
            part1 += f"이처럼 특정 오행이 태과(太過)하거나 편중된 경우, 삶의 지향점이 대단히 뚜렷하고 자기 주관이 확고한 성정으로 나타납니다. 외부의 간섭보다는 스스로의 신념을 관철하려는 의지가 강한 명조입니다. "
        else:
            part1 += "오행의 분포가 비교적 중화(中和)를 이루고 있어, 매사에 원만하고 유연하게 대처하는 성품을 가졌습니다. 편향되지 않은 시각으로 환경에 적응하는 능력이 돋보입니다. "

        part2 = f"본신인 일간 {my_day_gan}은 {my_element}의 성질을 지니고 있습니다. "
        if my_element == "木": part2 += "마치 나무가 뻗어 나가듯 인(仁)을 중시하며, 창의적인 기획력과 진취적인 추진력이 뛰어난 성정입니다. "
        elif my_element == "火": part2 += "예(禮)를 중시하고 열정적이며, 자신을 외부로 드러내어 빛을 발산하는 표현력과 명랑한 기질이 강력합니다. "
        elif my_element == "土": part2 += "신(信)을 바탕으로 두텁고 묵직한 안정감을 주며, 매사에 신중하고 한 번 정한 원칙을 변함없이 지켜나가는 중용의 덕이 있습니다. "
        elif my_element == "金": part2 += "의(義)를 중시하며 결단력이 날카롭고 냉철합니다. 시비지심이 분명하여 일 처리가 깔끔하고 완벽을 기하는 성격입니다. "
        else: part2 += "지(智)를 중시하며 유연하고 깊은 감수성을 지녔습니다. 흐르는 물처럼 지혜롭고 영감이 뛰어나며 내면의 깊이가 깊은 명조입니다. "

        part3 = f"사회적 환경과 격국을 결정짓는 월지의 {m_zi[0]}와 일간의 관계를 볼 때, {name}님은 "
        if m_zi[0] in zi_elements and zi_elements[m_zi[0]] == my_element:
            part3 += "자아의 세력이 강하여 독립적인 주체성이 강조되는 구조입니다. 타인과의 협력 속에서도 본인의 주도권을 유지할 때 가장 효율적인 성과를 냅니다. "
        else:
            part3 += "본인의 역량을 외부의 목적이나 가치를 위해 치환하는 능력이 발달하였습니다. 주어진 환경을 분석하고 이를 실질적인 결과물로 도출해내는 현실적인 감각이 뛰어납니다. "

        part3 += f"입력하신 {target_year}년의 운 흐름은 이러한 원국의 잠재력이 세운의 기운과 상호작용하여 새로운 변화의 기틀을 마련하는 해가 될 것입니다."

        st.info(part1 + "\n\n" + part2 + "\n\n" + part3)
        # ---------------------------------------------------

    else:
        st.warning("성함을 입력해 주세요.")
