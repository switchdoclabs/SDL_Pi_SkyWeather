-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 11, 2019 at 03:02 PM
-- Server version: 10.3.15-MariaDB-1
-- PHP Version: 7.0.33-0+deb9u3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SkyWeather`
--
CREATE DATABASE IF NOT EXISTS `SkyWeather` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `SkyWeather`;
-- --------------------------------------------------------

--
-- Table structure for table `PowerSystem`
--

CREATE TABLE `PowerSystem` (
  `ID` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `batteryVoltage` float NOT NULL,
  `batteryCurrent` float NOT NULL,
  `solarVoltage` float NOT NULL,
  `solarCurrent` float NOT NULL,
  `loadVoltage` float NOT NULL,
  `loadCurrent` float NOT NULL,
  `batteryPower` float NOT NULL,
  `solarPower` float NOT NULL,
  `loadPower` float NOT NULL,
  `batteryCharge` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Sunlight`
--

CREATE TABLE `Sunlight` (
  `ID` int(11) NOT NULL,
  `TimeStamp` datetime NOT NULL,
  `Visible` int(11) NOT NULL,
  `IR` int(250) NOT NULL,
  `UV` int(250) NOT NULL,
  `UVIndex` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `systemlog`
--

CREATE TABLE `systemlog` (
  `ID` int(11) NOT NULL,
  `TimeStamp` datetime NOT NULL,
  `Level` int(11) NOT NULL,
  `Source` varchar(250) NOT NULL,
  `Message` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `WeatherData`
--

CREATE TABLE `WeatherData` (
  `ID` int(20) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
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
  `AQI` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Weather Data';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `PowerSystem`
--
ALTER TABLE `PowerSystem`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Sunlight`
--
ALTER TABLE `Sunlight`
  ADD KEY `ID` (`ID`);

--
-- Indexes for table `systemlog`
--
ALTER TABLE `systemlog`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `WeatherData`
--
ALTER TABLE `WeatherData`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `PowerSystem`
--
ALTER TABLE `PowerSystem`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1553;
--
-- AUTO_INCREMENT for table `Sunlight`
--
ALTER TABLE `Sunlight`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1580;
--
-- AUTO_INCREMENT for table `systemlog`
--
ALTER TABLE `systemlog`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2181;
--
-- AUTO_INCREMENT for table `WeatherData`
--
ALTER TABLE `WeatherData`
  MODIFY `ID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1556;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
