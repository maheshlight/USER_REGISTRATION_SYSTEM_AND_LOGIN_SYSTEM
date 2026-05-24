import streamlit as st
import sqlite3

# ---------- Page Config ----------
st.set_page_config(
    page_title="Login & Signup System",
    page_icon="🔐",
    layout="centered"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    .stApp { background-color: #0f172a; }

    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 8px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        padding: 10px;
        margin-top: 5px;
        background-color: #1e293b;
        color: white !important;
        border: 1px solid #334155;
    }

    .stButton > button:hover {
        background-color: #334155;
        color: white !important;
    }

    .stCheckbox > label { color: white !important; }

    .success-box {
        background-color: #052e16;
        border: 1px solid #22c55e;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Database Setup ----------
def get_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn

def setup_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT,
            lname TEXT,
            dob TEXT,
            email TEXT,
            contact TEXT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    try:
        cur.execute("INSERT INTO users (fname,lname,dob,email,contact,username,password) VALUES (?,?,?,?,?,?,?)",
                    ("Admin","User","01-01-2000","admin@mail.com","9999999999","admin","admin123"))
        cur.execute("INSERT INTO users (fname,lname,dob,email,contact,username,password) VALUES (?,?,?,?,?,?,?)",
                    ("Test","User","02-02-2001","test@mail.com","8888888888","test","test123"))
        conn.commit()
    except:
        pass
    conn.close()

setup_db()

# ---------- Session State ----------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = ""

# ---------- Login Page ----------
def login_page():
    st.markdown("<h1 style='text-align:center; color:white;'>🔐 LOGIN</h1>", unsafe_allow_html=True)
    st.markdown("---")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    robot = st.checkbox("I am not a robot", key="login_robot")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="btn_login", use_container_width=True):
            if not robot:
                st.error("Please confirm you are not a robot.")
            elif not username or not password:
                st.error("Please fill in all fields.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT fname, lname, password FROM users WHERE username=?", (username,))
                data = cur.fetchone()
                conn.close()
                if not data:
                    st.error("Username does not exist.")
                elif data[2] != password:
                    st.error("Incorrect password.")
                else:
                    st.session_state.logged_in_user = data[0] + " " + data[1]
                    st.session_state.page = "welcome"
                    st.rerun()

    with col2:
        if st.button("Go to Sign Up", key="btn_goto_signup", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Forgot Username / Password", key="btn_forgot", use_container_width=True):
        st.info("Please contact the system administrator.")

# ---------- Signup Page ----------
def signup_page():
    st.markdown("<h1 style='text-align:center; color:white;'>📝 SIGN UP</h1>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fname    = st.text_input("First Name")
        dob      = st.text_input("Date of Birth (DD-MM-YYYY)")
        contact  = st.text_input("Contact")
        password = st.text_input("Password", type="password")
    with col2:
        lname    = st.text_input("Last Name")
        email    = st.text_input("Email")
        username = st.text_input("Username")

    robot = st.checkbox("I am not a robot", key="signup_robot")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("Sign Up", key="btn_signup", use_container_width=True):
            if not robot:
                st.error("Please confirm you are not a robot.")
            elif not all([fname, lname, dob, email, contact, username, password]):
                st.error("Please fill in all fields.")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO users (fname,lname,dob,email,contact,username,password) VALUES (?,?,?,?,?,?,?)",
                        (fname, lname, dob, email, contact, username, password)
                    )
                    conn.commit()
                    conn.close()
                    st.success("Signup successful! Please login.")
                    st.session_state.page = "login"
                    st.rerun()
                except:
                    st.error("Username already exists. Please choose another.")

    with col4:
        if st.button("Back to Login", key="btn_back", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ---------- Welcome Page ----------
def welcome_page():
    name = st.session_state.logged_in_user
    st.markdown(f"""
    <div class="success-box">
        <h1 style="color:#22c55e;">Thank You for Logging In!</h1>
        <h2 style="color:white;">Welcome, {name}!</h2>
        <p style="color:#94a3b8;">We are glad to have you here.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Logout", key="btn_logout", use_container_width=True):
        st.session_state.logged_in_user = ""
        st.session_state.page = "login"
        st.rerun()

# ---------- Router ----------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "welcome":
    welcome_page()
