-- USUARIO
INSERT INTO usuario (id_usuario, nome, senha, email, data_nascimento, sexo) VALUES
(1, 'sabrina', 'senha123', 'sabrina@gmail.com', '2000-01-01', 'Feminino'),
(2, 'eduarda', 'senha123', 'eduarda@gmail.com', '2000-01-01', 'Feminino'),
(3, 'issilany', 'senha123', 'issilany@gmail.com', '2000-01-01', 'Feminino'),
(4, 'priscila', 'senha123', 'priscila@gmail.com', '2000-01-01', 'Feminino'),
(5, 'branda', 'senha123', 'brenda@gmail.com', '2000-01-01', 'Feminino'),
(6, 'heloisa', 'senha123', 'heloisa@gmail.com', '2000-01-01', 'Feminino'),
(7, 'joana', 'senha123', 'joana@gmail.com', '2000-01-01', 'Feminino'),
(8, 'paula', 'senha123', 'paula@gmail.com', '2000-01-01', 'Feminino'),
(9, 'elen', 'senha123', 'elen@gmail.com', '2000-01-01', 'Feminino'),
(10, 'kevia', 'senha123', 'kevia@gmail.com', '2000-01-01', 'Feminino');

-- REGISTRO EXERCICIO
INSERT INTO registro_exercicio (tipo, calorias, intensidade, duracao_minutos, data, id_usuario) VALUES
('Corrida', 300, 'Alta', 30, '2025-07-20', 1),
('Caminhada', 150, 'Baixa', 45, '2025-07-19', 2),
('Natação', 400, 'Média', 60, '2025-07-18', 3),
('Yoga', 100, 'Baixa', 40, '2025-07-20', 4),
('Musculação', 350, 'Alta', 50, '2025-07-21', 5),
('Pilates', 200, 'Média', 30, '2025-07-22', 6),
('Bike', 250, 'Média', 45, '2025-07-23', 7),
('Dança', 300, 'Alta', 60, '2025-07-24', 8),
('Caminhada', 150, 'Baixa', 40, '2025-07-25', 9),
('Corrida', 320, 'Alta', 35, '2025-07-26', 10);

-- REGISTRO HUMOR
INSERT INTO registro_humor (tipo_humor, data, observacao, id_usuario) VALUES
('Feliz', '2025-07-20', 'Dia ótimo', 1),
('Triste', '2025-07-19', 'Sentindo cansado', 2),
('Animado', '2025-07-18', 'Muita energia', 3),
('Calmo', '2025-07-20', NULL, 4),
('Estressado', '2025-07-21', 'Trabalho acumulado', 5),
('Feliz', '2025-07-22', 'Encontro com amigos', 6),
('Cansado', '2025-07-23', 'Pouco sono', 7),
('Motivado', '2025-07-24', NULL, 8),
('Ansioso', '2025-07-25', 'Prova amanhã', 9),
('Feliz', '2025-07-26', 'Férias chegando', 10);

-- REGISTRO HIDRATAÇÃO
INSERT INTO registro_hidratacao (data, quantidade_ml, hora, id_usuario) VALUES
('2025-07-20', 500, '08:00:00', 1),
('2025-07-19', 300, '10:30:00', 2),
('2025-07-18', 700, '12:00:00', 3),
('2025-07-20', 400, '14:15:00', 4),
('2025-07-21', 600, '16:45:00', 5),
('2025-07-22', 500, '09:20:00', 6),
('2025-07-23', 350, '11:00:00', 7),
('2025-07-24', 450, '13:30:00', 8),
('2025-07-25', 550, '15:10:00', 9),
('2025-07-26', 500, '17:40:00', 10);

-- REGISTRO ATIVIDADE MENTAL
INSERT INTO registro_atividade_mental (data, duracao_minutos, tipo, observacao, id_usuario) VALUES
('2025-07-20', 60, 'Leitura', 'Livro sobre psicologia', 1),
('2025-07-19', 45, 'Meditação', NULL, 2),
('2025-07-18', 30, 'Estudo', 'Matemática', 3),
('2025-07-20', 90, 'Aulas online', 'Curso de programação', 4),
('2025-07-21', 50, 'Palestra', 'Desenvolvimento pessoal', 5),
('2025-07-22', 40, 'Leitura', 'Novela', 6),
('2025-07-23', 70, 'Meditação', NULL, 7),
('2025-07-24', 60, 'Estudo', 'História', 8),
('2025-07-25', 55, 'Aulas online', 'Design gráfico', 9),
('2025-07-26', 80, 'Leitura', 'Ciência', 10);

