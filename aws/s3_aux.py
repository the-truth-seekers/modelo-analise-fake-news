import boto3


# Definir credenciais Aws (cat .aws/credentials) no diretório home do usuário na pasta '.aws' no arquivo credentials
# Obs: Em caso de erro formatar o arquivo em ANSI
class S3Aux:
    def __init__(self):
        self.s3_obj = boto3.client('s3')

    def send_file_to_bucket(self, bucket_name: str, filepath: str, estrutura_s3: str = ''):
        self.s3_obj.upload_file(filepath, bucket_name, estrutura_s3)

    def download_file(self, bucket_name, file_key, local_filename):
        self.s3_obj.download_file(bucket_name, file_key, local_filename)
