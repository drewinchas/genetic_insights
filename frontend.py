#
# All of the code in this app was created with the assistance of GitHub Copilot
# and is intended to be used as a starting point for a Streamlit web application.
# The app is a simple genetic insights dashboard that allows users to log in, view
# their DNA information, view detailed insights, securely transmit information to
# their doctor, and chat with a bot about their DNA information.
#


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Global variable to store GitHub API Key
gh_token = None

# Function to display the login screen
def login_screen():
    st.title("Genetic Insights")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    gh_token = st.text_input("GitHub API Key")

    if st.button("Login"):
        if username and password and gh_token:
            st.session_state.logged_in = True
            st.session_state.gh_token = gh_token
            st.rerun()


# Function to display the home screen
def home_screen():
    st.title("Welcome to Genetic Insights")
    st.write("You are now logged in.")
    
    # Display user's DNA information
    st.subheader("Your DNA Information")
    st.write("Here is a summary of your DNA information...")

    # Create a grid layout for the buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("View Additional Details"):
            st.session_state.view_details = True
            st.rerun()

    with col2:
        if st.button("Securely Transmit to Doctor"):
            st.session_state.transmit_info = True
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:
        if st.button("Chat with Bot"):
            st.session_state.chat_with_bot = True
            st.rerun()

    with col4:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# Function to display detailed DNA information
def detailed_info():
    st.title("Detailed DNA Information")
    st.write("Here are the detailed insights of your DNA information...")

    # Example text information
    st.subheader("Genetic Markers")
    st.write("Marker 1: Value")
    st.write("Marker 2: Value")
    st.write("Marker 3: Value")

    # Example graph
    st.subheader("Genetic Data Visualization")
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y)
    st.pyplot(fig)

    if st.button("Back to Home"):
        st.session_state.view_details = False
        st.rerun()

# Function to display the transmit information screen
def transmit_info():
    st.title("Transmit Genetic Information to Doctor")
    st.write("Please provide the following information:")

    doctor_name = st.text_input("Doctor's Full Name")
    doctor_phone = st.text_input("Doctor's Phone Number")
    doctor_email = st.text_input("Doctor's Email Address")

    consent = st.radio("Do you consent to release of your genetic information?", ("Yes", "No"))
    agree_to_privacy = st.checkbox("Agree to Privacy Policy and Terms")

    if st.button("Send data"):
        if consent == "Yes" and agree_to_privacy:
            st.write("Your genetic information has been securely transmitted to your doctor.")
        else:
            st.write("You must consent to the release of your genetic information and agree to the privacy policy and terms.")

    if st.button("Back to Home"):
        st.session_state.transmit_info = False
        st.rerun()

# Function to display the chat with bot screen
def dna_chat():
    import os
    from openai import OpenAI

    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    client = OpenAI(
        base_url=endpoint,
        api_key=st.session_state.gh_token,
    )
    
    st.title("Chat with DNA Bot")
    st.write("Ask questions about your DNA information.")

    # Example DNA information to provide context
    dna_info = "Here is a summary of your DNA information: Marker 1: Value, Marker 2: Value, Marker 3: Value."

    user_input = st.text_input("Your question:")
    if st.button("Send"):
        if user_input:
            # Call to the OpenAI API (or any other LLM API)
                        
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a DNA bot. You will use this summary to answer questions about the user's DNA information: " + dna_info,
                    },
                    {
                        "role": "user",
                        "content": user_input,
                    },
                ],
                #prompt=f"{dna_info}\n\nUser: {user_input}\nBot:",
                max_tokens=150
            )
            st.write(response.choices[0].message.content)

    if st.button("Back to Home"):
        st.session_state.chat_with_bot = False
        st.rerun()

# Main function to control the app flow
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'view_details' not in st.session_state:
        st.session_state.view_details = False
    if 'transmit_info' not in st.session_state:
        st.session_state.transmit_info = False
    if 'chat_with_bot' not in st.session_state:
        st.session_state.chat_with_bot = False

    if st.session_state.logged_in:
        if st.session_state.view_details:
            detailed_info()
        elif st.session_state.transmit_info:
            transmit_info()
        elif st.session_state.chat_with_bot:
            dna_chat()
        else:
            home_screen()
    else:
        login_screen()

if __name__ == "__main__":
    main()