-- REGISTRO SONO
INSERT INTO registro_sono (data, hora_inicio, hora_fim, qualidade, id_usuario) VALUES
('2025-07-20', '22:30:00', '06:30:00', 'Boa', 1),
('2025-07-19', '23:00:00', '07:00:00', 'Regular', 2),
('2025-07-18', '21:45:00', '05:45:00', 'Boa', 3),
('2025-07-20', '00:00:00', '08:00:00', 'Ótima', 4),
('2025-07-21', '22:15:00', '06:15:00', 'Regular', 5),
('2025-07-22', '23:30:00', '07:30:00', 'Boa', 6),
('2025-07-23', '22:00:00', '06:00:00', 'Ruim', 7),
('2025-07-24', '22:45:00', '06:45:00', 'Boa', 8),
('2025-07-25', '23:15:00', '07:15:00', 'Ótima', 9),
('2025-07-26', '22:30:00', '06:30:00', 'Boa', 10);

-- REGISTRO ALIMENTAÇÃO
INSERT INTO registro_alimentacao (data, hora, tipo, calorias, id_usuario) VALUES
('2025-07-20', '08:00:00', 'Café da manhã', 350, 1),
('2025-07-19', '12:30:00', 'Almoço', 600, 2),
('2025-07-18', '19:00:00', 'Jantar', 500, 3),
('2025-07-20', '10:00:00', 'Lanche', 200, 4),
('2025-07-21', '13:00:00', 'Almoço', 650, 5),
('2025-07-22', '20:00:00', 'Jantar', 550, 6),
('2025-07-23', '07:30:00', 'Café da manhã', 300, 7),
('2025-07-24', '15:00:00', 'Lanche', 250, 8),
('2025-07-25', '12:00:00', 'Almoço', 620, 9),
('2025-07-26', '18:30:00', 'Jantar', 480, 10);

-- DESCRIÇÃO DOS ALIMENTOS
INSERT INTO registro_alimentacao_descricao (id_registro_alimentacao, descricao) VALUES
(1, 'Pão, café e frutas'),
(2, 'Arroz, feijão, carne e salada'),
(3, 'Sopa de legumes e pão'),
(4, 'Iogurte e bolacha'),
(5, 'Macarrão ao molho branco'),
(6, 'Peixe grelhado com legumes'),
(7, 'Cereal com leite'),
(8, 'Frutas e castanhas'),
(9, 'Feijoada'),
(10, 'Salada e frango grelhado');

INSERT INTO meta (id_meta, valor, id_usuario) VALUES

(1, 'Agua', 1),
(2, 'Agua', 2),
(3, 'Agua', 3),
(4, 'Agua', 4),
(5, 'Agua', 5),
(6, 'Agua', 6),
(7, 'Agua', 7),
(8, 'Agua', 8),
(9, 'Agua', 9),
(10, 'Agua', 10),
(11, 'Sono', 1),
(12, 'Sono', 2),
(13, 'Sono', 3),
(14, 'Sono', 4),
(15, 'Sono', 5),
(16, 'Sono', 6),
(17, 'Sono', 7),
(18, 'Sono', 8),
(19, 'Sono', 9),
(20, 'Sono', 10),
(21, 'Exercicio', 1),
(22, 'Exercicio', 2),
(23, 'Exercicio', 3),
(24, 'Exercicio', 4),
(25, 'Exercicio', 5),
(26, 'Exercicio', 6),
(27, 'Exercicio', 7),
(28, 'Exercicio', 8),
(29, 'Exercicio', 9),
(30, 'Exercicio', 10);  
INSERT INTO meta_agua (id_meta, id_usuario) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);
INSERT INTO meta_sono (id_meta, id_usuario) VALUES
(11, 1),
(12, 2),
(13, 3),
(14, 4),
(15, 5),
(16, 6),
(17, 7),
(18, 8),
(19, 9),
(20, 10);

INSERT INTO meta_exercicio (id_meta, id_usuario) VALUES
(21, 1),
(22, 2),
(23, 3),
(24, 4),
(25, 5),
(26, 6),
(27, 7),
(28, 8),
(29, 9),
(30, 10);