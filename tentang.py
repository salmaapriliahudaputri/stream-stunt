# tentang.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
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
    tab1, tab2, tab3 = st.tabs(["Prediksi & Atribut Data", "Solusi Penanganan Stunting", "Peringkat Fitur Model"])

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
        st.header("Peringkat Fitur (Feature Importance) Model Prediksi")
        st.markdown(
            """
            Bagian ini menampilkan peringkat pentingnya setiap fitur dalam model prediksi stunting.
            Fitur-fitur dengan nilai "importance" yang lebih tinggi memiliki dampak yang lebih signifikan
            terhadap hasil prediksi model.
            """
        )

        st.subheader("Visualisasi Peringkat Fitur")

        try:
            # Ganti 'feature_importance.sav' dengan path file pickle Anda yang sebenarnya
            # Pastikan file pickle ini berisi dictionary atau Series pandas
            # dengan nama fitur sebagai kunci/indeks dan nilai importance sebagai nilai.
            # Contoh: {'Usia Anak (Bulan)': 0.35, 'Berat Badan (kg)': 0.25, ...}

            # Use os.path.exists to check if the file exists
            models_folder = "model"
            feature_importance_file = "feature_importance1.sav"
            full_path = os.path.join(model_folder, feature_importance_file)
            if os.path.exists('full_path'):
                with open(full_path, 'rb') as f:
                    feature_importances_data = pickle.load(f)

                # Convert to DataFrame for plotting
                if isinstance(feature_importances_data, dict):
                    df_importance = pd.DataFrame(list(feature_importances_data.items()), columns=['Fitur', 'Importance'])
                elif isinstance(feature_importances_data, pd.Series):
                    df_importance = feature_importances_data.reset_index()
                    df_importance.columns = ['Fitur', 'Importance']
                else:
                    st.warning("Format data feature importance dalam file pickle tidak dikenali. Menampilkan data placeholder.")
                    # Placeholder data if format is wrong
                    df_importance = pd.DataFrame({
                        'Fitur': ['Usia Anak (Bulan)', 'Berat Badan (kg)', 'Tinggi Badan (cm)', 'Pendidikan Ibu', 'Panjang Badan Lahir (cm)'],
                        'Importance': [0.35, 0.25, 0.20, 0.10, 0.04]
                    })
            else:
                st.warning("File `feature_importance1.sav` tidak ditemukan. Harap pastikan Anda telah menyimpan data feature importance model Anda dalam file pickle dengan nama tersebut di direktori yang sama, atau sesuaikan path filenya.")
                st.write("Sebagai contoh, berikut adalah tampilan data peringkat fitur placeholder:")
                # Contoh data jika file tidak ditemukan
                df_importance = pd.DataFrame({
                    'Fitur': ['Usia Anak (Bulan)', 'Berat Badan (kg)', 'Tinggi Badan (cm)', 'Pendidikan Ibu', 'Panjang Badan Lahir (cm)', 'Riwayat ASI Eksklusif', 'Jenis Kelamin', 'Lingkar Kepala (cm)', 'Berat Badan Lahir (kg)', 'Pendapatan Keluarga (Rp)'],
                    'Importance': [0.35, 0.25, 0.20, 0.10, 0.04, 0.03, 0.02, 0.015, 0.01, 0.005]
                })

            # Sort the DataFrame from highest to lowest importance for plotting
            # For horizontal bar charts (x=value, y=category), we want to sort ascending
            # so the highest value appears at the top.
            df_importance = df_importance.sort_values(by='Importance', ascending=True)

            # Create the bar chart
            # Adjust figure size dynamically based on number of features
            # A base height of 0.7 units per feature usually gives good spacing
            # For smaller plot, you can reduce the width and the multiplier for height
            fig_width = 16 # Keep width reasonable
            fig_height = max(8, len(df_importance) * 0.2) # Adjust multiplier for height to make it more compact but still legible
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))

            sns.barplot(x='Importance', y='Fitur', data=df_importance, palette='magma', ax=ax)

            ax.set_title('Peringkat Pentingnya Fitur Model Prediksi Stunting', fontsize=14, pad=15) # Adjust title font size and padding
            ax.set_xlabel('Importance', fontsize=10) # Adjust label font size
            ax.set_ylabel('Fitur', fontsize=10) # Adjust label font size
            ax.tick_params(axis='both', labelsize=9) # Adjust tick label font size

            # Adjust padding around the plot to prevent labels from being cut off
            plt.tight_layout()
            st.pyplot(fig) # Display the plot

            st.dataframe(df_importance.sort_values(by='Importance', ascending=False), hide_index=True)

            st.markdown("""
            **Catatan:**
            * Nilai 'Importance' menunjukkan seberapa besar kontribusi fitur terhadap keputusan model.
            * Semakin tinggi nilainya, semakin penting fitur tersebut dalam memprediksi stunting.
            """)

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memuat atau menampilkan feature importance: {e}")
            st.write("Pastikan file pickle Anda berisi data feature importance yang valid (misalnya, dictionary atau pandas Series).")


    st.markdown("---")
    st.write("© 2025 Peduli Stunting. Semua hak dilindungi.")
