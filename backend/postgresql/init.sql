DROP TABLE IF EXISTS "pratos" CASCADE ;
DROP TABLE IF EXISTS "pedidos" CASCADE ;

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
    "horario" VARCHAR(50)  NOT NULL,
    FOREIGN KEY (prato_id) REFERENCES pratos (id)
);

INSERT INTO "pratos" ("nome", "descricao", "preco", "pessoas") VALUES ('Strogonoff', 'Strogonoff de frango acompanhado de arroz e batata-palha', 30.0, 1);
INSERT INTO "pratos" ("nome", "descricao", "preco", "pessoas") VALUES ('Lasanha', 'Lasanha de presunto e queijo ao molho branco', 50.0, 2);
INSERT INTO "pratos" ("nome", "descricao", "preco", "pessoas") VALUES ('Feijoada', 'Feijoada acompanhada de tiras de carne, arroz branco, farofa e batata-frita', 40.0, 1);
INSERT INTO "pedidos" ("cliente", "prato_id", "endereco", "forma_pagamento", "horario") VALUES ('João Silva', 1, 'Rua A, 123', 'Cartão de Crédito', '2024-12-08 12:30:00');
INSERT INTO "pedidos" ("cliente", "prato_id", "endereco", "forma_pagamento", "horario") VALUES ('Maria Oliveira', 2, 'Rua B, 456', 'Dinheiro', '2024-12-08 13:00:00');
INSERT INTO "pedidos" ("cliente", "prato_id", "endereco", "forma_pagamento", "horario") VALUES ('Carlos Souza', 3, 'Rua C, 789', 'Pix', '2024-12-08 14:15:00');
