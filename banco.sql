
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
    genero TEXT,
    FOREIGN KEY (matricula) REFERENCES user(matricula)
);

CREATE TABLE IF NOT EXISTS lembretes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pontos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT,
    data DATE,
    hora TEXT,
    tipo TEXT, -- "entrada", "saida", "intervalo_inicio", "intervalo_fim"
    FOREIGN KEY(matricula) REFERENCES user(matricula)
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

CREATE TABLE IF NOT EXISTS justificativas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data DATE NOT NULL,
    motivo TEXT NOT NULL
);