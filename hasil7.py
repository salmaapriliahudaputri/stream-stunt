import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import os
import base64
import json
from io import BytesIO

# --- Pemuatan Model, Scaler, dan Dataset Mentah (Menggunakan st.cache_resource) ---
@st.cache_resource
def load_all_resources():
    """
    Memuat scaler, model, dan dataset mentah.
    Fungsi ini akan di-cache oleh Streamlit, sehingga hanya dijalankan sekali saat aplikasi dimulai.
    """
    try:
        # Asumsi file berada di direktori yang sama
        # Pastikan nama dan ekstensi file benar
        scaler = joblib.load('scaler_stunting.sav')
        model = joblib.load('stuting_preduksi.sav') # Pastikan nama file ini benar
        raw_df = pd.read_csv('stunting_dataset.csv') # Pastikan nama file ini benar dan formatnya .csv
        
        return scaler, model, raw_df, True
    except FileNotFoundError as e:
        st.error(f"Error: File tidak ditemukan: {e}. Pastikan file 'scaler_stunting.sav', 'stuting_preduksi.sav', dan 'stunting_dataset.csv' berada di direktori yang sama dengan aplikasi.")
        return None, None, None, False
    except Exception as e:
        st.error(f"Error saat memuat sumber daya: {e}. Pastikan file tidak rusak atau formatnya benar.")
        return None, None, None, False

# Panggil fungsi yang di-cache
load_scaler, load_model, stunting_raw_df, MODEL_LOADED_SUCCESSFULLY = load_all_resources()

# --- Definisikan urutan kolom tampilan yang konsisten ---
DISPLAY_COLUMN_ORDER = [
    'child_name', # Kolom baru: Nama Anak
    'chAge', 'chSex', 'chSize', 'chBw', 'db', 'breaststart', 'chDiar', 'chDrug',
    'MmAge', 'MmEdu', 'MomWork', 'Mmstat', 'MmHeight', 'BMI','region',
    'nChild', 'residence', 'wi', 'water', 'toilet', 'altitudes', 'reading', 'tv', 'radio',
    'Status Prediksi', 'Probabilitas Normal (%)', 'Probabilitas Stunting (%)', 'Saran dan Solusi'
]


