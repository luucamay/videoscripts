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

CREATE TABLE `tciudad` (
  `cod_ciu` int(11) NOT NULL AUTO_INCREMENT,
  `nom_ciu` varchar(100) NOT NULL,
  `nom_ciu2` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`cod_ciu`)
)

INSERT INTO tciudad (cod_ciu,nom_ciu)
VALUES ('200', 'La Paz');

CREATE TABLE `tvcanal` (
  `cod_canal` int(10) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `numero` varchar(10) NOT NULL,
  `cod_ciudad` int(10) NOT NULL,
  `estado` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`cod_canal`),
  UNIQUE KEY `ucanal` (`nombre`,`numero`,`cod_ciudad`)
) ENGINE=MyISAM AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;

INSERT INTO tvcanal (cod_canal, nombre, numero, cod_ciudad)
VALUES ('1', 'BTV', '5', '200');

CREATE TABLE `tvrubro` (
  `cod_rubro` int(11) NOT NULL,
  `nom_rubro` varchar(255) NOT NULL,
  `estado` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`cod_rubro`),
  UNIQUE KEY `nom_rubro` (`nom_rubro`)
);

INSERT INTO tvrubro (cod_rubro, nom_rubro, estado)
VALUES (159, 'BANCOS', 1);

CREATE TABLE `tvanunciante` (
  `cod_anu` int(11) NOT NULL,
  `anunciante` varchar(255) NOT NULL,
  `estado` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`cod_anu`),
  UNIQUE KEY `anun` (`anunciante`)
);

INSERT INTO tvanunciante (cod_anu, anunciante, estado)
VALUES (9, 'BANCO MERCANTIL SANTA CRUZ S.A.',1 );

CREATE TABLE `tvproducto` (
  `cod_producto` int(10) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `cod_anu` int(10) NOT NULL,
  `cod_rubro` int(10) NOT NULL,
  `estado` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`cod_producto`),
  KEY `u_prodtv` (`cod_anu`,`nombre`)
);

INSERT INTO tvproducto (cod_producto, nombre, cod_anu, cod_rubro, estado)
VALUES (1313, 'INSTITUCIONAL', 9, 159, 1);