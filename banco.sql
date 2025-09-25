
CREATE TABLE IF NOT EXISTS user (
    idUser INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    matricula TEXT UNIQUE NOT NULL,
    jornada TEXT NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_complemento (
    idComplemento INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT NOT NULL,
    telefone TEXT,
    endereco TEXT,
    nascimento DATE,
    FOREIGN KEY (matricula) REFERENCES user(matricula)
);

-- Tabela de pontos (registro de entrada/saída)
CREATE TABLE IF NOT EXISTS pontos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER NOT NULL,
    data_ponto DATE NOT NULL,
    hora_entrada TIME,
    hora_saida_almoco TIME,
    hora_retorno_almoco TIME,
    hora_saida TIME,
    horas_trabalhadas DECIMAL(4,2),
    observacoes TEXT,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
);

CREATE TABLE IF NOT EXISTS suporte (
    idSuporte INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL,
    email TEXT NOT NULL,
    assunto TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (matricula) REFERENCES user(matricula)
);