# --- Fungsi untuk mendapatkan saran berdasarkan input dan prediksi ---
def get_stunting_advice(input_data_row, prediction_status):
    advice = []
    
    # Tambahkan nama anak ke awal saran jika tersedia
    child_name = input_data_row.get('child_name', 'Balita Ini') 
    
    if prediction_status == 'Stunting':
        advice.append(f"{child_name} diprediksi mengalami **stunting**. Intervensi segera sangat disarankan. Berikut adalah beberapa faktor yang mungkin berkontribusi dan saran terkait:")

        chAge_val = pd.to_numeric(input_data_row.get('chAge', ''), errors='coerce')
        if not pd.isna(chAge_val) and chAge_val < 24:
            advice.append(f"- **Usia Anak ({int(chAge_val)} bulan):** Pastikan asupan gizi yang adekuat, terutama di 1000 Hari Pertama Kehidupan (HPK). Fokus pada ASI eksklusif hingga 6 bulan dan MPASI yang bergizi dan bervariasi setelahnya.")
        if input_data_row.get('chSex') == 'f':
            advice.append(f"- **Jenis Kelamin Anak ({input_data_row.get('chSex')}):** Meskipun jenis kelamin tidak langsung menyebabkan stunting, pada beberapa kasus, anak perempuan mungkin kurang mendapat perhatian gizi dibandingkan anak laki-laki. Pastikan semua anak mendapat perhatian gizi yang sama.")
        if input_data_row.get('chSize') in ['small', 'average']:
            advice.append(f"- **Ukuran Anak Saat Lahir ({input_data_row.get('chSize')}):** Berat lahir rendah (small/average) meningkatkan risiko stunting. Perlu pemantauan pertumbuhan yang lebih ketat.")
        if input_data_row.get('chBw') == 'less then 2.5':
            advice.append(f"- **Berat Anak Saat Lahir ({input_data_row.get('chBw')} kg):** Berat lahir rendah (<2.5 kg) adalah faktor risiko tinggi. Pastikan nutrisi pasca-kelahiran optimal dan pantau pertumbuhan secara rutin.")
        if input_data_row.get('db') != 'still breastfeeding':
            advice.append(f"- **Status Menyusui Anak ({input_data_row.get('db')}):** ASI eksklusif sangat penting. Jika tidak menyusui, pastikan alternatif nutrisi yang memadai dan higienis.")
        if input_data_row.get('breaststart') != '1hr':
            advice.append(f"- **Waktu Anak Mendapat ASI Pertama Kali ({input_data_row.get('breaststart')}):** Inisiasi Menyusu Dini (IMD) penting. Jika IMD tertunda, pastikan dukungan laktasi yang kuat.")
        if input_data_row.get('chDiar') == 'yes':
            advice.append(f"- **Anak Mengalami Diare ({input_data_row.get('chDiar')}):** Diare berulang dapat menghambat penyerapan nutrisi. Tingkatkan kebersihan, akses air bersih, dan segera obati diare.")
        if input_data_row.get('chDrug') == 'no':
            advice.append(f"- **Anak Mengonsumsi Obat Parasit ({input_data_row.get('chDrug')}):** Jika anak tidak minum obat parasit, pertimbangkan untuk berkonsultasi dengan tenaga medis tentang pemberian obat cacing teratur di daerah endemis.")

        MmAge_val = pd.to_numeric(input_data_row.get('MmAge', ''), errors='coerce')
        if not pd.isna(MmAge_val) and (MmAge_val < 20 or MmAge_val > 35):
            advice.append(f"- **Usia Ibu ({int(MmAge_val)} tahun):** Kehamilan di usia terlalu muda atau terlalu tua dapat mempengaruhi kesehatan janin dan kemampuan ibu merawat anak. Pastikan ibu mendapat dukungan kesehatan yang komprehensif.")
        if input_data_row.get('MmEdu') in ['no', 'primary']:
            advice.append(f"- **Pendidikan Terakhir Ibu ({input_data_row.get('MmEdu')}):** Tingkat pendidikan ibu yang lebih rendah seringkali berkorelasi dengan kurangnya pengetahuan gizi. Berikan edukasi gizi dan kesehatan secara berkelanjutan.")
        if input_data_row.get('MomWork') == 'yes':
            advice.append(f"- **Status Ibu Bekerja ({input_data_row.get('MomWork')}):** Ibu bekerja mungkin memiliki waktu terbatas. Pastikan ketersediaan pengasuhan yang berkualitas dan makanan bergizi yang mudah diakses.")
        if input_data_row.get('Mmstat') in ['single', 'separated']:
            advice.append(f"- **Status Pernikahan Ibu ({input_data_row.get('Mmstat')}):** Ibu tunggal atau berpisah mungkin menghadapi tantangan ekonomi dan dukungan sosial. Berikan dukungan sosial dan akses ke program bantuan.")
        MmHeight_val = pd.to_numeric(input_data_row.get('MmHeight', ''), errors='coerce')
        if not pd.isna(MmHeight_val) and MmHeight_val < 150:
            advice.append(f"- **Tinggi Badan Ibu ({MmHeight_val} cm):** Tinggi badan ibu yang pendek (<150cm) bisa menjadi indikator riwayat gizi buruk pada ibu, yang dapat mempengaruhi pertumbuhan anak. Perlu perhatian khusus pada gizi ibu selama kehamilan dan menyusui.")
        if input_data_row.get('BMI') in ['uderweight', 'Overeight', 'obses']:
            advice.append(f"- **Body Mass Index Ibu ({input_data_row.get('BMI')}):** Berat badan ibu yang kurang atau berlebih (underweight/overweight/obese) sebelum atau selama kehamilan dapat memengaruhi kesehatan dan pertumbuhan anak. Edukasi gizi dan gaya hidup sehat untuk ibu.")
        # Perbaikan: 'more than 3' seharusnya bukan kategori region, ini perlu dikoreksi berdasarkan data aktual Anda
        # Jika 'more than 3' adalah kategori yang salah di sini, pertimbangkan untuk menghapusnya atau mengoreksinya.
        # Asumsi 'est' adalah kategori region yang valid untuk saran ini.
        if input_data_row.get('region') in ['est']:
            advice.append(f"- **Provinsi ({input_data_row.get('region')}):** Cek Fasilitas infrastruktur publik terdekat.")

        if input_data_row.get('nChild') in ['2 child', 'more than 3']:
            advice.append(f"- **Jumlah Anak dalam Keluarga ({input_data_row.get('nChild')}):** Jumlah anak yang banyak dapat membagi sumber daya. Pastikan setiap anak mendapat porsi gizi dan perhatian yang cukup.")
        if input_data_row.get('residence') == 'rural':
            advice.append(f"- **Domisili ({input_data_row.get('residence')}):** Area pedesaan seringkali memiliki akses terbatas terhadap fasilitas kesehatan dan pangan bergizi. Perkuat program gizi di tingkat komunitas.")
        if input_data_row.get('wi') == 'poor':
            advice.append(f"- **Index Kekayaan ({input_data_row.get('wi')}):** Status ekonomi 'poor' adalah faktor risiko utama. Dukungan program pangan, bantuan tunai, dan edukasi tentang pemanfaatan sumber daya.")
        if input_data_row.get('water') == 'unimproved':
            advice.append(f"- **Kondisi Saluran Air di Rumah ({input_data_row.get('water')}):** Akses ke air bersih yang tidak 'improved' meningkatkan risiko penyakit. Tingkatkan akses ke sumber air bersih dan edukasi kebersihan.")
        if input_data_row.get('toilet') == 'unimproved':
            advice.append(f"- **Kondisi Toilet dalam Rumah ({input_data_row.get('toilet')}):** Sanitasi yang buruk meningkatkan risiko infeksi. Promosikan penggunaan toilet 'improved' dan kebiasaan cuci tangan.")
        if input_data_row.get('altitudes') == ">2000":
            advice.append(f"- **Ketinggian Tempat Tinggal ({input_data_row.get('altitudes')}):** Ketinggian di atas 2000 mdpl dapat mempengaruhi ketersediaan pangan dan kesehatan pernapasan. Perlu strategi gizi yang disesuaikan dengan kondisi lokal.")
        if input_data_row.get('reading') == 'no' or input_data_row.get('tv') == 'no' or input_data_row.get('radio') == 'no':
            advice.append(f"- **Akses Informasi (Koran: {input_data_row.get('reading')}, TV: {input_data_row.get('tv')}, Radio: {input_data_row.get('radio')}):** Keterbatasan akses informasi dapat membatasi pengetahuan tentang gizi dan kesehatan. Manfaatkan berbagai media untuk edukasi kesehatan.")
    else: # Prediction is Normal
        advice.append(f"{child_name} diprediksi **tidak stunting**. Terus pertahankan pola asuh dan gizi yang baik.")
        
        advice.append("- **Nutrisi Optimal:** Pastikan asupan gizi seimbang sesuai usia, termasuk protein hewani, sayur, dan buah-buahan.")
        advice.append("- **Pemantauan Pertumbuhan:** Lakukan penimbangan dan pengukuran tinggi/panjang badan secara rutin di Posyandu atau fasilitas kesehatan.")
        advice.append("- **Higienitas:** Jaga kebersihan lingkungan, makanan, dan pribadi untuk mencegah infeksi.")
        advice.append("- **Stimulasi Dini:** Berikan stimulasi yang cukup untuk perkembangan kognitif dan motorik anak.")
        
        if input_data_row.get('chDiar') == 'yes':
            advice.append(f"- **Anak Mengalami Diare ({input_data_row.get('chDiar')}):** Meskipun tidak stunting saat ini, diare berulang dapat meningkatkan risiko di kemudian hari. Tetap perhatikan kebersihan dan penanganan diare yang cepat.")
        if input_data_row.get('chBw') == 'less then 2.5':
            advice.append(f"- **Berat Anak Saat Lahir ({input_data_row.get('chBw')} kg):** Anak dengan berat lahir rendah (<2.5 kg) tetap perlu perhatian khusus dan pemantauan pertumbuhan yang ketat meskipun saat ini tidak stunting.")
    
    return "\n".join(advice)

