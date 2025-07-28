INSERT INTO users (id_usuario, nome, senha, email, data_nascimento, sexo) VALUES
(45, 'sabrina', 'senha123', 'sabrina@gmail.com', '2000-01-01', 'Feminino'),
(46, 'eduarda', 'senha123', 'eduarda@gmail.com', '2000-01-01', 'Feminino'),
(47, 'issilany', 'senha123', 'issilany@gmail.com', '2000-01-01', 'Feminino'),
(48, 'priscila', 'senha123', 'priscila@gmail.com', '2000-01-01', 'Feminino'),
(49, 'branda', 'senha123', 'brenda@gmail.com', '2000-01-01', 'Feminino'),
(50, 'heloisa', 'senha123', 'heloisa@gmail.com', '2000-01-01', 'Feminino'),
(51, 'joana', 'senha123', 'joana@gmail.com', '2000-01-01', 'Feminino'),
(52, 'paula', 'senha123', 'paula@gmail.com', '2000-01-01', 'Feminino'),
(53, 'elen', 'senha123', 'elen@gmail.com', '2000-01-01', 'Feminino'),
(54, 'kevia', 'senha123', 'kevia@gmail.com', '2000-01-01', 'Feminino');  
INSERT INTO registro_exercicio (tipo, calorias, intensidade, duracao_minutos, data, id_usuario) VALUES
('Corrida', 300, 'Alta', 30, '2025-07-20', 45),
('Caminhada', 150, 'Baixa', 45, '2025-07-19', 46),
('Natação', 400, 'Média', 60, '2025-07-18', 47),
('Yoga', 100, 'Baixa', 40, '2025-07-20', 48),
('Musculação', 350, 'Alta', 50, '2025-07-21', 49),
('Pilates', 200, 'Média', 30, '2025-07-22', 50),
('Bike', 250, 'Média', 45, '2025-07-23', 51),
('Dança', 300, 'Alta', 60, '2025-07-24', 52),
('Caminhada', 150, 'Baixa', 40, '2025-07-25', 53),
('Corrida', 320, 'Alta', 35, '2025-07-26', 54);


INSERT INTO registro_humor (tipo_humor, data, observacao, id_usuario) VALUES
('Feliz', '2025-07-20', 'Dia ótimo', 45),
('Triste', '2025-07-19', 'Sentindo cansado', 46),
('Animado', '2025-07-18', 'Muita energia', 47),
('Calmo', '2025-07-20', NULL, 48),
('Estressado', '2025-07-21', 'Trabalho acumulado', 49),
('Feliz', '2025-07-22', 'Encontro com amigos', 50),
('Cansado', '2025-07-23', 'Pouco sono', 51),
('Motivado', '2025-07-24', NULL, 52),
('Ansioso', '2025-07-25', 'Prova amanhã', 53),
('Feliz', '2025-07-26', 'Férias chegando', 54);

-- 10 registros de hidratação
INSERT INTO registro_hidratacao (data, quantidade_ml, hora, id_usuario) VALUES
('2025-07-20', 500, '08:00:00', 45),
('2025-07-19', 300, '10:30:00', 46),
('2025-07-18', 700, '12:00:00', 47),
('2025-07-20', 400, '14:15:00', 48),
('2025-07-21', 600, '16:45:00', 49),
('2025-07-22', 500, '09:20:00', 50),
('2025-07-23', 350, '11:00:00', 51),
('2025-07-24', 450, '13:30:00', 52),
('2025-07-25', 550, '15:10:00', 53),
('2025-07-26', 500, '17:40:00', 54);


