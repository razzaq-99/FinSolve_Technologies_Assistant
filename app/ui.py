# fin_solve_streamlit_ui.py
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import base64

API_URL = "http://localhost:8000"

st.set_page_config(page_title="FinSolve Data Assistant", page_icon="🤖", layout="wide")

# -------------------------
# BACKGROUND IMAGES
# -------------------------
def set_bg_from_local(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
    except Exception:
        encoded = None

    if encoded:
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# adjust path if needed; keep your existing background file
set_bg_from_local("../static/images/background.jpg")

# -------------------------
# APP CSS (Polished UI)
# -------------------------
st.markdown(
    """
    # <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
    :root{
        --accent:#3b82f6;
        --muted:#6b7280;
        --card-bg: rgba(255,255,255,0.85);
        --glass: rgba(255,255,255,0.6);
        --glass-strong: rgba(255,255,255,0.9);
        --shadow: 0 8px 24px rgba(15,23,42,0.12);
        --radius: 14px;
    }
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Header card */
    .header-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(250,250,250,0.9));
        border-radius: var(--radius);
        padding: 28px 34px;
        box-shadow: var(--shadow);
        border: 1px solid rgba(15,23,42,0.04);
        margin-bottom: 18px;
    }
    .header-title {
        margin: 0;
        font-size: 34px;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: 0.2px;
    }
    .header-sub {
        margin: 4px 0 0 0;
        color: var(--muted);
        font-size: 14px;
    }

    /* Glass panel */
    .glass {
        background: linear-gradient(180deg, rgba(255,255,255,0.7), rgba(255,255,255,0.55));
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(2,6,23,0.08);
        border: 1px solid rgba(255,255,255,0.4);
    }

    /* Controls spacing */
    .controls {
        padding-top: 8px;
    }

    /* Streamlit input/button overrides */
    .stTextInput > label, .stFileUploader > label, .stSelectbox > label {
        color: #0f172a;
        font-weight: 600;
    }
    input[type="text"], input[type="password"], textarea {
        border-radius: 10px !important;
        padding: 12px 14px !important;
        border: 1px solid rgba(15,23,42,0.08) !important;
        box-shadow: none !important;
        background: rgba(250,250,250,0.9) !important;
    }
    /* Big primary button style */
    .stButton>button {
        background: linear-gradient(90deg, var(--accent), #2563eb) !important;
        color: white !important;
        border: none !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 18px rgba(37,99,235,0.18);
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        transition: all 120ms ease-in-out;
    }

    /* Small secondary button (logout) */
    .small-btn .stButton>button {
        background: transparent !important;
        color: #0f172a !important;
        border: 1px solid rgba(15,23,42,0.06) !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        font-weight: 600 !important;
    }

    /* Right column user card */
    .user-card {
        border-radius: 10px;
        padding: 12px;
        background: rgba(255,255,255,0.7);
        border: 1px solid rgba(15,23,42,0.04);
    }
    .muted {
        color: var(--muted);
        font-size: 13px;
    }
    .role-pill {
        display:inline-block;
        padding:6px 10px;
        background: rgba(59,130,246,0.12);
        color: #0b63d6;
        border-radius: 999px;
        font-weight:600;
        font-size:12px;
    }

    /* Tabs nicer spacing */
    .stTabs [role="tablist"] button {
        border-radius: 10px !important;
        border: 1px solid rgba(15,23,42,0.06) !important;
        padding: 8px 12px !important;
        font-weight: 600 !important;
    }

    /* Answer box */
    .answer {
        background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(250,250,250,0.9));
        border-radius: 10px;
        padding: 14px;
        border: 1px solid rgba(15,23,42,0.04);
    }

    /* Responsive tweaks */
    @media (max-width: 900px) {
        .header-title { font-size: 26px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# SESSION INIT (unchanged functionality)
# -------------------------
if "auth" not in st.session_state:
    st.session_state.auth = None
if "role" not in st.session_state:
    st.session_state.role = None
if "page" not in st.session_state:
    st.session_state.page = "login"

# Load roles into session state if not present
def fetch_roles():
    try:
        role_res = requests.get(f"{API_URL}/roles", auth=HTTPBasicAuth(*st.session_state.auth))
        return role_res.json().get("roles", [])
    except Exception:
        return []

# -------------------------
# LAYOUT - header + two columns
# -------------------------
left_col, right_col = st.columns([7, 1])

with left_col:
    st.markdown(
        """
        <div class="header-card">
            <h1 class="header-title">Welcome to FinSight</h1>
            <p class="header-sub">Your Document Assistant to get insights about Finsolve Technologies.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    # Right column will show login/user info, placed inside a glass card
    if st.session_state.page != "main":
        st.markdown(
            """
            <div class="user-card glass">
                <div style="display:flex;align-items:center;gap:10px">
                    <div style="width:44px;height:44px;border-radius:10px;background:linear-gradient(90deg,var(--accent),#2563eb);display:flex;align-items:center;justify-content:center;color:white;font-weight:800">FS</div>
                    <div>
                        <div style="font-weight:700">FinSight</div>
                        <div class="muted">Document Assistant</div>
                    </div>
                </div>
                <div style="margin-top:12px" class="muted">Please login to continue</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # show user info and logout button
        username = st.session_state.get("username", "")
        role = st.session_state.get("role", "")
        st.markdown(
            f"""
            <div class="user-card">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <div style="font-weight:700">{username}</div>
                        <div class="muted">Signed in</div>
                    </div>
                    <div style="text-align:right">
                        <div class="role-pill">{role}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # logout small button
        if st.button("Logout", key="logout_small"):
            st.session_state.auth = None
            st.session_state.role = None
            st.session_state.page = "login"
            st.rerun()


# -------------------------
# LOGIN PAGE (functionality preserved)
# -------------------------
if st.session_state.page == "login":
    # nice glass container for the form
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Login", key="login_btn"):
            # attempt login
            try:
                res = requests.get(f"{API_URL}/login", auth=HTTPBasicAuth(username, password))
                if res.status_code == 200:
                    st.session_state.auth = (username, password)
                    st.session_state.username = username
                    st.session_state.password = password
                    st.session_state.role = res.json()["role"]
                    # Fetch roles once login is successful
                    st.session_state.roles = fetch_roles()
                    st.session_state.page = "main"  # Navigate to main app
                    st.rerun()
                else:
                    try:
                        st.error(res.json().get("detail", "Login failed."))
                    except Exception:
                        st.error("Login failed. Check FastAPI logs or credentials.")
            except Exception:
                st.error("Unable to reach API. Make sure FastAPI is running on localhost:8000")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# MAIN APP AFTER LOGIN (functionality preserved)
# -------------------------
if st.session_state.page == "main":
    username = st.session_state.username
    role = st.session_state.role

    # top right has user card + logout already handled in header section
    # Main content area
    main_col, side_col = st.columns([7, 2])

    with main_col:
        st.markdown('<div class="glass">', unsafe_allow_html=True)

        # Role-specific tabs and content
        if role == "C-Level":
            st.markdown("<div style='display:flex;align-items:center;justify-content:space-between'>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:700;font-size:16px'>C-Level Dashboard</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            tab1, tab2, tab3 = st.tabs(["💬 Chat", "🧾 Upload (C-Level)", "👤 Admin (C-Level)"])

        elif role == "General":
            st.markdown("<div style='font-weight:700;font-size:16px'>General Access</div>", unsafe_allow_html=True)
            (tab1,) = st.tabs(["💬 Chat"])
        else:
            st.markdown(f"<div style='font-weight:700;font-size:16px'>Role: {role}</div>", unsafe_allow_html=True)
            st.markdown("<div class='muted'>You also have access to general company documents (policies, announcements).</div>", unsafe_allow_html=True)
            (tab1,) = st.tabs(["💬 Chat"])

        # --- Chat Tab ---
        with tab1:
            st.subheader("Ask a question:")
            st.markdown("<div class='controls'>", unsafe_allow_html=True)
            q_col, btn_col = st.columns([6, 1])
            with q_col:
                question = st.text_input("Your Question", key="chat_q")
            with btn_col:
                if st.button("Submit", key="chat_submit"):
                    if not question or question.strip() == "":
                        st.warning("Please enter a question.")
                    else:
                        try:
                            res = requests.post(
                                f"{API_URL}/chat",
                                json={"question": question, "role": st.session_state.role},
                                auth=HTTPBasicAuth(*st.session_state.auth)
                            )
                            if res.status_code == 200:
                                answer = res.json().get("answer", "")
                                st.markdown("<div class='answer'>", unsafe_allow_html=True)
                                st.success("✅ Answer:")
                                st.write(answer)
                                st.markdown("</div>", unsafe_allow_html=True)
                            else:
                                st.error("❌ Something went wrong while processing your question.")
                        except Exception:
                            st.error("Unable to reach the API. Ensure the backend is running.")
            st.markdown("</div>", unsafe_allow_html=True)

        # --- Upload Tab (C-Level) ---
        if st.session_state.role == "C-Level":
            with tab2:
                st.subheader("Upload Documents")
                # try to use cached roles from session state
                roles = st.session_state.get("roles", [])
                selected_role = st.selectbox("Select document access role", roles, key="upload_role")
                doc_file = st.file_uploader("Upload document (.md or .csv)", type=["csv", "md"], key="upload_file")

                if st.button("Upload Document", key="upload_btn"):
                    if not doc_file:
                        st.warning("Please choose a file to upload.")
                    else:
                        try:
                            res = requests.post(
                                f"{API_URL}/upload-docs",
                                files={"file": doc_file},
                                data={"role": selected_role},
                                auth=HTTPBasicAuth(*st.session_state.auth)
                            )
                            if res.ok:
                                st.success(res.json().get("message", "Uploaded successfully."))
                            else:
                                st.error(res.json().get("detail", "Something went wrong."))
                        except Exception:
                            st.error("Unable to reach the API. Ensure the backend is running.")

            # --- Admin Tab (C-Level) ---
            with tab3:
                st.subheader("Add User")
                new_user = st.text_input("New Username", key="new_user")
                new_pass = st.text_input("New Password", type="password", key="new_pass")
                # reuse roles list
                new_role = st.selectbox("Assign Role", st.session_state.get("roles", []), key="assign_role")
                if st.button("Create User", key="create_user_btn"):
                    if not (new_user and new_pass and new_role):
                        st.warning("Please fill username, password and role.")
                    else:
                        try:
                            res = requests.post(
                                f"{API_URL}/create-user",
                                data={"username": new_user, "password": new_pass, "role": new_role},
                                auth=HTTPBasicAuth(*st.session_state.auth)
                            )
                            if res.ok:
                                st.success(res.json().get("message", "User created."))
                            else:
                                st.error(res.json().get("detail", "Something went wrong."))
                        except Exception:
                            st.error("Unable to reach the API. Ensure the backend is running.")

                st.markdown("---")
                st.subheader("Create New Role")
                new_role_input = st.text_input("New Role Name", key="new_role_input")
                if st.button("Add Role", key="add_role_btn"):
                    if not new_role_input:
                        st.warning("Provide a role name.")
                    else:
                        try:
                            res = requests.post(
                                f"{API_URL}/create-role",
                                data={"role_name": new_role_input},
                                auth=HTTPBasicAuth(*st.session_state.auth)
                            )
                            if res.ok:
                                st.success(res.json().get("message", "Role created."))
                                st.session_state.roles = fetch_roles()  # Refresh role list
                                st.rerun()  # Rerun so dropdowns get updated
                            else:
                                st.error(res.json().get("detail", "Something went wrong."))
                        except Exception:
                            st.error("Unable to reach the API. Ensure the backend is running.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Right side column: quick links, tips, and logout
    with side_col:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Help & Quick Actions")
        st.markdown("- Use the **Chat** tab to ask document questions.")
        st.markdown("- **C-Level** can upload docs & manage users/roles.")
        st.markdown("- All requests are authenticated with your credentials.")
        st.markdown("---")
        st.markdown("**Session**")
        st.markdown(f"- **User:** `{username}`")
        st.markdown(f"- **Role:** `{role}`")
        if st.button("Logout", key="logout_side"):
            st.session_state.auth = None
            st.session_state.role = None
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
