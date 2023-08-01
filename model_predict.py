from services.noticia_service import NoticiaService
from utls.text_help import clean_text
from aws.s3_aux import S3Aux
import pandas as pd
import joblib


# Modelos
modelo = joblib.load('random_forest_model_news.pkl')
modelo_vec = joblib.load('count_vectorizer_model_news.pkl')


def predict_value(valor):
    previsao = modelo.predict(valor)
    return previsao


def vectorize_value(valor):
    valor_vec = modelo_vec.transform([valor])
    return valor_vec


bucket_name = 'seekers-bucket'
file_key = 'extracao/extracao.csv'
local_filename = 'extracao.csv'

s3_aux = S3Aux()
s3_aux.download_file(bucket_name, file_key, local_filename)

df = pd.read_csv(local_filename)

df['texto_noticia'] = df['texto_noticia'].str.lower()
df['texto_tratado'] = df['texto_noticia'].apply(clean_text)
df['texto_vetorizado'] = df['texto_tratado'].apply(vectorize_value)
df['resultado'] = df['texto_vetorizado'].apply(predict_value)[0][0]

ns = NoticiaService()

for index, row in df.iterrows():
    resultado = row['resultado']
    link = row['link']
    ns.inserir_resultado_noticia(resultado, link)
