import streamlit as st
from streamlit_option_menu import option_menu
import pyrebase
from datetime import datetime
import os
import base64

# Import your app modules
import tentang1, akun, beranda, hasil7

st.set_page_config(
    page_title="Peduli Stunting",
    layout="wide"
)

#Configuration key
firebaseConfig = {
    "apiKey": "AIzaSyDkE5dqnxOxJgeibegKX7vcaJbuc3EBhq8",
    "authDomain": "stunting-f5b4f.firebaseapp.com",
    "projectId": "stunting-f5b4f",
    "databaseURL":"https://stunting-f5b4f-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "stunting-f5b4f.firebasestorage.app",
    "messagingSenderId": "124975439842",
    "appId": "1:124975439842:web:01fd5b994a6e3e890e63bb",
    "measurementId": "G-1894ER91Q9"
}

#Firease authenti
firebase=pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#database
db =firebase.database()
storage = firebase.storage()

if 'auth' not in st.session_state:
    st.session_state.auth = auth
if 'db' not in st.session_state:
    st.session_state.db = db

# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'login'
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# --- Navbar Function ---
def top_navbar():
    """Displays a simple top navigation bar."""
    logo_path = os.path.join(".", "logo.png")
    logo_src = ""

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        logo_src = f"data:image/png;base64,{encoded_string}"
    else:
        logo_src = "https://via.placeholder.com/40x40.png?text=Logo+Tidak+Ditemukan"
        st.warning(f"File logo tidak ditemukan di: {logo_path}. Menggunakan placeholder.")

    st.markdown(f"""
        <style>
        .top-navbar {{
            background-color: #F36DA8;
            padding: 15px 30px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .top-navbar h1 {{
            color: #f3f3f3;
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            font-family: 'Poppins', sans-serif;
        }}
        .top-navbar img {{
            height: 40px;
            margin-right: 15px;
        }}
        .top-navbar-spacer {{
            height: 80px;
            width: 100%;
        }}
        </style>
        <div class="top-navbar">
            <img src="{logo_src}" alt="Logo Peduli Stunting">
            <h1>Peduli Stunting</h1>
        </div>
        <div class="top-navbar-spacer"></div>
    """, unsafe_allow_html=True)

# --- Authentication Functions ---
def login_page():
    """Displays the login form."""
    top_navbar()

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.title("Silahkan Login Aplikasi Peduli Stunting")
        st.markdown("---")
        email = st.text_input("Email", key="login_email_input")
        password = st.text_input("Kata Sandi", type="password", key="login_password_input")

        if st.button("Login", use_container_width=True):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.logged_in = True
                st.session_state.user_info = user
                st.success("Anda berhasil login! Memuat dashboard...")
                st.rerun()
            except Exception as e:
                error_message = str(e)
                if "INVALID_LOGIN_CREDENTIALS" in error_message or "EMAIL_NOT_FOUND" in error_message or "INVALID_PASSWORD" in error_message:
                    st.error("Email atau kata sandi salah.")
                elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                    st.error("Terlalu banyak percobaan login yang gagal. Silakan coba lagi nanti.")
                else:
                    st.error(f"Terjadi kesalahan: {error_message}")

        st.markdown("---")
        st.info("Belum punya akun? Buat akun baru di sini.")
        if st.button("Buat Akun Baru", key="switch_to_signup_btn", use_container_width=True):
            st.session_state.current_view = 'signup'
            st.rerun()

        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            html, body, [class*="st-"] {
                font-family: 'Poppins', sans-serif;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
            }
            .stButton button {
                background-color: #F36DA8;
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease, color 0.3s ease;
                width: 100%;
            }

            .stButton button:hover {
                background-color: #612C43;
                color: #f3f3f3;
                transform: translateY(-2px);
            }

            .stButton button:active {
                color: white;
                background-color: #4A2234;
                transform: translateY(0);
            }
            </style>
            """, unsafe_allow_html=True)

def signup_page():
    top_navbar()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("Buat Akun Baru Anda")
        st.markdown("---")
        username = st.text_input('Nama Pengguna', value='Default')
        new_email = st.text_input("Email", key="signup_email_input")
        new_password = st.text_input("Pilih Kata Sandi", type="password", key="signup_password_input")
        confirm_password = st.text_input("Konfirmasi Kata Sandi", type="password", key="signup_confirm_password_input")

        if st.button("Daftar", use_container_width=True):
            if new_email == "" or new_password == "" or confirm_password == "":
                st.warning("Email dan kata sandi tidak boleh kosong.")
            elif new_password != confirm_password:
                st.error("Konfirmasi kata sandi tidak cocok.")
            else:
                try:
                    user = auth.create_user_with_email_and_password(new_email, new_password)
                    st.success(f"Akun dengan email '{new_email}' berhasil dibuat! Silakan login.")
                    user = auth.sign_in_with_email_and_password(new_email,new_password)
                    db.child(user['localId']).child("Username").set(username)
                    db.child(user['localId']).child("ID").set(user['localId'])
                    st.session_state.current_view = 'login'
                    st.rerun()
                except Exception as e:
                    error_message = str(e)
                    if "EMAIL_EXISTS" in error_message:
                        st.error("Email ini sudah terdaftar. Silakan gunakan email lain atau login.")
                    elif "WEAK_PASSWORD" in error_message:
                        st.error("Kata sandi terlalu lemah. Harap gunakan setidaknya 6 karakter.")
                    elif "INVALID_EMAIL" in error_message:
                        st.error("Format email tidak valid.")
                    else:
                        st.error(f"Terjadi kesalahan: {error_message}")

        st.markdown("---")
        st.info("Sudah punya akun? Kembali ke halaman login.")
        if st.button("Kembali ke Login", key="switch_to_login_btn", use_container_width=True):
            st.session_state.current_view = 'login'
            st.rerun()

        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            html, body, [class*="st-"] {
                font-family: 'Poppins', sans-serif;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
            }
            .stButton button {
                background-color: #F36DA8;
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease, color 0.3s ease;
                width: 100%;
            }

            .stButton button:hover {
                background-color: #612C43;
                color: #f3f3f3;
                transform: translateY(-2px);
            }

            .stButton button:active {
                color: white;
                background-color: #4A2234;
                transform: translateY(0);
            }
            </style>
            """, unsafe_allow_html=True)