INSERT INTO registro_atividade_mental (data, duracao_minutos, tipo, observacao, id_usuario) VALUES
('2025-07-20', 60, 'Leitura', 'Livro sobre psicologia', 45),
('2025-07-19', 45, 'Meditação', NULL, 46),
('2025-07-18', 30, 'Estudo', 'Matemática', 47),
('2025-07-20', 90, 'Aulas online', 'Curso de programação', 48),
('2025-07-21', 50, 'Palestra', 'Desenvolvimento pessoal', 49),
('2025-07-22', 40, 'Leitura', 'Novela', 50),
('2025-07-23', 70, 'Meditação', NULL, 51),
('2025-07-24', 60, 'Estudo', 'História', 52),
('2025-07-25', 55, 'Aulas online', 'Design gráfico', 53),
('2025-07-26', 80, 'Leitura', 'Ciência', 54);


INSERT INTO registro_sono (data, hora_inicio, hora_fim, qualidade, id_usuario) VALUES
('2025-07-20', '22:30:00', '06:30:00', 'Boa', 45),
('2025-07-19', '23:00:00', '07:00:00', 'Regular', 46),
('2025-07-18', '21:45:00', '05:45:00', 'Boa', 47),
('2025-07-20', '00:00:00', '08:00:00', 'Ótima', 48),
('2025-07-21', '22:15:00', '06:15:00', 'Regular', 49),
('2025-07-22', '23:30:00', '07:30:00', 'Boa', 50),
('2025-07-23', '22:00:00', '06:00:00', 'Ruim', 51),
('2025-07-24', '22:45:00', '06:45:00', 'Boa', 52),
('2025-07-25', '23:15:00', '07:15:00', 'Ótima', 53),
('2025-07-26', '22:30:00', '06:30:00', 'Boa', 54);


INSERT INTO registro_alimentacao (data, hora, tipo, calorias, id_usuario) VALUES
('2025-07-20', '08:00:00', 'Café da manhã', 350, 45),
('2025-07-19', '12:30:00', 'Almoço', 600, 46),
('2025-07-18', '19:00:00', 'Jantar', 500, 47),
('2025-07-20', '10:00:00', 'Lanche', 200, 48),
('2025-07-21', '13:00:00', 'Almoço', 650, 49),
('2025-07-22', '20:00:00', 'Jantar', 550, 50),
('2025-07-23', '07:30:00', 'Café da manhã', 300, 51),
('2025-07-24', '15:00:00', 'Lanche', 250, 52),
('2025-07-25', '12:00:00', 'Almoço', 620, 53),
('2025-07-26', '18:30:00', 'Jantar', 480, 54);


INSERT INTO registro_alimentacao_descricao (id_registro_alimentacao, descricao) VALUES
(12, 'Pão, café e frutas'),
(12, 'Arroz, feijão, carne e salada'),
(13, 'Sopa de legumes e pão'),
(14, 'Iogurte e bolacha'),
(15, 'Macarrão ao molho branco'),
(16, 'Peixe grelhado com legumes'),
(17, 'Cereal com leite'),
(18, 'Frutas e castanhas'),
(19, 'Feijoada'),
(20, 'Salada e frango grelhado');

-- 10 metas (genéricas)
INSERT INTO meta (valor, id_usuario) VALUES
('Beber 2 litros de água por dia', 45),
('Dormir 8 horas por noite', 46),
('Correr 5 km por dia', 47),
('Meditar 30 minutos por dia', 48),
('Comer 5 porções de frutas por dia', 49),
('Fazer exercícios 4 vezes por semana', 50),
('Ler 1 livro por mês', 51),
('Reduzir açúcar na dieta', 52),
('Aumentar massa muscular', 53),
('Melhorar qualidade do sono', 54);

INSERT INTO registro_alimentacao_descricao (id_registro_alimentacao, descricao) VALUES
(81, 'Pão, café e frutas'),
(82, 'Arroz, feijão, carne e salada'),
(83, 'Sopa de legumes e pão'),
(84, 'Iogurte e bolacha'),
(85, 'Macarrão ao molho branco'),
(86, 'Peixe grelhado com legumes'),
(87, 'Cereal com leite'),
(88, 'Frutas e castanhas'),
(89, 'Feijoada'),
(90, 'Salada e frango grelhado');