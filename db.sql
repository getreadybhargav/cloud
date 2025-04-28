/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - medicalstorage
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`medicalstorage` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `medicalstorage`;

/*Table structure for table `filerequest` */

DROP TABLE IF EXISTS `filerequest`;

CREATE TABLE `filerequest` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `FileId` varchar(20) DEFAULT NULL,
  `doemail` varchar(200) DEFAULT NULL,
  `patirntname` varchar(200) DEFAULT NULL,
  `age` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `temperature` varchar(200) DEFAULT NULL,
  `respiratory` varchar(200) DEFAULT NULL,
  `pulserate` varchar(200) DEFAULT NULL,
  `motion` varchar(200) DEFAULT NULL,
  `hydration` varchar(200) DEFAULT NULL,
  `gas` varchar(200) DEFAULT NULL,
  `glucose` varchar(200) DEFAULT NULL,
  `FileName` varchar(200) DEFAULT NULL,
  `Keywords` varchar(200) DEFAULT NULL,
  `Files` varchar(200) DEFAULT NULL,
  `Secratekey` varchar(200) DEFAULT NULL,
  `Tagname` varchar(200) DEFAULT NULL,
  `pemail` varchar(200) DEFAULT NULL,
  `OTP` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `Verification` varchar(200) DEFAULT 'pending',
  `Requestedtime` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `filerequest` */

insert  into `filerequest`(`id`,`FileId`,`doemail`,`patirntname`,`age`,`contact`,`address`,`temperature`,`respiratory`,`pulserate`,`motion`,`hydration`,`gas`,`glucose`,`FileName`,`Keywords`,`Files`,`Secratekey`,`Tagname`,`pemail`,`OTP`,`status`,`Verification`,`Requestedtime`) values (1,'1','preeti@gmail.com','shiva','25','07458965874','tpt','89','bronchitis','below_60','Yes','60_100','No','normal_postprandial','file','123','E9	és·€a9Æçm7È€“Ó­©Ý}«Aé¤¬AV{²\">#ƒ¤±Ûq†><´L','YNSWsQJO','cloud tag','shiva@gmail.com','494780','Accepted','Verified','2024-07-23 17:27:11');

/*Table structure for table `filesupload` */

DROP TABLE IF EXISTS `filesupload`;

CREATE TABLE `filesupload` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `doemail` varchar(200) DEFAULT NULL,
  `patirntname` varchar(200) DEFAULT NULL,
  `age` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `temperature` varchar(200) DEFAULT NULL,
  `respiratory` varchar(200) DEFAULT NULL,
  `pulserate` varchar(200) DEFAULT NULL,
  `motion` varchar(200) DEFAULT NULL,
  `hydration` varchar(200) DEFAULT NULL,
  `gas` varchar(200) DEFAULT NULL,
  `glucose` varchar(200) DEFAULT NULL,
  `FileName` varchar(200) DEFAULT NULL,
  `Secratekey` varchar(200) DEFAULT 'pending',
  `Tagname` varchar(200) DEFAULT 'null',
  `Verification` varchar(200) DEFAULT 'Wating',
  `Keywords` varchar(200) DEFAULT NULL,
  `Files` varchar(200) DEFAULT NULL,
  `DateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `filesupload` */

insert  into `filesupload`(`id`,`doemail`,`patirntname`,`age`,`contact`,`address`,`temperature`,`respiratory`,`pulserate`,`motion`,`hydration`,`gas`,`glucose`,`FileName`,`Secratekey`,`Tagname`,`Verification`,`Keywords`,`Files`,`DateTime`) values (1,'preeti@gmail.com','shiva','25','07458965874','tpt','89','bronchitis','below_60','Yes','60_100','No','normal_postprandial','file','YNSWsQJO','cloud tag','Verified','123','E9	és·€a9Æçm7È€“Ó­©Ý}«Aé¤¬AV{²\">#ƒ¤±Ûq†><´L','2024-07-23 13:22:24');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `full_name` varchar(200) DEFAULT NULL,
  `phone` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `security_question1` varchar(200) DEFAULT NULL,
  `security_answer1` varchar(200) DEFAULT NULL,
  `security_question2` varchar(200) DEFAULT NULL,
  `security_answer2` varchar(200) DEFAULT NULL,
  `role` varchar(200) DEFAULT NULL,
  `institution` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`id`,`username`,`password`,`email`,`full_name`,`phone`,`address`,`security_question1`,`security_answer1`,`security_question2`,`security_answer2`,`role`,`institution`) values (1,'preeti','a01610228fe998f515a72dd730294d87','preeti@gmail.com','preeti desai','07458965874','tpt','what is your name','preeti','last name','desai','doctor','tpt'),(2,'shiv','a01610228fe998f515a72dd730294d87','shiva@gmail.com','shiva','07458965874','tpt','what is your name','shiva','last name','kumar','Patient','tpt');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;