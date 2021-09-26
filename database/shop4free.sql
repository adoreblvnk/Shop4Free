-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jul 18, 2021 at 06:49 AM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shop4free`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(125) NOT NULL,
  `lastName` varchar(125) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(25) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(128) NOT NULL,
  `type` varchar(20) NOT NULL,
  `confirmCode` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `firstName`, `lastName`, `email`, `mobile`, `address`, `password`, `type`, `confirmCode`) VALUES
(4, 'lazy', 'mod', 'test@gmail.com', '83019482', 'geylang, SG', '1942fc2821679bef38e449e15955dcf412ba2301de1b3f33ae885e929d3cd45c5cc3b09875ede179605d390a6d66881f8954f2db256141eb0367d609415ea122', 'manager', '0');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `pid` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `oplace` text NOT NULL,
  `dstatus` varchar(10) NOT NULL DEFAULT 'no',
  `odate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ddate` date DEFAULT NULL,
  `api_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `uid`, `pid`, `quantity`, `oplace`, `dstatus`, `odate`, `ddate`, `api_id`) VALUES
(1, 12, 1, 2, 'malware, SG', 'no', '2020-09-21 13:05:07', NULL, 'price_1JEEnpKE133RrhbdCn1c1fjC'),
(2, 12, 1, 3, 'clone, SG', 'no', '2020-09-21 13:08:55', NULL, 'price_1JEEnpKE133RrhbdCn1c1fjC'),
(3, 13, 2, 4, 'soho, SG', 'no', '2020-09-21 13:13:04', NULL, 'price_1JEG5eKE133RrhbdMHAnSYFw'),
(4, 14, 4, 1, 'shake, SG', 'no', '2020-09-21 13:18:47', NULL, 'price_1JEG7XKE133RrhbdEAzLvPd5'),
(5, 12, 9, 4, 'icarus, SG', 'no', '2020-09-22 02:01:02', NULL, 'price_1JEG93KE133Rrhbdys5K7wmm');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pName` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `description` text NOT NULL,
  `available` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `item` varchar(100) NOT NULL,
  `pCode` varchar(20) NOT NULL,
  `picture` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `api_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `pName`, `price`, `description`, `available`, `category`, `item`, `pCode`, `picture`, `date`, `api_id`) VALUES
(1, 'apple juice', 120, 'thirsty for vulnerabilities.', 4, 'fruit', 'fruits', 'f-007', 'apple-juice.png', '2020-09-19 15:10:40', 'price_1JEEnpKE133RrhbdCn1c1fjC'),
(2, 'broccoli', 2, 'dull-tasting. ~toxiklive', 3, 'vegetable', 'vegetable', 'v-004', 'broccoli.png', '2020-09-19 15:40:28', 'price_1JEG5eKE133RrhbdMHAnSYFw'),
(3, 'beef steak', 1, 'slightly too cheap. what\'s the catch?', 9, 'meat', 'meat', 'm-001', 'beef-steak.png', '2020-09-19 16:35:44', 'price_1JEGBuKE133RrhbdK0IL82rH'),
(4, 'banana plushie', 25, 'prolly not meant to be eaten. ~xam', 10, 'fruit', 't-shirt', 'f-010', 'banana-plushie.png', '2020-09-19 17:02:04', 'price_1JEG7XKE133RrhbdEAzLvPd5'),
(5, 'peaches', 5, 'clapped. ~dienandt', 20, 'fruit', 'fruits', 'f-005', 'peaches.png', '2020-09-19 16:45:39', 'price_1JEG93KE133Rrhbdys5K7wmm'),
(6, 'lemons', 6, 'sour. ~off lyne', 10, 'fruit', 'fruits', 'f-004', 'lemon.png', '2020-09-19 16:42:11', 'price_1JEG8OKE133Rrhbd56GI6ACR'),
(7, 'pickle rick', 1000, 'i\'m pickle rick. ~xsept', 20, 'vegetable', 'vegetable', 'v-007', 'pickle-rick.png', '2020-09-30 11:52:43', 'price_1JEG6FKE133Rrhbdc1keMcnd'),
(8, 'salmon', 9, 'quite . . . fishy. ~hxlfghoul', 15, 'meat', 'meat', 'm-005', 'salmon.png', '2020-09-30 11:49:08', 'price_1JEGBFKE133RrhbdZ5RWpprc'),
(9, 'pig plushie', 1000, 'animal farm. ~slushex', 20, 'meat', 'meat', 'm-004', 'pig-plushie.png', '2020-09-30 11:48:09', 'price_1JEGArKE133RrhbdkUzWHwiC'),
(10, 'whole chicken', 7, 'peta. ~kedalos', 20, 'meat', 'meat', 'm-003', 'chicken.png', '2020-09-30 11:47:08', 'price_1JEGAHKE133RrhbdSzvXvPj1');

