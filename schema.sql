-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 28, 2013 at 06:40 AM
-- Server version: 5.5.29
-- PHP Version: 5.3.10-1ubuntu3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `panopticlick`
--

-- --------------------------------------------------------

--
-- Table structure for table `font_total`
--

CREATE TABLE IF NOT EXISTS `font_total` (
  `type` enum('added','removed') NOT NULL,
  `number` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`type`,`number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `markov_estimates`
--

CREATE TABLE IF NOT EXISTS `markov_estimates` (
  `type` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `version1` varchar(255) NOT NULL,
  `version2` varchar(255) NOT NULL,
  `Pba` float NOT NULL,
  `Pba_laplace` float NOT NULL,
  UNIQUE KEY `type` (`type`,`name`,`version1`,`version2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `migration`
--

CREATE TABLE IF NOT EXISTS `migration` (
  `migration_id` int(11) NOT NULL AUTO_INCREMENT,
  `cookie_id` char(32) NOT NULL,
  `visit_from` int(11) NOT NULL,
  `visit_to` int(11) NOT NULL,
  `fonts_added` int(11) NOT NULL,
  `fonts_removed` int(11) NOT NULL,
  `train` tinyint(1) NOT NULL,
  PRIMARY KEY (`migration_id`),
  UNIQUE KEY `visit_from` (`visit_from`,`visit_to`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=36 ;

-- --------------------------------------------------------

--
-- Table structure for table `migration_total`
--

CREATE TABLE IF NOT EXISTS `migration_total` (
  `type` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `version1` varchar(255) NOT NULL DEFAULT '',
  `version2` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL,
  PRIMARY KEY (`type`,`name`,`version1`,`version2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `software`
--

CREATE TABLE IF NOT EXISTS `software` (
  `visit_id` int(11) NOT NULL,
  `cookie_id` varchar(32) NOT NULL,
  `type` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  PRIMARY KEY (`visit_id`,`type`,`name`,`version`),
  KEY `visit_id` (`visit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `software_total`
--

CREATE TABLE IF NOT EXISTS `software_total` (
  `type` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL,
  PRIMARY KEY (`type`,`name`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tested`
--

CREATE TABLE IF NOT EXISTS `tested` (
  `migration_id` int(11) NOT NULL,
  `result_visit_id` int(11) NOT NULL,
  `correct` tinyint(1) NOT NULL,
  `prob` float NOT NULL,
  `time` float NOT NULL,
  UNIQUE KEY `migration_id` (`migration_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `visit`
--

CREATE TABLE IF NOT EXISTS `visit` (
  `id` int(11) NOT NULL,
  `cookie_id` varchar(255) DEFAULT NULL,
  `js` tinyint(4) NOT NULL DEFAULT '0',
  `cookie_enabled` varchar(10) DEFAULT 'unknown',
  `user_agent` text NOT NULL,
  `http_accept` text NOT NULL,
  `plugins` text,
  `fonts` text,
  `timezone` varchar(255) DEFAULT NULL,
  `video` varchar(255) DEFAULT NULL,
  `signature` varchar(32) NOT NULL DEFAULT '',
  `supercookies` varchar(255) DEFAULT NULL,
  `ua_h` char(32) DEFAULT NULL,
  `ft_h` char(32) DEFAULT NULL,
  `ha_h` char(32) DEFAULT NULL,
  `pi_h` char(32) DEFAULT NULL,
  `ip` varbinary(16) DEFAULT NULL,
  `ip34` varbinary(16) DEFAULT NULL,
  `timestamp` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
  KEY `cookie_id` (`cookie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
