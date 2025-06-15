from database.db_model import DBModel 
import mysql.connector
from mysql.connector import Error

def criar_banco_de_dados():
    try:
        # Carrega as configurações do .env via DBModel
        db_config = DBModel.get_dotenv_create_db()

        connection = mysql.connector.connect(
            host=db_config.host,
            user=db_config.user,
            password=db_config.password
        )

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config.database};")
        connection.commit()  # <- IMPORTANTE!
        print(f"✅ Banco de dados '{db_config.database}' criado ou já existente.")
    except Error as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def criar_tabelas():
    connection = None
    cursor = None
    try:
        db_config = DBModel.get_dotenv()

        connection = mysql.connector.connect(
            host=db_config.host,
            user=db_config.user,
            password=db_config.password,
            database=db_config.database
        )
        cursor = connection.cursor()

        #CRIAÇÃO DE TABELAS

        # Tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS USUARIO(
            ID_USUARIO INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            EMAIL_USUARIO VARCHAR(255) NOT NULL UNIQUE,
            SENHA_USUARIO VARCHAR(255) NOT NULL,
            DATA_CADASTRO DATE DEFAULT NULL,
            DATA_ATUALIZACAO DATE DEFAULT NULL,
            CONSTRAINT CHK_SENHA_TAMANHO CHECK (LENGTH(SENHA_USUARIO) >= 3)
        )
        ''')
        
        # Tabela de estoque
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ESTOQUE(
	    ID_ESTOQUE INT AUTO_INCREMENT PRIMARY KEY,
    	CATEGORIA_ESTOQUE ENUM('Alimentos', 'Bebidas', 'Laticínios') NOT NULL,
	    QTDE_ESTOQUE INT
        );
        ''')
        
        #Tabela de produtos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PRODUTOS(
	    ID_PRODUTO INT AUTO_INCREMENT PRIMARY key,
        NOME_PRODUTO VARCHAR(255) NOT NULL UNIQUE,
        PRECO_PRODUTO FLOAT NOT NULL,
        FK_ID_ESTOQUE INT DEFAULT NULL,
	    DESC_PRODUTO VARCHAR(255) NULL,
        NUMERO_NF_PRODUTO VARCHAR(255) NULL UNIQUE,
        VALIDADE_PRODUTO DATE NOT NULL,
        FORNECEDOR_PRODUTO VARCHAR(255) NULL,
        QTD_MINIMA_PRODUTO INT NOT NULL,
        FOREIGN KEY (FK_ID_ESTOQUE) REFERENCES ESTOQUE(ID_ESTOQUE) ON DELETE SET NULL
        );               
        ''')
        
        #Tabela de movimentação
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MOVIMENTACAO(
	    ID_MOVIMENTACAO INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	    FK_ID_PRODUTO INT NOT NULL,
        QTDE INT NOT NULL, 
        TIPO_MOVIMENTACAO VARCHAR(255) NOT NULL,
        DATA_MOVIMENTACAO DATE NOT NULL,
        FOREIGN KEY (FK_ID_PRODUTO) REFERENCES PRODUTOS(ID_PRODUTO)
        );              
        ''')
        
        #tabela de pedido entrega
        cursor.execute('''
        create table IF NOT EXISTS PEDIDO_ENTREGA (
	    id_entrega int auto_increment primary key not null,
	    status_entrega boolean default FALSE,
        fk_id_produto int, 
        fk_ID_MOVIMENTACAO int, 
        foreign key (fk_id_produto) references PRODUTOS(ID_PRODUTO),
        foreign key (fk_ID_MOVIMENTACAO) references MOVIMENTACAO(ID_MOVIMENTACAO)
    
        );               
        ''')

        # Procedure de cadastrar usuário
        cursor.execute('''
        CREATE PROCEDURE CADASTRAR_USUARIO(
        IN P_EMAIL_USUARIO VARCHAR(255),
        IN P_SENHA_USUARIO VARCHAR(255)
        )
        BEGIN
        INSERT INTO USUARIO (EMAIL_USUARIO, SENHA_USUARIO)
        VALUES (P_EMAIL_USUARIO, P_SENHA_USUARIO);
        END
        ''')
        
        # Procedure de excluir usuários
        cursor.execute('''
        CREATE PROCEDURE EXCLUIR_USUARIO_ID( IN P_ID_USUARIO INT)
        BEGIN
        -- Verificar se o usuário existe
        DECLARE message_text VARChAR(100);
        IF NOT EXISTS (SELECT 1 FROM USUARIO WHERE ID_USUARIO = P_ID_USUARIO) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Usuário não encontrado.';
        ELSE
        DELETE FROM USUARIO
        WHERE ID_USUARIO = P_ID_USUARIO;
        END IF;
        END
        ''')
        
        # Procedure de alterar usuário
        cursor.execute('''
        CREATE PROCEDURE alterar_usuario(
        IN P_ID_USUARIO INT,
        IN P_EMAIL_USUARIO VARCHAR(255),
        IN P_SENHA_USUARIO VARCHAR(255)
        )
        BEGIN
        -- Verificar se o usuário JA´ eXiste via ID
        IF NOT EXISTS (SELECT 1 FROM USUARIO WHERE ID_USUARIO = P_ID_USUARIO) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Usuário não encontrado pelo ID.';
        ELSE
        -- Verificar se o usuário JA´ eXiste via email
        IF EXISTS (SELECT 1 FROM USUARIO WHERE EMAIL_USUARIO = P_EMAIL_USUARIO AND ID_USUARIO <> P_ID_USUARIO) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: O email informado já está cadastrado para outro usuário.';
        ELSE
        UPDATE USUARIO SET
        EMAIL_USUARIO = P_EMAIL_USUARIO,
        SENHA_USUARIO = P_SENHA_USUARIO
        WHERE ID_USUARIO = P_ID_USUARIO;
        END IF;
        END IF;
        END
        ''')        
        
        # Procedure de listar usuários
        cursor.execute('''
        CREATE PROCEDURE LISTAR_USUARIOS()
        BEGIN
        SELECT * FROM USUARIO;
        END

        ''')

        cursor.execute("DROP PROCEDURE IF EXISTS CADASTRAR_PRODUTO_ESTOQUE")
        
        #procedure cadastrar produto no estoque
        cursor.execute('''
        
        CREATE PROCEDURE CADASTRAR_PRODUTO_ESTOQUE(
            IN P_NOME_PRODUTO VARCHAR(255),
            IN P_CATEGORIA_ESTOQUE VARCHAR(50),
            IN P_DESC_PRODUTO VARCHAR(255),
            IN P_QTDE_ESTOQUE INT,
            IN P_PRECO_PRODUTO DECIMAL(10,2),
            IN P_QTD_MINIMA_PRODUTO INT,
            IN P_VALIDADE_PRODUTO DATE,
            IN P_NUMERO_NF_PRODUTO VARCHAR(255),
            IN P_FORNECEDOR_PRODUTO VARCHAR(255)
        )
        BEGIN
            DECLARE V_ID_ESTOQUE INT;
            DECLARE PRODUTO_EXISTENTE INT DEFAULT 0;

            DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;

            START TRANSACTION;

            -- Verifica se o produto já existe
            SELECT COUNT(*) INTO PRODUTO_EXISTENTE 
            FROM PRODUTOS 
            WHERE NOME_PRODUTO = P_NOME_PRODUTO;

            IF PRODUTO_EXISTENTE > 0 THEN
                SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = 'Produto já cadastrado. Use a função de atualização para modificar.';
            ELSE
                -- Cria novo estoque
                INSERT INTO ESTOQUE(CATEGORIA_ESTOQUE, QTDE_ESTOQUE)
                VALUES(P_CATEGORIA_ESTOQUE, P_QTDE_ESTOQUE);

                SET V_ID_ESTOQUE = LAST_INSERT_ID();

                -- Insere produto
                INSERT INTO PRODUTOS(
                    NOME_PRODUTO,
                    PRECO_PRODUTO,
                    FK_ID_ESTOQUE,
                    DESC_PRODUTO,
                    NUMERO_NF_PRODUTO,
                    VALIDADE_PRODUTO,
                    FORNECEDOR_PRODUTO,
                    QTD_MINIMA_PRODUTO
                )
                VALUES(
                    P_NOME_PRODUTO,
                    P_PRECO_PRODUTO,
                    V_ID_ESTOQUE,
                    P_DESC_PRODUTO,
                    P_NUMERO_NF_PRODUTO,
                    P_VALIDADE_PRODUTO,
                    P_FORNECEDOR_PRODUTO,
                    P_QTD_MINIMA_PRODUTO
                );
            END IF;

            COMMIT;
        END
        ''')
        
        #procedure de atualizar produto
        cursor.execute('''
        CREATE PROCEDURE ATUALIZAR_ESTOQUE_PRODUTO(
            IN p_id_estoque_upd INT,
            IN p_categoria_estoque_upd VARCHAR(255),
            IN p_qtde_estoque_upd INT,
            IN p_id_produto_upd INT,
            IN p_nome_produto_upd VARCHAR(255),
            IN p_preco_produto_upd DECIMAL(10,2),
            IN p_desc_produto_upd VARCHAR(255),
            IN p_numero_nf_produto_upd VARCHAR(255),
            IN p_validade_produto_upd DATE,
            IN p_fornecedor_produto_upd VARCHAR(255),
            IN p_qtd_minima_produto_upd INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;

            START TRANSACTION;

            UPDATE ESTOQUE
            SET
                CATEGORIA_ESTOQUE = IFNULL(p_categoria_estoque_upd, CATEGORIA_ESTOQUE),
                QTDE_ESTOQUE = IFNULL(p_qtde_estoque_upd, QTDE_ESTOQUE)
            WHERE ID_ESTOQUE = p_id_estoque_upd;

            UPDATE PRODUTOS
            SET
                NOME_PRODUTO = IFNULL(p_nome_produto_upd, NOME_PRODUTO),
                PRECO_PRODUTO = IFNULL(p_preco_produto_upd, PRECO_PRODUTO),
                DESC_PRODUTO = IFNULL(p_desc_produto_upd, DESC_PRODUTO),
                NUMERO_NF_PRODUTO = IFNULL(p_numero_nf_produto_upd, NUMERO_NF_PRODUTO),
                VALIDADE_PRODUTO = IFNULL(p_validade_produto_upd, VALIDADE_PRODUTO),
                FORNECEDOR_PRODUTO = IFNULL(p_fornecedor_produto_upd, FORNECEDOR_PRODUTO),
                QTD_MINIMA_PRODUTO = IFNULL(p_qtd_minima_produto_upd, QTD_MINIMA_PRODUTO)
            WHERE ID_PRODUTO = p_id_produto_upd;

            COMMIT;
        END
        ''')
        
        #Procedure de listar produtos
        cursor.execute('''
        CREATE PROCEDURE LISTAR_PRODUTOS()
        BEGIN
            SELECT 
                p.ID_PRODUTO,
                p.NOME_PRODUTO, 
                p.PRECO_PRODUTO, 
                p.DESC_PRODUTO,
                p.NUMERO_NF_PRODUTO,
                p.VALIDADE_PRODUTO,
                p.FORNECEDOR_PRODUTO,
                p.QTD_MINIMA_PRODUTO,
                p.FK_ID_ESTOQUE,
                e.ID_ESTOQUE,
                e.CATEGORIA_ESTOQUE, 
                e.QTDE_ESTOQUE
            FROM PRODUTOS p
            LEFT JOIN ESTOQUE e ON p.FK_ID_ESTOQUE = e.ID_ESTOQUE;
        END
        ''')

        
        # Procedure de fazer login
        cursor.execute('''
        CREATE PROCEDURE FAZER_LOGIN(
	    IN P_EMAIL_USUARIO VARCHAR(255),
	    IN P_SENHA_USUARIO VARCHAR(255)
        ) 
        BEGIN
        IF EXISTS (
        SELECT 1 FROM USUARIO 
        WHERE EMAIL_USUARIO = P_EMAIL_USUARIO 
        AND SENHA_USUARIO = P_SENHA_USUARIO)  
        THEN
        SELECT
        ID_USUARIO,
        EMAIL_USUARIO,
        'Login realizado com sucesso!' AS MENSAGEM
        FROM USUARIO
        WHERE EMAIL_USUARIO = P_EMAIL_USUARIO;
        ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Email ou senha inválidos.';
        END IF;
        END
        ''')
        
        #Procedure exluir produto geral
        cursor.execute('''
        CREATE PROCEDURE EXCLUIR_ESTOQUE_PRODUTOS(
            IN p_id_estoque INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;
            START TRANSACTION;

            DELETE FROM PRODUTOS
            WHERE FK_ID_ESTOQUE = p_id_estoque;

            DELETE FROM ESTOQUE
            WHERE ID_ESTOQUE = p_id_estoque;

            COMMIT;
        END                
        ''')
        
        # Procedure de procurar produto por nome
        cursor.execute('''
        CREATE PROCEDURE PROCURAR_PRODUTO_NOME(
        IN P_NOME_PRODUTO VARCHAR(100)
        )
        BEGIN
        SELECT
        p.ID_PRODUTO,
        p.NOME_PRODUTO,
        p.PRECO_PRODUTO,
        p.DESC_PRODUTO,
        p.NUMERO_NF_PRODUTO,
        p.VALIDADE_PRODUTO,
        p.FORNECEDOR_PRODUTO,
        p.QTD_MINIMA_PRODUTO,
        e.ID_ESTOQUE,
        e.CATEGORIA_ESTOQUE,
        e.QTDE_ESTOQUE
        FROM PRODUTOS p
        JOIN ESTOQUE e ON p.FK_ID_ESTOQUE = e.ID_ESTOQUE
        WHERE p.NOME_PRODUTO LIKE CONCAT('%', P_NOME_PRODUTO, '%');
        END               
        ''')

        #Procedure de consultar histórico
        cursor.execute('''
        CREATE PROCEDURE CONSULTAR_HISTORICO(
        IN P_ID_PRODUTO INT
        #p_produto_id 
        )
        BEGIN
        SELECT m.*, p.NOME_PRODUTO AS nome_produto
        FROM MOVIMENTACAO m
        JOIN PRODUTOS p ON m.FK_ID_PRODUTO = p.ID_PRODUTO
        WHERE m.FK_ID_PRODUTO = P_ID_PRODUTO
        ORDER BY m.DATA_MOVIMENTACAO DESC;
        END               
        ''')
        
        #procedure de gerar relatório
        cursor.execute('''
        CREATE PROCEDURE GERAR_RELATORIO_ESTOQUE(
        IN p_id_estoque INT
        )
        BEGIN
        SELECT p.ID_PRODUTO, p.NOME_PRODUTO, p.PRECO_PRODUTO, ep.QTDE, 
        (p.PRECO_PRODUTO * ep.QTDE) AS ValorTotal FROM ESTOQUE_PRODUTO ep
    
        JOIN PRODUTOS p ON ep.FK_ID_PRODUTO = p.ID_PRODUTO
        WHERE ep.FK_ID_ESTOQUE = p_id_estoque
        ORDER BY p.NOME_PRODUTO;
        END               
        ''')
        
        #Procedure de registrar movimento
        cursor.execute('''
        CREATE PROCEDURE REGISTRAR_MOVIMENTO(
        IN p_fk_id_produto INT,
        IN p_qtde INT,
        IN p_tipo_movimentacao VARCHAR(255)
        )
        BEGIN
        IF NOT EXISTS (SELECT 1 FROM PRODUTOS WHERE ID_PRODUTO = p_fk_id_produto) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: ID de produto inválido.';
        ELSEIF p_qtde = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: A quantidade movimentada não pode ser zero.';
        ELSEIF p_tipo_movimentacao NOT IN ('entrada', 'saida', 'ajuste') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Tipo de movimentação inválido (deve ser "entrada", "saida" ou "ajuste").';
        ELSE
        INSERT INTO MOVIMENTACAO (FK_ID_PRODUTO, QTDE, TIPO_MOVIMENTACAO, DATA_MOVIMENTACAO)
        VALUES (p_fk_id_produto, p_qtde, p_tipo_movimentacao, CURDATE());
        
        IF p_tipo_movimentacao = 'entrada' THEN
        UPDATE ESTOQUE_PRODUTO
        SET QTDE = QTDE + p_qtde
        WHERE FK_ID_PRODUTO = p_fk_id_produto;

        ELSEIF p_tipo_movimentacao = 'saida' THEN
        UPDATE ESTOQUE_PRODUTO
        SET QTDE = QTDE - p_qtde
        WHERE FK_ID_PRODUTO = p_fk_id_produto AND QTDE >= p_qtde;
        IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Quantidade insuficiente em estoque para realizar a saída.';
        END IF;
        ELSEIF p_tipo_movimentacao = 'ajuste' THEN
        UPDATE ESTOQUE_PRODUTO
        SET QTDE = QTDE + p_qtde
		WHERE FK_ID_PRODUTO = p_fk_id_produto;
        END IF;
        END IF;
        END               
        ''')
        
        #procedure de notificação de falta de produto
        cursor.execute('''
        CREATE PROCEDURE NOTIFICACAO_FALTA_PRODUTO(
            IN P_NOME_PRODUTO VARCHAR(255)
        )
        BEGIN
            DECLARE V_QTDE_ESTOQUE INT;
            DECLARE V_QTDE_MINIMA INT;

            -- Busca a quantidade atual e a mínima do produto
            SELECT E.QTDE_ESTOQUE, P.QTD_MINIMA_PRODUTO
            INTO V_QTDE_ESTOQUE, V_QTDE_MINIMA
            FROM PRODUTOS P
            JOIN ESTOQUE E ON P.FK_ID_ESTOQUE = E.ID_ESTOQUE
            WHERE P.NOME_PRODUTO = P_NOME_PRODUTO;

            -- Verificações
            IF V_QTDE_ESTOQUE IS NULL THEN
                SELECT CONCAT('Produto "', P_NOME_PRODUTO, '" não encontrado no estoque.') AS Notificação;

            ELSEIF V_QTDE_ESTOQUE = 0 THEN
                SELECT CONCAT('ALERTA: Produto "', P_NOME_PRODUTO, '" está esgotado!') AS Notificação;

            ELSEIF V_QTDE_ESTOQUE <= V_QTDE_MINIMA THEN
                SELECT CONCAT('ATENÇÃO: Produto "', P_NOME_PRODUTO, '" com estoque baixo (', V_QTDE_ESTOQUE, ' unidades).') AS Notificação;

            ELSE
                SELECT CONCAT('Produto "', P_NOME_PRODUTO, '" com estoque normal (', V_QTDE_ESTOQUE, ' unidades).') AS Notificação;
            END IF;
        END
        ''')               
        
        # ADICIONAR OUTRAS PROCEDURES AQUI
        connection.commit()
        print("Tabelas e procedures criadas com sucesso.")
    except Error as e:
        print(f"Erro ao criar tabelas ou procedures: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
