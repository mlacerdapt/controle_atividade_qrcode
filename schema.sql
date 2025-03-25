DROP TABLE IF EXISTS funcionario;
DROP TABLE IF EXISTS area;
DROP TABLE IF EXISTS equipamento;
DROP TABLE IF EXISTS tarefa;

CREATE TABLE funcionario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_sap TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL
);

CREATE TABLE area (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE equipamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE tarefa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER NOT NULL,
    area_id INTEGER NOT NULL,
    equipamento_id INTEGER NOT NULL,
    data_hora_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_hora_fim DATETIME,
    FOREIGN KEY (funcionario_id) REFERENCES funcionario (id),
    FOREIGN KEY (area_id) REFERENCES area (id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamento (id)
);