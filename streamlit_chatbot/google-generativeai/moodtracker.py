import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import random
import json

# Page configuration
st.set_page_config(
    page_title="MoodTracker",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .quote-container {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 2rem;
        font-style: italic;
        text-align: center;
    }
    .mood-emoji {
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'todos' not in st.session_state:
    st.session_state.todos = []
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = ""
if 'hydration_glasses' not in st.session_state:
    st.session_state.hydration_glasses = 0
if 'sleep_hours' not in st.session_state:
    st.session_state.sleep_hours = 0

# Predefined mood emojis and songs
MOOD_EMOJIS = {
    "Ecstatic": "🤩",
    "Happy": "😊",
    "Content": "😌",
    "Neutral": "😐",
    "Sad": "😢",
    "Angry": "😠",
    "Anxious": "😰",
    "Tired": "😴",
    "Excited": "🤗",
    "Grateful": "🙏"
}

SONG_RECOMMENDATIONS = {
    "Ecstatic": ["Don't Stop Me Now - Queen", "Happy - Pharrell Williams", "I Got a Feeling - Black Eyed Peas"],
    "Happy": ["Good Vibes - Chris Janson", "Three Little Birds - Bob Marley", "Walking on Sunshine - Katrina"],
    "Content": ["Perfect - Ed Sheeran", "Somewhere Over the Rainbow - Israel", "What a Wonderful World - Louis Armstrong"],
    "Neutral": ["Weightless - Marconi Union", "Clair de Lune - Debussy", "Mad World - Gary Jules"],
    "Sad": ["The Sound of Silence - Simon & Garfunkel", "Hurt - Johnny Cash", "Tears in Heaven - Eric Clapton"],
    "Angry": ["Break Stuff - Limp Bizkit", "Chop Suey - System of a Down", "Bodies - Drowning Pool"],
    "Anxious": ["Breathe - Pink Floyd", "The Scientist - Coldplay", "Fix You - Coldplay"],
    "Tired": ["Sleepyhead - Passion Pit", "Mr. Sandman - The Chordettes", "Sleep - Eric Whitacre"],
    "Excited": ["Uptown Funk - Bruno Mars", "Can't Stop the Feeling - Justin Timberlake", "Celebration - Kool & The Gang"],
    "Grateful": ["Thank You - Dido", "Grateful - Rita Ora", "Count on Me - Bruno Mars"]
}

DAILY_QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Life is what happens to you while you're busy making other plans. - John Lennon",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It is during our darkest moments that we must focus to see the light. - Aristotle",
    "The only impossible journey is the one you never begin. - Tony Robbins",
    "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
    "The purpose of our lives is to be happy. - Dalai Lama",
    "Life is really simple, but we insist on making it complicated. - Confucius",
    "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
    "Be yourself; everyone else is already taken. - Oscar Wilde"
]

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌟 MoodTracker - Your Daily Wellness Companion 🌟</h1>
</div>
""", unsafe_allow_html=True)

# Quote of the Day (Compulsory)
today_quote = random.choice(DAILY_QUOTES)
st.markdown(f"""
<div class="quote-container">
    <h3>💭 Quote of the Day</h3>
    <p style="font-size: 1.2rem; margin-top: 1rem;">"{today_quote}"</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for daily activities
with st.sidebar:
    st.markdown("## 📋 Daily Dashboard")
    
    # Daily Goal Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🎯 Goal of the Day")
    daily_goal = st.text_input("Set your daily goal:", value=st.session_state.daily_goal, key="goal_input")
    if daily_goal != st.session_state.daily_goal:
        st.session_state.daily_goal = daily_goal
    
    if st.session_state.daily_goal:
        st.success(f"Today's Goal: {st.session_state.daily_goal}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Todo List Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### ✅ Todo List")
    new_todo = st.text_input("Add new todo:", key="new_todo")
    if st.button("Add Todo") and new_todo:
        st.session_state.todos.append({"task": new_todo, "completed": False})
        st.rerun()
    
    # Display todos
    for i, todo in enumerate(st.session_state.todos):
        col1, col2 = st.columns([3, 1])
        with col1:
            completed = st.checkbox(todo["task"], value=todo["completed"], key=f"todo_{i}")
            st.session_state.todos[i]["completed"] = completed
        with col2:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.todos.pop(i)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hydration Status
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 💧 Hydration Status")
    hydration = st.slider("Glasses of water today:", 0, 12, st.session_state.hydration_glasses)
    st.session_state.hydration_glasses = hydration
    
    hydration_percentage = min((hydration / 8) * 100, 100)
    st.progress(hydration_percentage / 100)
    st.write(f"{hydration}/8 glasses ({hydration_percentage:.0f}%)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sleep Status
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 😴 Sleep Status")
    sleep = st.slider("Hours of sleep last night:", 0, 12, st.session_state.sleep_hours)
    st.session_state.sleep_hours = sleep
    
    if sleep >= 7:
        st.success(f"Great! {sleep} hours is excellent sleep!")
    elif sleep >= 6:
        st.warning(f"{sleep} hours - could be better")
    else:
        st.error(f"{sleep} hours - you need more sleep!")
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Mood Tracking Section
    st.markdown("## 😊 Track Your Mood")
    
    # Custom mood selection
    selected_mood = st.selectbox("How are you feeling today?", list(MOOD_EMOJIS.keys()))
    
    # Display selected mood emoji
    st.markdown(f"""
    <div class="mood-emoji">
        {MOOD_EMOJIS[selected_mood]}
    </div>
    """, unsafe_allow_html=True)
    
    # Optional mood note
    mood_note = st.text_area("Add a note about your mood (optional):", max_chars=200)
    
    # Mood intensity
    mood_intensity = st.slider("Mood intensity (1-10):", 1, 10, 5)
    
    # Save mood button
    if st.button("Save Today's Mood", type="primary"):
        mood_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "mood": selected_mood,
            "intensity": mood_intensity,
            "note": mood_note,
            "emoji": MOOD_EMOJIS[selected_mood]
        }
        st.session_state.mood_data.append(mood_entry)
        st.success("Mood saved successfully! 🎉")
        st.rerun()
    
    # Monthly Mood Graph
    if st.session_state.mood_data:
        st.markdown("## 📊 Monthly Mood Tracking")
        
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.mood_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Create mood mapping for numerical values
        mood_values = {mood: i for i, mood in enumerate(MOOD_EMOJIS.keys())}
        df['mood_value'] = df['mood'].map(mood_values)
        
        # Create the graph
        fig = go.Figure()
        
        # Add line trace
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['mood_value'],
            mode='lines+markers',
            name='Mood Trend',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#764ba2')
        ))
        
        # Customize layout
        fig.update_layout(
            title='Your Mood Journey',
            xaxis_title='Date',
            yaxis_title='Mood',
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(len(MOOD_EMOJIS))),
                ticktext=list(MOOD_EMOJIS.keys())
            ),
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Mood statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            most_common_mood = df['mood'].mode().iloc[0] if not df.empty else "N/A"
            st.metric("Most Common Mood", f"{MOOD_EMOJIS.get(most_common_mood, '')} {most_common_mood}")
        
        with col_stat2:
            avg_intensity = df['intensity'].mean() if not df.empty else 0
            st.metric("Average Intensity", f"{avg_intensity:.1f}/10")
        
        with col_stat3:
            total_entries = len(df)
            st.metric("Total Entries", total_entries)

with col2:
    # Song Recommendations
    st.markdown("## 🎵 Song Recommendations")
    
    if selected_mood in SONG_RECOMMENDATIONS:
        recommended_songs = SONG_RECOMMENDATIONS[selected_mood]
        st.markdown(f"**Based on your {selected_mood.lower()} mood:**")
        
        for i, song in enumerate(recommended_songs, 1):
            st.markdown(f"{i}. 🎶 {song}")
    
    # Recent Mood Entries
    if st.session_state.mood_data:
        st.markdown("## 📝 Recent Entries")
        recent_entries = sorted(st.session_state.mood_data, key=lambda x: x['date'], reverse=True)[:5]
        
        for entry in recent_entries:
            with st.expander(f"{entry['emoji']} {entry['date']} - {entry['mood']}"):
                st.write(f"**Intensity:** {entry['intensity']}/10")
                if entry['note']:
                    st.write(f"**Note:** {entry['note']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Made with ❤️ for your mental wellness journey | Track • Reflect • Grow
</div>
""", unsafe_allow_html=True)