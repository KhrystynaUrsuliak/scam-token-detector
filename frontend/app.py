import streamlit as st
import pandas as pd
import requests
import jwt
import plotly.express as px
import plotly.graph_objects as go


API_URL = "http://127.0.0.1:8000"

TRANSLATIONS = {
    "English": {
        "language": "Language",
        "navigation": "Navigation",
        "logged_in_as": "Logged in as {username}",
        "role": "Role: {role}",
        "log_out": "Log out",
        "nav_home": "Home",
        "nav_auth": "Auth",
        "nav_dashboard": "Dashboard",
        "nav_check_token": "Check Token",
        "nav_history": "History",
        "nav_favorites": "Favorites",
        "nav_admin": "Admin",
        "home_title": "Detect risky crypto tokens before you trust them",
        "home_subtitle": "A smart web platform for scam token detection, risk scoring, token intelligence, prediction history, favorites tracking, and crypto safety analytics.",
        "check_token_button": "Check Token ->",
        "view_dashboard": "View Dashboard",
        "core_features": "Core Features",
        "scam_detection": "Scam Detection",
        "scam_detection_text": "Analyze token names and URLs using TF-IDF vectorization and a Random Forest classifier to identify suspicious patterns.",
        "token_intelligence": "Token Intelligence",
        "token_intelligence_text": "Show token icon, ticker, description, price, market cap, volume, and chart data for reliable assets.",
        "personal_workspace": "Personal Workspace",
        "personal_workspace_text": "Save checks to history, add tokens to favorites, and review activity through a personalized dashboard.",
        "account_access": "Account Access",
        "login": "Login",
        "register": "Register",
        "email": "Email",
        "password": "Password",
        "username": "Username",
        "confirm_password": "Confirm Password",
        "enter_email": "Enter your email",
        "enter_password": "Enter your password",
        "choose_username": "Choose a username",
        "create_password": "Create a password",
        "repeat_password": "Repeat your password",
        "log_in": "Log In",
        "create_account": "Create Account",
        "fill_all_fields": "Please fill in all fields.",
        "passwords_not_match": "Passwords do not match.",
        "login_successful": "Login successful.",
        "login_failed": "Login failed.",
        "registration_successful": "Registration successful.",
        "registration_failed": "Registration failed.",
        "dashboard": "Dashboard",
        "please_log_in": "Please log in first.",
        "no_checks": "No checks yet.",
        "platform_summary": "Platform Summary",
        "total_checks": "Total Checks",
        "legit": "Legit",
        "scam": "Scam",
        "avg_risk": "Avg Risk",
        "high_risk": "High Risk",
        "risk_score_trend": "Risk Score Trend",
        "risk_score_trend_text": "Track how token risk scores change across your recent checks.",
        "prediction_distribution": "Prediction Distribution",
        "prediction_distribution_text": "See the balance between legitimate and suspicious tokens.",
        "recent_checks": "Recent Checks",
        "recent_checks_text": "Last 10 token searches.",
        "open": "Open",
        "failed_load_dashboard": "Failed to load dashboard",
        "check_token": "Check Token",
        "token_name": "Token Name",
        "token_url": "Token URL",
        "analyze": "Analyze",
        "prediction_failed": "Prediction failed",
        "result": "Result",
        "prediction": "Prediction",
        "risk_score": "Risk Score",
        "probability": "Probability",
        "market_data_hidden": "Market data is not displayed because this token was classified as high-risk or potentially scam.",
        "token_information": "Token Information",
        "unknown": "Unknown",
        "market_cap_rank": "Market Cap Rank: #{rank}",
        "official_website": "Official website",
        "description": "Description",
        "market_statistics": "Market Statistics",
        "price": "Price",
        "market_cap": "Market Cap",
        "volume_24h": "24h Volume",
        "change_24h": "24h Change",
        "price_chart_7d": "7-Day Price Chart",
        "date": "Date",
        "price_usd": "Price USD",
        "no_market_data": "No reliable market data was found for this token. This may happen for very new, unknown, or suspicious tokens.",
        "add_to_favorites": "Add to Favorites",
        "added_to_favorites": "Added to favorites.",
        "failed_add_favorite": "Failed to add favorite",
        "prediction_history": "Prediction History",
        "recent_token_checks": "Recent Token Checks",
        "slug": "Slug",
        "open_link": "Open link",
        "no_explanation": "No explanation available.",
        "failed_load_history": "Failed to load history",
        "favorite_tokens": "Favorite Tokens",
        "no_favorites": "No favorite tokens yet.",
        "saved_tokens": "Saved Tokens",
        "failed_load_favorites": "Failed to load favorites",
        "admin_access_required": "Admin access required.",
        "failed_load_admin": "Failed to load admin dashboard data.",
        "admin_dashboard": "Admin Dashboard",
        "admin_subtitle": "Monitor platform activity, users, prediction results, high-risk checks, and token analysis behavior.",
        "platform_overview": "Platform Overview",
        "platform_overview_text": "Main platform totals and scam detection activity.",
        "users": "Users",
        "checks": "Checks",
        "scam_checks": "Scam Checks",
        "scam_rate": "Scam Rate",
        "scam_vs_legit": "Scam vs Legit",
        "scam_vs_legit_text": "Distribution of all platform token predictions.",
        "number_of_checks": "Number of Checks",
        "risk_score_admin_text": "Risk score movement across all analyzed tokens.",
        "filter_checks": "Filter Checks",
        "filter_checks_text": "Review token checks by prediction type and minimum risk score.",
        "all": "All",
        "minimum_risk_score": "Minimum Risk Score",
        "no_checks_found": "No checks found yet.",
        "registered_users": "Registered platform users.",
        "no_users_found": "No users found.",
        "check_number": "Check Number",
        "count": "Count",
        "share": "Share",
        "model_performance": "Model Performance",
        "model_performance_text": "Test set evaluation metrics for the scam detection model (20% holdout, random_state=42).",
        "accuracy": "Accuracy",
        "precision": "Precision",
        "recall": "Recall",
        "f1_score": "F1 Score",
        "confusion_matrix": "Confusion Matrix",
        "prob_distribution": "Scam Probability Distribution",
        "prob_distribution_text": "How confident the model is across all test set predictions.",
        "per_class_report": "Per-Class Report",
        "support": "Support",
        "dataset_missing": "Dataset file not found — place Crypto_enhanced_dataset.csv or Crypto_final_labeled.csv in backend/data/ to enable this section.",
    },
    "Українська": {
        "language": "Мова",
        "navigation": "Навігація",
        "logged_in_as": "Ви увійшли як {username}",
        "role": "Роль: {role}",
        "log_out": "Вийти",
        "nav_home": "Головна",
        "nav_auth": "Вхід",
        "nav_dashboard": "Дашборд",
        "nav_check_token": "Перевірити токен",
        "nav_history": "Історія",
        "nav_favorites": "Обране",
        "nav_admin": "Адмін",
        "home_title": "Виявляйте ризикові криптотокени до того, як їм довіряти",
        "home_subtitle": "Розумна вебплатформа для виявлення скам-токенів, оцінки ризику, аналізу токенів, історії перевірок, обраного та криптобезпеки.",
        "check_token_button": "Перевірити токен ->",
        "view_dashboard": "Відкрити дашборд",
        "core_features": "Основні функції",
        "scam_detection": "Виявлення скаму",
        "scam_detection_text": "Аналіз назв токенів та URL за допомогою TF-IDF векторизації і Random Forest класифікатора для пошуку підозрілих патернів.",
        "token_intelligence": "Інформація про токен",
        "token_intelligence_text": "Показ іконки токена, тикера, опису, ціни, ринкової капіталізації, обсягу торгів і графіка для надійних активів.",
        "personal_workspace": "Особистий кабінет",
        "personal_workspace_text": "Зберігайте перевірки в історії, додавайте токени в обране та переглядайте активність у персональному дашборді.",
        "account_access": "Доступ до акаунта",
        "login": "Вхід",
        "register": "Реєстрація",
        "email": "Email",
        "password": "Пароль",
        "username": "Ім'я користувача",
        "confirm_password": "Підтвердіть пароль",
        "enter_email": "Введіть email",
        "enter_password": "Введіть пароль",
        "choose_username": "Оберіть ім'я користувача",
        "create_password": "Створіть пароль",
        "repeat_password": "Повторіть пароль",
        "log_in": "Увійти",
        "create_account": "Створити акаунт",
        "fill_all_fields": "Будь ласка, заповніть усі поля.",
        "passwords_not_match": "Паролі не збігаються.",
        "login_successful": "Вхід успішний.",
        "login_failed": "Не вдалося увійти.",
        "registration_successful": "Реєстрація успішна.",
        "registration_failed": "Не вдалося зареєструватися.",
        "dashboard": "Дашборд",
        "please_log_in": "Будь ласка, спочатку увійдіть.",
        "no_checks": "Перевірок ще немає.",
        "platform_summary": "Загальна статистика",
        "total_checks": "Усього перевірок",
        "legit": "Легітимні",
        "scam": "Скам",
        "avg_risk": "Середній ризик",
        "high_risk": "Високий ризик",
        "risk_score_trend": "Динаміка ризику",
        "risk_score_trend_text": "Показує, як змінювався рівень ризику у ваших останніх перевірках.",
        "prediction_distribution": "Розподіл результатів",
        "prediction_distribution_text": "Показує співвідношення легітимних і підозрілих токенів.",
        "recent_checks": "Останні перевірки",
        "recent_checks_text": "Останні 10 пошуків токенів.",
        "open": "Відкрити",
        "failed_load_dashboard": "Не вдалося завантажити дашборд",
        "check_token": "Перевірити токен",
        "token_name": "Назва токена",
        "token_url": "URL токена",
        "analyze": "Аналізувати",
        "prediction_failed": "Не вдалося виконати прогноз",
        "result": "Результат",
        "prediction": "Прогноз",
        "risk_score": "Рівень ризику",
        "probability": "Ймовірність",
        "market_data_hidden": "Ринкові дані не показуються, тому що токен класифіковано як високоризиковий або потенційно скамний.",
        "token_information": "Інформація про токен",
        "unknown": "Невідомо",
        "market_cap_rank": "Рейтинг за капіталізацією: #{rank}",
        "official_website": "Офіційний сайт",
        "description": "Опис",
        "market_statistics": "Ринкова статистика",
        "price": "Ціна",
        "market_cap": "Капіталізація",
        "volume_24h": "Обсяг за 24 год",
        "change_24h": "Зміна за 24 год",
        "price_chart_7d": "Графік ціни за 7 днів",
        "date": "Дата",
        "price_usd": "Ціна USD",
        "no_market_data": "Надійних ринкових даних для цього токена не знайдено. Це може траплятися з дуже новими, невідомими або підозрілими токенами.",
        "add_to_favorites": "Додати в обране",
        "added_to_favorites": "Додано в обране.",
        "failed_add_favorite": "Не вдалося додати в обране",
        "prediction_history": "Історія прогнозів",
        "recent_token_checks": "Останні перевірки токенів",
        "slug": "Slug",
        "open_link": "Відкрити посилання",
        "no_explanation": "Пояснення недоступне.",
        "failed_load_history": "Не вдалося завантажити історію",
        "favorite_tokens": "Обрані токени",
        "no_favorites": "Обраних токенів ще немає.",
        "saved_tokens": "Збережені токени",
        "failed_load_favorites": "Не вдалося завантажити обране",
        "admin_access_required": "Потрібен доступ адміністратора.",
        "failed_load_admin": "Не вдалося завантажити дані адмін-дешборду.",
        "admin_dashboard": "Адмін-дешборд",
        "admin_subtitle": "Моніторинг активності платформи, користувачів, результатів прогнозів, високоризикових перевірок і поведінки аналізу токенів.",
        "platform_overview": "Огляд платформи",
        "platform_overview_text": "Основні показники платформи та активність виявлення скаму.",
        "users": "Користувачі",
        "checks": "Перевірки",
        "scam_checks": "Скам-перевірки",
        "scam_rate": "Частка скаму",
        "scam_vs_legit": "Скам vs легітимні",
        "scam_vs_legit_text": "Розподіл усіх прогнозів токенів на платформі.",
        "number_of_checks": "Кількість перевірок",
        "risk_score_admin_text": "Динаміка рівня ризику для всіх проаналізованих токенів.",
        "filter_checks": "Фільтр перевірок",
        "filter_checks_text": "Переглядайте перевірки за типом прогнозу та мінімальним рівнем ризику.",
        "all": "Усі",
        "minimum_risk_score": "Мінімальний рівень ризику",
        "no_checks_found": "Перевірок ще не знайдено.",
        "registered_users": "Зареєстровані користувачі платформи.",
        "no_users_found": "Користувачів не знайдено.",
        "check_number": "Номер перевірки",
        "count": "Кількість",
        "share": "Частка",
        "model_performance": "Якість моделі",
        "model_performance_text": "Метрики на тестовій вибірці (20% holdout, random_state=42).",
        "accuracy": "Точність",
        "precision": "Precision",
        "recall": "Recall",
        "f1_score": "F1 Score",
        "confusion_matrix": "Матриця помилок",
        "prob_distribution": "Розподіл ймовірностей скаму",
        "prob_distribution_text": "Впевненість моделі на всіх прикладах тестової вибірки.",
        "per_class_report": "Звіт по класах",
        "support": "Підтримка",
        "dataset_missing": "Файл датасету не знайдено — помістіть Crypto_enhanced_dataset.csv або Crypto_final_labeled.csv у backend/data/ для активації цього розділу.",
    },
}


