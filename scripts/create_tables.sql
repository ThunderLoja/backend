CREATE TABLE colaborador (
    colab_id        NUMERIC(11) NOT NULL,
    colab_nome      VARCHAR(50) NOT NULL,
    colab_cpf       NUMERIC(11) NOT NULL,
    colab_salario   NUMERIC(9,2) NOT NULL,
    colab_data_admi DATE NOT NULL,
    colab_tipo      NUMERIC(2) NOT NULL,
    colab_ger_id    NUMERIC(11),
    colab_senha     VARCHAR(50) NOT NULL
    PRIMARY KEY(colab_id)
);

CREATE TABLE produto (
    prod_id        NUMERIC(11) NOT NULL,
    prod_nome      VARCHAR(30) NOT NULL,
    prod_valor     NUMERIC(9,2) NOT NULL,
    prod_descricao VARCHAR(512) NOT NULL,
    prod_categoria VARCHAR(30) NOT NULL,
    PRIMARY KEY(prod_id)
);

CREATE TABLE estoque (
    prod_id    NUMERIC(11) NOT NULL,
    loja_id    NUMERIC(2) NOT NULL,
    est_quant  NUMERIC(4) NOT NULL,
    PRIMARY KEY (prod_id, loja_id)
);


CREATE TABLE cliente (
    clt_cpf  NUMERIC(11) NOT NULL,
    clt_nome VARCHAR(50) NOT NULL,
    PRIMARY KEY(clt_cpf)
);

CREATE TABLE transacao (
    tr_id        NUMERIC(11) NOT NULL,
    tr_valor     NUMERIC(9,2) NOT NULL,
    tr_data      DATE NOT NULL,
    tr_descricao VARCHAR(512) NOT NULL,
    tr_tipo      NUMERIC(2) NOT NULL,
    PRIMARY KEY (tr_id)
);

CREATE TABLE pagamento (
    tr_id      NUMERIC(11) NOT NULL,
    colab_id   NUMERIC(11) NOT NULL,
    pag_bruto  NUMERIC(9,2) NOT NULL,
    pag_bonus  NUMERIC(9,2),
    pag_fgts   NUMERIC(9,2),
    pag_ferias NUMERIC(9,2),
    pag_13     NUMERIC(9,2),
    PRIMARY KEY (tr_id, colab_id)
);

CREATE TABLE venda (
    tr_id    NUMERIC(11) NOT NULL,
    clt_cpf  NUMERIC(11) NOT NULL,
    colab_id NUMERIC(11) NOT NULL
    PRIMARY KEY(tr_id)
);

CREATE TABLE itens_venda (
    tr_id      NUMERIC(11) NOT NULL,
    prod_id    NUMERIC(11) NOT NULL,
    vend_quant NUMERIC(3) NOT NULL,
    PRIMARY KEY (tr_id, prod_id)
);

ALTER TABLE colaborador
    ADD FOREIGN KEY (colab_ger_id) REFERENCES colaborador(colab_id);

ALTER TABLE estoque
    ADD FOREIGN KEY (prod_id) REFERENCES produto(prod_id);

ALTER TABLE pagamento
    ADD FOREIGN KEY (tr_id)    REFERENCES transacao(tr_id),
    ADD FOREIGN KEY (colab_id) REFERENCES colaborador(colab_id);

ALTER TABLE venda
    ADD FOREIGN KEY (tr_id)    REFERENCES transacao(tr_id),
    ADD FOREIGN KEY (clt_cpf)  REFERENCES cliente(clt_cpf),
    ADD FOREIGN KEY (colab_id) REFERENCES colaborador(colab_id);

ALTER TABLE itens_venda
    ADD FOREIGN KEY (id_venda) REFERENCES venda(id),
    ADD FOREIGN KEY (id_prod)  REFERENCES prod(id);


