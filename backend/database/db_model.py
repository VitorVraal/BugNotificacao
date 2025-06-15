import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol



class DBModel(BaseModel):
    """
    Modelo Pydantic para configurar a conexão do banco de dados.
    Gera automaticamente a URL de conexão MySQL.
    """
    user:str
    password:str
    host: str
    database:Optional[str] = None # Opcional: nome do banco de dados específico
    port:Optional[int] = 3306  # Opcional: porta do banco de dados (padrão 3306)
    sid: Optional[str] = None   # Opcional: ID de serviço (para Oracle, ignorado aqui)
    connection_url: Optional[str] = None # Gerada automaticamente na inicialização

    def __init__(self, **data):
        """

            Inicializa o modelo DBModel e gera a URL de conexão automaticamente.

        """
        super().__init__(**data)
        self.connection_url = self._generate_url()

    def _generate_url(self):
        """
        Gera a URL de conexão MySQL/MySQLConnector com base nos atributos do modelo.
        """
        if self.database:
            return f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            # Se 'database' não for fornecido, conecta apenas ao servidor
            return f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}"
   
    @classmethod
    def get_dotenv(cls, dotenv_path: Optional[str] = ".env") -> "DBModel": # Carrega variáveis de um arquivo .env para criar um DBModel.
        
        load_dotenv(dotenv_path="database/.env")
        # Função da biblioteca 'python-dotenv' que carrega as variáveis de ambiente de um arquivo .env para as variáveis de ambiente do sistema.        
        
        #Após ser chamado, constrói e retorna uma instância da própria classe (cls) 
        #com os dados coletados do arquivo .env.
        return cls(
            #'os' é um módulo em Python que fornece uma maneira de usar funcionalidades dependentes do sistema operacional.
            #O método 'os.getenv()' é usado para acessar variáveis de ambiente. 
            # Neste contexto, ele busca as variáveis que foram carregadas do arquivo .env pela função load_dotenv().
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            database=os.getenv("database"),
            port=int(os.getenv("port", 3306)), # Garante que a porta seja um número inteiro
            sid=os.getenv("sid")
        )

    @classmethod
    def get_dotenv_create_db(cls, dotenv_path: Optional[str] = "database/.env") -> "DBModel":
        """
        Um método auxiliar para carregar variáveis do .env e criar um DBModel.
        Esse método, diferente do anterior, que foca na conexão direta com o banco, será usado para criar o banco de dados.
        Args:
            dotenv_path (str): O caminho para o arquivo .env. O padrão é "database/.env".

        Returns:
            DBModel: Uma instância do modelo de configuração do banco de dados.
        """
        load_dotenv(dotenv_path)
        return cls(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database")
        )


class DataBaseConnector(Protocol):
    def connect(self)->bool:
        """
        Obrigatório: Qualquer conector deve ter um método `connect()`.
        Este método deverá tentar estabelecer uma conexão com o banco de dados.
        Retorna `True` se a conexão for bem-sucedida, `False` caso contrário.
        """
        ...
    def disconect(self)->None:
        """
        Obrigatório: Qualquer conector deve ter um método `disconect()`.
        Este método deverá ser responsável por fechar a conexão ativa com o banco de dados.
        Não retorna nenhum valor.
        """
        ...