def tr(key, **kwargs):
    language = st.session_state.get("language", "English")
    template = TRANSLATIONS[language].get(key, TRANSLATIONS["English"].get(key, key))
    return template.format(**kwargs)


def page_label(page_name):
    return {
        "Home": tr("nav_home"),
        "Auth": tr("nav_auth"),
        "Dashboard": tr("nav_dashboard"),
        "Check Token": tr("nav_check_token"),
        "History": tr("nav_history"),
        "Favorites": tr("nav_favorites"),
        "Admin": tr("nav_admin"),
    }.get(page_name, page_name)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Crypto Scam Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# SESSION STATE
# =========================

if "token" not in st.session_state:
    st.session_state.token = None

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "redirect_after_auth" not in st.session_state:
    st.session_state.redirect_after_auth = None

if "prefill_token_name" not in st.session_state:
    st.session_state.prefill_token_name = "Bitcoin"

if "prefill_token_url" not in st.session_state:
    st.session_state.prefill_token_url = "https://crypto.com/price/bitcoin"

if "auto_analyze_token" not in st.session_state:
    st.session_state.auto_analyze_token = False

if "language" not in st.session_state:
    st.session_state.language = "English"


# =========================
# HELPERS
# =========================

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def get_user_role():
    token = st.session_state.get("token")

    if not token:
        return None

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("role")
    except Exception:
        return None


def get_current_user():
    if not st.session_state.token:
        return None

    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers=auth_headers()
        )

        if response.status_code == 200:
            return response.json()

        return None
    except Exception:
        return None


