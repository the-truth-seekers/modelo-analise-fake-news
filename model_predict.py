from services.noticia_service import NoticiaService
from utls.text_help import clean_text
from keras.models import load_model
from aws.s3_aux import S3Aux
import pandas as pd
from joblib import load
import spacy
import re

# Modelos
modelo_predicao_rnn = load_model('models/model_rnn.h5')
modelo_pad_sequences = load('models/padsequences.pkl')
modelo_tokenizer = load('models/tokenizer.pkl')


def lematize_sentence(sentence):
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(sentence)
    return ' '.join([word.lemma_ for word in doc])


def limpar_texto(value):
    value = re.sub(r"(#\S+)|(@\S+)|(http\S+)", "", value)
    for char in ['.', ';', '-', ':', ')']:
        value = value.replace(char, '')
    return value.strip().lower()


def texts_to_sequences(value):
    return modelo_tokenizer.texts_to_sequences([value])


def pad_seq(value):
    return modelo_pad_sequences(value, maxlen=300)


bucket_name = 'seekers-bucket'
file_key = 'extracao/extracao.csv'
local_filename = 'extracao.csv'

s3_aux = S3Aux()
s3_aux.download_file(bucket_name, file_key, local_filename)

df = pd.read_csv(local_filename)

df['texto_noticia'] = df['texto_noticia'].str.lower()
df['texto_tratado'] = df['texto_noticia'].apply(clean_text)
df['texto_vetorizado'] = df['texto_tratado'].apply(limpar_texto)
df['lematize_txt'] = df['texto_vetorizado'].apply(lematize_sentence)
df['seq'] = df['lematize_txt'].apply(texts_to_sequences)
df['padded_seq'] = df['seq'].apply(pad_seq)
df['resultado'] = df['padded_seq'].apply(modelo_predicao_rnn.predict)

ns = NoticiaService()

for index, row in df.iterrows():
    resultado = 1 if row['resultado'][0][0] >= 0.5 else 0
    link = row['link']
    ns.inserir_resultado_noticia(resultado, link)
