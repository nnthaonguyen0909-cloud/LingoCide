import streamlit as st
import random
import pandas as pd

# ================= CONFIGURATION =================
st.set_page_config(
    page_title="LingoCine - Smart Learning",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SESSION STATE =================
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
# Skill score table
if 'skills' not in st.session_state:
    st.session_state.skills = {
        "Listening": 10,   # Assumption starting point
        "Vocabulary": 10,
        "Grammar": 10
    }
if 'vocab_list' not in st.session_state:
    st.session_state.vocab_list = [
        {"word": "Resilient", "meaning": "Kiên cường", "example": "She is resilient.", "video_id": "frozen"},
        {"word": "Inevitability", "meaning": "Điều không thể tránh khỏi", "example": "Dread it. Run from it. Destiny arrives all the same.", "video_id": "thanos"},
        {"word": "Adventure", "meaning": "Cuộc phiêu lưu", "example": "Adventure is out there!", "video_id": "up"},
        {"word": "Sacrifice", "meaning": "Sự hy sinh", "example": "The hardest choices require the strongest wills.", "video_id": "thanos"},
    ]

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .big-font { font-size:30px !important; font-weight: bold; color: #FF4B4B; }
    .highlight { background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    .stButton>button { width: 100%; border-radius: 20px; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
# ================= THANH BÊN (SIDEBAR) =================
with st.sidebar:
    # Nếu chưa có tên thì hiện ô nhập tên
    if st.session_state.user_name == "":
        st.markdown("### Welcome to LingoCine!")
        name_input = st.text_input("Enter your name to start:")
        if st.button("Let's Go!"):
            if name_input.strip() != "":
                st.session_state.user_name = name_input.strip()
                st.rerun() # Tải lại trang để cập nhật tên
    
    # Nếu đã nhập tên rồi thì hiện thông tin
    else:
        st.title(f"Hi, {st.session_state.user_name}! 🌟")
        st.subheader(f"Level {st.session_state.level}")
        
        st.metric("Total XP", f"{st.session_state.xp} XP")
        
        st.markdown("---")
        st.header("Skill Overview")
        st.write(f"Listening: {st.session_state.skills['Listening']}")
        st.write(f"Vocabulary: {st.session_state.skills['Vocabulary']}")
        st.write(f"Grammar: {st.session_state.skills['Grammar']}")
        
        # Nút đổi tên nếu lỡ nhập sai
        st.markdown("---")
        if st.button("Change Name"):
            st.session_state.user_name = ""
            st.rerun()

# ================= MAIN INTENTS =================

def tab_cinema_mode():
    st.markdown('<p class="big-font">Cinema Mode: Watch & Learn</p>', unsafe_allow_html=True)
    
    movie_options = {
        "Avengers: Infinity War (Thanos)": "https://www.youtube.com/watch?v=6ZfuNTqbHE8",
        "Frozen (Let it Go)": "https://www.youtube.com/watch?v=L0MK7qz13bU"
    }
    
    selected_movie = st.selectbox("Choose a Scene:", list(movie_options.keys()))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.video(movie_options[selected_movie])
    
    with col2:
        st.info("Listening Challenge")
        
        if "Thanos" in selected_movie:
            st.markdown("**Complete the quote:**")
            st.markdown('*"Dread it. Run from it. _______ arrives all the same."*')
            ans = st.text_input("Type the missing word:", key="vid_q1")
            
            if st.button("Check Answer", key="btn_check_vid"):
                if ans.lower() == "destiny":
                    st.balloons()
                    st.success("Correct! +20 XP | +5 Listening")
                    st.session_state.xp += 20
                    st.session_state.skills['Listening'] += 5 # Tăng điểm kỹ năng Nghe
                else:
                    st.error("Try again! Hint: It starts with 'D'")
        
        elif "Frozen" in selected_movie:
            st.markdown("**Vocabulary Check:**")
            st.markdown("What does **'Isolation'** mean?")
            options = ["Sự kết nối", "Sự cô lập", "Sự vui vẻ"]
            choice = st.radio("Choose meaning:", options)
            if st.button("Check", key="btn_frozen"):
                if choice == "Sự cô lập":
                    st.success("Correct! +15 XP | +5 Vocabulary")
                    st.session_state.xp += 15
                    st.session_state.skills['Vocabulary'] += 5 # Tăng điểm Từ vựng
                else:
                    st.error("Wrong answer.")

def tab_flashcards():
    st.markdown('<p class="big-font">Rapid Flashcards</p>', unsafe_allow_html=True)
    
    if 'current_card' not in st.session_state:
        st.session_state.current_card = random.choice(st.session_state.vocab_list)
    
    card = st.session_state.current_card
    
    container = st.container()
    container.markdown(f"""
    <div class="highlight" style="text-align: center; margin-bottom: 20px;">
        <h2>{card['word']}</h2>
        <p style="color: #aaa;">/ {card['type'] if 'type' in card else 'Noun'} /</p>
        <hr style="border-color: #555;">
        <p style="font-size: 18px;">"{card['example']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Reveal Meaning"):
        st.info(f"Meaning: **{card['meaning']}**")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("I forgot"):
            st.warning("Reviewing is key!")
            st.session_state.current_card = random.choice(st.session_state.vocab_list)
            st.rerun()
    with col_b2:
        if st.button("I know it"):
            st.session_state.xp += 10
            st.session_state.skills['Vocabulary'] += 2 # Tăng nhẹ điểm từ vựng
            st.success("Great! +2 Vocabulary Points")
            st.session_state.current_card = random.choice(st.session_state.vocab_list)
            st.rerun()

def tab_grammar_duel():
    st.markdown('<p class="big-font">Grammar Duel</p>', unsafe_allow_html=True)
    
    st.write("Rearrange the words:")
    scrambled = ["movie", "yesterday", "watched", "I", "a", "good"]
    correct_sentence = "I watched a good movie yesterday"
    
    st.code(" ".join(random.sample(scrambled, len(scrambled))), language="text")
    
    user_input = st.text_input("Your answer:")
    
    if st.button("Submit Fight"):
        if user_input.strip() == correct_sentence:
            st.balloons()
            st.success("K.O! +30 XP | +10 Grammar Points")
            st.session_state.xp += 30
            st.session_state.skills['Grammar'] += 10 # Boost grammar score
        else:
            st.warning(f"Wrong! Correct: {correct_sentence}")

def tab_progress_coach():
    st.markdown('<p class="big-font">My Progress & AI Coach</p>', unsafe_allow_html=True)
    
    col_chart, col_coach = st.columns([2, 1])
    
    with col_chart:
        st.subheader("Skill Breakdown")
        # Tabular data design
        chart_data = pd.DataFrame({
            "Skill": list(st.session_state.skills.keys()),
            "Points": list(st.session_state.skills.values())
        })
        # Generate a bar chart
        st.bar_chart(chart_data, x="Skill", y="Points", color="#FF4B4B")
    
    with col_coach:
        st.subheader("AI Coach Suggestion")
        
        # Detect the weakest skill
        weakest_skill = min(st.session_state.skills, key=st.session_state.skills.get)
        
        st.markdown(f"""
        <div class="highlight">
            <h3 style="color: #FFD700;">Focus on: {weakest_skill}</h3>
            <p>Your <b>{weakest_skill}</b> score is the lowest right now.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### Recommended Action:")
        if weakest_skill == "Listening":
            st.info("Go to 'Cinema Mode' and watch 2 more clips without subtitles.")
        elif weakest_skill == "Vocabulary":
            st.info("Use 'Flashcards' to learn 5 new words today.")
        else:
            st.info("Enter 'Grammar Duel' and complete 3 sentence challenges.")

# ================= APP LAYOUT =================
tabs = st.tabs(["Cinema Mode", "Flashcards", "Grammar Duel", "Progress & Coach"])

with tabs[0]:
    tab_cinema_mode()

with tabs[1]:
    tab_flashcards()

with tabs[2]:
    tab_grammar_duel()

with tabs[3]:
    tab_progress_coach()

# Footer
st.markdown("---")
st.caption("LingoCine v2.0 - Personalized Learning Dashboard")