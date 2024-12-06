DROP TABLE IF EXISTS "pratos";
DROP TABLE IF EXISTS "pedidos";

CREATE TABLE "pratos" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "descricao" VARCHAR(255) NOT NULL,
    "preco" FLOAT NOT NULL,
    "pessoas" INTEGER NOT NULL
);

CREATE TABLE "pedidos" (
    "id" SERIAL PRIMARY KEY,
    "cliente" VARCHAR(100) NOT NULL,
    "prato_id" INTEGER NOT NULL,
    "endereco" VARCHAR(255) NOT NULL,
    "forma_pagamento" VARCHAR(50)  NOT NULL,
    "horario" TIMESTAMP NOT NULL,
    FOREIGN KEY (prato_id) REFERENCES pratos (id)
);

INSERT INTO "pratos" ("nome", "descricao", "preco", "pessoas") VALUES ('Strogonoff', 'Strogonoff de frango acompanhado de arroz e batata-palha', 30.0, 1);
INSERT INTO "pratos" ("nome", "descricao", "preco", "pessoas") VALUES ('Lasanha', 'Lasanha de presunto e queijo ao molho branco', 50.0, 2);
INSERT INTO "pratos" ("nome", "descricao", "preco", "pessoas") VALUES ('Feijoada', 'Feijoada acompanhada de tiras de carne, arroz branco, farofa e batata-frita', 40.0, 1);
