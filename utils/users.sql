CREATE DATABASE `users`;
USE `users`;


CREATE TABLE `Users`.`Students` ( 
    `id` INT(11) NOT NULL AUTO_INCREMENT , 
    `name` VARCHAR(100) NOT NULL , 
    `email` VARCHAR(100) NOT NULL ,
    `Age` INT(100) NOT NULL ,
    `City` VARCHAR(100) NOT NULL ,
    PRIMARY KEY (`id`)) ENGINE = InnoDB;

