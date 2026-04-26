import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Crypto Scam Detector",
    page_icon="🛡️",
    layout="wide"
)

if "token" not in st.session_state:
    st.session_state.token = None

st.title("🛡️ Crypto Scam Token Detector")

menu = st.sidebar.radio(
    "Navigation",
    ["Login", "Register", "Check Token", "History", "Favorites"]
)

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


if menu == "Register":
    st.header("Create Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.success("Registration successful!")
        else:
            st.error(response.json().get("detail", "Registration failed"))


elif menu == "Login":
    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.success("Login successful!")
        else:
            st.error(response.json().get("detail", "Login failed"))


elif menu == "Check Token":
    st.header("Check Token")

    if not st.session_state.token:
        st.warning("Please log in first.")
    else:
        token_name = st.text_input("Token Name", "Bitcoin")
        token_url = st.text_input("Token URL", "https://crypto.com/price/bitcoin")

        if st.button("Analyze"):
            response = requests.post(
                f"{API_URL}/predict/",
                headers=auth_headers(),
                json={
                    "name": token_name,
                    "url": token_url
                }
            )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Result")

                col1, col2, col3 = st.columns(3)
                col1.metric("Prediction", result["prediction"])
                col2.metric("Risk Score", result["risk_score"])
                col3.metric("Probability", result["probability"])

                st.info(result["explanation"])

                if "token_id" in result:
                    token_id = result["token_id"]
                    if st.button("Add to Favorites"):
                        fav_response = requests.post(
                            f"{API_URL}/favorites/{token_id}",
                            headers=auth_headers()
                        )
                        if fav_response.status_code == 200:
                            st.success("Added to favorites!")
                        else:
                            st.error(fav_response.json().get("detail", "Failed to add favorite"))
            else:
                st.error(response.json().get("detail", "Prediction failed"))


elif menu == "History":
    st.header("Prediction History")

    if not st.session_state.token:
        st.warning("Please log in first.")
    else:
        response = requests.get(
            f"{API_URL}/checks/",
            headers=auth_headers()
        )

        if response.status_code == 200:
            history = response.json()

            if history:
                st.dataframe(history, use_container_width=True)
            else:
                st.info("No checks yet.")
        else:
            st.error(response.json().get("detail", "Failed to load history"))


elif menu == "Favorites":
    st.header("Favorite Tokens")

    if not st.session_state.token:
        st.warning("Please log in first.")
    else:
        response = requests.get(
            f"{API_URL}/favorites/",
            headers=auth_headers()
        )

        if response.status_code == 200:
            favorites = response.json()

            if favorites:
                st.dataframe(favorites, use_container_width=True)
            else:
                st.info("No favorite tokens yet.")
        else:
            st.error(response.json().get("detail", "Failed to load favorites"))
