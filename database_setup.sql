CREATE TABLE IF NOT EXISTS tvmencion(
    cod_mencion INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha_registro DATE,
    fecha_emision DATE,
    cod_canal VARCHAR(255),
    cod_ciu VARCHAR(255),
    cod_rubro VARCHAR(255),
    cod_anunciante VARCHAR(255),
    cod_producto VARCHAR(255),
    nombre_spot VARCHAR(255),
    duracion VARCHAR(50),
    hora_emision TIMESTAMP,
    cod_programa VARCHAR(255),
    observacion VARCHAR(255)
    );