-- MySQL Script generated by MySQL Workbench
-- Thu Nov 22 10:31:01 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema acidentesdb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `acidentesdb` ;

-- -----------------------------------------------------
-- Schema acidentesdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `acidentesdb` DEFAULT CHARACTER SET utf8 ;
USE `acidentesdb` ;

-- -----------------------------------------------------
-- Table `acidentesdb`.`causa_acidente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`causa_acidente` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`causa_acidente` (
  `id_causa_acidente` INT(11) NOT NULL AUTO_INCREMENT,
  `causa_acidente` VARCHAR(90) NULL DEFAULT NULL,
  PRIMARY KEY (`id_causa_acidente`),
  UNIQUE INDEX `id_causa_acidente` (`id_causa_acidente` ASC),
  UNIQUE INDEX `causa_acidente` (`causa_acidente` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`classificacao_acidente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`classificacao_acidente` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`classificacao_acidente` (
  `id_classificacao_acidente` INT(11) NOT NULL AUTO_INCREMENT,
  `classificacao_acidente` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_classificacao_acidente`),
  UNIQUE INDEX `classificacao_acidente` (`classificacao_acidente` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`br`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`br` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`br` (
  `id_br` INT(11) NOT NULL AUTO_INCREMENT,
  `br` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_br`),
  UNIQUE INDEX `br` (`br` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`uf`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`uf` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`uf` (
  `id_uf` INT(11) NOT NULL AUTO_INCREMENT,
  `uf` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_uf`),
  UNIQUE INDEX `uf` (`uf` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`municipio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`municipio` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`municipio` (
  `id_municipio` INT(11) NOT NULL AUTO_INCREMENT,
  `municipio` VARCHAR(45) NULL DEFAULT NULL,
  `id_uf` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id_municipio`),
  UNIQUE INDEX `municipio` (`municipio` ASC),
  INDEX `id_uf_idx` (`id_uf` ASC),
  CONSTRAINT `id_uf`
    FOREIGN KEY (`id_uf`)
    REFERENCES `acidentesdb`.`uf` (`id_uf`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`endereco`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`endereco` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`endereco` (
  `id_endereco` INT(11) NOT NULL AUTO_INCREMENT,
  `id_br` INT(11) NULL DEFAULT NULL,
  `km` VARCHAR(45) NULL DEFAULT NULL,
  `id_municipio` INT(11) NULL DEFAULT NULL,
  `latitude` VARCHAR(45) NULL DEFAULT NULL,
  `longitude` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_endereco`),
  UNIQUE INDEX `latitude` (`latitude` ASC, `longitude` ASC),
  INDEX `id_br_idx` (`id_br` ASC),
  INDEX `id_municipio_idx` (`id_municipio` ASC),
  CONSTRAINT `id_br`
    FOREIGN KEY (`id_br`)
    REFERENCES `acidentesdb`.`br` (`id_br`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_municipio`
    FOREIGN KEY (`id_municipio`)
    REFERENCES `acidentesdb`.`municipio` (`id_municipio`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`condicao_metereologica`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`condicao_metereologica` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`condicao_metereologica` (
  `id_condicao_metereologica` INT(11) NOT NULL AUTO_INCREMENT,
  `condicao_metereologica` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_condicao_metereologica`),
  UNIQUE INDEX `condicao_metereologica` (`condicao_metereologica` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`tipo_pista`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`tipo_pista` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`tipo_pista` (
  `id_tipo_pista` INT(11) NOT NULL AUTO_INCREMENT,
  `tipo_pista` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_tipo_pista`),
  UNIQUE INDEX `tipo_pista` (`tipo_pista` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`uso_solo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`uso_solo` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`uso_solo` (
  `id_uso_solo` INT(11) NOT NULL AUTO_INCREMENT,
  `uso_solo` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_uso_solo`),
  UNIQUE INDEX `uso_solo` (`uso_solo` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`pista`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`pista` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`pista` (
  `id_pista` INT(11) NOT NULL AUTO_INCREMENT,
  `id_condicao_metereologica` INT(11) NULL DEFAULT NULL,
  `id_tipo_pista` INT(11) NULL DEFAULT NULL,
  `id_uso_solo` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id_pista`),
  INDEX `id_condicao_metereologica_idx` (`id_condicao_metereologica` ASC),
  INDEX `id_tipo_pista_idx` (`id_tipo_pista` ASC),
  INDEX `id_uso_solo_idx` (`id_uso_solo` ASC),
  CONSTRAINT `id_condicao_metereologica`
    FOREIGN KEY (`id_condicao_metereologica`)
    REFERENCES `acidentesdb`.`condicao_metereologica` (`id_condicao_metereologica`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_tipo_pista`
    FOREIGN KEY (`id_tipo_pista`)
    REFERENCES `acidentesdb`.`tipo_pista` (`id_tipo_pista`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_uso_solo`
    FOREIGN KEY (`id_uso_solo`)
    REFERENCES `acidentesdb`.`uso_solo` (`id_uso_solo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`tipo_acidente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`tipo_acidente` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`tipo_acidente` (
  `id_tipo_acidente` INT(11) NOT NULL AUTO_INCREMENT,
  `tipo_acidente` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_tipo_acidente`),
  UNIQUE INDEX `tipo_acidente` (`tipo_acidente` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`tipo_veiculo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`tipo_veiculo` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`tipo_veiculo` (
  `id_tipo_veiculo` INT(11) NOT NULL AUTO_INCREMENT,
  `tipo_veiculo` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_tipo_veiculo`),
  UNIQUE INDEX `tipo_veiculo` (`tipo_veiculo` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`acidente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`acidente` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`acidente` (
  `id_acidente` INT(11) NOT NULL AUTO_INCREMENT,
  `id_causa_acidente` INT(11) NULL,
  `id_tipo_acidente` INT(11) NULL,
  `id_classificacao_acidente` INT(11) NULL DEFAULT NULL,
  `id_pista` INT(11) NULL DEFAULT NULL,
  `id_endereco` INT(11) NULL DEFAULT NULL,
  `id_tipo_veiculo` INT(11) NULL,
  `data_inversa` VARCHAR(45) NULL,
  `horario` VARCHAR(45) NULL,
  PRIMARY KEY (`id_acidente`),
  UNIQUE INDEX `id_causa_acidente` (`id_causa_acidente` ASC, `id_tipo_acidente` ASC, `id_classificacao_acidente` ASC, `id_pista` ASC, `id_endereco` ASC),
  INDEX `id_tipo_acidente_idx` (`id_tipo_acidente` ASC),
  INDEX `id_classificacao_acidente_idx` (`id_classificacao_acidente` ASC),
  INDEX `id_causa_acidente_idx` (`id_causa_acidente` ASC),
  INDEX `id_pista_idx` (`id_pista` ASC),
  INDEX `id_endereco_idx` (`id_endereco` ASC),
  INDEX `id_tipo_veiculo_idx` (`id_tipo_veiculo` ASC),
  CONSTRAINT `id_causa_acidente`
    FOREIGN KEY (`id_causa_acidente`)
    REFERENCES `acidentesdb`.`causa_acidente` (`id_causa_acidente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_classificacao_acidente`
    FOREIGN KEY (`id_classificacao_acidente`)
    REFERENCES `acidentesdb`.`classificacao_acidente` (`id_classificacao_acidente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_endereco`
    FOREIGN KEY (`id_endereco`)
    REFERENCES `acidentesdb`.`endereco` (`id_endereco`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_pista`
    FOREIGN KEY (`id_pista`)
    REFERENCES `acidentesdb`.`pista` (`id_pista`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_tipo_acidente`
    FOREIGN KEY (`id_tipo_acidente`)
    REFERENCES `acidentesdb`.`tipo_acidente` (`id_tipo_acidente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_tipo_veiculo`
    FOREIGN KEY (`id_tipo_veiculo`)
    REFERENCES `acidentesdb`.`tipo_veiculo` (`id_tipo_veiculo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`estado_fisico`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`estado_fisico` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`estado_fisico` (
  `id_estado_fisico` INT(11) NOT NULL AUTO_INCREMENT,
  `estado_fisico` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_estado_fisico`),
  UNIQUE INDEX `estado_fisico` (`estado_fisico` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`sexo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`sexo` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`sexo` (
  `id_sexo` INT(11) NOT NULL AUTO_INCREMENT,
  `sexo` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_sexo`),
  UNIQUE INDEX `sexo` (`sexo` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`tipo_envolvido`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`tipo_envolvido` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`tipo_envolvido` (
  `id_tipo_envolvido` INT(11) NOT NULL AUTO_INCREMENT,
  `tipo_envolvido` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_tipo_envolvido`),
  UNIQUE INDEX `tipo_envolvido` (`tipo_envolvido` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`pessoa`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`pessoa` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`pessoa` (
  `pes_id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_tipo_envolvido` INT(11) NULL DEFAULT NULL,
  `idade` INT(11) NULL DEFAULT NULL,
  `id_sexo` INT(11) NULL DEFAULT NULL,
  `id_estado_fisico` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`pes_id`),
  UNIQUE INDEX `id_tipo_envolvido` (`id_tipo_envolvido` ASC, `idade` ASC, `id_sexo` ASC, `id_estado_fisico` ASC),
  INDEX `id_sexo_idx` (`id_sexo` ASC),
  INDEX `id_estado_fisico_idx` (`id_estado_fisico` ASC),
  INDEX `id_tipo_envolvido_idx` (`id_tipo_envolvido` ASC),
  CONSTRAINT `id_estado_fisico`
    FOREIGN KEY (`id_estado_fisico`)
    REFERENCES `acidentesdb`.`estado_fisico` (`id_estado_fisico`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_sexo`
    FOREIGN KEY (`id_sexo`)
    REFERENCES `acidentesdb`.`sexo` (`id_sexo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_tipo_envolvido`
    FOREIGN KEY (`id_tipo_envolvido`)
    REFERENCES `acidentesdb`.`tipo_envolvido` (`id_tipo_envolvido`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `acidentesdb`.`acidente_pessoa`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `acidentesdb`.`acidente_pessoa` ;

CREATE TABLE IF NOT EXISTS `acidentesdb`.`acidente_pessoa` (
  `id_pessoa` INT(11) NOT NULL,
  `id_acidente` INT(11) NOT NULL,
  PRIMARY KEY (`id_pessoa`, `id_acidente`),
  INDEX `id_acidente_idx` (`id_acidente` ASC),
  CONSTRAINT `id_acidente`
    FOREIGN KEY (`id_acidente`)
    REFERENCES `acidentesdb`.`acidente` (`id_acidente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `id_pessoa`
    FOREIGN KEY (`id_pessoa`)
    REFERENCES `acidentesdb`.`pessoa` (`pes_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
