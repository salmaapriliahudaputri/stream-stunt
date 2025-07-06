import streamlit as st
import time
from PIL import Image
import base64
from io import BytesIO
# import pyrebase # Pastikan pyrebase atau firebase_admin diimpor jika diperlukan
# from PIL import Image # Untuk memproses gambar, jika diperlukan
# import io # Untuk membaca gambar yang diunggah

def app():
    st.markdown(
        """
        <style>
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'); /* Font Awesome untuk ikon profil default */

            .stApp {
                background-color: #FFFFFF;
                color: #333333;
            }
            .stPageTitle {
                font-size: 2.5em;
                color: #F36DA8;
                text-align: center;
                margin-bottom: 1em;
                font-weight: bold;
            }
            .stSubHeader {
                font-size: 1.8em;
                color: #555555;
                margin-top: 1.5em;
                margin-bottom: 1em;
            }
            .stInfoCard {
                background-color: #f8f9fa;
                border-left: 5px solid #F36DA8;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .stInfoCard p {
                margin: 5px 0;
            }

            /* --- Gaya untuk tombol di dalam form (Perbarui Nama Pengguna, Perbarui Bio) --- */
            div.stForm button {
                background-color: #612C43; /* Warna ungu */
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
                transition: background-color 0.3s ease; /* Transisi halus untuk hover */
            }

            div.stForm button:hover {
                background-color: #F36DA8; /* Ungu lebih gelap saat hover */
                color: white;
            }

            /* --- Gaya untuk tombol umum (misal: Kembali ke Login) --- */
            div.stButton > button:first-child { 
                background-color: #612C43; /* Warna ungu */
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
                transition: background-color 0.3s ease; /* Transisi halus untuk hover */
            }

            div.stButton > button:first-child:hover {
                background-color: #F36DA8; /* Ungu lebih gelap saat hover */
                color: white;
            }

            /* Gaya untuk ikon profil default */
            .profile-icon {
                font-size: 100px; /* Ukuran ikon */
                color: #F36DA8; /* Warna ikon, bisa disesuaikan */
                text-align: center;
                display: block; /* Agar bisa di-center */
                margin: 0 auto; /* Tengah secara horizontal */
                padding: 20px;
                border: 2px solid #F36DA8;
                border-radius: 50%; /* Bentuk lingkaran */
                width: 150px; /* Sesuaikan dengan lebar gambar */
                height: 150px; /* Sesuaikan dengan tinggi gambar */
                display: flex; /* Untuk memusatkan ikon di dalam lingkaran */
                align-items: center;
                justify-content: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 class='stPageTitle'>Informasi Akun Anda</h1>",unsafe_allow_html=True)

    # Pastikan pengguna sudah login dan user_info tersedia
    if st.session_state.logged_in and st.session_state.user_info:
        user_email = st.session_state.user_info.get('email', 'Tidak Tersedia')
        user_username = st.session_state.user_info.get('username', 'Tidak Tersedia')
        user_local_id = st.session_state.user_info.get('localId', 'Tidak Tersedia')
        user_bio = st.session_state.user_info.get('bio', 'Belum ada bio.') # Ambil bio, default jika tidak ada

        # Tampilkan ikon profil default
        path_foto_lokal = "pp.JPG" 

        try:
            foto = Image.open(path_foto_lokal)
            buffered = BytesIO()
            if path_foto_lokal.lower().endswith(('.jpg', '.jpeg')):
                foto.save(buffered, format="JPEG")
                mime_type = "image/jpeg"
            elif path_foto_lokal.lower().endswith('.png'):
                foto.save(buffered, format="PNG")
                mime_type = "image/png"
            else:
                st.error("Format gambar tidak didukung untuk encoding Base64. Gunakan JPG atau PNG.")
                st.stop()

            img_str = base64.b64encode(buffered.getvalue()).decode()

            st.markdown(f'''
            <div class="profile-image-container">
                <img src="data:{mime_type};base64,{img_str}" alt="Foto Profil" class="profile-image">
            </div>
            ''', unsafe_allow_html=True)

            # --- Styling CSS Opsional (sama seperti Opsi 1) ---
            st.markdown("""
            <style>
                .profile-image-container {
                    width: 150px; 
                    height: 150px; 
                    border-radius: 50%; 
                    overflow: hidden; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    margin: 20px auto; 
                    border: 2px solid #336699; 
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
                }
                .profile-image {
                    width: 100%; 
                    height: 100%; 
                    object-fit: cover; 
                    display: block; 
                }
            </style>
            """, unsafe_allow_html=True)

        except FileNotFoundError:
            st.error(f"Error: Foto tidak ditemukan di '{path_foto_lokal}'. Pastikan path sudah benar.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memuat atau menampilkan foto: {e}")

        st.markdown("---") # Garis pemisah visual


        st.markdown("<h2 class='stSubHeader'>Detail Akun</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="stInfoCard">
                <p><strong>Email:</strong> {user_email}</p>
                <p><strong>Nama Pengguna:</strong> {user_username}</p>
                <p><strong>ID Unik:</strong> {user_local_id}</p>
                <p><strong>Bio:</strong> {user_bio}</p> </div>
        """, unsafe_allow_html=True)

        st.markdown("<h2 class='stSubHeader'>Perbarui Bio</h2>", unsafe_allow_html=True)

        # Form untuk mengubah bio
        with st.form("update_bio_form", clear_on_submit=False):
            new_bio = st.text_area("Bio Anda", value=user_bio, height=100)
            bio_submitted = st.form_submit_button("Perbarui Bio")

            if bio_submitted:
                try:
                    # Memperbarui Bio di Firebase Realtime Database
                    if 'db' not in st.session_state:
                        st.error("Firebase Realtime Database belum diinisialisasi.")
                        return

                    st.session_state.db.child(user_local_id).child("bio").set(new_bio.strip())

                    # Perbarui session_state agar perubahan langsung terlihat
                    st.session_state.user_info['bio'] = new_bio.strip()

                    st.success("Bio berhasil diperbarui!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal memperbarui bio: {e}")

        st.markdown("<h2 class='stSubHeader'>Perbarui Nama Pengguna</h2>", unsafe_allow_html=True)

        # Form untuk mengubah username
        with st.form("update_username_form", clear_on_submit=False):
            new_username = st.text_input("Nama Pengguna Baru", value=user_username)
            username_submitted = st.form_submit_button("Perbarui Nama Pengguna")

            if username_submitted:
                try:
                    if not new_username.strip():
                        st.error("Nama Pengguna tidak boleh kosong.")
                    else:
                        # Memperbarui Username di Firebase Realtime Database
                        if 'db' not in st.session_state:
                            st.error("Firebase Realtime Database belum diinisialisasi.")
                            return

                        st.session_state.db.child(user_local_id).child("Username").set(new_username.strip())

                        # Perbarui session_state agar perubahan langsung terlihat
                        st.session_state.user_info['username'] = new_username.strip()

                        st.success("Nama pengguna berhasil diperbarui!")
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"Gagal memperbarui nama pengguna: {e}")

    else:
        st.warning("Anda harus login untuk melihat halaman akun.")
        if st.button("Kembali ke Login"):
            st.session_state.current_view = 'login'
            st.rerun()