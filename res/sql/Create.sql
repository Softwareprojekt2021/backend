-- MySQL Script generated by MySQL Workbench
-- Sat May  8 05:04:11 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema studiboerse
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `studiboerse` ;

-- -----------------------------------------------------
-- Schema studiboerse
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `studiboerse` DEFAULT CHARACTER SET utf8 ;
USE `studiboerse` ;

-- -----------------------------------------------------
-- Table `studiboerse`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`category` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`chat`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`chat` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`chat` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `offer_id` INT NOT NULL,
  INDEX `fk_chat_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_chat_offer1_idx` (`offer_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_chat_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `studiboerse`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_chat_offer1`
    FOREIGN KEY (`offer_id`)
    REFERENCES `studiboerse`.`offer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`message`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`message` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `message` VARCHAR(255) NOT NULL,
  `timestamp` TIMESTAMP NOT NULL,
  `chat_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_message_chat1_idx` (`chat_id` ASC) VISIBLE,
  INDEX `fk_message_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_message_chat1`
    FOREIGN KEY (`chat_id`)
    REFERENCES `studiboerse`.`chat` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_message_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `studiboerse`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`offer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`offer` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`offer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(50) NOT NULL,
  `compensation_type` VARCHAR(50) NOT NULL,
  `price` DECIMAL(5,2) NULL,
  `description` VARCHAR(1000) NULL,
  `sold` TINYINT NULL,
  `category_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_offer_category_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_offer_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_offer_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `studiboerse`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_offer_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `studiboerse`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`picture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`picture` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`picture` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `data` MEDIUMBLOB NOT NULL,
  `offer_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_picture_offer1_idx` (`offer_id` ASC) VISIBLE,
  CONSTRAINT `fk_picture_offer1`
    FOREIGN KEY (`offer_id`)
    REFERENCES `studiboerse`.`offer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`rating`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`rating` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`rating` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rating` SMALLINT NOT NULL,
  `comment` VARCHAR(255) NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rating_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_rating_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `studiboerse`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`university`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`university` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`university` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `university` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`user` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `e_mail` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `course` VARCHAR(50) NOT NULL,
  `profile_picture` MEDIUMBLOB NULL,
  `admin` TINYINT NULL,
  `university_id` INT NOT NULL,
  PRIMARY KEY (`id`, `university_id`),
  INDEX `fk_user_university1_idx` (`university_id` ASC) VISIBLE,
  UNIQUE INDEX `e_mail_UNIQUE` (`e_mail` ASC) VISIBLE,
  CONSTRAINT `fk_user_university1`
    FOREIGN KEY (`university_id`)
    REFERENCES `studiboerse`.`university` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studiboerse`.`watchlist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `studiboerse`.`watchlist` ;

CREATE TABLE IF NOT EXISTS `studiboerse`.`watchlist` (
  `offer_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  INDEX `fk_watchlist_offer1_idx` (`offer_id` ASC) VISIBLE,
  INDEX `fk_watchlist_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_watchlist_offer1`
    FOREIGN KEY (`offer_id`)
    REFERENCES `studiboerse`.`offer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_watchlist_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `studiboerse`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE = ``;

DROP USER IF EXISTS studiboerse_backend;
SET SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
CREATE USER 'studiboerse_backend' IDENTIFIED BY 'R1<$0piXS>Yh:H*P';

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE `studiboerse`.* TO 'studiboerse_backend';
FLUSH PRIVILEGES;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
