import streamlit as st
import pandas as pd
from io import StringIO
import re
import nltk
import csv
import string
from nltk import word_tokenize 
from nltk.probability import FreqDist
nltk.download('punkt')
nltk.download('brown')
import warnings
warnings.filterwarnings('ignore')
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import swifter

st.set_page_config(
    page_title="Input From Teks Area",
    page_icon="▶️",
)

st.header(':violet[Teks processing dari teks area]')
st.subheader('Pada halaman ini, kamu dapat melakukan teks processing atau teks cleaning pada kalimat yang kamu tulis pada :green[_teks area_] dibawah $\downarrow$')
st.markdown('Yang akan dilakukan pada teks kamu adalah :\n1.  Remove special character\n2.  Remove number\n3.  Remove whitespace\n4.  Remove punctuation\n5.  Remove single character\n6.  Tokenize\n7.  Menghitung kata-kata(token)\n8.  Remove stopword\n9.  Normalisasi sesuai dictionary _"new_kamusalay.csv"_ yang diupload\n10. Stemming')
# -------- Fungsi -----------
# ------ Tokenizing ---------

def remove_tweet_special(text):
    # remove tab, new line, ans back slice
    text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
    # remove non ASCII (emoticon, chinese word, .etc)
    text = text.encode('ascii', 'replace').decode('ascii')
    # remove mention, link, hashtag
    text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
    # remove incomplete URL
    return text.replace("http://", " ").replace("https://", " ")

#remove number
def remove_number(text):
    return  re.sub(r"\d+", "", text)

#remove punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("","",string.punctuation))

#remove whitespace leading & trailing
def remove_whitespace_LT(text):
    return text.strip()

#remove multiple whitespace into single whitespace
def remove_whitespace_multiple(text):
    return re.sub('\s+',' ',text)

# remove single char
def remove_singl_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)

# NLTK word tokenize 
def word_tokenize_wrapper(text, language="indonesia"):
    return word_tokenize(text)

# NLTK calc frequency distribution
def freqDist_wrapper(text):
    return FreqDist(text)

# Stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def stemming(text):
    text = [stemmer.stem(word) for word in text]
    return text

# ----------------------- get stopword from Sastrawi ------------------------------------
# get stopword indonesia
stop_factory = StopWordRemoverFactory()

# ---------------------------- manualy add stopword  ------------------------------------
more_stopword = ["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
                'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                '&amp', 'yah', 'user']
# ---------------------------------------------------------------------------------------
# append additional stopword

list_stopwords = stop_factory.get_stop_words()+more_stopword
stopword = stop_factory.create_stop_word_remover()

# convert list to dictionary
list_stopwords = set(list_stopwords)

#remove stopword pada list token
def stopwords_removal(words):
    return [word for word in words if word not in list_stopwords]

# ---------------------------------------------------------------------------------------

kamus = st.file_uploader("Upload file dictionary kamu terlebih dahulu !", key='kamus', type='csv')
if kamus is not None:  
    # Can be used wherever a "file-like" object is accepted:
    ids_before = pd.read_csv(kamus, encoding = 'latin-1', sep=',', header=None)
    ids_before = ids_before.set_index(0).to_dict()
    ids = dict(ele for sub in ids_before.values() for ele in sub.items())

txt = st.text_area('Text untuk di cleaning')

txt = txt.lower()
txt = remove_tweet_special(txt)
txt = remove_number(txt)
txt = remove_punctuation(txt)
txt = remove_whitespace_LT(txt)
txt = remove_whitespace_multiple(txt)
txt = remove_singl_char(txt)
txt = word_tokenize_wrapper(txt)
txt = stopwords_removal(txt)
    
# Normalized with dictionary
def normalized_term(text):
    return [ids[term] if term in ids else term for term in text]

txt = normalized_term(txt)
txt = stemming(txt)
token = freqDist_wrapper(txt)

# ---------------------------------- Results ------------------------------------
st.write(':green[Frekuensi token] yang muncul :', token)
st.write('Teks :green[setelah cleaning] :', txt) 