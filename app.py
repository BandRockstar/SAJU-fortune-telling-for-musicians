import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(page_title="정통 사주 명리 분석", page_icon="☯️")

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

        # 3층: 삼재 분석 (고정 및 아이콘 오타 수정)
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
            # [수정] 삼재가 아닐 때의 아이콘을 ✅로 변경
            st.success(f"✅ **삼재(三災) 정보: {target_year}년은 귀하의 삼재 기간에 해당하지 않습니다.**{desc_text}")

        # --- [4층: 정통 명리 심층 통변] ---
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
            res_list = [f"{k}({counts[k]})" for k in ["木", "火", "土", "金", "水"]]
            st.code(" | ".join(res_list))
        with col_res2:
            st.write("**[일간 속성]**")
            st.code(f"{my_day_gan} ({my_element}의 기운)")

        max_ele = max(counts, key=counts.get)
        part1 = f"{name}님의 사주 구성을 분석한 결과, 현재 {max_ele}의 기운이 {counts[max_ele]}개로 가장 강성한 세력을 형성하고 있습니다. "
        if counts[max_ele] >= 3:
            part1 += f"명리학적으로 특정 오행이 태과(太過)한 명조는 기질이 선명하고 주관이 뚜렷하여 자기 세계가 확고함을 의미합니다. 외부의 환경 변화에 휩쓸리기보다 자신의 신념과 원칙을 관철해 나가는 강인한 성정을 지녔습니다. "
        else:
            part1 += "오행의 분포가 전반적으로 중화(中和)를 이루고 있어 성품이 원만하고 매사에 균형 감각이 뛰어납니다. 편중되지 않은 시각으로 사물을 바라보며 주변 환경과 조화롭게 융화되는 유연한 기질을 갖추고 있습니다. "

        part2 = f"본신인 일간 {my_day_gan}은 {my_element}의 성질을 지니고 있습니다. "
        if my_element == "木": part2 += "오상 중 인(仁)을 상징하며, 나무가 위로 뻗어 나가는 성질처럼 창의적인 기획력과 어질고 진취적인 마음을 품고 있습니다. "
        elif my_element == "火": part2 += "오상 중 예(禮)를 상징하며, 불꽃이 주변을 밝히듯 열정적이고 자신을 드러내어 소통하려는 표현력이 강력한 기질입니다. "
        elif my_element == "土": part2 += "오상 중 신(信)을 상징하며, 대지가 만물을 품듯 묵직하고 신의가 두터우며 매
