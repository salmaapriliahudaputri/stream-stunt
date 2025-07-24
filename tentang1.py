# tentang.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import base64
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
import numpy as np
from sklearn.metrics import RocCurveDisplay


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
            /* Main app background and text color */
            .stApp {
                background-color: #F8F8F8; /* Light gray background */
                color: #333333;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            /* Main title */
            .stApp > header {
                background-color: #F8F8F8; /* Match app background */
            }
            .st-emotion-cache-1jmve6v {
                background-color: #F8F8F8; /* Ensure header background matches app */
            }
            .st-emotion-cache-z5fcl4 { /* Target header element */
                background-color: #F8F8F8;
            }

            h1 {
                font-size: 2.8em;
                color: #B1006E; /* Darker shade of your pink for contrast */
                margin-bottom: 0.8em;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
            h2 {
                font-size: 2.2em;
                color: #E91E63; /* Brighter pink for subheaders */
                margin-top: 1.5em;
                margin-bottom: 0.8em;
                border-bottom: 2px solid #F36DA8; /* Underline effect */
                padding-bottom: 0.3em;
            }
            h3 {
                font-size: 1.6em;
                color: #6A1B9A; /* Deep purple for smaller headings */
                margin-top: 1em;
                margin-bottom: 0.5em;
            }
            li {
                font-size: 1.1em;
                line-height: 1.7;
                color: #4A4A4A;
            }
            /* Tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 5px;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: nowrap;
                background-color: #FFE0F0; /* Light pink tab background */
                border-radius: 7px 7px 0 0;
                gap: 10px;
                padding-left: 20px;
                padding-right: 20px;
                color: #B1006E; /* Dark pink tab text */
                font-weight: bold;
                font-size: 1.1em;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #F36DA8; /* Darker pink on hover */
                color: white;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #F36DA8; /* Active tab background */
                color: white;
                border-bottom: 3px solid #6A1B9A; /* Dark purple active tab border */
            }

            /* Info box */
            .stAlert.st-emotion-cache-1c7v050 { /* Target Streamlit info box */
                background-color: #E8F5E9; /* Light green */
                border-left: 6px solid #612C43; /* Green border */
                color: #612C43; /* Dark green text */
                border-radius: 8px;
                padding: 15px;
            }
            .stAlert.st-emotion-cache-1c7v050 p {
                color: #2E7D32; /* Ensure info text is correct color */
            }

            /* Warning box */
            .stAlert.st-emotion-cache-1fcp7b7 { /* Target Streamlit warning box */
                background-color: #FFFDE7; /* Light yellow */
                border-left: 6px solid #FFC107; /* Orange border */
                color: #FFA000; /* Dark yellow text */
                border-radius: 8px;
                padding: 15px;
            }
            .stAlert.st-emotion-cache-1fcp7b7 p {
                color: #FFA000; /* Ensure warning text is correct color */
            }

            /* Error box */
            .stAlert.st-emotion-cache-1e01k5 { /* Target Streamlit error box */
                background-color: #FFEBEE; /* Light red */
                border-left: 6px solid #D32F2F; /* Red border */
                color: #C62828; /* Dark red text */
                border-radius: 8px;
                padding: 15px;
            }
            .stAlert.st-emotion-cache-1e01k5 p {
                color: #C62828; /* Ensure error text is correct color */
            }

            /* Dataframe styling (for the feature importance table) */
            .stDataFrame {
                margin-top: 1.5em;
                border-radius: 10px;
                overflow: hidden; /* Ensures borders are rounded */
                box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Subtle shadow */
            }
            .dataframe-column-header {
                background-color: #F36DA8 !important;
                color: white !important;
                font-weight: bold !important;
            }
            .st-emotion-cache-vdgyx8 th { /* Specific target for dataframe headers */
                background-color: #F36DA8 !important;
                color: white !important;
                font-weight: bold !important;
            }
            .st-emotion-cache-vdgyx8 td {
                color: #4A4A4A;
            }

            /* Footer styling */
            .st-emotion-cache-h4xjwx p { /* Target for footer text */
                text-align: center;
                font-size: 0.9em;
                color: #f3f3f3;
                margin-top: 3em;
            }

            /* Styling for list items in markdown */
            ul li {
                margin-bottom: 0.5em;
            }

            /* General container padding */
            .st-emotion-cache-1c7v050 { /* Adjust padding for markdown content */
                padding: 1.5rem;
            }

            /* Custom table styling */
            .custom-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 1.1em;
                text-align: left;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Deeper shadow */
                border-radius: 10px; /* Rounded corners for the whole table */
                overflow: hidden; /* Ensures shadow and border-radius are applied correctly */
            }
            .custom-table th, .custom-table td {
                padding: 15px 20px; /* More padding */
                border-bottom: 1px solid #ddd;
            }
            .custom-table th {
                background-color: #E91E63; /* Pink header */
                color: white;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .custom-table tbody tr:nth-of-type(even) {
                background-color: #fcfcfc; /* Lighter alternating row */
            }
            
            /* Specific styling for attribute names */
            .custom-table td:first-child {
                font-weight: bold;
                color: #B1006E; /* Darker pink for attribute names */
                width: 35%; /* Give more space to attribute names */
            }
            div.stButton > button:nth-child(1) {
                background-color: #612C43; /* Warna hijau */
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

            div.stButton > button:nth-child(1):hover {
                background-color: #F36DA8; /* Warna hijau lebih gelap saat hover */
                color: white;
            }
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
    username_to_display = "User" # Default value
    if 'user_info' in st.session_state and st.session_state.user_info is not None:
        username_to_display = st.session_state.user_info.get('username', 'User')
    # --- End of Changes for Dynamic Username ---

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

    st.title("Panduan Website Peduli Stunting")
    st.write(
        """
        Selamat datang di aplikasi Peduli Stunting. Kami hadir untuk membantu Anda memahami dan mencegah stunting
        melalui informasi yang akurat dan fitur prediksi yang mudah digunakan.
        """
    )

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Prediksi & Atribut Data", "Solusi Penanganan Stunting", "Informasi Model"])

    with tab1:
        st.header("Cara Melakukan Prediksi Stunting")
        st.markdown(
            """
            Fitur prediksi stunting kami dirancang untuk memudahkan Anda dalam menganalisis data dan mendapatkan perkiraan
            risiko stunting. Untuk menggunakan fitur ini, silakan ikuti langkah-langkah berikut:
            """
        )
        st.markdown("""
        1.  **Akses Menu Prediksi:** Masuk ke akun Anda dan navigasikan ke menu **"Prediksi"** yang tersedia di bilah navigasi utama website.
        2.  **Unggah File Data:** Anda dapat mengunggah data yang ingin diprediksi dalam format file **.xlsx** (Microsoft Excel) atau **.csv** (Comma Separated Values). Pastikan format data Anda sudah sesuai dengan ketentuan yang akan dijelaskan di bawah ini.
        3.  **Proses Prediksi:** Setelah file berhasil diunggah, sistem kami akan secara otomatis memproses data dan menampilkan hasil prediksi stunting.
        """)

        st.markdown("---")
        st.header("Atribut Data yang Diperlukan")
        st.markdown(
            """
            Untuk hasil prediksi yang akurat, pastikan file data Anda mengandung atribut-atribut berikut beserta keterangannya:
            """
        )

        # Start of custom HTML table
        st.markdown(
            """
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Atribut</th>
                        <th>Keterangan & Pilihan</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Usia Anak</b> (`chAge`)</td>
                        <td>Usia anak dihitung dalam **bulan saat ini**. Contoh: jika anak berusia 1 tahun 3 bulan, masukkan `15`.</td>
                    </tr>
                    <tr>
                        <td><b>Jenis Kelamin Anak</b> (`chSex`)</td>
                        <td>Pilih jenis kelamin anak: <br>• `m` (laki-laki)<br>• `f` (perempuan)</td>
                    </tr>
                    <tr>
                        <td><b>Ukuran Anak Saat Lahir</b> (`chSize`)</td>
                        <td>Pilih kategori ukuran anak saat lahir: <br>• `average`<br>• `large`<br>• `small`</td>
                    </tr>
                    <tr>
                        <td><b>Berat Anak Saat Lahir</b> (`chBw`)</td>
                        <td>Pilih kategori berat anak saat lahir: <br>• `more than 2.5` (lebih dari 2.5 kg)<br>• `less than 2.5` (kurang dari 2.5 kg)</td>
                    </tr>
                    <tr>
                        <td><b>Status Anak Menyusui Saat Ini</b> (`db`)</td>
                        <td>Pilih status menyusui anak:<br>• `ever breastfed, not currently breastfeeding` (pernah menyusui, tapi tidak sedang)<br>• `still breastfeeding` (masih menyusui)<br>• `never breastfed` (tidak pernah menyusui)</td>
                    </tr>
                    <tr>
                        <td><b>Waktu Anak Mendapat ASI Pertama Kali</b> (`breaststart`)</td>
                        <td>Pilih waktu pemberian ASI pertama kali:<br>• `1hr` (dalam 1 jam setelah lahir)<br>• `1-24hr` (antara 1-24 jam setelah lahir)<br>• `30day` (lebih dari 24 jam hingga 30 hari setelah lahir)</td>
                    </tr>
                    <tr>
                        <td><b>Anak Mengalami Diare 2 Minggu Terakhir</b> (`chDiar`)</td>
                        <td>Pilih `yes` (ya) jika anak mengalami diare atau `no` (tidak).</td>
                    </tr>
                    <tr>
                        <td><b>Anak Mengonsumsi Obat Parasit 2 Minggu Terakhir</b> (`chDrug`)</td>
                        <td>Pilih `yes` (ya) jika anak mengonsumsi obat parasit atau `no` (tidak).</td>
                    </tr>
                    <tr>
                        <td colspan="2" style="background-color: #F36DA8; color: white; text-align: center; font-weight: bold;">DATA IBU</td>
                    </tr>
                    <tr>
                        <td><b>Usia Ibu</b> (`MmAge`)</td>
                        <td>Usia ibu dihitung dalam **tahun saat ini**.</td>
                    </tr>
                    <tr>
                        <td><b>Pendidikan Terakhir Ibu</b> (`MmEdu`)</td>
                        <td>Pilih tingkat pendidikan terakhir ibu:<br>• `no` (tidak sekolah)<br>• `primary` (SD)<br>• `second or higher` (SMP ke atas)</td>
                    </tr>
                    <tr>
                        <td><b>Status Ibu Bekerja</b> (`MomWork`)</td>
                        <td>Pilih `yes` (ya) jika ibu bekerja atau `no` (tidak) jika ibu tidak bekerja.</td>
                    </tr>
                    <tr>
                        <td><b>Status Pernikahan Ibu</b> (`Mmstat`)</td>
                        <td>Pilih status pernikahan ibu: <br>• `married`<br>• `single`<br>• `separated`</td>
                    </tr>
                    <tr>
                        <td><b>Tinggi Badan Ibu (cm)</b> (`MmHeight`)</td>
                        <td>Tinggi badan ibu saat ini dalam satuan **sentimeter**.</td>
                    </tr>
                    <tr>
                        <td><b>Body Mass Index Ibu</b> (`BMI`)</td>
                        <td>Pilih kategori BMI ibu:<br>• `normal`<br>• `obses` (obesitas)<br>• `uderweight` (kurang berat badan)<br>• `Overeight` (berat badan berlebih)</td>
                    </tr>
                    <tr>
                        <td colspan="2" style="background-color: #F36DA8; color: white; text-align: center; font-weight: bold;">DATA RUMAH TINGGAL & LINGKUNGAN</td>
                    </tr>
                    <tr>
                        <td><b>Jumlah Anak dalam Keluarga</b> (`nChild`)</td>
                        <td>Pilih jumlah anak dalam keluarga:<br>• `1 child`<br>• `2 child`<br>• `more than 3` (lebih dari 3 anak)</td>
                    </tr>
                    <tr>
                        <td><b>Domisili</b> (`residence`)</td>
                        <td>Pilih domisili: <br>• `urban` (perkotaan)<br>• `rural` (pedesaan)</td>
                    </tr>
                    <tr>
                        <td><b>Indeks Kekayaan Keluarga</b> (`wi`)</td>
                        <td>Pilih kategori indeks kekayaan keluarga:<br>• `poor` (miskin)<br>• `middle` (menengah)<br>• `rich` (kaya)</td>
                    </tr>
                    <tr>
                        <td><b>Kondisi Saluran Air di Rumah</b> (`water`)</td>
                        <td>Pilih kondisi saluran air di rumah: <br>• `improved` (membaik/layak)<br>• `unimproved` (belum membaik/tidak layak)</td>
                    </tr>
                    <tr>
                        <td><b>Kondisi Toilet dalam Rumah</b> (`toilet`)</td>
                        <td>Pilih kondisi toilet dalam rumah:<br>• `improved` (membaik/layak)<br>• `unimproved` (belum membaik/tidak layak)</td>
                    </tr>
                    <tr>
                        <td><b>Ketinggian Tempat Tinggal</b> (`altitudes`)</td>
                        <td>Pilih kategori ketinggian tempat tinggal:<br>• `<=2000` (kurang dari atau sama dengan 2000 meter di atas permukaan laut)<br>• `>2000` (lebih dari 2000 meter di atas permukaan laut)</td>
                    </tr>
                    <tr>
                        <td><b>Media Informasi Dari Koran</b> (`reading`)</td>
                        <td>Pilih `yes` (ya) jika mengakses informasi dari koran atau `no` (tidak).</td>
                    </tr>
                    <tr>
                        <td><b>Media Informasi Dari Televisi</b> (`tv`)</td>
                        <td>Pilih `yes` (ya) jika mengakses informasi dari televisi atau `no` (tidak).</td>
                    </tr>
                    <tr>
                        <td><b>Media Informasi Dari Radio</b> (`radio`)</td>
                        <td>Pilih `yes` (ya) jika mengakses informasi dari radio atau `no` (tidak).</td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )
        # End of custom HTML table

        st.info("*Pastikan tidak ada data yang kosong atau salah format agar proses prediksi berjalan lancar.*")

    with tab2:
        st.header("Solusi untuk Mencegah Stunting")
        st.markdown(
            """
            Pencegahan stunting adalah upaya kolektif yang membutuhkan perhatian pada berbagai aspek. Berikut adalah beberapa
            solusi penting untuk mencegah stunting, bersumber dari **UNICEF**:
            """
        )
        st.markdown("""
        * **Gizi Optimal Sejak Dini:**
            * **Pemberian ASI Eksklusif:** Berikan ASI eksklusif selama enam bulan pertama kehidupan bayi, dilanjutkan dengan pemberian ASI bersama makanan pendamping ASI (MPASI) yang bergizi hingga anak berusia dua tahun atau lebih.
            * **MPASI yang Tepat:** Pastikan MPASI kaya akan nutrisi makro (karbohidrat, protein, lemak) dan mikro (vitamin dan mineral) yang esensial untuk pertumbuhan dan perkembangan anak.
            * **Diversifikasi Pangan:** Perkenalkan berbagai jenis makanan dari berbagai kelompok pangan untuk memastikan asupan nutrisi yang lengkap.
        * **Akses Air Bersih dan Sanitasi:**
            * **Air Bersih:** Pastikan keluarga memiliki akses terhadap air minum yang aman dan bersih untuk mencegah infeksi yang dapat menghambat penyerapan nutrisi.
            * **Sanitasi yang Memadai:** Praktikkan kebersihan diri dan lingkungan yang baik, termasuk cuci tangan pakai sabun, serta memiliki fasilitas sanitasi yang layak untuk mencegah penyakit diare dan infeksi lainnya.
        * **Pelayanan Kesehatan Primer yang Kuat:**
            * **Antenatal Care (ANC) Teratur:** Ibu hamil harus mendapatkan pemeriksaan kehamilan secara teratur untuk memastikan kesehatan ibu dan janin.
            * **Imunisasi Lengkap:** Pastikan anak mendapatkan imunisasi lengkap sesuai jadwal untuk melindungi dari penyakit yang dapat memperburuk kondisi gizi.
            * **Pemantauan Pertumbuhan:** Rutin memantau berat badan dan tinggi badan anak di fasilitas kesehatan untuk deteksi dini masalah pertumbuhan.
        * **Pendidikan dan Pemberdayaan Masyarakat:**
            * **Edukasi Gizi:** Meningkatkan pengetahuan masyarakat, khususnya ibu dan pengasuh, tentang praktik gizi yang baik dan pola asuh yang mendukung pertumbuhan anak.
            * **Pemberdayaan Wanita:** Memberdayakan perempuan melalui pendidikan dan ekonomi dapat meningkatkan kesejahteraan keluarga dan kesehatan anak.
        """)
        st.info("*Informasi lebih lanjut mengenai pencegahan stunting dapat diakses di situs web resmi [UNICEF](https://www.unicef.org/topic/nutrition/stunting).*") # Added a link

    with tab3:
        st.header("Detail Model Prediksi Stunting")
        st.markdown(
            """
            Bagian ini menyajikan informasi mendalam mengenai data yang digunakan, distribusi label,
            performa model, dan peringkat fitur yang paling berpengaruh dalam model prediksi stunting.
            """
        )

        # --- Dataset Sebelum dan Sesudah Preprocessing ---
        st.subheader("Tampilan Dataset Sebelum dan Sesudah Preprocessing")
        st.markdown(
            """
            Berikut adalah tampilan sebagian dari dataset yang digunakan, **sebelum** (`initial_dataset.csv`) dan **sesudah** (`feature_selected_dataset.csv`)
            preprocessing dan seleksi fitur. Preprocessing umumnya meliputi penanganan nilai yang hilang, pengkodean variabel kategorikal, dan normalisasi.
            Sumber Dataset : https://dhsprogram.com/
            """
        )

        try:
            # Load initial dataset
            initial_data_path = 'initial_dataset.csv'
            if os.path.exists(initial_data_path):
                initial_df = pd.read_csv(initial_data_path)
                st.write("**Dataset Sebelum Preprocessing (5 baris pertama):**")
                st.dataframe(initial_df.head())
            else:
                st.warning(f"File '{initial_data_path}' tidak ditemukan. Menampilkan data placeholder.")
                initial_df = pd.DataFrame({
                    'chAge': [12, 24, 18, 30, 6],
                    'chSex': ['m', 'f', 'm', 'f', 'm'],
                    'MmAge': [25, 30, 28, 32, 27],
                    'Stunting': [0, 1, 0, 1, 0]
                })
                st.write("**Dataset Sebelum Preprocessing (5 baris pertama - Placeholder):**")
                st.dataframe(initial_df.head())

            # Load feature-selected dataset (after preprocessing)
            processed_data_path = 'feature_selected_dataset.csv'
            if os.path.exists(processed_data_path):
                processed_df = pd.read_csv(processed_data_path)
                st.write("**Dataset Sesudah Preprocessing & Seleksi Fitur (5 baris pertama):**")
                st.dataframe(processed_df.head())
            else:
                st.warning(f"File '{processed_data_path}' tidak ditemukan. Menampilkan data placeholder.")
                processed_df = pd.DataFrame({
                    'chAge_scaled': [0.2, 0.6, 0.4, 0.8, 0.1],
                    'MmAge_scaled': [0.3, 0.7, 0.5, 0.9, 0.4],
                    'chSex_f': [0, 1, 0, 1, 0],
                    'Stunting': [0, 1, 0, 1, 0]
                })
                st.write("**Dataset Sesudah Preprocessing & Seleksi Fitur (5 baris pertama - Placeholder):**")
                st.dataframe(processed_df.head())

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memuat atau menampilkan dataset: {e}")
            st.write("Pastikan file CSV Anda tersedia dan dalam format yang benar.")
        
        st.markdown("---")

        # --- Distribusi Label Sebelum dan Sesudah SMOTE ---
        st.subheader("Distribusi Label Stunting Sebelum dan Sesudah SMOTE")
        st.markdown(
            """
            Grafik di bawah ini menunjukkan distribusi kelas target **'Stunting'** (`0: Tidak Stunting`, `1: Stunting`)
            sebelum dan sesudah aplikasi metode Synthetic Minority Over-sampling Technique (**SMOTE**)
            untuk mengatasi ketidakseimbangan kelas dalam dataset.
            """
        )

        try:
            label_before_smote = None
            label_after_smote = None

            # Load distribution before SMOTE
            dist_before_path = 'distribusi_label_sebelum_smote.sav'
            if os.path.exists(dist_before_path):
                with open(dist_before_path, 'rb') as f:
                    label_before_smote = pickle.load(f)
            else:
                st.warning(f"File '{dist_before_path}' tidak ditemukan. Menggunakan data placeholder.")
                label_before_smote = pd.Series([800, 200], index=[0, 1], name='Count')

            # Load distribution after SMOTE
            dist_after_path = 'distribusi_label_setelah_smote.sav'
            if os.path.exists(dist_after_path):
                with open(dist_after_path, 'rb') as f:
                    label_after_smote = pickle.load(f)
            else:
                st.warning(f"File '{dist_after_path}' tidak ditemukan. Menggunakan data placeholder.")
                # Simulate SMOTE effect if file not found
                minority_count = label_before_smote.get(1, 0)
                majority_count = label_before_smote.get(0, 0)
                label_after_smote = pd.Series({0: majority_count, 1: majority_count}, name='Count')


            fig_dist, axes = plt.subplots(1, 2, figsize=(14, 5))

            # Plot before SMOTE
            sns.barplot(x=label_before_smote.index, y=label_before_smote.values, ax=axes[0], palette='pastel')
            axes[0].set_title('Distribusi Label Sebelum SMOTE')
            axes[0].set_xlabel('Stunting (0: Tidak Stunting, 1: Stunting)')
            axes[0].set_ylabel('Jumlah Sampel')
            for i, v in enumerate(label_before_smote.values):
                axes[0].text(i, v + 10, str(v), color='black', ha='center')

            # Plot after SMOTE
            sns.barplot(x=label_after_smote.index, y=label_after_smote.values, ax=axes[1], palette='pastel')
            axes[1].set_title('Distribusi Label Sesudah SMOTE')
            axes[1].set_xlabel('Stunting (0: Tidak Stunting, 1: Stunting)')
            axes[1].set_ylabel('Jumlah Sampel')
            for i, v in enumerate(label_after_smote.values):
                axes[1].text(i, v + 10, str(v), color='black', ha='center')

            plt.tight_layout()
            st.pyplot(fig_dist)

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menampilkan distribusi label: {e}")
            st.write("Pastikan file pickle distribusi label Anda tersedia dan dalam format `pd.Series`.")

        st.markdown("---")

        # --- Akurasi, Presisi, Recall, F1-Score, dan AUC ---
        st.subheader("Metrik Evaluasi Model")
        st.markdown(
            """
            Berikut adalah performa model prediksi stunting kami berdasarkan berbagai metrik evaluasi
            yang dihitung dari *confusion matrix* dan data *ROC curve*.
            """
        )

        try:
            # Load confusion matrix
            cm_path = 'confusion_matrix.sav'
            if os.path.exists(cm_path):
                with open(cm_path, 'rb') as f:
                    cm = pickle.load(f)

                # Assume cm is a numpy array: [[TN, FP], [FN, TP]]
                tn, fp, fn, tp = cm.ravel()

                accuracy = (tp + tn) / (tp + tn + fp + fn)
                precision = tp / (tp + fp) 
                recall = tp / (tp + fn)
                f1 = 2 * (precision * recall) / (precision + recall)

                metrics = {
                    'Accuracy': accuracy,
                    'Precision': precision,
                    'Recall': recall,
                    'F1-Score': f1
                }

                # --- Display Confusion Matrix ---
                st.write("### Matriks Konfusi")
                # Ukuran figsize diperkecil menjadi (4, 3.5)
                fig_cm, ax_cm = plt.subplots(figsize=(4, 3.5))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                            xticklabels=['Tidak Stunting', 'Stunting'],
                            yticklabels=['Tidak Stunting', 'Stunting'], ax=ax_cm)
                ax_cm.set_xlabel('Prediksi')
                ax_cm.set_ylabel('Aktual')
                ax_cm.set_title('Confusion Matrix')
                st.pyplot(fig_cm)
                plt.close(fig_cm) # Close the plot to prevent it from being displayed twice

            else:
                st.warning(f"File '{cm_path}' tidak ditemukan. Menampilkan metrik placeholder dan tidak ada Confusion Matrix.")
                metrics = {
                    'Accuracy': 0.88,
                    'Precision': 0.85,
                    'Recall': 0.82,
                    'F1-Score': 0.83
                }

            # Load ROC curve data for AUC
            roc_path = 'rocfile.sav' # Your original code uses 'rocfile.sav' for ROC data
            if os.path.exists(roc_path):
                with open(roc_path, 'rb') as f:
                    fpr, tpr, thresholds = pickle.load(f)
                auc_score = auc(fpr, tpr)
                metrics['AUC'] = auc_score

                # --- Display ROC AUC Curve ---
                st.write("### Kurva ROC")
                # Ukuran figsize diperkecil menjadi (5, 4.5)
                fig_roc, ax_roc = plt.subplots(figsize=(5, 4.5))
                ax_roc.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc_score:.2f})')
                ax_roc.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
                ax_roc.set_xlim([0.0, 1.0])
                ax_roc.set_ylim([0.0, 1.05])
                ax_roc.set_xlabel('False Positive Rate')
                ax_roc.set_ylabel('True Positive Rate')
                ax_roc.set_title('Receiver Operating Characteristic (ROC) Curve')
                ax_roc.legend(loc="lower right")
                st.pyplot(fig_roc)
                plt.close(fig_roc) # Close the plot

            else:
                st.warning(f"File '{roc_path}' tidak ditemukan. Menggunakan AUC placeholder dan tidak ada ROC Curve.")
                metrics['AUC'] = 0.91

            metrics_df = pd.DataFrame(metrics.items(), columns=['Metric', 'Value'])
            st.dataframe(metrics_df, hide_index=True)

            st.markdown(
                """
                * **Accuracy:** Proporsi prediksi benar dari total prediksi.
                * **Precision:** Proporsi *true positive* dari total prediksi positif. Penting untuk meminimalkan *false positive* (anak tidak stunting diprediksi stunting).
                * **Recall:** Proporsi *true positive* dari total aktual positif. Penting untuk meminimalkan *false negative* (anak stunting tidak terdeteksi).
                * **F1-Score:** Rata-rata harmonik dari Precision dan Recall, berguna saat ada ketidakseimbangan kelas.
                * **AUC (Area Under the Receiver Operating Characteristic Curve):** Mengukur kemampuan model membedakan antara kelas positif dan negatif. Semakin mendekati 1, semakin baik.
                """
            )

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menampilkan metrik evaluasi model: {e}")
            st.write("Pastikan file pickle *confusion matrix* (`confusion_matrix.sav`) dan data *ROC curve* (`rocfile.sav`) Anda tersedia dan dalam format yang benar.")
        st.markdown("---")

        # --- Feature Importance ---
        st.subheader("Visualisasi Peringkat Fitur (Feature Importance)")
        st.markdown(
            """
            Fitur-fitur dengan nilai "Importance" yang lebih tinggi memiliki dampak yang lebih signifikan
            terhadap hasil prediksi model. Ini menunjukkan atribut mana yang paling berkontribusi
            dalam menentukan risiko stunting.
            """
        )

        try:
            # Ganti 'feature_importance1.sav' dengan path file pickle Anda yang sebenarnya
            if os.path.exists('feature_importance.sav'):
                with open('feature_importance.sav', 'rb') as f:
                    feature_importances_data = pickle.load(f)

                if isinstance(feature_importances_data, dict):
                    df_importance = pd.DataFrame(list(feature_importances_data.items()), columns=['Fitur', 'Importance'])
                elif isinstance(feature_importances_data, pd.Series):
                    df_importance = feature_importances_data.reset_index()
                    df_importance.columns = ['Fitur', 'Importance']
                else:
                    st.warning("Format data feature importance dalam file pickle tidak dikenali. Menampilkan data placeholder.")
                    df_importance = pd.DataFrame({
                        'Fitur': ['Usia Anak (Bulan)', 'Berat Badan (kg)', 'Tinggi Badan (cm)', 'Pendidikan Ibu', 'Panjang Badan Lahir (cm)'],
                        'Importance': [0.35, 0.25, 0.20, 0.10, 0.04]
                    })
            else:
                st.warning("File `feature_importance1.sav` tidak ditemukan. Harap pastikan Anda telah menyimpan data feature importance model Anda dalam file pickle dengan nama tersebut di direktori yang sama, atau sesuaikan path filenya.")
                st.write("Sebagai contoh, berikut adalah tampilan data peringkat fitur placeholder:")
                df_importance = pd.DataFrame({
                    'Fitur': ['Usia Anak (Bulan)', 'Berat Badan (kg)', 'Tinggi Badan (cm)', 'Pendidikan Ibu', 'Panjang Badan Lahir (cm)', 'Riwayat ASI Eksklusif', 'Jenis Kelamin', 'Lingkar Kepala (cm)', 'Berat Badan Lahir (kg)', 'Pendapatan Keluarga (Rp)'],
                    'Importance': [0.35, 0.25, 0.20, 0.10, 0.04, 0.03, 0.02, 0.015, 0.01, 0.005]
                })

            df_importance = df_importance.sort_values(by='Importance', ascending=True)

            fig_width = 16
            fig_height = max(8, len(df_importance) * 0.2)
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))

            sns.barplot(x='Importance', y='Fitur', data=df_importance, palette='magma', ax=ax)

            ax.set_title('Peringkat Pentingnya Fitur Model Prediksi Stunting', fontsize=14, pad=15)
            ax.set_xlabel('Importance', fontsize=10)
            ax.set_ylabel('Fitur', fontsize=10)
            ax.tick_params(axis='both', labelsize=9)

            plt.tight_layout()
            st.pyplot(fig)

            st.dataframe(df_importance.sort_values(by='Importance', ascending=False), hide_index=True)

            st.markdown("""
            **Catatan:**
            * Nilai 'Importance' menunjukkan seberapa besar kontribusi fitur terhadap keputusan model.
            * Semakin tinggi nilainya, semakin penting fitur tersebut dalam memprediksi stunting.
            """)

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memuat atau menampilkan feature importance: {e}")
            st.write("Pastikan file pickle Anda berisi data feature importance yang valid (misalnya, dictionary atau pandas Series).")
        
        st.markdown("---") # Add a separator

        # --- Tabel Referensi Penelitian Stunting ---
        st.subheader("Tabel Referensi Penelitian Stunting")
        st.markdown(
            """
            Berikut adalah referensi penelitian terkait prediksi stunting yang relevan,
            menampilkan metode yang digunakan, hasil akurasi serta ROC-AUC yang dicapai,
            beserta tautan untuk akses jurnal.
            """
        )

        # Create a DataFrame for the references
        # Anda perlu MENGGANTI placeholder URL di bawah dengan URL jurnal yang sebenarnya
        references_data = {
            'Referensi': [
                'Ndagijimana et al., 2023', # <-- GANTI URL INI
                'Ndagijimana et al., 2024', # <-- GANTI URL INI
                'Munyemana et al., 2024', # <-- GANTI URL INI
                'Shen et al., 2023' # <-- GANTI URL INI
            ],
            'Metode / Algoritma': [
                'XGBoost, Random Forest Classifier, Gradient Boost, Logistic Regression, Support Vector Machine, dan Naïve Bayes dengan tuning Grid SearchCV',
                'Artificial Neural Networks',
                'Logistic Regression, Decision Tree, Random Forest, K-Nearest Neighbors dengan tuning Grid SearchCV',
                'Logistic Regression, Ctree, XGBoost, serta model ensemble Support Vector Machine dan Random Forest dengan tuning Grid SearchCV dan Bayesian Optimatization'
            ],
            'Hasil Akurasi & ROC-AUC': [
                'Model XGBoost Akurasi : 79,13% , ROC-AUC sebesar 89%',
                'Model ANN Akurasi  72, ROC-AUC sebesar 84%',
                'Model Random Forest Akurasi 83,98%, ROC-AUC sebesar 82,37%',
                'Model XGBoost + Bayesian Optimatization Akurasi  72,8%, ROC-AUC sebesar 76,7%.'
            ],
            'Link Referensi':[
                'https://doi.org/10.3961/jpmph.22.388',
                'https://f1000research.com/articles/13-128/v1',
                'https://doi.org/10.1186/s40795-024-00903-4',
                'https://www.mdpi.com/2227-9067/10/10/1638',

            ]
        }
        df_references = pd.DataFrame(references_data)
        # --- Mengubah kolom 'Link Referensi' menjadi tautan HTML ---
        # Kita akan membuat DataFrame baru atau memodifikasi yang sudah ada
        # untuk memiliki tautan dalam format HTML <a> tag.
        df_references_html = df_references.copy()

        # Fungsi untuk mengonversi URL menjadi tautan HTML
        def create_clickable_link(url, display_text="Link"):
            # Menggunakan display_text sebagai nama referensi jika kolom Referensi ada dan sesuai
            # atau bisa juga menggunakan 'Link' generik
            return f'<a href="{url}" target="_blank">{display_text}</a>'

        # Terapkan fungsi ke kolom 'Link Referensi'
        # Kita akan gunakan nama referensi sebagai teks tautan jika diinginkan,
        # atau bisa juga pakai teks generik seperti "Lihat Jurnal"
        df_references_html['Link Referensi'] = [
            create_clickable_link(url, df_references['Referensi'][i])
            for i, url in enumerate(df_references_html['Link Referensi'])
        ]

        # --- Menampilkan DataFrame sebagai HTML menggunakan st.markdown ---
        # Konversi DataFrame ke HTML
        # Parameter `escape=False` penting agar tag HTML tidak di-escape dan dirender sebagai teks biasa
        html_table = df_references_html.to_html(escape=False, index=False)

        # Tampilkan HTML tabel di Streamlit
        st.markdown(html_table, unsafe_allow_html=True)


    st.markdown("---")
    st.write("© 2025 Peduli Stunting. Semua hak dilindungi.")
