SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `raspoc`
--
CREATE DATABASE IF NOT EXISTS raspoc;
USE raspoc;
-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ras_fms_hist`
--

CREATE TABLE IF NOT EXISTS `ras_fms_hist` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `kennung` varchar(8) NOT NULL DEFAULT '',
  `status` varchar(2) NOT NULL DEFAULT '',
  `richtung` varchar(15) NOT NULL DEFAULT '',
  `kanal` varchar(8) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Daten für Tabelle `ras_fms_hist`
--


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ras_pocsag_hist`
--

CREATE TABLE IF NOT EXISTS `ras_pocsag_hist` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `ric` varchar(7) NOT NULL DEFAULT '0',
  `funktion` int(1) NOT NULL,
  `text` text NOT NULL,
  KEY `ID` (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Daten für Tabelle `ras_pocsag_hist`
--


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ras_zvei_hist`
--

CREATE TABLE IF NOT EXISTS `ras_zvei_hist` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `schleife` varchar(5) NOT NULL DEFAULT '0',
  `kanal` varchar(8) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Daten für Tabelle `ras_zvei_hist`
--

