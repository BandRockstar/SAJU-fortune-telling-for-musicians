import streamlit as st
from lunar_python import Solar, Lunar

# 1️⃣ 페이지 설정 및 UI 디자인
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main-title { text-align: center; color: #1A202C; padding: 25px 0; border-bottom: 3px solid #E2E8F0; margin-bottom: 30px; }
    .section-card, .music-card, .position-card, .target-year-card { 
        padding: 2.2rem; border-radius: 1.5rem; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.05); 
    }
    .section-card { background-color: #ffffff; border-left: 10px solid #4A5568; }
    .music-card { background-color: #FDF2F8; border-left: 10px solid #D53F8C; }
    .position-card { background-color: #FFFBEB; border-left: 10px solid #D97706; }
    .target-year-card { background-color: #F0F9FF; border-left: 10px solid #3182CE; }
    .content-text { line-height: 2.4; font-size: 1.1rem; color: #2D3748; text-align: justify; word-break: keep-all; }
    .saju-grid { display: flex; justify-content: space-around; margin-bottom: 2.5rem; gap: 12px; }
    .saju-box { flex: 1; text-align: center; padding: 20px 5px; background: #F7FAFC; border-radius: 18px; font-weight: bold; border: 2px solid #E2E8F0; }
    .highlight { color: #D53F8C; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2️⃣ 연도별 심층 통변 엔진 (10개 세운 완벽 매핑)
def get_comprehensive_report(name, target_y):
    # 일간 병화(丙) 기준 10개 천간 순환 로직
    # 0:경(편재), 1:신(정재), 2:임(편관), 3:계(정관), 4:갑(편인), 5:을(정인), 6:병(비견), 7:정(겁재), 8:무(식신), 9:기(상관)
    ten_gods_list = ["경(편재)", "신(정재)", "임(편관)", "계(정관)", "갑(편인)", "을(정인)", "병(비견)", "정(겁재)", "무(식신)", "기(상관)"]
    god_idx = target_y % 10
    current_god = ten_gods_list[god_idx]
    
    # [일반 운세 DB]
    general_db = {
        "경(편재)": f"{target_y}년은 활동 반경이 크게 넓어지고 예상치 못한 재물적 기회가 찾아오는 '편재'의 해입니다. 사회적으로 본인의 역량이 높게 평가받으며, 새로운 프로젝트나 비즈니스를 확장하기에 매우 유리한 시기입니다. 다만 지출 관리와 실리적인 선택에 집중해야 성취를 온전히 본인의 것으로 만들 수 있습니다. 올해의 에너지는 매우 역동적이니 적극적으로 움직이십시오.",
        "신(정재)": f"{target_y}년은 성실함이 결실을 맺는 '정재'의 해입니다. 안정적인 수입과 신뢰를 바탕으로 한 계약운이 매우 좋으며, 가정과 일의 균형이 완벽하게 이루어지는 시기입니다. 꼼꼼한 자기 관리를 통해 장기적인 토대를 마련하는 데 집중하십시오. 무리한 확장보다는 내실을 기할 때 우주의 기운이 본인을 돕는 해가 될 것입니다.",
        "임(편관)": f"{target_y}년은 강력한 명예와 책임감이 따르는 '편관'의 해입니다. 어려운 과업을 완수하며 본인의 권위를 세우게 되며, 조직이나 단체에서 중심적인 역할을 수행하게 됩니다. 스트레스 관리에 유의한다면 커리어에서 가장 빛나는 성취를 이룰 수 있는 해입니다. 본인을 담금질하는 과정이 향후 큰 그릇을 만드는 밑거름이 될 것입니다.",
        "계(정관)": f"{target_y}년은 사회적 인정과 안정이 뒤따르는 '정관'의 해입니다. 합리적인 판단과 규범적인 태도로 인해 주변의 깊은 신뢰를 얻게 되며, 공식적인 승진이나 자격 취득 등 문서상의 경사가 예상됩니다. 순리에 맞는 흐름이 본인을 돕는 해이므로, 원칙을 지키며 활동한다면 명예로운 결과를 얻게 될 것입니다.",
        "갑(편인)": f"{target_y}년은 깊은 성찰과 독창적인 직관이 발휘되는 '편인'의 해입니다. 본인만의 전문 기술이나 지식을 심화시키기에 최적이며, 남들이 생각지 못한 창의적인 해법으로 난관을 극복하게 됩니다. 내면의 에너지를 축적하는 시간을 가지는 것이 좋으며, 독특한 아이디어가 예상치 못한 성과를 가져다주는 한 해가 될 것입니다.",
        "을(정인)": f"{target_y}년은 윗사람의 도움과 학문적 성취가 따르는 '정인'의 해입니다. 안정적인 문서운과 후원운이 강하게 작용하여, 무리하지 않아도 본인의 자리가 보존되고 명예가 드높아집니다. 마음의 평온을 찾고 지혜를 나누는 해가 될 것이며, 그동안의 노고를 인정받아 편안한 보상을 받는 시기입니다.",
        "병(비견)": f"{target_y}년은 주체성과 독립심이 극대화되는 '비견'의 해입니다. 외부의 압력에 굴하지 않고 본인만의 소신을 바탕으로 새로운 프로젝트를 추진하기에 최적의 시기입니다. 대인관계에서는 동료들과 대등한 위치에서 리더십을 발휘하며 사회적 영역을 넓히게 될 것입니다. 본인만의 영역을 확고히 굳히는 매우 역동적인 시기입니다.",
        "정(겁재)": f"{target_y}년은 강력한 경쟁심과 돌파력이 요구되는 '겁재'의 해입니다. 주변의 자극이 오히려 성장의 발판이 되며, 난관을 극복하며 본인의 존재감을 확실히 각인시키게 됩니다. 강력한 추진력으로 인생의 새로운 변곡점을 만들어낼 것이며, 이를 통해 한 단계 더 높은 사회적 위치로 도약하게 될 것입니다.",
        "무(식신)": f"{target_y}년은 창의적인 즐거움과 표현의 확장이 일어나는 '식신'의 해입니다. 그동안 구상만 하던 아이디어들을 현실로 끄집어내어 결과물을 만들기에 가장 적합한 시기입니다. 주변 사람들에게 본인의 재능을 아낌없이 보여주며 신뢰와 명성을 동시에 쌓게 될 것이며, 성실한 노력의 대가가 실질적인 이득으로 돌아오는 결실의 해입니다.",
        "기(상관)": f"{target_y}년은 화려한 재능 표출과 변화를 추구하는 '상관'의 해입니다. 기존의 틀을 깨는 혁신적인 시도로 대중의 이목을 집중시키게 되며, 화술과 예술적 감각이 최고조에 달합니다. 본인의 에너지를 예술적으로 승화시키기에 더없이 좋은 해이며, 새로운 분야에 대한 도전이 큰 즐거움으로 다가올 것입니다."
    }
    
    # [음악 사주 DB]
    music_db = {
        "경(편재)": f"음악적으로 {target_y}년은 대규모 공연이나 대중적인 성공 가능성이 높은 해입니다. 사운드의 규모감을 키우고 과감한 편곡을 시도해 보십시오. 본인의 음악이 더 넓은 시장으로 전달되는 강력한 확장 운을 가지고 있습니다.",
        "신(정재)": f"아티스트로서 {target_y}년은 소리의 완성도와 디테일에 집중하는 시기입니다. 정교한 믹싱과 정돈된 사운드가 대중에게 신뢰감을 줍니다. 본인만의 견고한 사운드 포트폴리오가 완성되는 시기입니다.",
        "임(편관)": f"음악적으로 {target_y}년은 무대 위에서의 압도적인 카리스마가 돋보이는 해입니다. 거칠고 강력한 사운드나 웅장한 연출이 효과적입니다. 예술적 완성도를 위해 본인을 담금질하는 과정이 명작을 탄생시킬 것입니다.",
        "계(정관)": f"아티스트로서 {target_y}년은 정석적인 미학과 세련된 음악성이 조화를 이루는 해입니다. 대중적인 공감을 얻기 쉬운 멜로디와 깔끔한 사운드 디자인이 강점입니다. 공식적인 명예 제안이 따를 수 있습니다.",
        "갑(편인)": f"음악적으로 {target_y}년은 독창적인 실험이 빛을 발하는 시기입니다. 본인만의 독특한 질감을 발견하여 음악적 지평을 넓히게 됩니다. 매니아층의 강력한 지지를 받는 앨범이 나올 수 있는 해입니다.",
        "을(정인)": f"아티스트로서 {target_y}년은 음악적 영감이 부드럽게 흐르는 시기입니다. 클래식하거나 서정적인 감수성이 돋보이며, 본인의 음악적 뿌리를 되새기는 작업을 통해 대중과 깊은 정서적 교감을 나누게 됩니다.",
        "병(비견)": f"음악적으로 {target_y}년은 독보적인 '시그니처 사운드'를 확립하는 해입니다. 밴드 내에서 본인이 추구하는 음악적 방향성을 관철시키기에 최적이며, 유행에 흔들리지 않는 철학이 담긴 작업물을 완성하게 됩니다.",
        "정(겁재)": f"아티스트로서 {target_y}년은 파격적인 에너지와 역동적인 연주가 빛을 발하는 해입니다. 라이브 퍼포먼스에서 폭발적인 반응을 이끌어내기에 매우 유리하며, 경쟁적인 음악 씬에서 독보적인 존재감을 드러냅니다.",
        "무(식신)": f"음악적으로 {target_y}년은 창작의 풍요로움을 만끽하는 해입니다. 자연스럽게 터져 나오는 영감을 통해 다작이 가능하며, 소리의 질감이 매우 풍성하고 따뜻해지는 시기입니다. 작업 자체가 큰 치유가 됩니다.",
        "기(상관)": f"아티스트로서 {target_y}년은 화려한 테크닉과 쇼맨십이 돋보이는 시기입니다. 대중을 매료시키는 감각적인 사운드와 세련된 연출이 결합되어 본인의 매력을 극대화하는 최고의 한 해가 될 것입니다."
    }

    return current_god, general_db.get(current_god), music_db.get(current_god)

# 3️⃣ 메인 UI 및 입력창
st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):
    with st.form("saju_form"):
        u_name = st.text_input("성함", value="임환백")
        c1, c2, c3 = st.columns(3)
        with c1: b_y = st.number_input("출생년", 1900, 2100, 1981)
        with c2: b_m = st.number_input("출생월", 1, 12, 2)
        with c3: b_d = st.number_input("출생일", 1, 31, 7)
        
        col_t, col_c = st.columns(2)
        with col_t: u_time = st.selectbox("출생 시간", ["05:30~07:30 묘시", "07:30~09:30 진시", "09:30~11:30 사시", "모름"])
        with col_c: cal_type = st.radio("달력 선택", ["양력", "음력", "음력(윤달)"], horizontal=True)
            
        target_y = st.number_input("조회 연도 (운세를 보고 싶은 해)", 1900, 2100, 2026)
        submitted = st.form_submit_button("🎭 심층 이원 통변 리포트 생성", use_container_width=True)

# 4️⃣ 결과 도출
if submitted:
    god, gen_rep, mus_rep = get_comprehensive_report(u_name, target_y)
    
    st.markdown(f"### 🍀 {u_name} 아티스트님 심층 리포트")
    
    
    st.markdown("""
        <div class='saju-grid'>
            <div class='saju-box'>신유(辛酉)<br>년주</div><div class='saju-box'>경인(庚寅)<br>월주</div>
            <div class='saju-box'>병진(丙辰)<br>일주</div><div class='saju-box'>신묘(辛卯)<br>시주</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='section-card'><h2>👤 타고난 성정과 일반 통변</h2><div class='content-text'>{u_name}님은 병화(丙火) 일간으로 태양과 같은 열정을 타고났습니다. 명확한 판단력과 예술적 감수성을 동시에 지닌 귀한 명식입니다.</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-card'><h2>🎸 타고난 음악적 사주 통변</h2><div class='content-text'>정밀한 금(金)의 기운이 사운드의 디테일을 잡고, 병화의 에너지가 무대 위 발산력을 책임집니다. 하이엔드 사운드를 지향하는 아티스트적 자질이 충분합니다.</div></div>", unsafe_allow_html=True)

    st.markdown(f"### 📅 {target_y}년 심층 운세 분석")
    st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ 일반 운세 흐름</h2>
            <div class='content-text'><b>[{god}의 운]</b><br>{gen_rep}</div>
        </div>
        <div class='music-card' style='background-color:#FFF5F7;'>
            <h2>🎹 음악적 흐름 이야기</h2>
            <div class='content-text'>{mus_rep}</div>
        </div>
    """, unsafe_allow_html=True)