#-------------------------------------Dashboard------------------------------------------------------------
def dashboard_app():

    with st.sidebar:
        st.markdown(
                """
                <style>
                [data-testid="stSidebar"] {
                    background-color: #f36da8;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

        st.title("Peduli Stunting")
        if st.session_state.user_info:
            st.write(f"Selamat datang, {st.session_state.user_info['email']}!")
            # Fetch username from DB if available
            user_uid = st.session_state.user_info['localId']
            username_from_db = db.child(user_uid).child("Username").get().val()
            if username_from_db:
                st.session_state.user_info['username'] = username_from_db # Store in session state
                st.write(f"Nama Pengguna: {username_from_db}") # Display username too

        st.markdown("---")

        app_selected = option_menu(
            menu_title=None,
            options=['Beranda', 'Prediksi', 'Tentang', 'Akun'],
            icons=['house-fill', 'trophy-fill', "info-circle", 'person-circle'],
            menu_icon='cast',
            default_index=0,
            styles={
                "container": {"background-color": "#F36DA8","border-radius": "0px"},
                "icon": {"color": "#f3f3f3", "font-size": "23px"},
                "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin": "0px","margin-bottom": "10px", "--hover-color": "#612C43","font-family": "'Poppins', sans-serif"},
                "nav-link-selected": {"background-color": "#612C43", "color": "white","font-family": "'Poppins', sans-serif"},
            }
        )

        st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 24px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 8px;
                }

                div.stButton > button:first-child:hover {
                    background-color: #45a049;
                    color: white;
                }
                </style>
                """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("Logout", key="logout_sidebar_btn", use_container_width=True):
            try:
                st.session_state.logged_in = False
                st.session_state.current_view = 'login'
                st.session_state.user_info = None
                st.info("Anda telah berhasil logout.")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal logout: {e}")

    if app_selected == 'Beranda':
        beranda.app()
    elif app_selected == 'Prediksi':
        # Pass db object and user_info to hasil6.app()
        hasil6.app(db, st.session_state.user_info) # <--- IMPORTANT CHANGE HERE
    elif app_selected == 'Tentang':
        tentang.app()
    elif app_selected == 'Akun':
        akun.app()

# --- Main Application Flow ---
def main():
    if not st.session_state.logged_in:
        if st.session_state.current_view == 'login':
            login_page()
        else:
            signup_page()
    else:
        dashboard_app()

if __name__ == "__main__":
    main()