def login_user(email, password):
    return requests.post(
        f"{API_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )


def register_user(username, email, password):
    return requests.post(
        f"{API_URL}/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


def go_to_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()


def redirect_after_successful_auth():
    if get_user_role() == "admin":
        st.session_state.redirect_after_auth = None
        st.session_state.current_page = "Admin"
    else:
        target_page = st.session_state.redirect_after_auth or "Dashboard"
        st.session_state.redirect_after_auth = None
        st.session_state.current_page = target_page


def format_money(value, digits=2):
    if value is None:
        return "N/A"
    return f"${value:,.{digits}f}"


def format_large_money(value):
    if value is None:
        return "N/A"
    return f"${value:,.0f}"


@st.cache_data(ttl=3600)
def get_token_icon(name, slug, prediction):
    if prediction != "LEGIT":
        return None

    try:
        query = slug or name

        response = requests.get(
            "https://api.coingecko.com/api/v3/search",
            params={"query": query},
            timeout=8
        )

        if response.status_code != 200:
            return None

        data = response.json()
        coins = data.get("coins", [])

        if not coins:
            return None

        normalized_name = (name or "").lower().strip()
        normalized_slug = (slug or "").lower().strip()

        for coin in coins:
            coin_id = (coin.get("id") or "").lower()
            coin_name = (coin.get("name") or "").lower()
            coin_symbol = (coin.get("symbol") or "").lower()

            if (
                coin_id == normalized_slug
                or coin_name == normalized_name
                or coin_symbol == normalized_slug
            ):
                return coin.get("large") or coin.get("thumb")

        return coins[0].get("large") or coins[0].get("thumb")

    except Exception:
        return None


# =========================
# GLOBAL CSS
# =========================

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #173b5f 0%, #07111f 42%, #030712 100%);
        color: #ffffff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    section[data-testid="stSidebar"] {
        background: #070f1c;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #dbeafe !important;
    }

    /* Nav radio: change active dot from default red to blue */
    section[data-testid="stSidebar"] [data-baseweb="radio"] label > div:first-child > div {
        border-color: #38bdf8 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] label > div:first-child > div > div {
        background-color: #0ea5e9 !important;
    }

    .sidebar-divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 16px 0 12px;
        border: none;
    }

    .sidebar-user-card {
        background: linear-gradient(135deg, rgba(37,99,235,0.18), rgba(14,165,233,0.10));
        border: 1px solid rgba(56,189,248,0.22);
        border-radius: 16px;
        padding: 14px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }

    .sidebar-user-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0ea5e9, #2563eb);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 800;
        color: white !important;
        flex-shrink: 0;
    }

    .sidebar-user-name {
        font-size: 14px;
        font-weight: 700;
        color: #e0f2fe !important;
        margin-bottom: 3px;
    }

    .sidebar-user-role {
        font-size: 11px;
        font-weight: 600;
        color: #7dd3fc !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    p, span, label {
        color: #dbeafe;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #2563eb);
        color: white;
        border: none;
        padding: 0.75rem 1.4rem;
        border-radius: 14px;
        font-weight: 800;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.28);
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 40px rgba(37, 99, 235, 0.38);
        color: white;
        border: none;
    }

    div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.75rem 1.4rem;
        border-radius: 14px;
        font-weight: 800;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.28);
        transition: 0.2s ease;
    }

    div.stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 40px rgba(37, 99, 235, 0.38);
        color: #ffffff !important;
        border: none !important;
    }

    div.stFormSubmitButton > button p {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    .stTextInput > div > div > input {
        background: #0f1b31;
        color: white;
        border: 1px solid #2d5e92;
        border-radius: 12px;
        padding: 12px;
    }

    .stTextInput label {
        color: #dbeafe !important;
        font-weight: 600;
    }

    .stSelectbox label {
        color: #dbeafe !important;
        font-weight: 700 !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
        border: 2px solid #7dd3fc !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 26px rgba(37, 99, 235, 0.35) !important;
    }

    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 800 !important;
    }

    .stSelectbox [data-baseweb="select"] svg {
        fill: #e0f2fe !important;
        color: #e0f2fe !important;
    }

    [data-baseweb="popover"] [role="listbox"] {
        background: #0b1f3a !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] [role="option"] * {
        background: #0b1f3a !important;
        color: #dbeafe !important;
        -webkit-text-fill-color: #dbeafe !important;
        font-weight: 700 !important;
    }

    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] [aria-selected="true"],
    [data-baseweb="popover"] [aria-selected="true"] * {
        background: #2563eb !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .hero-title {
        font-size: 68px;
        line-height: 1.05;
        font-weight: 900;
        letter-spacing: -2px;
        max-width: 980px;
        margin-bottom: 20px;
        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 22px;
        line-height: 1.5;
        color: #b6c7dc;
        max-width: 820px;
        margin-bottom: 34px;
    }

    .premium-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.045));
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 22px 70px rgba(0,0,0,0.35);
        min-height: 170px;
    }

    .premium-card h3 {
        color: #ffffff;
        font-size: 22px;
        margin-bottom: 12px;
    }

    .premium-card p {
        color: #b6c7dc;
        font-size: 15px;
        line-height: 1.5;
    }

    .section-title {
        font-size: 34px;
        font-weight: 850;
        margin-top: 55px;
        margin-bottom: 18px;
        color: #ffffff;
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.07);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.10);
    }

    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }

    .chart-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        padding: 20px 20px 10px 20px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    .chart-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .chart-subtitle {
        font-size: 14px;
        color: #9fb7d3;
        margin-bottom: 12px;
    }

    .history-name,
    .favorite-name {
        font-size: 22px;
        font-weight: 850;
        color: white;
        margin-bottom: 4px;
    }

    .history-meta,
    .favorite-meta {
        color: #9fb7d3;
        font-size: 14px;
        margin-bottom: 6px;
    }

    .history-link a,
    .favorite-link a {
        color: #38bdf8 !important;
        text-decoration: none;
        font-weight: 700;
    }

    .history-link a:hover,
    .favorite-link a:hover {
        text-decoration: underline;
    }

    .history-explanation {
        color: #c7d7e8;
        line-height: 1.5;
        font-size: 15px;
    }

    .recent-token-name {
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 6px;
    }

    .status-pill-legit {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.18);
        border: 1px solid rgba(34, 197, 94, 0.35);
        color: #86efac;
        font-weight: 800;
        text-align: center;
        margin-top: 4px;
    }

    .status-pill-scam {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(239, 68, 68, 0.18);
        border: 1px solid rgba(239, 68, 68, 0.35);
        color: #fca5a5;
        font-weight: 800;
        text-align: center;
        margin-top: 4px;
    }

    .simple-divider {
        width: 100%;
        height: 2px;
        background: rgba(255, 255, 255, 0.18);
        border: none;
        border-radius: 999px;
        margin: 18px 0 22px 0;
    }

    .admin-title {
        font-size: 42px;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }

    .admin-subtitle {
        color: #9fb7d3;
        font-size: 16px;
        margin-bottom: 30px;
        max-width: 820px;
        line-height: 1.6;
    }

    .admin-section-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.035));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.25);
        margin-bottom: 22px;
    }

    .admin-section-title {
        font-size: 26px;
        font-weight: 850;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .admin-section-subtitle {
        font-size: 14px;
        color: #9fb7d3;
        margin-bottom: 0;
    }

    .admin-table-card {
        background: linear-gradient(180deg, rgba(10, 24, 46, 0.95), rgba(5, 15, 30, 0.92));
        border: 1px solid rgba(80, 140, 255, 0.18);
        border-radius: 22px;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 10px 28px rgba(0,0,0,0.28);
    }

    .perf-metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }

    .perf-metric-card {
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 20px;
        padding: 22px 18px 18px;
        position: relative;
        overflow: hidden;
    }

    .perf-metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 20px 20px 0 0;
    }

    .perf-metric-acc::before { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .perf-metric-prec::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .perf-metric-rec::before { background: linear-gradient(90deg, #06b6d4, #38bdf8); }
    .perf-metric-f1::before { background: linear-gradient(90deg, #10b981, #34d399); }

    .perf-metric-label {
        font-size: 11px;
        font-weight: 700;
        color: #7c9bbf;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }

    .perf-metric-value {
        font-size: 32px;
        font-weight: 900;
        letter-spacing: -1px;
        line-height: 1;
    }

    .perf-metric-acc .perf-metric-value { color: #93c5fd; }
    .perf-metric-prec .perf-metric-value { color: #c4b5fd; }
    .perf-metric-rec .perf-metric-value { color: #67e8f9; }
    .perf-metric-f1 .perf-metric-value { color: #6ee7b7; }

    .perf-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 14px;
        font-size: 14px;
    }

    .perf-table th {
        background: rgba(255,255,255,0.06);
        color: #9fb7d3;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 10px 14px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        text-align: left;
    }

    .perf-table th:first-child { border-radius: 10px 0 0 0; }
    .perf-table th:last-child { border-radius: 0 10px 0 0; }

    .perf-table td {
        padding: 11px 14px;
        color: #dbeafe;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-weight: 600;
    }

    .perf-table tr:last-child td { border-bottom: none; }

    .perf-table tr:hover td { background: rgba(255,255,255,0.03); }

    .perf-row-label {
        color: #9fb7d3 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .perf-cell-good {
        color: #86efac !important;
        font-size: 16px !important;
        font-weight: 800 !important;
    }

    .perf-cell-bad {
        color: #fca5a5 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
    }

    .perf-test-note {
        font-size: 12px;
        color: #5a7a9e;
        margin-top: 10px;
        text-align: right;
        font-style: italic;
    }

    .filter-controls-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 18px 6px;
        margin-bottom: 14px;
    }

    .stSlider label {
        color: #dbeafe !important;
        font-weight: 600;
    }

    [data-testid="stSlider"] > div > div {
        background: rgba(255,255,255,0.12) !important;
    }

    [data-testid="stSlider"] > div > div > div[role="slider"] {
        background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
        border: 2px solid #7dd3fc !important;
        box-shadow: 0 0 10px rgba(14,165,233,0.45) !important;
    }

    .checks-count-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
        padding: 0 2px;
    }

    .checks-count-badge {
        background: rgba(14,165,233,0.15);
        border: 1px solid rgba(14,165,233,0.30);
        color: #7dd3fc;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 999px;
    }

    .checks-count-label {
        font-size: 13px;
        color: #5a7a9e;
    }

    .admin-dark-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .admin-dark-table th {
        background: rgba(255,255,255,0.06);
        color: #7c9bbf;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 12px 18px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        text-align: left;
    }

    .admin-dark-table td {
        padding: 12px 18px;
        color: #dbeafe;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .admin-dark-table tr:last-child td { border-bottom: none; }

    .admin-dark-table tr:hover td { background: rgba(255,255,255,0.03); }

    .tbl-id {
        color: #5a7a9e !important;
        font-size: 13px !important;
        width: 70px;
    }

    .tbl-muted { color: #7c9bbf !important; }

    .role-pill-admin {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        background: rgba(139,92,246,0.18);
        border: 1px solid rgba(139,92,246,0.35);
        color: #c4b5fd;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .role-pill-user {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        background: rgba(148,163,184,0.10);
        border: 1px solid rgba(148,163,184,0.22);
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR NAVIGATION
# =========================

user_role = get_user_role()

selected_language = st.sidebar.selectbox(
    "Language / Мова",
    list(TRANSLATIONS.keys()),
    index=list(TRANSLATIONS.keys()).index(st.session_state.language)
)

if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.rerun()

if user_role == "admin":
    navigation_items = ["Admin"]

    if st.session_state.current_page != "Admin":
        st.session_state.current_page = "Admin"
else:
    navigation_items = ["Home", "Auth", "Dashboard", "Check Token", "History", "Favorites"]

    if st.session_state.current_page not in navigation_items:
        st.session_state.current_page = "Home"

menu = st.sidebar.radio(
    tr("navigation"),
    navigation_items,
    index=navigation_items.index(st.session_state.current_page),
    format_func=page_label
)

st.session_state.current_page = menu

if get_user_role() == "admin" and menu != "Admin":
    st.session_state.current_page = "Admin"
    st.rerun()

user_info = get_current_user()

if st.session_state.token and user_info:
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    avatar = user_info["username"][0].upper() if user_info.get("username") else "U"
    st.sidebar.markdown(
        f"""
        <div class="sidebar-user-card">
            <div class="sidebar-user-avatar">{avatar}</div>
            <div>
                <div class="sidebar-user-name">{user_info["username"]}</div>
                <div class="sidebar-user-role">{user_info["role"]}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button(tr("log_out")):
        st.session_state.token = None
        st.session_state.last_prediction = None
        st.session_state.current_page = "Home"
        st.session_state.redirect_after_auth = None
        st.rerun()


# =========================
# HOME PAGE
# =========================

if menu == "Home":
    st.markdown(
        f'<div class="hero-title">{tr("home_title")}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero-subtitle">
            {tr("home_subtitle")}
        </div>
        """,
        unsafe_allow_html=True
    )

    col_btn1, col_btn2, col_empty = st.columns([1.2, 1.2, 5])

    with col_btn1:
        if st.button(tr("check_token_button")):
            if st.session_state.token:
                go_to_page("Check Token")
            else:
                st.session_state.redirect_after_auth = "Check Token"
                go_to_page("Auth")

    with col_btn2:
        if st.button(tr("view_dashboard")):
            if st.session_state.token:
                go_to_page("Dashboard")
            else:
                st.session_state.redirect_after_auth = "Dashboard"
                go_to_page("Auth")

    st.markdown(f'<div class="section-title">{tr("core_features")}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="premium-card">
            <h3>{tr("scam_detection")}</h3>
            <p>
                {tr("scam_detection_text")}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="premium-card">
            <h3>{tr("token_intelligence")}</h3>
            <p>
                {tr("token_intelligence_text")}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="premium-card">
            <h3>{tr("personal_workspace")}</h3>
            <p>
                {tr("personal_workspace_text")}
            </p>
        </div>
        """, unsafe_allow_html=True)


# =========================
# AUTH PAGE
# =========================

elif menu == "Auth":
    st.header(tr("account_access"))

    login_tab, register_tab = st.tabs([tr("login"), tr("register")])

    with login_tab:
        st.subheader(tr("login"))

        with st.form("login_form"):
            login_email = st.text_input(tr("email"), placeholder=tr("enter_email"))
            login_password = st.text_input(tr("password"), type="password", placeholder=tr("enter_password"))
            login_submit = st.form_submit_button(tr("log_in"))

            if login_submit:
                if not login_email or not login_password:
                    st.error(tr("fill_all_fields"))
                else:
                    response = login_user(login_email, login_password)

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data["access_token"]
                        redirect_after_successful_auth()
                        st.success(tr("login_successful"))
                        st.rerun()
                    else:
                        try:
                            st.error(response.json()["detail"])
                        except Exception:
                            st.error(tr("login_failed"))

    with register_tab:
        st.subheader(tr("register"))

        with st.form("register_form"):
            reg_username = st.text_input(tr("username"), placeholder=tr("choose_username"))
            reg_email = st.text_input(tr("email"), placeholder=tr("enter_email"), key="reg_email")
            reg_password = st.text_input(tr("password"), type="password", placeholder=tr("create_password"), key="reg_password")
            reg_confirm = st.text_input(tr("confirm_password"), type="password", placeholder=tr("repeat_password"))
            reg_submit = st.form_submit_button(tr("create_account"))

            if reg_submit:
                if not reg_username or not reg_email or not reg_password or not reg_confirm:
                    st.error(tr("fill_all_fields"))
                elif reg_password != reg_confirm:
                    st.error(tr("passwords_not_match"))
                else:
                    response = register_user(reg_username, reg_email, reg_password)

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data["access_token"]
                        redirect_after_successful_auth()
                        st.success(tr("registration_successful"))
                        st.rerun()
                    else:
                        try:
                            st.error(response.json()["detail"])
                        except Exception:
                            st.error(tr("registration_failed"))


# =========================
# DASHBOARD PAGE
# =========================

elif menu == "Dashboard":
    st.header(tr("dashboard"))

    if not st.session_state.token:
        st.warning(tr("please_log_in"))
    else:
        response = requests.get(
            f"{API_URL}/checks/",
            headers=auth_headers()
        )

        if response.status_code == 200:
            history = response.json().get("items", [])

            if not history:
                st.info(tr("no_checks"))
            else:
                df = pd.DataFrame(history)

                df["created_at"] = pd.to_datetime(df["created_at"])
                df = df.sort_values("created_at").reset_index(drop=True)
                df["Check #"] = range(1, len(df) + 1)

                total_checks = len(df)
                scam_count = (df["prediction"] == "SCAM").sum()
                legit_count = (df["prediction"] == "LEGIT").sum()
                avg_risk = round(df["risk_score"].mean(), 2)
                high_risk_count = (df["risk_score"] >= 70).sum()

                st.markdown(f"### {tr('platform_summary')}")

                col1, col2, col3, col4, col5 = st.columns(5)

                col1.metric(tr("total_checks"), total_checks)
                col2.metric(tr("legit"), legit_count)
                col3.metric(tr("scam"), scam_count)
                col4.metric(tr("avg_risk"), avg_risk)
                col5.metric(tr("high_risk"), high_risk_count)

                st.markdown("<br>", unsafe_allow_html=True)

                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.markdown(
                        f"""
                        <div class="chart-card">
                            <div class="chart-title">{tr("risk_score_trend")}</div>
                            <div class="chart-subtitle">
                                {tr("risk_score_trend_text")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    fig_line = go.Figure()

                    fig_line.add_trace(
                        go.Scatter(
                            x=df["Check #"],
                            y=df["risk_score"],
                            mode="lines+markers",
                            name=tr("risk_score"),
                            line=dict(color="#38bdf8", width=4),
                            marker=dict(size=8, color="#0ea5e9"),
                            fill="tozeroy",
                            fillcolor="rgba(56, 189, 248, 0.12)",
                            hovertemplate=f"<b>{tr('check_number')} #%{{x}}</b><br>{tr('risk_score')}: %{{y}}<extra></extra>"
                        )
                    )

                    fig_line.update_layout(
                        height=420,
                        margin=dict(l=20, r=20, t=10, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(255,255,255,0.02)",
                        font=dict(color="#e5eef9"),
                        xaxis=dict(
                            title=tr("check_number"),
                            showgrid=False,
                            zeroline=False,
                            tickfont=dict(color="#b6c7dc")
                        ),
                        yaxis=dict(
                            title=tr("risk_score"),
                            range=[0, 100],
                            gridcolor="rgba(255,255,255,0.08)",
                            zeroline=False,
                            tickfont=dict(color="#b6c7dc")
                        ),
                        showlegend=False
                    )

                    st.plotly_chart(fig_line, use_container_width=True)

                with chart_col2:
                    st.markdown(
                        f"""
                        <div class="chart-card">
                            <div class="chart-title">{tr("prediction_distribution")}</div>
                            <div class="chart-subtitle">
                                {tr("prediction_distribution_text")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    prediction_counts = df["prediction"].value_counts().reset_index()
                    prediction_counts.columns = ["Prediction", "Count"]

                    fig_donut = px.pie(
                        prediction_counts,
                        names="Prediction",
                        values="Count",
                        hole=0.62,
                        color="Prediction",
                        color_discrete_map={
                            "LEGIT": "#22c55e",
                            "SCAM": "#ef4444"
                        }
                    )

                    fig_donut.update_traces(
                        textinfo="percent+label",
                        textfont_size=14,
                        marker=dict(
                            line=dict(
                                color="rgba(255,255,255,0.08)",
                                width=2
                            )
                        ),
                        hovertemplate=f"<b>%{{label}}</b><br>{tr('count')}: %{{value}}<br>{tr('share')}: %{{percent}}<extra></extra>"
                    )

                    fig_donut.update_layout(
                        height=420,
                        margin=dict(l=20, r=20, t=10, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e5eef9"),
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.15,
                            xanchor="center",
                            x=0.5,
                            font=dict(color="#dbeafe")
                        )
                    )

                    st.plotly_chart(fig_donut, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="chart-card">
                        <div class="chart-title">{tr("recent_checks")}</div>
                        <div class="chart-subtitle">
                            {tr("recent_checks_text")}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                recent_df = df.sort_values("created_at", ascending=False).head(10).copy()

                for index, row in recent_df.iterrows():
                    name = row.get("name", "Unknown")
                    url = row.get("url", "")
                    slug = row.get("slug", "N/A")
                    prediction = row.get("prediction", "N/A")

                    icon_url = get_token_icon(name, slug, prediction)

                    col1, col2, col3, col4 = st.columns([0.7, 4, 2, 1.2])

                    with col1:
                        if icon_url:
                            st.image(icon_url, width=38)
                        else:
                            st.markdown("## 🚨" if prediction == "SCAM" else "## 🪙")

                    with col2:
                        st.markdown(
                            f'<div class="recent-token-name">{name}</div>',
                            unsafe_allow_html=True
                        )

                    with col3:
                        if prediction == "LEGIT":
                            st.markdown(
                                '<div class="status-pill-legit">LEGIT</div>',
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                '<div class="status-pill-scam">SCAM</div>',
                                unsafe_allow_html=True
                            )

                    with col4:
                        if st.button(tr("open"), key=f"open_dashboard_recent_{index}"):
                            st.session_state.prefill_token_name = name
                            st.session_state.prefill_token_url = url
                            st.session_state.last_prediction = None
                            st.session_state.auto_analyze_token = True
                            go_to_page("Check Token")

                    st.markdown('<div class="simple-divider"></div>', unsafe_allow_html=True)

        else:
            try:
                st.error(response.json().get("detail", tr("failed_load_dashboard")))
            except Exception:
                st.error(tr("failed_load_dashboard"))


# =========================
# CHECK TOKEN PAGE
# =========================

elif menu == "Check Token":
    st.header(tr("check_token"))

    if not st.session_state.token:
        st.warning(tr("please_log_in"))
    else:
        token_name = st.text_input(
            tr("token_name"),
            value=st.session_state.prefill_token_name
        )

        token_url = st.text_input(
            tr("token_url"),
            value=st.session_state.prefill_token_url
        )

        analyze_clicked = st.button(tr("analyze"))

        if analyze_clicked or st.session_state.auto_analyze_token:
            st.session_state.auto_analyze_token = False
            st.session_state.prefill_token_name = token_name
            st.session_state.prefill_token_url = token_url

            with st.spinner("Analyzing token..."):
                response = requests.post(
                    f"{API_URL}/predict/",
                    headers=auth_headers(),
                    json={
                        "name": token_name,
                        "url": token_url
                    }
                )

            if response.status_code == 200:
                st.session_state.last_prediction = response.json()
            else:
                try:
                    st.error(response.json().get("detail", tr("prediction_failed")))
                except Exception:
                    st.error(tr("prediction_failed"))

        if st.session_state.last_prediction:
            result = st.session_state.last_prediction

            st.subheader(tr("result"))

            col1, col2, col3 = st.columns(3)
            col1.metric(tr("prediction"), result["prediction"])
            col2.metric(tr("risk_score"), result["risk_score"])
            col3.metric(tr("probability"), result["probability"])

            st.info(result["explanation"])

            market_data = result.get("market_data")

            if result["prediction"] == "SCAM":
                st.warning(
                    tr("market_data_hidden")
                )

            elif market_data:
                st.divider()
                st.subheader(tr("token_information"))

                info_col1, info_col2 = st.columns([1, 4])

                with info_col1:
                    if market_data.get("image"):
                        st.image(market_data["image"], width=90)

                with info_col2:
                    st.markdown(
                        f"### {market_data.get('name', tr('unknown'))} "
                        f"({market_data.get('symbol', 'N/A')})"
                    )

                    if market_data.get("market_cap_rank"):
                        st.caption(tr("market_cap_rank", rank=market_data["market_cap_rank"]))

                    if market_data.get("homepage"):
                        st.markdown(f"[{tr('official_website')}]({market_data['homepage']})")

                if market_data.get("description"):
                    st.markdown(f"#### {tr('description')}")
                    st.write(market_data["description"])

                st.markdown(f"#### {tr('market_statistics')}")

                stat1, stat2, stat3, stat4 = st.columns(4)

                price = market_data.get("current_price_usd")
                market_cap = market_data.get("market_cap_usd")
                volume = market_data.get("volume_24h_usd")
                change = market_data.get("price_change_24h_percent")

                stat1.metric(
                    tr("price"),
                    format_money(price, 4) if price is not None else "N/A"
                )

                stat2.metric(
                    tr("market_cap"),
                    format_large_money(market_cap) if market_cap is not None else "N/A"
                )

                stat3.metric(
                    tr("volume_24h"),
                    format_large_money(volume) if volume is not None else "N/A"
                )

                stat4.metric(
                    tr("change_24h"),
                    f"{change:.2f}%" if change is not None else "N/A"
                )

                chart_data = market_data.get("chart_7d")

                if chart_data:
                    st.markdown(f"#### {tr('price_chart_7d')}")

                    chart_df = pd.DataFrame(chart_data)
                    chart_df["datetime"] = pd.to_datetime(chart_df["timestamp"], unit="ms")
                    chart_df = chart_df.sort_values("datetime")

                    min_price = chart_df["price"].min()
                    max_price = chart_df["price"].max()

                    if min_price == max_price:
                        y_min = min_price * 0.995
                        y_max = max_price * 1.005
                    else:
                        padding = (max_price - min_price) * 0.15
                        y_min = min_price - padding
                        y_max = max_price + padding

                    fig_price = go.Figure()

                    fig_price.add_trace(
                        go.Scatter(
                            x=chart_df["datetime"],
                            y=chart_df["price"],
                            mode="lines",
                            name=tr("price"),
                            line=dict(color="#38bdf8", width=4),
                            fill="tozeroy",
                            fillcolor="rgba(56, 189, 248, 0.12)",
                            hovertemplate=f"<b>%{{x}}</b><br>{tr('price')}: $%{{y:.6f}}<extra></extra>"
                        )
                    )

                    fig_price.update_layout(
                        height=420,
                        margin=dict(l=20, r=20, t=20, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(255,255,255,0.02)",
                        font=dict(color="#e5eef9"),
                        xaxis=dict(
                            title=tr("date"),
                            showgrid=False,
                            zeroline=False,
                            tickfont=dict(color="#b6c7dc")
                        ),
                        yaxis=dict(
                            title=tr("price_usd"),
                            range=[y_min, y_max],
                            gridcolor="rgba(255,255,255,0.08)",
                            zeroline=False,
                            tickfont=dict(color="#b6c7dc")
                        ),
                        showlegend=False
                    )

                    st.plotly_chart(fig_price, use_container_width=True)

            else:
                st.warning(
                    tr("no_market_data")
                )

            if "token_id" in result:
                if st.button(tr("add_to_favorites")):
                    fav_response = requests.post(
                        f"{API_URL}/favorites/{result['token_id']}",
                        headers=auth_headers()
                    )

                    if fav_response.status_code == 200:
                        st.success(tr("added_to_favorites"))
                    else:
                        try:
                            st.error(fav_response.json().get("detail", tr("failed_add_favorite")))
                        except Exception:
                            st.error(tr("failed_add_favorite"))


# =========================
# HISTORY PAGE
# =========================

elif menu == "History":
    st.header(tr("prediction_history"))

    if not st.session_state.token:
        st.warning(tr("please_log_in"))
    else:
        response = requests.get(
            f"{API_URL}/checks/",
            headers=auth_headers()
        )

        if response.status_code == 200:
            history = response.json().get("items", [])

            if not history:
                st.info(tr("no_checks"))
            else:
                df = pd.DataFrame(history)

                columns_to_show = [
                    "name",
                    "url",
                    "slug",
                    "prediction",
                    "risk_score",
                    "probability",
                    "explanation",
                ]

                available_columns = [col for col in columns_to_show if col in df.columns]
                df = df[available_columns]

                st.markdown(f"### {tr('recent_token_checks')}")

                for index, row in df.iterrows():
                    name = row.get("name", tr("unknown"))
                    url = row.get("url", "")
                    slug = row.get("slug", "N/A")
                    prediction = row.get("prediction", "N/A")
                    risk_score = row.get("risk_score", 0)
                    probability = row.get("probability", 0)
                    explanation = row.get("explanation", tr("no_explanation"))

                    icon_url = get_token_icon(name, slug, prediction)

                    card_col1, card_col2, card_col3, card_col4 = st.columns(
                        [0.7, 2.3, 3.2, 1.4]
                    )

                    with card_col1:
                        if icon_url:
                            st.image(icon_url, width=44)
                        else:
                            st.markdown("## 🚨" if prediction == "SCAM" else "## 🪙")

                    with card_col2:
                        st.markdown(
                            f'<div class="history-name">{name}</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f'<div class="history-meta">{tr("slug")}: {slug}</div>',
                            unsafe_allow_html=True
                        )

                        if url:
                            st.markdown(
                                f'<div class="history-link"><a href="{url}" target="_blank">{tr("open_link")}</a></div>',
                                unsafe_allow_html=True
                            )

                    with card_col3:
                        if prediction == "SCAM":
                            st.error(f"{tr('prediction')}: {prediction}")
                        elif prediction == "LEGIT":
                            st.success(f"{tr('prediction')}: {prediction}")
                        else:
                            st.info(f"{tr('prediction')}: {prediction}")

                        st.markdown(
                            f'<div class="history-explanation">{explanation}</div>',
                            unsafe_allow_html=True
                        )

                    with card_col4:
                        try:
                            probability_value = round(float(probability), 4)
                        except Exception:
                            probability_value = probability

                        st.metric(tr("risk_score"), risk_score)
                        st.metric(tr("probability"), probability_value)

                        if st.button(tr("open"), key=f"open_history_{index}"):
                            st.session_state.prefill_token_name = name
                            st.session_state.prefill_token_url = url
                            st.session_state.last_prediction = None
                            st.session_state.auto_analyze_token = True
                            go_to_page("Check Token")

                    st.markdown('<div class="simple-divider"></div>', unsafe_allow_html=True)

        else:
            try:
                st.error(response.json().get("detail", tr("failed_load_history")))
            except Exception:
                st.error(tr("failed_load_history"))


# =========================
# FAVORITES PAGE
# =========================

elif menu == "Favorites":
    st.header(tr("favorite_tokens"))

    if not st.session_state.token:
        st.warning(tr("please_log_in"))
    else:
        response = requests.get(
            f"{API_URL}/favorites/",
            headers=auth_headers()
        )

        if response.status_code == 200:
            favorites = response.json().get("items", [])

            if not favorites:
                st.info(tr("no_favorites"))
            else:
                df = pd.DataFrame(favorites)

                st.subheader(tr("saved_tokens"))

                for index, row in df.iterrows():
                    name = row.get("name", tr("unknown"))
                    url = row.get("url", "")
                    slug = row.get("slug", "N/A")

                    icon_url = get_token_icon(name, slug, "LEGIT")

                    col1, col2, col3 = st.columns([0.7, 4, 1])

                    with col1:
                        if icon_url:
                            st.image(icon_url, width=44)
                        else:
                            st.markdown("## ⭐")

                    with col2:
                        st.markdown(
                            f'<div class="favorite-name">{name}</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f'<div class="favorite-meta">{tr("slug")}: {slug}</div>',
                            unsafe_allow_html=True
                        )
                        if url:
                            st.markdown(
                                f'<div class="favorite-link"><a href="{url}" target="_blank">{tr("open_link")}</a></div>',
                                unsafe_allow_html=True
                            )

                    with col3:
                        if st.button(tr("open"), key=f"open_favorite_{index}"):
                            st.session_state.prefill_token_name = name
                            st.session_state.prefill_token_url = url
                            st.session_state.last_prediction = None
                            st.session_state.auto_analyze_token = True
                            go_to_page("Check Token")

                    st.markdown('<div class="simple-divider"></div>', unsafe_allow_html=True)

        else:
            try:
                st.error(response.json().get("detail", tr("failed_load_favorites")))
            except Exception:
                st.error(tr("failed_load_favorites"))


# =========================
# ADMIN PAGE
# =========================

elif menu == "Admin":
    if not st.session_state.token:
        st.warning(tr("please_log_in"))
    elif get_user_role() != "admin":
        st.error(tr("admin_access_required"))
    else:
        headers = auth_headers()

        stats_response = requests.get(f"{API_URL}/admin/stats", headers=headers)
        users_response = requests.get(f"{API_URL}/admin/users", headers=headers)
        checks_response = requests.get(f"{API_URL}/admin/checks", headers=headers)

        if (
            stats_response.status_code != 200
            or users_response.status_code != 200
            or checks_response.status_code != 200
        ):
            st.error(tr("failed_load_admin"))
            st.stop()

        stats = stats_response.json()
        users = users_response.json().get("items", [])
        checks = checks_response.json().get("items", [])

        st.markdown(
            f"""
            <div class="admin-title">{tr("admin_dashboard")}</div>
            <div class="admin-subtitle">
                {tr("admin_subtitle")}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="admin-section-card">
                <div class="admin-section-title">{tr("platform_overview")}</div>
                <div class="admin-section-subtitle">
                    {tr("platform_overview_text")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(tr("users"), stats["total_users"])
        col2.metric(tr("checks"), stats["total_checks"])
        col3.metric(tr("scam_checks"), stats["scam_checks"])
        col4.metric(tr("scam_rate"), f"{stats['scam_rate']}%")

        st.markdown("<br>", unsafe_allow_html=True)

        checks_df = pd.DataFrame(checks)
        users_df = pd.DataFrame(users)

        if not checks_df.empty:
            checks_df["created_at"] = pd.to_datetime(checks_df["created_at"])
            checks_df = checks_df.sort_values("created_at")
            checks_df["Check #"] = range(1, len(checks_df) + 1)

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown(
                    f"""
                    <div class="chart-card">
                        <div class="chart-title">{tr("scam_vs_legit")}</div>
                        <div class="chart-subtitle">
                            {tr("scam_vs_legit_text")}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                prediction_counts = checks_df["prediction_label"].value_counts().reset_index()
                prediction_counts.columns = ["Prediction", "Count"]

                fig_admin_bar = px.bar(
                    prediction_counts,
                    x="Prediction",
                    y="Count",
                    color="Prediction",
                    color_discrete_map={
                        "LEGIT": "#22c55e",
                        "SCAM": "#ef4444"
                    },
                    text="Count"
                )

                fig_admin_bar.update_traces(
                    textposition="outside",
                    marker_line_width=0,
                    hovertemplate=f"<b>%{{x}}</b><br>{tr('checks')}: %{{y}}<extra></extra>"
                )

                fig_admin_bar.update_layout(
                    height=420,
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(255,255,255,0.02)",
                    font=dict(color="#e5eef9"),
                    xaxis=dict(
                        title=tr("prediction"),
                        showgrid=False,
                        zeroline=False,
                        tickfont=dict(color="#b6c7dc")
                    ),
                    yaxis=dict(
                        title=tr("number_of_checks"),
                        gridcolor="rgba(255,255,255,0.08)",
                        zeroline=False,
                        tickfont=dict(color="#b6c7dc")
                    ),
                    showlegend=False
                )

                st.plotly_chart(fig_admin_bar, use_container_width=True)

            with chart_col2:
                st.markdown(
                    f"""
                    <div class="chart-card">
                        <div class="chart-title">{tr("risk_score_trend")}</div>
                        <div class="chart-subtitle">
                            {tr("risk_score_admin_text")}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                fig_admin_line = go.Figure()

                fig_admin_line.add_trace(
                    go.Scatter(
                            x=checks_df["Check #"],
                            y=checks_df["risk_score"],
                            mode="lines+markers",
                            name=tr("risk_score"),
                        line=dict(color="#38bdf8", width=4),
                        marker=dict(size=7, color="#0ea5e9"),
                        fill="tozeroy",
                        fillcolor="rgba(56, 189, 248, 0.12)",
                            hovertemplate=f"<b>{tr('check_number')} #%{{x}}</b><br>{tr('risk_score')}: %{{y}}<extra></extra>"
                        )
                    )

                fig_admin_line.update_layout(
                    height=420,
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(255,255,255,0.02)",
                    font=dict(color="#e5eef9"),
                        xaxis=dict(
                            title=tr("check_number"),
                        showgrid=False,
                        zeroline=False,
                        tickfont=dict(color="#b6c7dc")
                    ),
                        yaxis=dict(
                            title=tr("risk_score"),
                        range=[0, 100],
                        gridcolor="rgba(255,255,255,0.08)",
                        zeroline=False,
                        tickfont=dict(color="#b6c7dc")
                    ),
                    showlegend=False
                )

                st.plotly_chart(fig_admin_line, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="admin-section-card">
                    <div class="admin-section-title">{tr("filter_checks")}</div>
                    <div class="admin-section-subtitle">{tr("filter_checks_text")}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown('<div class="filter-controls-card">', unsafe_allow_html=True)
            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                prediction_filter = st.selectbox(
                    tr("prediction"),
                    ["All", "SCAM", "LEGIT"],
                    format_func=lambda value: tr("all") if value == "All" else value
                )

            with filter_col2:
                min_risk = st.slider(
                    tr("minimum_risk_score"),
                    0,
                    100,
                    0
                )
            st.markdown('</div>', unsafe_allow_html=True)

            filtered_df = checks_df.copy()

            if prediction_filter != "All":
                filtered_df = filtered_df[
                    filtered_df["prediction_label"] == prediction_filter
                ]

            filtered_df = filtered_df[
                filtered_df["risk_score"] >= min_risk
            ]

            display_checks = filtered_df[
                [
                    "id",
                    "user_id",
                    "token_id",
                    "prediction_label",
                    "risk_score",
                    "probability",
                    "created_at",
                    "explanation",
                ]
            ].copy()

            display_checks["created_at"] = display_checks["created_at"].dt.strftime("%Y-%m-%d %H:%M")

            st.markdown(
                f"""
                <div class="checks-count-row">
                    <span class="checks-count-badge">{len(filtered_df)}</span>
                    <span class="checks-count-label">records</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if display_checks.empty:
                st.info(tr("no_checks_found"))
            else:
                rows_html = ""
                for _, row in display_checks.iterrows():
                    label = str(row.get("prediction_label", ""))
                    label_pill = (
                        '<span class="status-pill-legit" style="font-size:11px;padding:3px 10px">LEGIT</span>'
                        if label == "LEGIT"
                        else '<span class="status-pill-scam" style="font-size:11px;padding:3px 10px">SCAM</span>'
                    )
                    risk = float(row.get("risk_score", 0))
                    risk_color = "#fca5a5" if risk >= 60 else ("#fcd34d" if risk >= 30 else "#86efac")
                    prob_pct = f"{float(row.get('probability', 0)) * 100:.1f}%"

                    rows_html += f"""
                    <tr>
                        <td class="tbl-id">#{int(row['id'])}</td>
                        <td class="tbl-muted">{int(row['user_id'])}</td>
                        <td class="tbl-muted">{int(row['token_id'])}</td>
                        <td>{label_pill}</td>
                        <td style="color:{risk_color};font-weight:700">{risk:.2f}</td>
                        <td class="tbl-muted">{prob_pct}</td>
                        <td class="tbl-muted">{row['created_at']}</td>
                        <td style="color:#c7d7e8;font-size:13px">{row['explanation']}</td>
                    </tr>
                    """

                st.markdown(
                    f"""
                    <div class="admin-table-card">
                        <table class="admin-dark-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>User</th>
                                    <th>Token</th>
                                    <th>Prediction</th>
                                    <th>Risk Score</th>
                                    <th>Probability</th>
                                    <th>Date</th>
                                    <th>Explanation</th>
                                </tr>
                            </thead>
                            <tbody>{rows_html}</tbody>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.info(tr("no_checks_found"))

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="admin-section-card">
                <div class="admin-section-title">{tr("users")}</div>
                <div class="admin-section-subtitle">{tr("registered_users")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not users_df.empty:
            rows_html = ""
            for _, row in users_df.iterrows():
                role = str(row.get("role", "user"))
                role_pill = (
                    f'<span class="role-pill-admin">{role}</span>'
                    if role == "admin"
                    else f'<span class="role-pill-user">{role}</span>'
                )
                rows_html += f"""
                <tr>
                    <td class="tbl-id">#{int(row['id'])}</td>
                    <td>{row['email']}</td>
                    <td>{role_pill}</td>
                </tr>
                """

            st.markdown(
                f"""
                <div class="admin-table-card">
                    <table class="admin-dark-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Email</th>
                                <th>Role</th>
                            </tr>
                        </thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info(tr("no_users_found"))

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="admin-section-card">
                <div class="admin-section-title">{tr("model_performance")}</div>
                <div class="admin-section-subtitle">{tr("model_performance_text")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        metrics_response = requests.get(f"{API_URL}/admin/model-metrics", headers=headers)

        if metrics_response.status_code == 200:
            m = metrics_response.json()

            cm = m["confusion_matrix"]
            tn, fp_val = cm[0][0], cm[0][1]
            fn_val, tp = cm[1][0], cm[1][1]
            cr = m["class_report"]

            st.markdown(f"""
            <div class="perf-metric-grid">
                <div class="perf-metric-card perf-metric-acc">
                    <div class="perf-metric-label">{tr("accuracy")}</div>
                    <div class="perf-metric-value">{m['accuracy'] * 100:.2f}%</div>
                </div>
                <div class="perf-metric-card perf-metric-prec">
                    <div class="perf-metric-label">{tr("precision")}</div>
                    <div class="perf-metric-value">{m['precision'] * 100:.2f}%</div>
                </div>
                <div class="perf-metric-card perf-metric-rec">
                    <div class="perf-metric-label">{tr("recall")}</div>
                    <div class="perf-metric-value">{m['recall'] * 100:.2f}%</div>
                </div>
                <div class="perf-metric-card perf-metric-f1">
                    <div class="perf-metric-label">{tr("f1_score")}</div>
                    <div class="perf-metric-value">{m['f1_score'] * 100:.2f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown(f"""
                <div class="chart-card">
                    <div class="chart-title">{tr("confusion_matrix")}</div>
                    <table class="perf-table">
                        <thead>
                            <tr>
                                <th></th>
                                <th>Pred LEGIT</th>
                                <th>Pred SCAM</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="perf-row-label">True LEGIT</td>
                                <td class="perf-cell-good">{tn}</td>
                                <td class="perf-cell-bad">{fp_val}</td>
                            </tr>
                            <tr>
                                <td class="perf-row-label">True SCAM</td>
                                <td class="perf-cell-bad">{fn_val}</td>
                                <td class="perf-cell-good">{tp}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="chart-card" style="margin-top: 16px">
                    <div class="chart-title">{tr("per_class_report")}</div>
                    <table class="perf-table">
                        <thead>
                            <tr>
                                <th>Class</th>
                                <th>Precision</th>
                                <th>Recall</th>
                                <th>F1</th>
                                <th>{tr("support")}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span class="status-pill-legit" style="font-size:12px;padding:4px 10px">LEGIT</span></td>
                                <td>{cr["legit"]["precision"] * 100:.2f}%</td>
                                <td>{cr["legit"]["recall"] * 100:.2f}%</td>
                                <td>{cr["legit"]["f1"] * 100:.2f}%</td>
                                <td>{cr["legit"]["support"]}</td>
                            </tr>
                            <tr>
                                <td><span class="status-pill-scam" style="font-size:12px;padding:4px 10px">SCAM</span></td>
                                <td>{cr["scam"]["precision"] * 100:.2f}%</td>
                                <td>{cr["scam"]["recall"] * 100:.2f}%</td>
                                <td>{cr["scam"]["f1"] * 100:.2f}%</td>
                                <td>{cr["scam"]["support"]}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="perf-test-note">Test set: {m['test_size']} samples</div>
                </div>
                """, unsafe_allow_html=True)

            with chart_col2:
                if m.get("probability_distribution"):
                    pd_data = m["probability_distribution"]
                    st.markdown(f"""
                    <div class="chart-card" style="padding-bottom: 4px">
                        <div class="chart-title">{tr("prob_distribution")}</div>
                        <div class="chart-subtitle">{tr("prob_distribution_text")}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    fig_prob = px.bar(
                        x=pd_data["labels"],
                        y=pd_data["values"],
                        labels={"x": "P(scam)", "y": tr("count")},
                        color=pd_data["values"],
                        color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"],
                    )
                    fig_prob.update_layout(
                        height=380,
                        margin=dict(l=20, r=20, t=10, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(255,255,255,0.02)",
                        font=dict(color="#e5eef9"),
                        coloraxis_showscale=False,
                        xaxis=dict(showgrid=False, tickfont=dict(color="#b6c7dc")),
                        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#b6c7dc")),
                    )
                    fig_prob.update_traces(marker_line_width=0)
                    st.plotly_chart(fig_prob, use_container_width=True)

        elif metrics_response.status_code == 404:
            st.info(tr("dataset_missing"))
        else:
            st.error(tr("failed_load_admin"))
