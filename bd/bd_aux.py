import pyodbc
import os


class BdAux:
    def __init__(self, h_log=False):
        self.conn_str = None
        self.conn = None
        self.cursor = None
        self.hab_log = h_log

        self._conectar()

    @staticmethod
    def _validar_ambiente():
        required_variables = ['DB_SERVER', 'DATABASE_NAME', 'DB_USERNAME', 'DB_PASSWORD']
        missing_variables = []

        for variable in required_variables:
            if not os.environ.get(variable):
                missing_variables.append(variable)

        if missing_variables:
            missing_variables_str = ', '.join(missing_variables)
            raise ValueError(f"As seguintes variáveis de ambiente estão ausentes: {missing_variables_str}")

    def _build_conn_str(self):
        self._validar_ambiente()
        server = os.environ.get('DB_SERVER')
        database = os.environ.get('DATABASE_NAME')
        username = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')
        driver = '{ODBC Driver 18 for SQL Server}'

        self.conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    def _conectar(self):
        self._build_conn_str()

        if self.conn is None:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
        else:
            print("A conexão já está estabelecida.")

    def desconectar(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def executar_query(self, query, *args):
        if self.cursor is None:
            print("A conexão não foi estabelecida.")
            return

        try:
            self.cursor.execute(query, *args)
            self.conn.commit()
            if self.hab_log:
                print("Query executada com sucesso.")
        except pyodbc.Error as e:
            print(f"Ocorreu um erro ao executar a query: {e}")

    def get_query(self, query, *args):
        if self.cursor is None:
            print("A conexão não foi estabelecida.")
            return

        try:
            self.cursor.execute(query, *args)
            rows = self.cursor.fetchall()

            if self.hab_log:
                print("Query executada com sucesso.")

            return rows
        except pyodbc.Error as e:
            print(f"Ocorreu um erro ao executar a query: {e}")
