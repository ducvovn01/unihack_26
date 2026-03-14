import streamlit as st


def load_css():
    st.markdown("""
    <style>
        :root {
            --app-bg: var(--background-color);
            --app-text: var(--text-color);
            --muted-text: rgba(128, 128, 128, 0.95);
            --card-bg: rgba(255, 255, 255, 0.04);
            --border-color: rgba(128, 128, 128, 0.22);
            --soft-bg: rgba(128, 128, 128, 0.08);
            --hero-badge-bg: rgba(16, 185, 129, 0.14);
            --hero-badge-text: #10b981;
            --footer-bg: rgba(128, 128, 128, 0.06);
        }

        .main {
            padding-top: 0rem;
        }

        .block-container {
            padding-top: 0rem;
            padding-bottom: 1.5rem;
            max-width: 100% !important;
        }

        section[data-testid="stSidebar"] {
            width: 260px !important;
            min-width: 260px !important;
            border-right: 1px solid var(--border-color);
        }

        .stSidebar > div:first-child {
            width: 260px !important;
        }

        .header-wrap {
            width: 100%;
            margin-top: 55px;
            margin-bottom: 26px;
        }

        .navbar {
            background: linear-gradient(90deg, #CE273D);
            padding: 22px 34px;
            color: white;
            border-radius: 0 0 16px 16px;
            margin-top: 0;
        }

        .navbar-title {
            font-size: 35px;
            font-weight: 700;
            margin: 0;
            line-height: 1.2;
        }

        .navbar-subtitle {
            font-size: 16px;
            color: #FFFFFF;
            margin-top: 6px;
        }

        .section-title {
            font-size: 30px;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 12px;
            color: var(--app-text);
        }

        .section-text {
            font-size: 16px;
            color: var(--muted-text);
            margin-bottom: 22px;
        }

        .small-badge {
            display: inline-block;
            background: var(--hero-badge-bg);
            color: var(--hero-badge-text);
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 14px;
        }

        .hero-title {
            font-size: 42px;
            font-weight: 800;
            line-height: 1.1;
            color: var(--app-text);
            margin-bottom: 10px;
        }

        .hero-text {
            font-size: 18px;
            color: var(--muted-text);
            max-width: 700px;
        }

        .footer {
            margin-top: 40px;
            padding: 24px 30px 18px 30px;
            text-align: center;
            color: var(--muted-text);
            font-size: 14px;
            border-top: 1px solid var(--border-color);
            background: var(--footer-bg);
            border-radius: 12px 12px 0 0;
        }

        div[data-testid="stChatMessage"] {
            padding-top: 0.35rem;
            padding-bottom: 0.35rem;
        }

        div[data-testid="stVerticalBlock"] div[data-testid="stContainer"] {
            border-color: var(--border-color) !important;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            border-color: var(--border-color) !important;
        }

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: inherit;
        }
    </style>
    """, unsafe_allow_html=True)