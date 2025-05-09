import streamlit as st
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Cognitive Architecture Extractor", page_icon="🧠")
st.title("🧠 Cognitive Architecture Extractor")
st.markdown("**Answer surgically. This isn't personality — it's cognitive root structure.**")

analyzer = SentimentIntensityAnalyzer()

# --- QUESTIONS
section1 = [
    "When you’re overwhelmed, what’s the first thing you try to control?",
    "Do you seek truth more to understand reality — or to control your future?",
    "What part of you feels “non-negotiable” no matter what life throws at you?",
    "Do you feel closer to yourself when you’re thinking or when you’re acting?",
    "What kind of chaos feels weirdly comforting?"
]

section2 = [
    "What type of person do you almost never trust — no matter how “nice” they seem?",
    "What do you instinctively filter out when making decisions?",
    "Do you run toward intensity or away from it? Why?",
    "In your internal monologue, who are you always trying to explain yourself to?",
    "What do you deeply wish you believed — but can't?"
]

section3 = [
    "If your inner world had a landscape, what would it look like?",
    "What metaphor describes how your mind moves through a problem?",
    "What emotion do you treat like a luxury — only feeling when it's safe?"
]

free_write_prompt = (
    "⚡ For 3 minutes, write without thinking. Don’t censor. Don’t try to be smart. "
    "Just bleed onto the page about who you are, what you fear, or what you want most."
)

all_questions = section1 + section2 + section3
responses = {}

with st.form("mirror_form"):
    for q in all_questions:
        responses[q] = st.text_area(q, height=80)
    free_response = st.text_area("✍️ Free Writing Window", placeholder=free_write_prompt, height=200)
    submitted = st.form_submit_button("🧬 Analyze Mind")

if submitted:
    st.subheader("🩺 Mind Structure Report")

    compression_total = 0
    insight_flags = {"projective": 0, "owned": 0}
    metaphors_detected = 0

    for answer in responses.values():
        blob = TextBlob(answer)
        words = len(blob.words)
        sentences = len(blob.sentences)
        compression_score = round(sentences / words, 2) if words else 0
        compression_total += compression_score

        if any(x in answer.lower() for x in ["they always", "everyone thinks"]):
            insight_flags["projective"] += 1
        if any(x in answer.lower() for x in ["i know", "i tend to", "i’ve learned"]):
            insight_flags["owned"] += 1
        if "like" in answer or "as if" in answer:
            metaphors_detected += 1

    avg_compression = round(compression_total / len(responses), 2)
    shadow_type = "Projected" if insight_flags["projective"] > insight_flags["owned"] else "Owned"
    metaphor_density = (
        "High" if metaphors_detected >= 4 else
        "Moderate" if metaphors_detected >= 2 else
        "Low"
    )

    sentiment = analyzer.polarity_scores(free_response)["compound"]
    mood = (
        "Elevated" if sentiment >= 0.5 else
        "Positive" if sentiment > 0.1 else
        "Distressed" if sentiment < -0.5 else
        "Anxious" if sentiment < -0.1 else
        "Flat/Neutral"
    )

    st.markdown(f"### 🧠 Compression Rate: `{avg_compression}`")
    st.markdown(f"### 🪞 Shadow Structure: `{shadow_type}`")
    st.markdown(f"### 🧭 Metaphor Density: `{metaphor_density}`")
    st.markdown(f"### 🧬 Emotional Charge (Free Write): `{mood}`")

    st.markdown("---")
    st.markdown("#### 🧩 Observations:")
    st.markdown("- High compression = fast integration / potential inner loops.")
    st.markdown("- Metaphor use = abstraction level (story-form cognition vs. literal).")
    st.markdown("- Shadow = how responsibility is handled (projected or integrated).")
    st.markdown("- Emotional tone = architecture tension.")

    st.success("✅ Mirror extraction complete.")
