from .db_model import DataBaseConnector, DBModel # Importa as ferramentas que definem como configurar o banco e o "contrato" de conexão.
from typing import Optional # Usado para indicar que algo pode ser de um tipo OU None (vazio).
from mysql.connector import Error, connect, MySQLConnection # Traz as funções necessárias para trabalhar com MySQL: 'Error' para erros, 'connect' para conectar, e 'MySQLConnection' para o tipo de conexão.
 


class MySqlConnector(DataBaseConnector):
    """
    Esta classe é o seu conectador com o MySQL.
    Ela sabe como iniciar e fechar uma conexão, seguindo o padrão que definimos em DataBaseConnector.
    """
    def __init__(self, db_config: DBModel):
        """
        Ao criar um conectador MySQL, você passa as configurações do banco (DBModel).
        'self.conn' guarda a conexão ativa com o banco, que começa vazia.
        """
        self.db_config = db_config
        self.conn = Optional[MySQLConnection] | None


    def connection(self):
        """
        Tenta se conectar ao banco de dados MySQL, usando todas as configurações, incluindo o banco específico.
        Se der certo, retorna a conexão e uma mensagem de sucesso. Se falhar, mostra o erro.
        """
        try:
            self.conn = connect(
                user = self.db_config.user,
                password = self.db_config.password,
                host = self.db_config.host,
                database = self.db_config.database, # Aqui ele tenta conectar a um banco de dados específico.
                port = self.db_config.port,
            )
            return self.conn, f'Conexão com mysql bem-sucedida'  # Retorna a conexão e uma mensagem.
        except Error as err:
            print(f"Erro ao conectar ao MySQL: {err}")  # Se algo der errado na conexão, ele avisa (meramente visual para ter uma resposta direta no terminal).
            return None, f'Erro ao conectar {err}' # Retorna 'None' para a conexão e a mensagem de erro.
        
    def connection_mysql(self):
        """
        Tenta se conectar ao servidor MySQL, mas sem especificar um banco de dados particular.
        Isso é útil para operações de administração, como criar um novo banco de dados.
        Se der certo, retorna a conexão e uma mensagem de sucesso. Se falhar, mostra o erro.
        """
        try:
            self.conn = connect(
                user = self.db_config.user,
                password = self.db_config.password,
                host = self.db_config.host
            )
            # Retorna a conexão e uma mensagem de sucesso, pois a conexão foi bem-sucedida ao servidor.
            # A mensagem de erro está na linha original, mas o sucesso não tinha um retorno explícito.
            # return self.conn, 'Conexão com o servidor MySQL bem-sucedida (sem banco específico)'
        except Error as err:
            print(f"Erro ao conectar ao MySQL: {err}")
            return None, f'Erro ao conectar {err}' # Retorna 'None' e a mensagem de erro.
          
    def disconnect(self):
        """
        Fecha a conexão ativa com o banco de dados, se ela existir e estiver aberta.
        Retorna uma mensagem informando se a conexão foi fechada.
        """
        if self.conn and self.conn.is_connected():
            self.conn.close()
            return False, f'Conexão fechada com sucesso'