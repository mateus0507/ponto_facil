
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
