-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 10, 2014 at 10:37 AM
-- Server version: 5.5.34
-- PHP Version: 5.3.10-1ubuntu3.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `gpcrtools`
--

-- --------------------------------------------------------

--
-- Table structure for table `protein_selection_set`
--

CREATE TABLE IF NOT EXISTS `protein_selection_set` (
  `protein_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `selection_set_id` smallint(5) unsigned NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `protein_selection_set`
--

INSERT INTO `protein_selection_set` (`protein_id`, `selection_set_id`) VALUES
('acm2_human', 1),
('acm3_rat', 1),
('adrb1_melga', 1),
('adrb2_human', 1),
('drd3_human', 1),
('hrh1_human', 1),
('5ht1b_human', 1),
('5ht2b_human', 1),
('ccr5_human', 1),
('cxcr4_human', 1),
('ntr1_rat', 1),
('oprd_mouse', 1),
('oprd_human', 1),
('oprk_human', 1),
('oprm_mouse', 1),
('oprx_human', 1),
('par1_human', 1),
('opsd_bovin', 1),
('opsd_todpa', 1),
('aa2ar_human', 1),
('p2y12_human', 1),
('s1pr1_human', 1),
('ffar1_human', 1),
('crfr1_human', 1),
('glr_human', 1),
('grm1_human', 1),
('grm5_human', 1),
('smo_human', 1);

-- --------------------------------------------------------

--
-- Table structure for table `selection_set`
--

CREATE TABLE IF NOT EXISTS `selection_set` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` tinytext CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

--
-- Dumping data for table `selection_set`
--

INSERT INTO `selection_set` (`id`, `name`) VALUES
(1, 'Crystallized receptors');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
