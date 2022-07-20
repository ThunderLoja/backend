INSERT INTO colaborador(colab_nome, colab_cpf, colab_salario, colab_data_admi, colab_tipo, colab_ativo, colab_senha)
VALUES  ('Antonio', 10000000001, 1000.00, '2000-08-01', 1, B'1','senha1');

INSERT INTO colaborador(colab_nome, colab_cpf, colab_salario, colab_data_admi, colab_tipo, colab_ativo, colab_ger_id, colab_senha)
VALUES  ('Lucas Guedes', 10000000002, 200.00, '2000-08-02', 2, B'1', 1, 'senha2'),
        ('Greghory', 10000000003, 300.00, '2000-08-03', 2, B'1', 1, 'senha3'),
        ('Vanderson', 10000000004, 400.00, '2000-08-04', 2, B'0', 1, 'senha4'),
        ('Lucas Schneider', 10000000005, 500.00, '2000-08-05', 2, B'1', 1, 'senha5');

INSERT INTO produto(prod_nome, prod_valor, prod_descricao, prod_categoria, prod_quant)
VALUES  ('ThunderMeia', 25.00, 'Meias cano longo estampada azul e amarela', 'Vestuário', 22),
        ('Calça de pijama P', 35.00, 'Calça de pijama estampada azul e amarela', 'Vestuário', 4),
        ('Calça de pijama M', 35.00, 'Calça de pijama estampada azul e amarela', 'Vestuário', 10),
        ('Calça de pijama G', 35.00, 'Calça de pijama estampada azul e amarela', 'Vestuário', 7),
        ('Camiseta P', 20.00, 'Camiseta estampada azul e amarela', 'Vestuário', 4),
        ('Camiseta M', 20.00, 'Camiseta estampada azul e amarela', 'Vestuário', 10),
        ('Camiseta G', 20.00, 'Camiseta estampada azul e amarela', 'Vestuário', 7),
        ('Mousepad', 10.00, 'Mousepad estampado azul e amarelo', 'Acessórios', 27),
        ('Chaveiro', 7.00, 'Chaveiro abridor de garrafa', 'Acessórios', 3),
        ('Caderno', 20.00, 'Caderno 50 folhas', 'Acessórios', 45),
        ('Poster', 6.00, 'Poster com arte da equipe', 'Decoração', 12),
        ('Cartela de adesivos', 8.00, 'Cartela de adesivos com arte da equipe', 'Decoração', 1);

INSERT INTO cliente(clt_cpf, clt_nome)
VALUES  (00000000001, 'Haug'),
        (00000000002, 'Renzo'),
        (00000000003, 'Hama');


INSERT INTO transacao(tr_valor, tr_data, tr_descricao, tr_tipo)
VALUES(-400.00, '2022-04-01', 'Compra de material', '1');


INSERT INTO transacao(tr_valor, tr_data, tr_descricao, tr_tipo)
VALUES(50.00, '2022-07-01', 'Venda', '2');

INSERT INTO venda(tr_id, clt_cpf, colab_id)
VALUES(2, 00000000001, 5);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(2, 1, 2);


INSERT INTO transacao(tr_valor, tr_data, tr_descricao, tr_tipo)
VALUES(12.00, '2022-07-02', 'Venda', '2');

INSERT INTO venda(tr_id, clt_cpf, colab_id)
VALUES(3, 00000000003, 3);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(3, 11, 1);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(3, 12, 1);


INSERT INTO transacao(tr_valor, tr_data, tr_descricao, tr_tipo)
VALUES(35.00, '2022-07-03', 'Venda', '2');

INSERT INTO venda(tr_id, clt_cpf, colab_id)
VALUES(4, 00000000002, 2);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(4, 3, 1);


INSERT INTO transacao(tr_valor, tr_data, tr_descricao, tr_tipo)
VALUES(44.00, '2022-07-04', 'Venda', '2');

INSERT INTO venda(tr_id, clt_cpf, colab_id)
VALUES(5, 00000000001, 2);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(5, 8, 1);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(5, 9, 2);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(5, 10, 2);


INSERT INTO transacao(tr_valor, tr_data, tr_descricao, tr_tipo)
VALUES(127.00, '2022-07-05', 'Venda', '2');

INSERT INTO venda(tr_id, clt_cpf, colab_id)
VALUES(6, 00000000002, 5);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(6, 1, 3);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(6, 3, 1);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(6, 8, 1);

INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
VALUES(6, 9, 1);
