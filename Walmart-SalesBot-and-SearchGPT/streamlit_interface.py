import streamlit as st
import requests

# Counter for generating unique keys
input_counter = 0

# Function to initialize session state
def initialize_session_state():
    if "is_dark_theme" not in st.session_state:
        st.session_state.is_dark_theme = False

# Streamlit app code
def main():
    global input_counter
    initialize_session_state()

    st.title("AI Chatbot 🤖")

    # Sidebar for selecting the bot type and theme toggle button
    st.sidebar.title("Settings")
    selected_bot = st.sidebar.radio("Select Bot:", ("WalmartBot", "SearchGPT"))

    # Theme toggle button
    st.sidebar.button("Toggle Theme", on_click=toggle_theme)

    # Main content
    st.subheader("Developed by: Shaon Sikder 👨‍💻")

    # Load previous messages from session state
    prev_messages = st.session_state.get("prev_messages", [])

    # Display previous messages in a chat-like interface
    for msg in prev_messages:
        st.text(f"You: {msg['user']}")
        st.text(f"Bot: 💬 {msg['bot']}")

    user_input = st.text_input(f"You {input_counter}:", key=input_counter)

    if st.button("Submit"):
        if selected_bot == "WalmartBot":
            response = get_walmart_bot_response(user_input)
            display_response(response, user_input, prev_messages)
        elif selected_bot == "SearchGPT":
            response = get_searchgpt_response(user_input)
            display_response(response, user_input, prev_messages)

        # Update input counter
        input_counter += 1

    # Footer with LinkedIn profile link
    st.markdown("[Connect with me on LinkedIn](https://www.linkedin.com/in/shaon2221/) 🔗")

    # Apply the selected theme
    apply_theme()

def get_walmart_bot_response(user_input):
    endpoint = "http://localhost:5000/walmartbot"
    data = {"messages": [user_input]}
    response = requests.post(endpoint, json=data)
    return response.json()

def get_searchgpt_response(user_input):
    endpoint = "http://localhost:5000/searchgpt"
    reply = requests.post(endpoint, json={"text": user_input})
    response = {"messages": [reply.json()]}
    return response

def display_response(response, user_input, prev_messages):
    if "messages" in response:
        for message in response["messages"]:
            st.text(f"Bot: 💬 {message}")

    if "sources" in response:
        for source in response["sources"]:
            st.text(f"Source: 📚 {source}")

    # Update previous messages
    prev_messages.append({"user": user_input, "bot": response.get("messages", [""])[0]})
    st.session_state.prev_messages = prev_messages[-5:]  # Keep only the last 5 messages

def apply_theme():
    # Check if dark theme is enabled
    is_dark_theme = st.session_state.get("is_dark_theme", False)

    # Apply the theme based on the user's choice
    if is_dark_theme:
        st.markdown(
            """
            <style>
                body {
                    background-color: #00172B;
                    color: #C6CDD4;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Default light theme
        st.markdown(
            """
            <style>
                body {
                    background-color: #FFFFFF;
                    color: #000000;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

def toggle_theme():
    st.session_state.is_dark_theme = not st.session_state.is_dark_theme
    # Use this to rerun the script when the button is clicked
    st.rerun()

# Run the Streamlit app
if __name__ == "__main__":
    main()
