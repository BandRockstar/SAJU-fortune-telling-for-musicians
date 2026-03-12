import streamlit as st
from lunar_python import Solar

# 페이지 설정
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; }

.main-title { text-align: center; color: #1A202C; padding: 25px 0; border-bottom: 3px solid #E2E8F0; margin-bottom: 30px; }

.section-card, .music-card, .target-year-card {
padding: 2.2rem; border-radius: 1.5rem; margin-bottom: 2rem;
box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.section-card { background-color: #ffffff; border-left: 10px solid #4A5568; }
.music-card { background-color: #FDF2F8; border-left: 10px solid #D53F8C; }
.target-year-card { background-color: #F0F9FF; border-left: 10px solid #3182CE; }

.content-text { line-height: 2.2; font-size: 1.1rem; color: #2D3748; }

.saju-grid { display: flex; justify-content: space-around; margin-bottom: 2.5rem; gap: 12px; }

.saju-box {
flex: 1; text-align: center; padding: 20px 5px;
background: #F7FAFC; border-radius: 18px;
font-weight: bold; border: 2px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 천간지지 계산
# -----------------------------

def get_year_stem_branch(year):

    stems = ["갑","을","병","정","무","기","경","신","임","계"]
    branches = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

    stem = stems[(year - 4) % 10]
    branch = branches[(year - 4) % 12]

    return stem, branch


# -----------------------------
# 병화 기준 십신
# -----------------------------

def get_ten_god_for_bing(stem):

    mapping = {
        "갑":"편인",
        "을":"정인",
        "병":"비견",
        "정":"겁재",
        "무":"식신",
        "기":"상관",
        "경":"편재",
        "신":"정재",
        "임":"편관",
        "계":"정관"
    }

    return mapping.get(stem)


# -----------------------------
# 운세 리포트
# -----------------------------

def get_comprehensive_report(name, target_y):

    stem, branch = get_year_stem_branch(target_y)

    ten_god = get_ten_god_for_bing(stem)

    current_god = f"{stem}{branch}년 ({ten_god})"

    general_db = {

    "편재": f"{target_y}년은 활동 반경이 크게 넓어지고 예상치 못한 재물 기회가 찾아오는 해입니다. 사회적으로 본인의 능력이 높게 평가받으며 새로운 사업이나 프로젝트가 확장되는 흐름이 나타납니다. 다만 재물의 흐름이 커지는 만큼 지출 관리도 중요합니다.",

    "정재": f"{target_y}년은 안정적인 수입과 꾸준한 성과가 나타나는 해입니다. 성실함이 결실을 맺으며 장기적으로 기반을 다지기에 좋은 시기입니다. 무리한 확장보다는 현재 기반을 강화하는 전략이 좋습니다.",

    "편관": f"{target_y}년은 책임과 도전이 동시에 찾아오는 해입니다. 어려운 과업을 맡을 가능성이 있으며 이를 통해 사회적 위치가 상승할 수 있습니다. 스트레스 관리가 중요합니다.",

    "정관": f"{target_y}년은 명예와 안정의 흐름이 강한 해입니다. 사회적 평판이 좋아지고 공적인 자리에서 인정받는 일이 많아질 수 있습니다.",

    "편인": f"{target_y}년은 내면의 통찰과 창의적인 사고가 강해지는 해입니다. 독창적인 아이디어가 떠오르기 쉬우며 학문이나 연구, 예술적 탐구에 유리한 시기입니다.",

    "정인": f"{target_y}년은 도움과 후원이 따르는 해입니다. 주변의 지지와 협력 속에서 안정적인 발전이 이루어질 수 있습니다.",

    "비견": f"{target_y}년은 자립심과 주도성이 강해지는 해입니다. 스스로 길을 개척하려는 의지가 강해지며 새로운 프로젝트를 시작하기 좋습니다.",

    "겁재": f"{target_y}년은 경쟁이 강해지는 해입니다. 주변의 자극을 통해 성장하는 시기이며 과감한 도전이 필요한 시기입니다.",

    "식신": f"{target_y}년은 창작과 표현이 활발해지는 시기입니다. 아이디어가 실제 결과물로 이어지기 쉽습니다.",

    "상관": f"{target_y}년은 기존 틀을 깨는 창의적 변화가 나타나는 해입니다. 예술적 재능이 돋보일 수 있습니다."
    }


    music_db = {

    "편재": f"{target_y}년 음악적으로는 시장 확장과 공연 기회가 늘어날 가능성이 있습니다. 상업적인 프로젝트와 협업이 늘어날 수 있습니다.",

    "정재": f"{target_y}년은 음악 작업의 완성도를 높이기에 좋은 시기입니다. 사운드 디테일과 안정적인 활동이 중요합니다.",

    "편관": f"{target_y}년은 강한 무대 에너지와 카리스마가 돋보이는 시기입니다.",

    "정관": f"{target_y}년은 음악적 명예와 공식 활동이 늘어날 가능성이 있습니다.",

    "편인": f"{target_y}년은 실험적인 음악과 새로운 사운드 탐구가 좋은 결과로 이어질 수 있습니다.",

    "정인": f"{target_y}년은 감성적인 음악과 서정적인 작품이 좋은 반응을 얻을 수 있습니다.",

    "비견": f"{target_y}년은 본인만의 시그니처 사운드를 확립하기 좋은 시기입니다.",

    "겁재": f"{target_y}년은 강렬한 라이브 퍼포먼스가 돋보이는 시기입니다.",

    "식신": f"{target_y}년은 창작의 풍요가 나타나는 시기입니다. 곡 작업이 잘 풀릴 수 있습니다.",

    "상관": f"{target_y}년은 화려한 표현과 실험적인 음악이 주목받을 가능성이 있습니다."
    }

    gen_rep = general_db.get(ten_god)
    mus_rep = music_db.get(ten_god)

    return current_god, gen_rep, mus_rep


# -----------------------------
# UI
# -----------------------------

st.markdown("<div class='main-title'><h1>🎸 음악인을 위한 사주통변 Ver 1.0</h1></div>", unsafe_allow_html=True)

with st.expander("📝 사주 정보 및 분석 설정", expanded=True):

    with st.form("saju_form"):

        u_name = st.text_input("성함", value="임환백")

        c1,c2,c3 = st.columns(3)

        with c1:
            b_y = st.number_input("출생년",1900,2100,1981)

        with c2:
            b_m = st.number_input("출생월",1,12,2)

        with c3:
            b_d = st.number_input("출생일",1,31,7)

        target_y = st.number_input("조회 연도",1900,2100,2026)

        submitted = st.form_submit_button("🎭 심층 리포트 생성", use_container_width=True)


# -----------------------------
# 결과
# -----------------------------

if submitted:

    god, gen_rep, mus_rep = get_comprehensive_report(u_name,target_y)

    st.markdown(f"### 🍀 {u_name} 아티스트님 심층 리포트")

    st.markdown("""
    <div class='saju-grid'>
    <div class='saju-box'>신유(辛酉)<br>년주</div>
    <div class='saju-box'>경인(庚寅)<br>월주</div>
    <div class='saju-box'>병진(丙辰)<br>일주</div>
    <div class='saju-box'>신묘(辛卯)<br>시주</div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown(f"""
    <div class='section-card'>
    <h2>👤 타고난 성정</h2>
    <div class='content-text'>
    {u_name}님은 병화(丙火) 일간으로 태양과 같은 에너지를 가진 사주입니다.
    예술적 표현력과 리더십이 동시에 나타나는 특징이 있습니다.
    </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown(f"""
    <div class='music-card'>
    <h2>🎸 음악적 사주</h2>
    <div class='content-text'>
    금(金)의 기운이 사운드 디테일을 잡고 병화의 에너지가 무대 발산력을 강화합니다.
    </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown(f"### 📅 {target_y}년 운세")

    st.markdown(f"""
    <div class='target-year-card'>
    <h2>일반 운세</h2>
    <div class='content-text'><b>{god}</b><br>{gen_rep}</div>
    </div>

    <div class='music-card'>
    <h2>음악 운세</h2>
    <div class='content-text'>{mus_rep}</div>
    </div>
    """, unsafe_allow_html=True)
