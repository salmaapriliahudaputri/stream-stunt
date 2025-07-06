import streamlit as st
import os
import base64

def app():
    # Path ke file logo
    logo_path = os.path.join(".", "pp.JPG")
    logo_src = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        logo_src = f"data:image/png;base64,{encoded_string}"
    else:
        # Fallback jika logo tidak ditemukan
        logo_src = "https://placehold.co/40x40/FFFFFF/F36DA8?text=PP" # Menggunakan placeholder jika logo tidak ditemukan
        st.warning(f"File logo tidak ditemukan di: {logo_path}. Menggunakan placeholder.")

    st.markdown(
        """
        <style>
            .stApp {
                color: #333333; /* Ensure consistent black text */
            }
            .stPageTitle {
                font-size: 3em;
                color: #F36DA8; /* Pink color from navbar */
                text-align: center;
                /* margin-bottom: 0.5em; */
                font-weight: bold;
            }
            .stSubtitle {
                font-size: 1.5em;
                color: #555555;
                text-align: center;
                margin-bottom: 2em;
            }
            .stSectionHeader {
                font-size: 2em;
                color: #F36DA8;
                margin-top: 1.5em;
                margin-bottom: 1em;
                font-weight: bold;
            }
            .stText {
                font-size: 1.1em;
                line-height: 1.6;
                margin-bottom: 1em;
            }
            .stCallToAction {
                display: flex;
                justify-content: center;
                margin-top: 3em;
            }
            div.stButton > button:nth-child(1) {
                background-color: #612C43; /* Green color */
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
                transition: background-color 0.3s ease; /* Smooth transition for hover */
            }

            div.stButton > button:nth-child(1):hover {
                background-color: #F36DA8; /* Darker green on hover */
                color: white;
            }
            .info-card {
                background-color: #f8f9fa; /* Info card background color */
                border-left: 5px solid #F36DA8; /* Pink left border */
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .info-card h3 {
                color: #F36DA8;
                margin-top: 0;
            }
            .info-card p {
                color: #666666;
            }
            /* New styles for header */
            .app-header {
                display: flex;
                justify-content: flex-end; /* Align items to the end (right) */
                /* align-items: center; */
                padding: 10px 20px;
                background-color: #F36DA8; /* Pink color from navbar */
                color: white;
                border-radius: 8px;
                margin-bottom: 2em;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                width: calc(100% + 40px); /* Adjust width to span across, accounting for default padding */
                margin-left: -20px; /* Adjust margin to align with the left edge */
                margin-top: -10px; /* Adjust margin to align with the top edge */
            }
            .header-item {
                display: flex;
                align-items: center;
                margin-left: px; /* Spacing between items, adjusted for right alignment */
            }
            .profile-pic {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 10px; /* Space between profile pic and username */
                object-fit: cover;
                border: 2px solid white;
            }
            .username {
                font-weight: bold;
            }
            .notification-icon {
                font-size: 1.5em;
                margin-right: 10px; /* Space between icon and next item */
                cursor: pointer;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Start of Changes for Dynamic Username ---
    # Get username from session_state if available, default to 'Pengguna'
    # It assumes 'user_info' is set in session_state after a successful login.
    username_to_display = "User" # Default value
    if 'user_info' in st.session_state and st.session_state.user_info is not None:
        username_to_display = st.session_state.user_info.get('username', 'User')
    # --- End of Changes for Dynamic Username ---

    # Header aplikasi
    st.markdown(
        f"""
        <div class="app-header">
            <div class="header-item">
                <span class="notification-icon">🔔</span>
            </div>
            <div class="header-item">
                <img src="{logo_src}" class="profile-pic">
                <span class="username">Halo, {username_to_display}!</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Kolom untuk konten utama agar terpusat
    col_empty1, col_main, col_empty2 = st.columns([0.5, 3, 0.5])

    with col_main:
        st.markdown("<h1 class='stPageTitle'>Selamat Datang di Peduli Stunting!</h1>", unsafe_allow_html=True)
        st.markdown("<p class='stSubtitle'>Aplikasi prediksi dan edukasi stunting untuk masa depan anak Indonesia yang lebih baik.</p>", unsafe_allow_html=True)

        st.image("Family-cuate.svg",
                 caption="Ilustrasi pertumbuhan anak sehat",
                 use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True) # Jarak

        st.markdown("<h2 class='stSectionHeader'>Apa itu Stunting?</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="stText">
            <p>Stunting adalah kondisi gagal tumbuh pada anak balita (usia di bawah 5 tahun) akibat kekurangan gizi kronis, terutama dalam 1000 Hari Pertama Kehidupan (HPK). Kondisi ini ditandai dengan tinggi badan anak yang berada di bawah standar usianya.</p>
            <p>Dampak stunting sangat serius, tidak hanya menghambat pertumbuhan fisik, tetapi juga dapat memengaruhi perkembangan kognitif, kekebalan tubuh yang lemah, dan risiko penyakit tidak menular di kemudian hari.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<h2 class='stSectionHeader'>Bagaimana Peduli Stunting Membantu?</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="stText">
            <p>Aplikasi <b>Peduli Stunting</b> hadir untuk membantu Anda memahami risiko stunting pada anak Anda melalui fitur prediksi yang cerdas. Kami menggunakan data dan model yang telah dilatih untuk memberikan estimasi risiko berdasarkan informasi yang Anda berikan.</p>
            <p>Selain itu, kami menyediakan informasi edukatif, tips nutrisi, dan panduan untuk pencegahan stunting, memastikan setiap anak memiliki kesempatan untuk tumbuh optimal dan mencapai potensi penuhnya.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<h2 class='stSectionHeader'>Fitur Unggulan Kami:</h2>", unsafe_allow_html=True)
        
        col_feat1, col_feat2 = st.columns(2)

        with col_feat1:
            st.markdown(
                """
                <div class="info-card">
                    <h3>Prediksi Akurat</h3>
                    <p>Dapatkan estimasi risiko stunting berdasarkan data antropometri dan riwayat gizi anak.</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col_feat2:
            st.markdown(
                """
                <div class="info-card">
                    <h3>Edukasi Komprehensif</h3>
                    <p>Akses informasi terbaru tentang nutrisi, pola asuh, dan pencegahan stunting.</p>
                </div>
                """, unsafe_allow_html=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True) # Jarak