-- --------------------------------------------------------

--
-- Table structure for table `product_level`
--

DROP TABLE IF EXISTS `product_level`;
CREATE TABLE IF NOT EXISTS `product_level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `fruit_juice` varchar(10) NOT NULL DEFAULT 'no',
  `tropical_fruits` varchar(10) NOT NULL DEFAULT 'no',
  `temperate_fruit` varchar(10) NOT NULL DEFAULT 'no',
  `plushies` varchar(10) NOT NULL DEFAULT 'no',
  `vegetables` varchar(10) NOT NULL DEFAULT 'no',
  `pickle_rick` varchar(10) NOT NULL DEFAULT 'no',
  `spoiled_meat` varchar(10) NOT NULL DEFAULT 'no',
  `meat` varchar(10) NOT NULL DEFAULT 'no',
  `fish` varchar(10) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product_level`
--

INSERT INTO `product_level` (`id`, `product_id`, `fruit_juice`, `tropical_fruits`, `temperate_fruit`, `plushies`, `vegetables`, `pickle_rick`, `spoiled_meat`, `meat`, `fish`) VALUES
(1, 1, 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no'),
(2, 2, 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no'),
(4, 4, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no'),
(5, 5, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no'),
(6, 6, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no'),
(7, 7, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no'),
(8, 8, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes'),
(9, 9, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no'),
(10, 10, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'),
(3, 3, 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `product_view`
--

DROP TABLE IF EXISTS `product_view`;
CREATE TABLE IF NOT EXISTS `product_view` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product_view`
--

INSERT INTO `product_view` (`id`, `user_id`, `product_id`, `date`) VALUES
(1, 9, 9, '2018-09-22 02:19:30');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` varchar(128) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `online` varchar(1) NOT NULL DEFAULT '0',
  `activation` varchar(3) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `mobile`, `reg_time`, `online`, `activation`) VALUES
(12, 'John', 'john@gmail.com', 'john', '01bf081276bb54bf2184e66e523332291184183c9dac7a60d0ced0cc5174357cdd1b2309c52d87cf40bac7e54c97efc7ff3156ac9ec0e442d506f8b0962177ae', '', '2018-07-23 14:09:14', '0', 'No'),
(9, 'Thomas', 'thomas@gmail.com', 'thomas', '31c34888d4512c88c31296aa9c9efd0f930515e54b6044a85998b82756e8d67e8ce1cb74f1a38222c0e55450a12749048a40318ef32b5deeba693a72cee89f50', '12345678902', '2018-07-21 06:47:57', '0', 'No'),
(14, 'Harry', 'harry@gmail.com', 'harry', 'ceb9edfb04331ae5814b0e43421e810dcf7dec8a7f4a3486d1bdcd17c078ad6220c6dac8f9d2e3e319786c5b27b87b0bf59609333b78d2c2da8b715ccbeb27fb', '', '2018-09-07 09:02:35', '0', 'No'),
(13, 'Jordan', 'jordan@yahoo.com', 'yourmum', '066641b22f0d91eb21265d2c1f2e79224a0b4657f1248c71f6750b080c260dc32b533173b22729be90fb07567b7e92c4afc4592127696745b7aa66a199b6aaf3', '', '2018-07-26 12:36:57', '0', 'No'),
(15, 'Josh', 'josh@yahoo.com', 'yourfather', '43b713654c4b4376a21aaa6d922b473ed784a3a01d16dfc3e06b6abe3eb86f22d8fba591b74714884cb2e7daecce82fe149e5986b54184be0aed1c95478cea7c', '89345793753', '2018-09-08 13:58:36', '0', 'No'),
(16, 'Test', 'test@gmail.com', 'test', 'fad5207f29b088c5cfdf5844eb85ef45cc5cbf50bc5ab35072836913ed7c7ee97cebe4506161cb6e0d195e2443b2c06177f3d81dac68f9b9028d1a3179a35a06', '89345793513', '2021-07-26 11:58:57', '0', 'No');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
