-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 10, 2015 at 05:31 PM
-- Server version: 5.5.41
-- PHP Version: 5.4.4-14+deb7u12

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `WeatherPi`
--

-- --------------------------------------------------------

--
-- Table structure for table `PowerSystem`
--

CREATE TABLE IF NOT EXISTS `PowerSystem` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `batteryVoltage` float NOT NULL,
  `batteryCurrent` float NOT NULL,
  `solarVoltage` float NOT NULL,
  `solarCurrent` float NOT NULL,
  `loadVoltage` float NOT NULL,
  `loadCurrent` float NOT NULL,
  `batteryPower` float NOT NULL,
  `solarPower` float NOT NULL,
  `loadPower` float NOT NULL,
  `batteryCharge` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6381 ;

-- --------------------------------------------------------

--
-- Table structure for table `Sunlight`
--

CREATE TABLE IF NOT EXISTS `Sunlight` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` datetime NOT NULL,
  `Visible` int(11) NOT NULL,
  `IR` int(250) NOT NULL,
  `UV` int(250) NOT NULL,
  `UVIndex` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------
--
-- Table structure for table `systemlog`
--

CREATE TABLE IF NOT EXISTS `systemlog` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` datetime NOT NULL,
  `Level` int(11) NOT NULL,
  `Source` varchar(250) NOT NULL,
  `Message` varchar(250) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=295 ;

-- --------------------------------------------------------

--
-- Table structure for table `WeatherData`
--

CREATE TABLE IF NOT EXISTS `WeatherData` (
  `ID` int(20) NOT NULL AUTO_INCREMENT,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `as3935LightningCount` float NOT NULL,
  `as3935LastInterrupt` float NOT NULL,
  `as3935LastDistance` float NOT NULL,
  `as3935LastStatus` varchar(200) NOT NULL,
  `currentWindSpeed` float NOT NULL,
  `currentWindGust` float NOT NULL,
  `currentWindDirection` float NOT NULL,
  `currentWindDirectionVoltage` float NOT NULL,
  `totalRain` float NOT NULL,
  `bmp180Temperature` int(20) NOT NULL,
  `bmp180Pressure` float NOT NULL,
  `bmp180Altitude` float NOT NULL,
  `bmp180SeaLevel` float NOT NULL,
  `outsideTemperature` float NOT NULL,
  `outsideHumidity` float NOT NULL,
  `insideTemperature` float NOT NULL,
  `insideHumidity` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='Weather Data' AUTO_INCREMENT=6019 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

