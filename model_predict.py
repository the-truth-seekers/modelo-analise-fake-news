from services.noticia_service import NoticiaService
import pandas as pd
import joblib
import boto3
import re

modelo = joblib.load('random_forest_model_news.pkl')
modelo_vec = joblib.load('count_vectorizer_model_news.pkl')

stopwords = ['pra', 'teve', 'éramos', 'aquela', 'esse', 'houvermos', 'suas', 'como', 'lhes', 'tu', 'nas', 'aqueles',
             'ser', 'nem', 'esteja', 'tive', 'aquelas', 'às', 'estiverem', 'formos', 'estiveram', 'estivessem', 'já',
             'tenham', 'hão', 'terei', 'é', 'a', 'teu', 'seria', 'teremos', 'aos', 'estar', 'tem', 'pelos', 'qual',
             'eu', 'estávamos', 'estes', 'minhas', 'estiver', 'seja', 'uma', 'mas', 'sou', 'dela', 'num', 'eram',
             'eles', 'deles', 'sua', 'houverá', 'tinha', 'ao', 'houvesse', 'fossem', 'nos', 'tuas', 'meus', 'pelo',
             'haver', 'será', 'teriam', 'quando', 'tivesse', 'estivermos', 'tiverem', 'esta', 'até', 'me', 'hajam',
             'essa', 'nós', 'tivessem', 'sejamos', 'entre', 'são', 'havemos', 'minha', 'estavam', 'hei', 'estivéssemos',
             'este', 'tua', 'pela', 'houve', 'um', 'tivéssemos', 'houvéramos', 'serei', 'por', 'haja', 'do', 'teríamos',
             'fosse', 'esses', 'isso', 'nossas', 'estou', 'fomos', 'teus', 'no', 'somos', 'tenhamos', 'houver', 'não',
             'estas', 'sejam', 'só', 'os', 'fui', 'terá', 'nossos', 'você', 'forem', 'vos', 'pelas', 'com', 'estivera',
             'houveríamos', 'dele', 'tém', 'houverei', 'também', 'estejamos', 'houvéssemos', 'houvera', 'houvessem',
             'era', 'houveriam', 'estivemos', 'seu', 'à', 'fôramos', 'tivéramos', 'mesmo', 'temos', 'isto',
             'houveremos', 'meu', 'tivemos', 'estava', 'lhe', 'estive', 'numa', 'tínhamos', 'que', 'tivera', 'terão',
             'tenho', 'esteve', 'seríamos', 'de', 'tiveram', 'aquele', 'estamos', 'para', 'tiver', 'houverem',
             'estivéramos', 'na', 'quem', 'ou', 'teria', 'ele', 'em', 'estão', 'as', 'fora', 'mais', 'estivesse',
             'seus', 'vocês', 'da', 'essas', 'houveria', 'está', 'ela', 'houverão', 'tinham', 'o', 'fôssemos',
             'houveram', 'hajamos', 'se', 'serão', 'estejam', 'te', 'for', 'dos', 'elas', 'seriam', 'tivermos', 'há',
             'nosso', 'seremos', 'tenha', 'das', 'houvemos', 'sem', 'e', 'foram', 'aquilo', 'foi', 'nossa']


def clean_text(value):
    x = re.sub(r"(#\S+)|(@\S+)|(http\S+)", "", value).lower().replace('.', '').replace(';', '') \
        .replace('-', '').replace(':', '').replace(')', '').strip().split()
    x = [palavra.lower() for palavra in x if palavra.isalpha() and palavra not in stopwords and not len(palavra) <= 2]
    return ' '.join(x)


def predict_value(valor):
    previsao = modelo.predict(valor)
    return previsao


def vectorize_value(valor):
    valor_vec = modelo_vec.transform([valor])
    return valor_vec


s3 = boto3.client('s3')
bucket_name = 'seekers-bucket'
file_key = 'extracao/extracao.csv'
local_filename = 'extracao.csv'

s3.download_file(bucket_name, file_key, local_filename)

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
