--init.sql
CREATE TYPE lrr_enum AS ENUM ('oficio', 'comunicado', 'instrucao normativa', 'resolucao', 'informe');

-- Criação da tabela lrr
CREATE TABLE IF NOT EXISTS lrr (
    id SERIAL PRIMARY KEY,
    regulator VARCHAR(255) NOT NULL,
    publication_date DATE NOT NULL,
    effective_date DATE NOT NULL,
    lrr_type lrr_enum NOT NULL,
    repealed_lrr BOOLEAN NOT NULL DEFAULT FALSE,  
    file_url VARCHAR(2083),
    lrr_explanation TEXT,
    pdf BYTEA 
);

CREATE TABLE IF NOT EXISTS tag (
    id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100) NOT NULL UNIQUE,
    tag_explanation TEXT
);

CREATE TABLE IF NOT EXISTS lrr_tag (
    lrr_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (lrr_id, tag_id),
    FOREIGN KEY (lrr_id) REFERENCES lrr(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);

INSERT INTO tag (tag_name, tag_explanation) VALUES
('Sustentabilidade', 'Tags relacionadas a práticas sustentáveis e ambientais.'),
('Saúde', 'Tags relacionadas a regulamentações na área da saúde.'),
('Economia', 'Tags relacionadas a políticas econômicas.'),
('Educação', 'Tags relacionadas à área educacional.'),
('Segurança', 'Tags relacionadas a normas de segurança.');

    
INSERT INTO lrr (regulator, publication_date, effective_date, lrr_type, repealed_lrr, file_url, lrr_explanation) VALUES
('B3', '2024-01-10', '2024-02-01', 'resolucao', FALSE, 'http://example.com/lei1.pdf', 'Regulamentação sobre áreas protegidas.'),
('B3', '2024-02-15', '2024-03-01', 'instrucao normativa', FALSE, 'http://example.com/lei2.pdf', 'Normas para controle sanitário em hospitais.'),
('B3', '2024-03-20', '2024-04-01', 'oficio', FALSE, 'http://example.com/lei3.pdf', 'Política monetária e taxas de juros.'),
('B3', '2024-04-25', '2024-05-01', 'resolucao', FALSE, 'http://example.com/lei4.pdf', 'Diretrizes para o ensino básico.'),
('B3', '2024-05-30', '2024-06-01', 'comunicado', FALSE, 'http://example.com/lei5.pdf', 'Protocolos de segurança em áreas públicas.'),
('B3', '2024-06-10', '2024-07-01', 'resolucao', FALSE, 'http://example.com/lei6.pdf', 'Regulamentação sobre resíduos sólidos.'),
('B3', '2024-07-15', '2024-08-01', 'instrucao normativa', FALSE, 'http://example.com/lei7.pdf', 'Normas para produção de medicamentos.'),
('B3', '2024-08-20', '2024-09-01', 'oficio', FALSE, 'http://example.com/lei8.pdf', 'Regulamentação de criptomoedas.'),
('B3', '2024-09-25', '2024-10-01', 'resolucao', FALSE, 'http://example.com/lei9.pdf', 'Educação digital nas escolas públicas.'),
('B3', '2024-10-30', '2024-11-01', 'comunicado', FALSE, 'http://example.com/lei10.pdf', 'Medidas de segurança em eventos de grande porte.'),
('B3', '2024-11-10', '2024-12-01', 'resolucao', FALSE, 'http://example.com/lei11.pdf', 'Proteção de mananciais.'),
('B3', '2024-12-15', '2025-01-01', 'instrucao normativa', FALSE, 'http://example.com/lei12.pdf', 'Vacinação obrigatória para doenças tropicais.'),
('B3', '2025-01-20', '2025-02-01', 'oficio', FALSE, 'http://example.com/lei13.pdf', 'Controle de fluxo de capital estrangeiro.'),
('B3', '2025-02-25', '2025-03-01', 'resolucao', FALSE, 'http://example.com/lei14.pdf', 'Programas de intercâmbio estudantil.'),
('B3', '2025-03-30', '2025-04-01', 'comunicado', FALSE, 'http://example.com/lei15.pdf', 'Normas de segurança para transporte público.');

INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (1, 1), (1, 5);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (2, 2);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (3, 3);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (4, 4);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (5, 5);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (6, 1);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (7, 2);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (8, 3);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (9, 4), (9, 1);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (10, 5);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (11, 1);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (12, 2);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (13, 3);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (14, 4);
INSERT INTO lrr_tag (lrr_id, tag_id) VALUES (15, 5), (15, 3);

-- Criação da tabela audio
CREATE TABLE IF NOT EXISTS audio_data (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL UNIQUE,
    audio_bytes BYTEA NOT NULL,
    transcription TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);