DROP TABLE IF EXISTS client CASCADE
;

CREATE TABLE client (
    id      INTEGER PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    email   VARCHAR(50)
)
;

DROP TABLE IF EXISTS transaction
;

CREATE TABLE transaction (
    id          SERIAL PRIMARY KEY,
    client_id   INTEGER REFERENCES client(id),
    txn_date    TIMESTAMP NOT NULL,
    amount      NUMERIC(10, 2) NOT NULL,
    batch_file  VARCHAR(255)
)
;
