
CREATE TABLE usuario (
    id_usuario BIGSERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    data_nascimento DATE,
    sexo VARCHAR(50)
);

CREATE TABLE registro_exercicio (
    id_exercicio BIGSERIAL PRIMARY KEY,
    tipo VARCHAR(255) NOT NULL,
    calorias INTEGER,
    intensidade VARCHAR(100),
    duracao_minutos INTEGER,
    data DATE NOT NULL,
    id_usuario BIGINT NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE registro_humor (
    id_humor BIGSERIAL PRIMARY KEY,
    tipo_humor VARCHAR(100) NOT NULL,
    data DATE NOT NULL,
    observacao TEXT,
    id_usuario BIGINT NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE registro_hidratacao (
    id_hidratacao BIGSERIAL PRIMARY KEY,
    data DATE NOT NULL,
    quantidade_ml INTEGER NOT NULL,
    hora TIME NOT NULL,
    id_usuario BIGINT NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE registro_atividade_mental (
    id_atividade BIGSERIAL PRIMARY KEY,
    data DATE NOT NULL,
    duracao_minutos INTEGER,
    tipo VARCHAR(255) NOT NULL,
    observacao TEXT,
    id_usuario BIGINT NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE registro_sono (
    id_sono BIGSERIAL PRIMARY KEY,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    qualidade VARCHAR(100),
    id_usuario BIGINT NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE registro_alimentacao (
    id_registro_alimentacao BIGSERIAL PRIMARY KEY,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    tipo VARCHAR(100) NOT NULL, 
    calorias INTEGER,
    id_usuario BIGINT NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE registro_alimentacao_descricao (
    id_registro_alimentacao BIGINT NOT NULL,
    descricao TEXT NOT NULL,
    PRIMARY KEY (id_registro_alimentacao, descricao),
    CONSTRAINT fk_registro_alimentacao
        FOREIGN KEY(id_registro_alimentacao)
        REFERENCES registro_alimentacao(id_registro_alimentacao)
        ON DELETE CASCADE
);

CREATE TABLE meta (
    id_meta BIGSERIAL PRIMARY KEY,
    valor VARCHAR(255) NOT NULL, 
    id_usuario BIGINT NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE meta_agua (
    id_meta BIGINT PRIMARY KEY,
    CONSTRAINT fk_meta
        FOREIGN KEY(id_meta)
        REFERENCES meta(id_meta)
        ON DELETE CASCADE
);

CREATE TABLE meta_sono (
    id_meta BIGINT PRIMARY KEY,
    CONSTRAINT fk_meta
        FOREIGN KEY(id_meta)
        REFERENCES meta(id_meta)
        ON DELETE CASCADE
);

CREATE TABLE meta_exercicio (
    id_meta BIGINT PRIMARY KEY,
    CONSTRAINT fk_meta
        FOREIGN KEY(id_meta)
        REFERENCES meta(id_meta)
        ON DELETE CASCADE
);
