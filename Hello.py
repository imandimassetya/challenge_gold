import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Selamat datang di halaman utama teks processing dan teks cleaning! 👋")

st.sidebar.success("Pilih metode input diatas")

st.markdown(
    """
    Pada halaman ini kamu dapat melakukan teks processing dan
    teks cleaning dengan pilihan metode input.
    **👈 Pilih metode input di samping** untuk melakukan teks processing dan teks cleaning.
    ### Pilihan metode input :
    - **Input From Text Area :** input teks kamu pada teks box yang tersedia
    - **Input From Uploaded File :** upload file teks dengan _extension csv_
    
    Jangan lupa untuk upload file _new_kamusalay.csv_ sebagai dictionary kamu ya !
"""
)
    