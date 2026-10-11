
import streamlit as st
import json
import re
from pathlib import Path

st.set_page_config(
    page_title="SaaSum AI",
    page_icon="🤖",
    layout="centered"
)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f3ff 0%, #eef4ff 100%);
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: #5b21b6 !important;
        font-weight: 800 !important;
        text-align: center;
    }

    h2, h3 {
        color: #4338ca !important;
    }

    .stApp p {
        color: #374151;
    }

    div.stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        border: 1px solid #c4b5fd;
        background: white;
        color: #5b21b6;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #ede9fe;
        border-color: #7c3aed;
        color: #4c1d95;
    }

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 12px;
        border: 1px solid #e5e7eb;
        background-color: rgba(255, 255, 255, 0.85);
    }

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)
# Load FAQ data
faq_file = Path(__file__).parent / "faq_data.json"

with open(faq_file, "r", encoding="utf-8") as file:
    data = json.load(file)

faqs = data["faqs"]

# Website design
# Website design
st.title("🤖 SaaSum AI")
st.subheader("Your Smart Business Assistant")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #6d28d9, #2563eb);
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
">
    <h2 style="color: white !important;">
        👋 Welcome to SaaSum AI!
    </h2>
    <p style="color: white !important; font-size: 16px;">
        Your smart business support assistant.
    </p>
    <p style="color: white !important;">
        Ask me about orders, delivery, payments, returns and refunds.
    </p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Welcome to ShopEase! Ask me about orders, "
    "delivery, payments, returns, and refunds."
)

st.markdown("### 💡 Suggested Questions")

suggested_questions = [
    "How can I track my order?",
    "Do you offer refunds?",
    "What are your business hours?",
    "How much does shipping cost?"
]

cols = st.columns(2)

for i, question in enumerate(suggested_questions):
    with cols[i % 2]:
        if st.button(question, key=f"suggest_{i}"):
            st.session_state.suggested_question = question

st.info("Demo chatbot powered by an FAQ knowledge base.")


# FAQ matching function
def find_answer(user_question):
    question = user_question.lower().strip()
    question = re.sub(r"[^\w\s]", "", question)

        # Handle common question variations
    aliases = {
        "where is my order": "order tracking",
        "track my package": "order tracking",
        "track my parcel": "order tracking",
        "where is my package": "order tracking",
        "when will my order arrive": "delivery time",
        "how long does delivery take": "delivery time",
        "how can i get my money back": "refund",
        "how do i return a damaged item": "return damaged product",
        "what payment methods do you accept": "payment methods"
    }

    for phrase, replacement in aliases.items():
        if phrase in question:
            question += " " + replacement

    # Handle greetings
        # Handle greetings
    greetings = [
        "hello", "hi", "hey", "how are you",
        "whats up", "what is up", "how is it going",
        "good morning", "good afternoon", "good evening"
    ]

    if question in greetings:
        if question in [
            "how are you", "whats up",
            "what is up", "how is it going"
        ]:
            return (
                "I'm doing great! 😊 Thanks for asking. "
                "I'm SaaSum AI, ready to help you with ShopEase!"
            )

        return (
            "Hello! 👋 Welcome to ShopEase Support. "
            "How can I help you today?"
        )
        if question in ["how are you", "whats up", "what is up", "how is it going"]:
            return (
                "I'm doing great! 😊 Thanks for asking. "
                "I'm SaaSum AI, ready to help you with ShopEase!"
            )

        return (
            "Hello! 👋 Welcome to ShopEase Support. "
            "How can I help you today?"
        )

    # Handle identity questions
    if question in [
        "what is your name",
        "who are you",
        "tell me your name"
    ]:
        return (
            "I'm SaaSum AI 🤖, your smart business assistant! "
            "I help customers with orders, delivery, payments, "
            "returns, and refunds."
        )

    # Match the question with FAQs
    best_faq = None
    best_score = 0

    for faq in faqs:
        score = 0

        # Match FAQ keywords
        for keyword in faq.get("keywords", []):
            keyword = keyword.lower().strip()

            if keyword and keyword in question:
                score += 3

        # Match important words in the FAQ question
        faq_words = set(
            re.findall(r"\b\w+\b", faq["question"].lower())
        )

        question_words = set(
            re.findall(r"\b\w+\b", question)
        )

        common_words = {
            "what", "is", "are", "the", "a", "an", "do",
            "does", "can", "i", "my", "me", "how", "to",
            "your", "you", "of", "for", "and", "in"
        }

        faq_words -= common_words
        question_words -= common_words

        score += 2 * len(faq_words & question_words)

        if score > best_score:
            best_score = score
            best_faq = faq

    if best_faq is not None and best_score >= 2:
        return best_faq["answer"]

    return (
    "I'm sorry, I couldn't find an answer to that question yet. 😊\n\n"
    "I'm here to help with:\n"
    "- 📦 Order tracking\n"
    "- 🚚 Delivery information\n"
    "- 💳 Payment methods\n"
    "- ↩️ Returns and refunds\n\n"
    "Please try asking about one of these topics!"
)

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("💬 Ask your question here...")

if "suggested_question" in st.session_state:
    user_input = st.session_state.pop("suggested_question")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    response = find_answer(user_input)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    # About section
with st.expander("ℹ️ About SaaSum AI"):
    st.write("""
    **SaaSum AI** is a customer-support chatbot prototype
    designed for ShopEase.

    **Features:**
    - FAQ-based customer support
    - Keyword matching for user questions
    - Order, delivery, payment, return and refund information
    - Interactive chat interface

    **Current limitation:**
    This demo uses a predefined FAQ knowledge base.
    It does not access live orders or process real payments.

    **Future scope:**
    Generative AI integration, multilingual support,
    and live order-tracking integration.
    """)