# --- Fungsi untuk mendapatkan riwayat prediksi (TIDAK LAGI DARI FIREBASE) ---
# Karena kita tidak menyimpan ke database, fungsi ini sekarang hanya akan mengembalikan data kosong.
# Jika Anda ingin menyimpan riwayat secara lokal (misalnya di session_state), logika di sini perlu diubah.
@st.cache_data(ttl=3600) 
def get_prediction_history(user_uid_param, _db_param):
    """
    Mengambil riwayat prediksi. Karena penyimpanan database dihapus, fungsi ini akan selalu kosong.
    """
    st.info("Fitur riwayat prediksi tidak aktif karena penyimpanan database dinonaktifkan.")
    return []

# --- Fungsi Utama Aplikasi Streamlit ---
def app(db, user_info): # Parameter db dan user_info masih ada tapi tidak digunakan untuk penyimpanan
    if not MODEL_LOADED_SUCCESSFULLY:
        st.warning("Aplikasi tidak dapat berfungsi penuh karena model, scaler, atau dataset gagal dimuat. Harap periksa file-file tersebut.")
        return

    user_uid = user_info['localId'] if user_info and 'localId' in user_info else None

    # Jika Anda tidak menggunakan user_uid untuk Firebase, baris ini bisa dihilangkan
    # atau disesuaikan jika ada autentikasi lain.
    if not user_uid:
        st.error("Tidak dapat mengakses data pengguna. Pastikan Anda sudah login.")
        return

    # Pastikan logo_path dan logo_src diatur dengan benar
    logo_path = os.path.join(".", "pp.JPG") # Sesuaikan path sesuai lokasi file gambar Anda
    logo_src = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        logo_src = f"data:image/png;base64,{encoded_string}"
    else:
        # Fallback jika gambar tidak ditemukan
        logo_src = "https://placehold.co/40x40/FFFFFF/F36DA8?text=PP" 

    username_to_display = user_info.get('username', 'User')

    # --- Bagian CSS dan Header Aplikasi ---
    st.markdown(f"""
        <style>
        div.stButton > button:nth-child(1) {{
            background-color: #612C43;
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
            transition: background-color 0.3s ease;
        }}

        div.stButton > button:nth-child(1):hover {{
            background-color: #F36DA8;
            color: white;
        }}

        .stForm button {{
            background-color: #612C43;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            font-size: 16px;
            margin: 4px 2px;
        }}
        .stForm button:hover {{
            background-color: #F36DA8;
        }}

        .app-header {{
            display: flex;
            justify-content: flex-end;
            padding: 10px 20px;
            background-color: #F36DA8;
            color: white;
            border-radius: 8px;
            margin-bottom: 2em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            width: calc(100% + 40px);
            margin-left: -20px;
            margin-top: -10px;
        }}
        .header-item {{
            display: flex;
            align-items: center;
            margin-left: 15px;
        }}
        .profile-pic {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
            object-fit: cover;
            border: 2px solid white;
        }}
        .username {{
            font-weight: bold;
        }}
        .notification-icon {{
            font-size: 1.5em;
            margin-right: 10px;
            cursor: pointer;
        }}
        .stunting-card {{
            background-color: #f0f2f6;
            border-left: 5px solid #612C43;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stunting-card h4 {{
            color: #F36DA8;
            margin-top: 0;
            margin-bottom: 10px;
        }}
        .stunting-card p {{
            margin-bottom: 5px;
            font-size: 0.95em;
        }}
        .stunting-card .status-normal {{
            color: #28a745;
            font-weight: bold;
        }}
        .stunting-card .status-stunting {{
            color: #dc3545;
            font-weight: bold;
        }}
        .card-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}
        .card-buttons .stButton button {{
            padding: 8px 12px;
            font-size: 0.85em;
            border-radius: 5px;
        }}
        .card-buttons .stButton button:first-child {{
            background-color: #28a745;
        }}
        .card-buttons .stButton button:first-child:hover {{
            background-color: #218838;
        }}
        .card-buttons .stButton button:last-child {{
            background-color: #dc3545;
        }}
        .card-buttons .stButton button:last-child:hover {{
            background-color: #c82333;
        }}
        .advice-list {{
            list-style-type: none;
            padding-left: 0;
        }}
        .advice-list li {{
            margin-bottom: 5px;
        }}
        </style>
        """, unsafe_allow_html=True)
    
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

    st.write("""
    # Prediksi Status Stunting Balita
    Aplikasi berbasis web untuk memprediksi status stunting balita.
    """)

    if 'manual_inputs_list' not in st.session_state:
        st.session_state.manual_inputs_list = []
    
    input_type = "Tidak Ada"

    tab1, tab2 = st.tabs(["Input dan Hasil Prediksi", " "])

    with tab1:
        upload_file = st.file_uploader('Upload file Excel Anda (opsional)', type=['xlsx', 'xls'])

        inputan = None

        if upload_file is not None:
            try:
                inputan = pd.read_excel(upload_file)
                st.success("File berhasil diunggah!")
                st.session_state.manual_inputs_list = [] # Clear manual inputs if file is uploaded
                input_type = "File Excel"
            except Exception as e:
                st.error(f"Error saat membaca file Excel: {e}. Pastikan format file benar.")
                inputan = None
                input_type = "Error Unggah File"
        else:
            st.subheader("Atau Masukkan Data Secara Manual:")
            
            with st.form("manual_data_input_form", clear_on_submit=True):
                st.title("Data Anak")
                child_name = st.text_input('Nama Anak', value='', key='child_name_input')
                chAge = st.text_input('Usia Anak *(dalam satuan bulan)*', value='', key='chAge_input')
                chSex = st.selectbox('Jenis Kelamin Anak *(m:laki-laki, f:perempuan)*', ('','m', 'f'), key='chSex_input')
                chSize = st.selectbox('Ukuran Anak Saat Lahir ', ('','average','large','small'), key='chSize_input')
                chBw = st.selectbox('Berat Anak Saat Lahir', ('','more than 2.5','less then 2.5'), key='chBw_input')
                db_status = st.selectbox('Status Anak Menyusui Saat ini', ('','ever breastfed, not currently breastfeeding','still breastfeeding','never breastfed'), key='db_input')
                breaststart = st.selectbox('Waktu Anak Mendapat ASI Pertama Kali',('','1hr','1-24hr','30day'), key='breaststart_input')
                chDiar = st.selectbox('Anak Mengalami Diare 2 Minggu Terakhir', ('','yes','no'), key='chDiar_input')
                chDrug = st.selectbox('Anak Mengonsumsi Obat Parasit 2 Minggu Terakhir',('','yes','no'), key='chDrug_input')

                st.title("Data Ibu")
                MmAge = st.text_input('Usia Ibu *(dalam satuan tahun)*', value='', key='MmAge_input')
                MmEdu = st.selectbox('Pendidikan Terakhir Ibu', ('','no', 'primary', 'second or higher'), key='MmEdu_input')
                MomWork = st.selectbox('Status Ibu Bekerja', ('','yes','no'), key='MomWork_input')
                Mmstat = st.selectbox('Status Pernikahan Ibu', ['','married', 'single','separated'], key='Mmstat_input')
                MmHeight = st.text_input('Tinggi Badan Ibu dalam centimeter (cm)', value='', key='MmHeight_input')
                BMI = st.selectbox('Body Mass Index Ibu',('','normal','obses','uderweight','Overeight'), key='BMI_input')

                st.title("Data Rumah Tinggal")
                region = st.selectbox('provinsi',('','est','kigali','north','south','west'), key ='region_input')
                nChild = st.selectbox('Jumlah Anak dalam Keluarga',('','1 child','2 child','more than 3'), key='nChild_input')
                residence = st.selectbox('Domisili *(urban: kota, rural: desa)*', ('','urban', 'rural'), key='residence_input')
                wi = st.selectbox('Index Kekayaan', ('','poor', 'middle', 'rich'), key='wi_input')
                water = st.selectbox('Kondisi Saluran Air di Rumah', ('','improved', 'unimproved'), key='water_input')
                toilet = st.selectbox('Kondisi Toilet dalam Rumah', ('','improved', 'unimproved'), key='toilet_input')
                altitudes = st.selectbox('Ketinggian Tempat Tinggal',('',"<=2000",">2000"), key='altitudes_input')
                reading = st.selectbox('Media Informasi Dari Koran',('','yes','no'), key='reading_input')
                tv = st.selectbox('Media Informasi Dari Televisi',('','yes','no'), key='tv_input')
                radio = st.selectbox('Media Informasi Dari Radio', ('','yes','no'), key='radio_input')

                add_data_button = st.form_submit_button("Tambah Data Ini")

                if add_data_button:
                    current_data = {
                        'child_name': child_name,
                        'MmHeight': MmHeight, 'chAge': chAge, 'wi': wi, 'tv': tv, 'radio': radio,
                        'MmEdu': MmEdu, 'chSize': chSize, 'chDrug': chDrug, 'chBw': chBw,
                        'region':region,
                        'toilet': toilet, 'breaststart': breaststart,
                        'MmAge': MmAge, 'residence': residence, 'db': db_status, 'altitudes': altitudes, 
                        'BMI': BMI, 'reading': reading, 'chSex': chSex, 'nChild': nChild,
                        'Mmstat': Mmstat, 'MomWork': MomWork, 'water': water, 'chDiar': chDiar
                    }
                    # Perbaikan: Validasi minimal satu input terisi selain child_name
                    # Ini akan memeriksa jika ada nilai yang tidak kosong atau bukan NaN
                    if any(value != '' and not pd.isna(value) for key, value in current_data.items() if key != 'child_name'):
                        st.session_state.manual_inputs_list.append(current_data)
                        st.success("Data berhasil ditambahkan! Tambahkan data lain atau lakukan prediksi.")
                    else:
                        st.warning("Semua input kosong. Tidak ada data yang ditambahkan.")
            
            if st.session_state.manual_inputs_list:
                st.subheader("Data yang Sudah Ditambahkan (Input Manual):")
                inputan = pd.DataFrame(st.session_state.manual_inputs_list)
                st.dataframe(inputan)
                input_type = "Input Manual"
                if st.button("Hapus Semua Data Manual", key="clear_manual_data"):
                    st.session_state.manual_inputs_list = []
                    st.rerun()
            else:
                st.info("Anda belum menambahkan data secara manual. Silakan isi form di atas dan klik 'Tambah Data Ini'.")
                inputan = None

        status_balita_labels = np.array(['Normal', 'Stunting'])
        prediction_status_message = "Menunggu input data dan klik 'Lakukan Prediksi'..."
        prediction_success = False
        
        st.subheader('Parameter Inputan')
        if inputan is not None and not inputan.empty:
            if 'child_name' in inputan.columns and 'Status Prediksi' not in inputan.columns:
                st.dataframe(inputan) 
            else:
                columns_to_display = [col for col in DISPLAY_COLUMN_ORDER if col in inputan.columns]
                st.dataframe(inputan[columns_to_display]) 
        else:
            st.info('Silakan unggah file Excel atau masukkan data secara manual di atas.')

        if st.button("Lakukan Prediksi", disabled=not MODEL_LOADED_SUCCESSFULLY):
            if not MODEL_LOADED_SUCCESSFULLY:
                prediction_status_message = "❌ Model atau scaler tidak dapat dimuat. Prediksi tidak bisa dilakukan."
                st.error(prediction_status_message)
            else:
                if inputan is None or inputan.empty:
                    prediction_status_message = "⚠️ Tidak ada data input. Silakan unggah file atau masukkan data manual."
                    st.warning(prediction_status_message)
                else:
                    inputan_original_for_advice = inputan.copy() 

                    if isinstance(inputan, pd.DataFrame) and upload_file is None:
                        initial_rows_count = len(inputan)
                        # Perbaikan: Menggunakan pendekatan yang lebih vektorisasi untuk mendeteksi baris kosong
                        # Menganggap baris kosong jika semua kolom, kecuali 'child_name', adalah string kosong atau NaN
                        cols_for_empty_check = [col for col in inputan.columns if col != 'child_name']
                        
                        # Pastikan semua kolom yang diperiksa adalah string untuk strip(), lalu periksa ke-kosongan
                        # atau periksa apakah itu NaN
                        empty_rows_mask = (inputan[cols_for_empty_check].astype(str).apply(lambda x: x.str.strip() == '')).all(axis=1) | \
                                          (inputan[cols_for_empty_check].isnull().all(axis=1))
                                          
                        inputan = inputan[~empty_rows_mask].reset_index(drop=True)
                        
                        if initial_rows_count > len(inputan):
                            st.info(f"Menghapus {initial_rows_count - len(inputan)} baris kosong dari input manual sebelum prediksi.")
                        
                        if inputan.empty:
                            prediction_status_message = "⚠️ Tidak ada data input yang valid setelah menghapus baris kosong. Silakan unggah file atau masukkan data manual."
                            st.warning(prediction_status_message)
                            inputan = None
                    
                    if inputan is not None and not inputan.empty:
                        inputan_to_process = inputan.copy()
                        if 'child_name' in inputan_to_process.columns:
                            inputan_to_process = inputan_to_process.drop(columns=['child_name'])
                        
                        # Perbaikan: Mengisi nilai kosong di DataFrame sebelum one-hot encoding dan scaling
                        # Mengganti string kosong menjadi NaN untuk penanganan yang lebih baik
                        inputan_to_process.replace('', np.nan, inplace=True) 

                        # Pastikan semua kolom kategorikal ditangani dengan benar
                        # Pastikan stunting_raw_df sudah dimuat dengan benar
                        if stunting_raw_df is None:
                            st.error("Dataset mentah tidak tersedia. Tidak bisa menentukan kolom kategorikal untuk encoding.")
                            prediction_status_message = "❌ Dataset mentah tidak dimuat."
                            st.error(prediction_status_message)
                            return

                        all_categorical_cols = [col for col in stunting_raw_df.columns if stunting_raw_df[col].dtype == 'object' and col != 'status']
                        
                        # Buat dummy template dari seluruh dataset mentah untuk memastikan semua kolom dummy ada
                        # Ini adalah langkah krusial untuk memastikan konsistensi fitur dengan model yang dilatih.
                        # Ini mungkin memakan waktu jika stunting_raw_df sangat besar.
                        dummy_template = pd.get_dummies(stunting_raw_df.drop(columns=['status'], errors='ignore'), columns=all_categorical_cols, prefix=all_categorical_cols)
                        
                        # Lakukan one-hot encoding pada inputan pengguna
                        # Ini juga bisa memakan waktu tergantung pada ukuran inputan_to_process dan jumlah kolom kategorikal
                        input_df_encoded = pd.get_dummies(inputan_to_process, columns=all_categorical_cols, prefix=all_categorical_cols)
                        
                        # Sesuaikan kolom inputan yang sudah di-encode dengan template dummy
                        # Ini penting untuk memastikan jumlah dan urutan fitur sesuai dengan yang dilatih oleh model
                        df_processed = input_df_encoded.reindex(columns=dummy_template.columns, fill_value=0)

                        numeric_cols = ['MmHeight', 'chAge', 'MmAge'] 
                        for col in numeric_cols:
                            if col in df_processed.columns:
                                df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')

                        for col in numeric_cols:
                            if col in df_processed.columns and df_processed[col].isnull().any():
                                median_val = stunting_raw_df[col].median()
                                df_processed[col].fillna(median_val, inplace=True)
                                st.info(f"Kolom numerik '{col}' memiliki nilai hilang, diisi dengan median dari dataset training: {median_val}")
                        
                        try:
                            # Perbaikan: Ambil feature_names_in_ dari scaler jika tersedia
                            expected_features = load_scaler.feature_names_in_
                        except AttributeError:
                            st.warning("Scaler tidak memiliki attribute 'feature_names_in_'. Menggunakan daftar fitur default. Pastikan ini sesuai dengan model Anda.")
                            # Ini adalah fallback jika scaler tidak memiliki feature_names_in_
                            # Daftar ini harus sesuai dengan fitur yang digunakan saat melatih model
                            # Pastikan daftar ini SELALU SAMA dengan fitur yang digunakan saat training model
                            expected_features = [
                                'MmHeight', 'chAge', 'MmAge',
                                'wi_middle', 'wi_poor', 'wi_rich',
                                'tv_no', 'tv_yes',
                                'radio_no', 'radio_yes',
                                'MmEdu_no', 'MmEdu_primary', 'MmEdu_second or higher',
                                'chSize_average', 'chSize_large', 'chSize_small',
                                'chDrug_no', 'chDrug_yes',
                                'chBw_less then 2.5', 'chBw_more than 2.5',
                                'region_est', 'region_kigali', 'region_north', 'region_south', 'region_west', # Pastikan kolom region yang sesuai
                                'toilet_improved', 'toilet_unimproved',
                                'breaststart_1-24hr', 'breaststart_1hr', 'breaststart_30day',
                                'residence_rural', 'residence_urban',
                                'db_ever breastfed, not currently breastfeeding', 'db_never breastfed', 'db_still breastfeeding',
                                'altitudes_<=2000', 'altitudes_>2000',
                                'BMI_normal', 'BMI_obses', 'BMI_uderweight', 'BMI_Overeight', # Pastikan urutan dan penulisan sama dengan saat training
                                'reading_no', 'reading_yes',
                                'chSex_f', 'chSex_m',
                                'nChild_1 child', 'nChild_2 child', 'nChild_more than 3',
                                'Mmstat_married', 'Mmstat_separated', 'Mmstat_single',
                                'MomWork_no', 'MomWork_yes',
                                'water_improved', 'water_unimproved',
                                'chDiar_no', 'chDiar_yes'
                            ]
                        
                        # Reindex ulang DataFrame agar memiliki semua kolom yang diharapkan oleh scaler
                        # dan urutannya sesuai dengan yang digunakan saat pelatihan model.
                        df_final_for_prediction = df_processed.reindex(columns=expected_features, fill_value=0)

                        if df_final_for_prediction.isnull().any().any():
                            prediction_status_message = "❌ Input data tidak lengkap atau tidak valid setelah pemrosesan (ada nilai NaN yang tersisa). Prediksi tidak dapat dilakukan."
                            st.error(prediction_status_message)
                        else:
                            try:
                                scaled = load_scaler.transform(df_final_for_prediction)
                                predik_array = load_model.predict(scaled)
                                prediksi_proba_array = load_model.predict_proba(scaled)
                                
                                inputan['Status Prediksi'] = [status_balita_labels[p] for p in predik_array]
                                inputan['Probabilitas Normal (%)'] = [f"{proba[0]*100:.2f}" for proba in prediksi_proba_array]
                                inputan['Probabilitas Stunting (%)'] = [f"{proba[1]*100:.2f}" for proba in prediksi_proba_array]

                                advices_for_df = []
                                for idx, row in inputan.iterrows():
                                    # Menggunakan baris dari inputan_original_for_advice untuk saran
                                    advice_text = get_stunting_advice(inputan_original_for_advice.iloc[idx].to_dict(), row['Status Prediksi'])
                                    advices_for_df.append(advice_text)
                                
                                inputan['Saran dan Solusi'] = advices_for_df

                                prediction_status_message = "✅ Prediksi berhasil!"
                                prediction_success = True

                                # --- Bagian ini dihapus/dinonaktifkan untuk menghentikan penyimpanan ke Firebase ---
                                # current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                # prediction_entry = {
                                #     'Timestamp': current_timestamp,
                                #     'Input_Type': input_type,
                                #     'Data_Prediksi': inputan.to_dict(orient='records')
                                # }
                                # try:
                                #     if db:
                                #         db.child(user_uid).child("predictions").push(prediction_entry)
                                #         st.success("Hasil prediksi berhasil disimpan ke database!")
                                #         get_prediction_history.clear() 
                                #     else:
                                #         st.warning("Objek database tidak tersedia. Hasil prediksi tidak disimpan.")
                                # except Exception as firebase_e:
                                #     st.error(f"Gagal menyimpan prediksi ke database: {firebase_e}")

                            except Exception as e:
                                prediction_status_message = f"Terjadi kesalahan saat melakukan prediksi: {e}. Periksa format data atau model."
                                st.error(prediction_status_message)

        st.markdown(f"**Status Prediksi:** {prediction_status_message}")

        if prediction_success and inputan is not None and not inputan.empty:
            st.subheader("Hasil Prediksi:")
            columns_to_display = [col for col in DISPLAY_COLUMN_ORDER if col in inputan.columns]
            st.dataframe(inputan[columns_to_display])

            st.subheader("Saran dan Solusi Berdasarkan Prediksi:")
            # Jika jumlah baris prediksi sangat banyak, rendering detail saran satu per satu
            # di sini bisa memperlambat aplikasi. Pertimbangkan untuk membatasi tampilan atau
            # menyediakan opsi "Lihat Detail" jika ini menjadi bottleneck.
            for idx, row in inputan.iterrows():
                card_class = "status-stunting" if row['Status Prediksi'] == 'Stunting' else "status-normal"
                child_name_display = row.get('child_name', f'Balita {idx + 1}')
                st.markdown(
                    f"""
                    <div class="stunting-card">
                        <h4>Data {child_name_display} - Status: <span class="{card_class}">{row['Status Prediksi']}</span></h4>
                        <p>Probabilitas Normal: {row['Probabilitas Normal (%)']}%</p>
                        <p>Probabilitas Stunting: {row['Probabilitas Stunting (%)']}%</p>
                        <ul class="advice-list">
                    """, unsafe_allow_html=True
                )
                advice_content = row.get('Saran dan Solusi', 'Tidak ada saran.')
                if pd.isna(advice_content):
                    advice_content = 'Tidak ada saran yang dihasilkan.'

                for advice_line in advice_content.split('\n'):
                    st.markdown(f"<li>{advice_line}</li>", unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # --- Tab Riwayat Prediksi ---
    with tab2:
        st.header("Riwayat Prediksi")
        
        # Tombol refresh riwayat (sekarang tidak relevan untuk data dari DB)
        if st.button("Refresh Riwayat"):
            get_prediction_history.clear() # Cache akan selalu kosong
            st.rerun() 

        # --- Muat riwayat prediksi (akan selalu kosong) ---
        prediction_history_from_db = get_prediction_history(user_uid, db)

        if not prediction_history_from_db:
            st.info("Fitur riwayat prediksi tidak aktif karena penyimpanan database dinonaktifkan.")
        else:
            # Bagian ini tidak akan pernah dieksekusi jika `get_prediction_history` selalu kosong
            combined_df_for_download = pd.DataFrame()

            for i, (firebase_key, entry) in enumerate(prediction_history_from_db):
                timestamp = entry.get('Timestamp', 'N/A')
                input_type = entry.get('Input_Type', 'N/A')
                data_prediksi_list = entry.get('Data_Prediksi', [])

                data_prediksi = pd.DataFrame(data_prediksi_list)

                st.markdown(f"""
                    <div class="stunting-card">
                        <h4>Riwayat #{i+1} - <small>{timestamp}</small></h4>
                        <p>Tipe Input: <strong>{input_type}</strong></p>
                        <p>Jumlah Data Diprediksi: <strong>{len(data_prediksi_list)}</strong></p>
                        """, unsafe_allow_html=True)

                normal_count = 0
                stunting_count = 0
                if not data_prediksi.empty and 'Status Prediksi' in data_prediksi.columns:
                    status_counts = data_prediksi['Status Prediksi'].value_counts()
                    normal_count = status_counts.get('Normal', 0)
                    stunting_count = status_counts.get('Stunting', 0)
                
                st.markdown(f"""
                    <p>Jumlah Balita Normal: <strong>{normal_count}</strong></p>
                    <p>Jumlah Balita Stunting: <strong>{stunting_count}</strong></p>
                    """, unsafe_allow_html=True)
                
                with st.expander(f"Lihat Detail Data Prediksi untuk Riwayat #{i+1}"):
                    if not data_prediksi.empty:
                        # Perbaikan: Pastikan kolom yang ditampilkan ada di data_prediksi
                        cols_to_display_in_history = [col for col in DISPLAY_COLUMN_ORDER if col in data_prediksi.columns]
                        data_prediksi_display = data_prediksi[cols_to_display_in_history]
                        st.dataframe(data_prediksi_display)
                        st.markdown("---")
                        st.subheader("Saran dan Solusi:")
                        for idx, row in data_prediksi.iterrows():
                            card_class = "status-stunting" if row.get('Status Prediksi') == 'Stunting' else "status-normal"
                            child_name_display = row.get('child_name', f'Balita {idx + 1}')
                            st.markdown(
                                f"""
                                <p>Data {child_name_display} - Status: <span class="{card_class}">{row.get('Status Prediksi', 'N/A')}</span></p>
                                <ul class="advice-list">
                            """, unsafe_allow_html=True
                            )
                            advice_content = row.get('Saran dan Solusi', 'Tidak ada saran.')
                            if pd.isna(advice_content): # Handle NaN for advice
                                advice_content = 'Tidak ada saran yang dihasilkan.'
                            for advice_line in advice_content.split('\n'):
                                st.markdown(f"<li>{advice_line}</li>", unsafe_allow_html=True)
                            st.markdown("</ul>")
                    else:
                        st.info("Tidak ada data detail untuk riwayat ini.")

                st.markdown(
                    f"""
                    <div class="card-buttons">
                    """, unsafe_allow_html=True
                )
                
                if not data_prediksi.empty:
                    excel_buffer = BytesIO()
                    # Perbaikan: Gunakan cols_to_display_in_history untuk download juga
                    data_prediksi[cols_to_display_in_history].to_excel(excel_buffer, index=False, engine='xlsxwriter')
                    excel_buffer.seek(0)

                    st.download_button(
                        label="Download Data ini",
                        data=excel_buffer.getvalue(),
                        file_name=f"prediksi_stunting_{timestamp.replace(':', '-')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_history_{firebase_key}"
                    )

                # --- Tombol "Hapus Riwayat ini" juga tidak akan berfungsi karena tidak ada penyimpanan DB ---
                if st.button("Hapus Riwayat ini", key=f"delete_history_{firebase_key}"):
                    st.warning("Fitur penghapusan riwayat tidak aktif karena penyimpanan database dinonaktifkan.")
                    # try:
                    #     if db:
                    #         db.child(user_uid).child("predictions").child(firebase_key).remove()
                    #         get_prediction_history.clear() 
                    #         st.success("Riwayat berhasil dihapus!")
                    #         st.rerun()
                    #     else:
                    #         st.warning("Objek database tidak tersedia. Tidak bisa menghapus riwayat.")
                    # except Exception as delete_e:
                    #     st.error(f"Gagal menghapus riwayat: {delete_e}")
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                if not data_prediksi.empty:
                    data_prediksi['Timestamp'] = timestamp
                    data_prediksi['Input_Type'] = input_type
                    # Perbaikan: Gunakan semua kolom yang ada di data_prediksi + timestamp dan input_type untuk digabung
                    # Pastikan semua kolom yang diperlukan untuk digabung ada
                    all_cols_for_combined_df = list(set(DISPLAY_COLUMN_ORDER + ['Timestamp', 'Input_Type'] + list(data_prediksi.columns)))
                    combined_df_for_download = pd.concat([combined_df_for_download, data_prediksi.reindex(columns=all_cols_for_combined_df, fill_value=None)], ignore_index=True)


            if not combined_df_for_download.empty:
                st.markdown("---")
                st.subheader("Download Semua Riwayat Prediksi")
                
                all_history_excel_buffer = BytesIO()
                combined_df_for_download.to_excel(all_history_excel_buffer, index=False, engine='xlsxwriter')
                all_history_excel_buffer.seek(0)

                st.download_button(
                    label="Download Semua Riwayat (Excel)",
                    data=all_history_excel_buffer.getvalue(),
                    file_name=f"semua_riwayat_stunting_prediksi_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_all_history"
                )
                # --- Tombol "Hapus Semua Riwayat" juga tidak akan berfungsi ---
                if st.button("Hapus Semua Riwayat", key="clear_all_history"):
                    st.warning("Fitur penghapusan semua riwayat tidak aktif karena penyimpanan database dinonaktifkan.")
                    # try:
                    #     if db:
                    #         db.child(user_uid).child("predictions").remove()
                    #         get_prediction_history.clear() 
                    #         st.success("Semua riwayat berhasil dihapus!")
                    #         st.rerun()
                    #     else:
                    #         st.warning("Objek database tidak tersedia. Tidak bisa menghapus semua riwayat.")
                    # except Exception as clear_all_e:
                    #     st.error(f"Gagal menghapus semua riwayat: {clear_all_e}")