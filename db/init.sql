CREATE SCHEMA IF NOT EXISTS `surveys` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;

CREATE TABLE IF NOT EXISTS `surveys`.`logging` (
  `userid` VARCHAR(45) NOT NULL COMMENT '',
  `section` VARCHAR(45) NOT NULL COMMENT '',
  `payload` LONGBLOB NULL COMMENT '',
  `datetime` INT(11) NOT NULL COMMENT '',
  INDEX `user_section` (`userid` ASC, `section` ASC)  COMMENT '');
ENGINE = InnoDB;
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `surveys`.`socinfo` (
  `userid` VARCHAR(45) NOT NULL COMMENT '',
  `round` VARCHAR(10) NOT NULL COMMENT '',
  `percentages` json NOT NULL COMMENT '',
  INDEX `user_section` (`userid` ASC)  COMMENT '');
ENGINE = InnoDB;
DEFAULT CHARACTER SET = utf8;
