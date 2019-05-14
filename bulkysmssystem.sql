-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 14, 2019 at 07:05 PM
-- Server version: 5.7.25-0ubuntu0.16.04.2
-- PHP Version: 7.0.33-0ubuntu0.16.04.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bulkysmssystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `address_book`
--

CREATE TABLE `address_book` (
  `contact_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `region` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `ward` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `address_book`
--

INSERT INTO `address_book` (`contact_id`, `first_name`, `middle_name`, `last_name`, `gender`, `birth_date`, `country`, `region`, `district`, `ward`) VALUES
(1, 'Ashalulu', 'S', 'Mwandu', 'Female', '1981-05-29', 'Tanzania', 'Morogoro', 'Morogoro', 'Mbuyuni'),
(2, 'Ntwa', 'A', 'Katule', 'Male', '1982-03-13', 'Tanzania', 'Dar es salaam', 'Kinondoni', 'Kunduchi'),
(3, 'Lucas', 'Ntwa', 'Katule', 'Male', '2080-05-05', 'Tanzania', 'Dar es salaam', 'Kinondoni', 'Kunduchi');

-- --------------------------------------------------------

--
-- Table structure for table `campaigns`
--

CREATE TABLE `campaigns` (
  `campaign_id` int(11) NOT NULL,
  `campaign_name` varchar(200) DEFAULT NULL,
  `campaign_descr` varchar(500) DEFAULT NULL,
  `date_created` date NOT NULL,
  `delivery_mechanism` enum('SMS','Whatsapp','Email') NOT NULL,
  `campaign_category` enum('IR','GR','BW','HG','HO','GM') DEFAULT NULL,
  `target_level` enum('Specific Groups','All') DEFAULT NULL,
  `is_campaign_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `campaigns`
--

INSERT INTO `campaigns` (`campaign_id`, `campaign_name`, `campaign_descr`, `date_created`, `delivery_mechanism`, `campaign_category`, `target_level`, `is_campaign_active`) VALUES
(1, 'Birthday Greetings', 'This campaign has been dedicated for birthday greetings to customers', '2018-11-01', 'SMS', 'BW', 'All', 1),
(5, 'My first campaign', 'I am just testing things', '2018-10-08', 'Whatsapp', 'IR', 'All', 0),
(6, 'My fsecond campaign', 'I am just testing things', '2018-11-07', 'SMS', 'IR', 'All', 0),
(7, 'My third campaign', 'I am just testing things', '2018-11-10', 'SMS', 'IR', 'All', 1),
(10, 'My new Campaign', 'It has has delivery days. Modification also works', '2018-11-12', 'SMS', 'IR', 'All', 1),
(12, 'My other campaign today', 'Nothing much here', '2018-11-13', 'SMS', 'IR', 'Specific Groups', 1),
(13, 'My campaign with defined audience', 'Check my values', '2018-11-20', 'SMS', 'IR', 'Specific Groups', 1),
(14, 'I am still testing', 'Check my values', '2018-11-20', 'SMS', 'IR', 'Specific Groups', 1),
(16, 'Renew of Insurance', 'Renew', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(17, 'Renew of Driver licence', 'edqqwfqw', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(18, 'Renew of Driver licence 2', 'Testing ', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(19, 'Renew of Driver licence 3', 'Testing ', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(20, 'Renew of Driver licence 4', 'Testing ', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(21, 'Renew of Driver licence campaign', 'Testing ', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(22, 'Renew of Driver licence campaign 2', 'Testing ', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(23, 'ASAS Drivers', 'ASAS Drivers', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1),
(24, 'Drivers for Trucks', 'Drivers for trucks.', '2019-05-10', 'SMS', 'IR', 'Specific Groups', 1);

-- --------------------------------------------------------

--
-- Table structure for table `campaigns_defined_messages`
--

CREATE TABLE `campaigns_defined_messages` (
  `campaign_message_id` int(11) NOT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `message_txt` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `campaigns_defined_messages`
--

INSERT INTO `campaigns_defined_messages` (`campaign_message_id`, `campaign_id`, `message_txt`) VALUES
(578, 5, 'Hello. This is my message'),
(579, 5, 'Hello. Another message'),
(580, 6, 'Hello. This is my message'),
(581, 6, 'Hello. Another message'),
(588, 7, 'Hello. This is my message. I have changed it '),
(589, 7, 'Hello. Another message but changed'),
(590, 7, 'Put one extra message'),
(591, 12, 'We are testing thsi campaign'),
(592, 13, 'One defined message'),
(617, 1, 'As you celebrate your birthday, we wish you more success in business. Thank for being with us all this time.'),
(618, 1, 'Happy birthday. We value you as our esteemed customer'),
(619, 1, 'Hello there. We wish you happy birthday. Thank you for being our loyal customer');

-- --------------------------------------------------------

--
-- Table structure for table `campaign_end_day`
--

CREATE TABLE `campaign_end_day` (
  `campaign_id` int(11) NOT NULL,
  `campaign_end_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `campaign_start_day`
--

CREATE TABLE `campaign_start_day` (
  `campaign_id` int(11) NOT NULL,
  `campaign_start_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `campaign_start_day`
--

INSERT INTO `campaign_start_day` (`campaign_id`, `campaign_start_date`) VALUES
(10, '2018-11-21'),
(12, '2018-11-21'),
(13, '2018-11-22'),
(14, '2018-11-22');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `email_details`
--

CREATE TABLE `email_details` (
  `email_id` int(11) NOT NULL,
  `email_address` varchar(50) DEFAULT NULL,
  `is_it_primary_email` tinyint(1) NOT NULL,
  `contact_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `email_details`
--

INSERT INTO `email_details` (`email_id`, `email_address`, `is_it_primary_email`, `contact_id`) VALUES
(3, 'katulentwa@gmail.com', 1, 2),
(4, 'katulentwa@hotmail.com', 0, 2),
(5, 'nkatule@aru.ac.tz', 0, 2),
(6, 'katulentwa@gmail.com', 1, 3),
(7, 'katulentwa@hotmail.com', 1, 3),
(8, 'nkatule@aru.ac.tz', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `recipient_mobile` varchar(20) DEFAULT NULL,
  `message` varchar(1000) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `recipient_mobile`, `message`, `status`) VALUES
(112, '+255742340759', 'Hello. We wish you happy new year...', 0),
(113, '+255742340759', 'Hello. We wish you happy new year...', 0),
(114, '+255742340759', 'Hello Ntwa. You are doing great!!', 0),
(115, '+255742340759', 'Hello. We wish you happy new year...', 0),
(116, '+255742340759', 'Hello. We wish you happy new year...', 0),
(117, '+255742340759', 'We are testing if everything is okay.', 0),
(118, '+255742340759', 'Test if the system still work', 0),
(119, '+255742340759', '', 0),
(120, '+255742340759', 'Test sendin sms', 0),
(121, '+255742340759', '', 0),
(122, '+255742340759', 'Goodnight', 0),
(123, '11', 'test sending', 0),
(124, '11', 'test sending', 0),
(125, '11', 'test sending f', 0),
(126, '11', 'I am sending this', 0),
(127, '11', 'I am sending this', 0),
(128, '11', 'I am sending this', 0),
(129, '11', 'I am sending this', 0),
(130, '11', 'I am sending this', 0),
(131, '11', 'I am sending this', 0),
(132, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(133, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(134, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(135, '+255742340759', 'I am sending this as the final test', 0),
(136, '2', 'Hello, we are testing sending of one SMS.', 0),
(137, '2', 'Hello, we are testing sending of one SMS.', 0),
(138, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(139, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(140, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(141, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(142, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(143, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(144, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(145, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(146, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(147, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(148, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(149, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(150, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(151, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(152, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(153, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(154, '+255718255585', 'Hello, we are testing sending of one SMS.', 0),
(155, '+255742340759', 'Hello, we are testing sending of one SMS.', 0),
(156, '+255742340759', 'Hello Mr. @@firstname@@ @@lastname@@. We remind you to pay your outstanding bills.', 0),
(157, '2', '. We remind you to pay your outstanding billlastnam. We remind you to pay your outstanding bill', 0),
(158, '2', 'Hello Mr. @@firstname@@ @@lastname@@. We remind you to pay your outstanding bill', 0),
(159, '0742340759', 'Hello Mr.  . We remind you to pay your outstanding bill', 0),
(160, '0742340759', 'Hello Mr.  . We remind you to pay your outstanding bill', 0),
(161, '+255742340759', 'Hello Mr. Ntwa Katule. We remind you to pay your outstanding bill', 0),
(162, '+255742340759', 'Happy holidays Ntwa! We value you as our esteemed customer. Thank you for your support.', 0),
(163, '+255742340759', 'Happy holidays Ntwa! We value you as our esteemed customer. Thank you for your support.', 0),
(164, '+255742340759', 'How are you Ntwa. We remind you to pay your outstanding bills.', 0),
(165, '+255742340759', 'How are you Ntwa. We remind you to pay your outstanding bills.', 0),
(166, '+255742340759', 'Hello Mr. Ntwa Katule. We remind you to pay your outstanding bill', 0),
(167, '+255742340759', 'Hello Mr. Ntwa. We remind you to pay your outstanding bill', 0),
(168, '+255742340759', 'Hello Ntwa! We wish you safe journey.', 0),
(169, '+255742340759', 'Happy holidays Ntwa! We value you as our esteemed customer. Thank you for your support.', 0),
(170, '+255658336097', 'Happy holidays Franklin! We value you as our esteemed customer. Thank you for your support.', 0),
(171, '+255658336097', 'Hi Franklin! Drive safely.', 0),
(172, '+255718255585', 'Happy holidays Ntwa! We value you as our esteemed customer. Thank you for your support.', 0),
(173, '+255718255585', 'Happy holidays @@firstname@@! We value you as our esteemed customer. Thank you for your support.', 0),
(174, '+255718255585', 'Happy holidays Ntwa! We value you as our esteemed customer. Thank you for your support.', 0),
(175, '+255742857735', 'How are you Zulfa. We remind you to pay your outstanding bills.', 0),
(177, '+255752333235', 'Habari Miss Anna Mufui. Unakumbushwa kurudisha la ndugu Ntwa Katule kabla hujachukuliwa hatua za kisheria', 0),
(178, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(179, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(180, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(181, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(182, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(183, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(184, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(185, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(186, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(187, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(188, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(189, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(190, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(191, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(192, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(193, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(194, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(195, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(196, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(197, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(198, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(199, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(200, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 1),
(201, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 1),
(202, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 1),
(203, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 1),
(204, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 1),
(205, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(206, '+255742340759', 'Hello Mr. Michael. We remind you to pay your outstanding bill', 0),
(207, '+255742340759', 'Hello Mr. Michael. We would like to inform you about our Xmass offers', 0),
(208, '+255742340759', 'Hello Mr. Michael. We would like to wish happy festive season', 0),
(209, '+255742340759', 'Hello Mr. Michael. We would like to wish happy festive season', 0),
(210, '+255742340759', 'Hello Mr. Michael. We would like to wish happy festive season', 0),
(211, '+255742340759', 'Hi. Michael. We are testing how to schedule messages using threads', 0),
(212, '+255742340759', 'Hi. Michael. We are testing how to schedule messages using threads', 0),
(213, '+255742340759', 'Hi. Michael. We are testing how to schedule messages using threads', 0),
(214, '+255758867676', 'Hi. Ashalulu. We are testing how to schedule messages using threads', 0),
(215, '+255742340759', 'Hi. Ntwa. We are testing how to schedule messages using threads', 0),
(216, '+255758867676', 'Hi. Ashalulu. We are testing how to schedule messages using threads', 0),
(217, '+255742340759', 'Hi. Ntwa. We are testing how to schedule messages using threads', 0),
(218, '+255758867676', 'Hello Ashalulu. We are are in the phase of testing our bulky sms system. ', 0),
(219, '+255742340759', 'Hello Ntwa. We are are in the phase of testing our bulky sms system. ', 0),
(220, '+255758867676', 'Hello Ashalulu. We are are in the phase of testing our bulk sms system. ', 0),
(221, '+255742340759', 'Hello Ntwa. We are are in the phase of testing our bulk sms system. ', 0),
(222, '+255742340759', '@@firstname@@, thank you for being our customer. We wish you happy new year. From Chef Buddy. ', 0),
(223, '+255742340759', 'Hello Ntwa. The bulky SMS is ini action now. ', 0),
(224, '+255742340759', 'Habari. Ntwa. Tunajaribisha mfumo wetu wa kutuma meseji.', 0),
(225, '+255742340759', 'Habari. Ntwa. Tunajaribisha mfumo wetu wa kutuma meseji.', 0),
(226, '+255742340759', 'Habari. Ntwa. Tunajaribisha mfumo wetu wa kutuma meseji.', 0),
(227, '+255742340759', 'Habari. Ntwa. Tunajaribisha mfumo wetu wa kutuma meseji.', 0),
(228, '+255742340759', 'Habari. Ntwa. Tunajaribisha mfumo wetu wa kutuma meseji.', 0),
(229, '+255742340759', 'Habari. Ntwa. Tunajaribisha mfumo wetu wa kutuma meseji.', 0),
(230, '+255742340759', 'Habari. Ntwa. Tunajaribisha mfumo wetu wa kutuma meseji.', 0),
(231, '+255742340759', 'Asante. Ntwa. Majaribio yetu ya mfumo bado yanaendelea.', 0),
(232, '+255742340759', 'Asante. Ntwa. Majaribio yetu ya mfumo bado yanaendelea.', 0),
(233, '+255742340759', 'Asante. Ntwa. Majaribio yetu ya mfumo bado yanaendelea.', 0),
(234, '+255742340759', 'Hello. I am here to test if my bulky system works. ', 0);

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `group_id` int(11) NOT NULL,
  `group_name` varchar(50) DEFAULT NULL,
  `group_description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`group_id`, `group_name`, `group_description`) VALUES
(2, 'Drivers', 'This group is important for communicating important information to Drivers'),
(3, 'High paying customers', 'This group is important for communicating important information to High Paying Customers'),
(4, 'Farmers Kilolo', 'This group is important for communicating important information to Farmers in Kilolo'),
(10, 'Customers in Temeke', 'This group is created for customers in Temeke.'),
(11, 'Customers in Ilala', 'This group is created for customers in Ilala, Dar es salaam.'),
(12, 'Customers in Kinondoni', 'This group is for customers in Kinondoni and nearby area.'),
(13, 'Customers in Ubungo', 'I have created new group for customers in Ubungo'),
(14, 'Customers in Morogoro', 'This group is for customers that reside in Morogoro'),
(15, 'Customers in Kilombero', 'This group is for customers in Kilombero');

-- --------------------------------------------------------

--
-- Table structure for table `group_members`
--

CREATE TABLE `group_members` (
  `group_id` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `group_members`
--

INSERT INTO `group_members` (`group_id`, `contact_id`) VALUES
(2, 1),
(3, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `individualized_reminders`
--

CREATE TABLE `individualized_reminders` (
  `individualized_reminders_id` int(11) NOT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `reminder_end_date` date DEFAULT NULL,
  `event_deadline_date` date DEFAULT NULL,
  `no_running_days` int(11) DEFAULT NULL,
  `reason_for_reminder` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `individualized_reminders`
--

INSERT INTO `individualized_reminders` (`individualized_reminders_id`, `campaign_id`, `contact_id`, `reminder_end_date`, `event_deadline_date`, `no_running_days`, `reason_for_reminder`) VALUES
(3, 22, 1, '2010-01-01', '2010-01-01', 7, 'None'),
(4, 22, 2, '2010-01-01', '2010-01-01', 7, 'None'),
(5, 23, 1, '2019-06-10', '2019-06-01', 7, 'Renew'),
(6, 23, 2, '2019-08-08', '2019-08-01', 7, 'Renew'),
(9, 24, 1, '2019-06-10', '2019-06-01', 7, 'Renew of Insurance'),
(10, 24, 2, '2019-08-08', '2019-08-01', 7, 'Renew of Insurance');

-- --------------------------------------------------------

--
-- Table structure for table `mobile_details`
--

CREATE TABLE `mobile_details` (
  `mobile_id` int(11) NOT NULL,
  `mobile_number` varchar(15) DEFAULT NULL,
  `is_it_primary_number` tinyint(1) NOT NULL,
  `contact_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mobile_details`
--

INSERT INTO `mobile_details` (`mobile_id`, `mobile_number`, `is_it_primary_number`, `contact_id`) VALUES
(2, '+255742340759', 1, 2),
(3, '+255718255585', 0, 2),
(4, '+255758867676', 1, 1),
(5, '+255718255585', 1, 3),
(6, '+255742340759', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `selected_days_of_delivery`
--

CREATE TABLE `selected_days_of_delivery` (
  `selected_day_id` int(11) NOT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `selected_day` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `selected_days_of_delivery`
--

INSERT INTO `selected_days_of_delivery` (`selected_day_id`, `campaign_id`, `selected_day`) VALUES
(166, 10, 0),
(167, 10, 1),
(168, 10, 2),
(169, 10, 3),
(170, 10, 4),
(171, 10, 5),
(172, 10, 6),
(327, 12, 0),
(328, 12, 1),
(329, 12, 2),
(330, 12, 3),
(331, 12, 4),
(332, 12, 5),
(333, 12, 6),
(334, 13, 0),
(335, 13, 1),
(336, 13, 2),
(337, 13, 3),
(338, 13, 4),
(339, 13, 5),
(340, 13, 6),
(362, 14, 0),
(363, 14, 1),
(364, 14, 2),
(365, 14, 3),
(366, 14, 4),
(367, 14, 5),
(368, 14, 6),
(425, 1, 0),
(426, 1, 1),
(427, 1, 2),
(428, 1, 3),
(429, 1, 4),
(430, 1, 5),
(431, 1, 6),
(439, 16, 0),
(440, 16, 1),
(441, 16, 2),
(442, 16, 3),
(443, 16, 4),
(444, 16, 5),
(445, 16, 6),
(446, 17, 0),
(447, 17, 1),
(448, 17, 2),
(449, 17, 3),
(450, 17, 4),
(451, 17, 5),
(452, 17, 6),
(453, 18, 0),
(454, 18, 1),
(455, 18, 2),
(456, 18, 3),
(457, 18, 4),
(458, 18, 5),
(459, 18, 6),
(460, 19, 0),
(461, 19, 1),
(462, 19, 2),
(463, 19, 3),
(464, 19, 4),
(465, 19, 5),
(466, 19, 6),
(467, 20, 0),
(468, 20, 1),
(469, 20, 2),
(470, 20, 3),
(471, 20, 4),
(472, 20, 5),
(473, 20, 6),
(481, 22, 0),
(482, 22, 1),
(483, 22, 2),
(484, 22, 3),
(485, 22, 4),
(486, 22, 5),
(487, 22, 6),
(488, 21, 0),
(489, 21, 1),
(490, 21, 2),
(491, 21, 3),
(492, 21, 4),
(493, 21, 5),
(494, 21, 6),
(509, 23, 0),
(510, 23, 1),
(511, 23, 2),
(512, 23, 3),
(513, 23, 4),
(514, 23, 5),
(515, 23, 6),
(523, 24, 0),
(524, 24, 1),
(525, 24, 2),
(526, 24, 3),
(527, 24, 4),
(528, 24, 5),
(529, 24, 6);

-- --------------------------------------------------------

--
-- Table structure for table `selected_time_of_delivery`
--

CREATE TABLE `selected_time_of_delivery` (
  `campaign_id` int(11) NOT NULL,
  `selected_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `selected_time_of_delivery`
--

INSERT INTO `selected_time_of_delivery` (`campaign_id`, `selected_time`) VALUES
(1, '05:00:00'),
(1, '08:00:00'),
(21, '00:00:00'),
(23, '00:00:00'),
(24, '14:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `sms_campaign_targeted_groups`
--

CREATE TABLE `sms_campaign_targeted_groups` (
  `group_id` int(11) NOT NULL,
  `campaign_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sms_campaign_targeted_groups`
--

INSERT INTO `sms_campaign_targeted_groups` (`group_id`, `campaign_id`) VALUES
(2, 12),
(3, 12),
(4, 12),
(2, 13),
(4, 13),
(3, 14),
(4, 14),
(2, 16),
(2, 17),
(2, 18),
(2, 19),
(2, 20),
(2, 21),
(2, 22),
(2, 23),
(2, 24);

-- --------------------------------------------------------

--
-- Table structure for table `sms_signatures`
--

CREATE TABLE `sms_signatures` (
  `sms_signature_id` int(11) NOT NULL,
  `signature_content` varchar(50) DEFAULT NULL,
  `signature_status` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sms_templates`
--

CREATE TABLE `sms_templates` (
  `sms_template_id` int(11) NOT NULL,
  `template_class_id` int(11) DEFAULT NULL,
  `template_content` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sms_templates`
--

INSERT INTO `sms_templates` (`sms_template_id`, `template_class_id`, `template_content`) VALUES
(1, 1, 'Hello Mr. @@firstname@@ @@lastname@@. We remind you to pay your outstanding bills.'),
(3, 3, 'How are you @@firstname@@. We remind you to pay your outstanding bills.'),
(4, 4, 'Happy holidays @@firstname@@! We value you as our esteemed customer. Thank you for your support.'),
(5, 5, 'Hello @@firstname@@! We wish you safe journey.'),
(6, 5, 'Hi @@firstname@@! Drive safely.');

-- --------------------------------------------------------

--
-- Table structure for table `sms_template_categories`
--

CREATE TABLE `sms_template_categories` (
  `template_category_id` int(11) NOT NULL,
  `template_category_name` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sms_template_categories`
--

INSERT INTO `sms_template_categories` (`template_category_id`, `template_category_name`) VALUES
(1, 'Monthly Outstanding Bill'),
(3, 'Reminder'),
(4, 'Seasonal Greetings'),
(5, 'Driving Safety Reminders');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address_book`
--
ALTER TABLE `address_book`
  ADD PRIMARY KEY (`contact_id`);

--
-- Indexes for table `campaigns`
--
ALTER TABLE `campaigns`
  ADD PRIMARY KEY (`campaign_id`);

--
-- Indexes for table `campaigns_defined_messages`
--
ALTER TABLE `campaigns_defined_messages`
  ADD PRIMARY KEY (`campaign_message_id`),
  ADD KEY `campaign_id` (`campaign_id`);

--
-- Indexes for table `campaign_end_day`
--
ALTER TABLE `campaign_end_day`
  ADD PRIMARY KEY (`campaign_id`);

--
-- Indexes for table `campaign_start_day`
--
ALTER TABLE `campaign_start_day`
  ADD PRIMARY KEY (`campaign_id`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `email_details`
--
ALTER TABLE `email_details`
  ADD PRIMARY KEY (`email_id`),
  ADD KEY `contact_id` (`contact_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`group_id`);

--
-- Indexes for table `group_members`
--
ALTER TABLE `group_members`
  ADD PRIMARY KEY (`group_id`,`contact_id`),
  ADD KEY `contact_id` (`contact_id`);

--
-- Indexes for table `individualized_reminders`
--
ALTER TABLE `individualized_reminders`
  ADD PRIMARY KEY (`individualized_reminders_id`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `contact_id` (`contact_id`);

--
-- Indexes for table `mobile_details`
--
ALTER TABLE `mobile_details`
  ADD PRIMARY KEY (`mobile_id`),
  ADD KEY `contact_id` (`contact_id`);

--
-- Indexes for table `selected_days_of_delivery`
--
ALTER TABLE `selected_days_of_delivery`
  ADD PRIMARY KEY (`selected_day_id`),
  ADD KEY `campaign_id` (`campaign_id`);

--
-- Indexes for table `selected_time_of_delivery`
--
ALTER TABLE `selected_time_of_delivery`
  ADD PRIMARY KEY (`campaign_id`,`selected_time`);

--
-- Indexes for table `sms_campaign_targeted_groups`
--
ALTER TABLE `sms_campaign_targeted_groups`
  ADD PRIMARY KEY (`group_id`,`campaign_id`),
  ADD KEY `campaign_id` (`campaign_id`);

--
-- Indexes for table `sms_signatures`
--
ALTER TABLE `sms_signatures`
  ADD PRIMARY KEY (`sms_signature_id`);

--
-- Indexes for table `sms_templates`
--
ALTER TABLE `sms_templates`
  ADD PRIMARY KEY (`sms_template_id`),
  ADD KEY `template_class_id` (`template_class_id`);

--
-- Indexes for table `sms_template_categories`
--
ALTER TABLE `sms_template_categories`
  ADD PRIMARY KEY (`template_category_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address_book`
--
ALTER TABLE `address_book`
  MODIFY `contact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `campaigns`
--
ALTER TABLE `campaigns`
  MODIFY `campaign_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
--
-- AUTO_INCREMENT for table `campaigns_defined_messages`
--
ALTER TABLE `campaigns_defined_messages`
  MODIFY `campaign_message_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=620;
--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `email_details`
--
ALTER TABLE `email_details`
  MODIFY `email_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=235;
--
-- AUTO_INCREMENT for table `groups`
--
ALTER TABLE `groups`
  MODIFY `group_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `individualized_reminders`
--
ALTER TABLE `individualized_reminders`
  MODIFY `individualized_reminders_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `mobile_details`
--
ALTER TABLE `mobile_details`
  MODIFY `mobile_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `selected_days_of_delivery`
--
ALTER TABLE `selected_days_of_delivery`
  MODIFY `selected_day_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=530;
--
-- AUTO_INCREMENT for table `sms_signatures`
--
ALTER TABLE `sms_signatures`
  MODIFY `sms_signature_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `sms_templates`
--
ALTER TABLE `sms_templates`
  MODIFY `sms_template_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `sms_template_categories`
--
ALTER TABLE `sms_template_categories`
  MODIFY `template_category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `campaigns_defined_messages`
--
ALTER TABLE `campaigns_defined_messages`
  ADD CONSTRAINT `campaigns_defined_messages_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`);

--
-- Constraints for table `campaign_end_day`
--
ALTER TABLE `campaign_end_day`
  ADD CONSTRAINT `campaign_end_day_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`);

--
-- Constraints for table `campaign_start_day`
--
ALTER TABLE `campaign_start_day`
  ADD CONSTRAINT `campaign_start_day_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`);

--
-- Constraints for table `email_details`
--
ALTER TABLE `email_details`
  ADD CONSTRAINT `email_details_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `address_book` (`contact_id`);

--
-- Constraints for table `group_members`
--
ALTER TABLE `group_members`
  ADD CONSTRAINT `group_members_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  ADD CONSTRAINT `group_members_ibfk_2` FOREIGN KEY (`contact_id`) REFERENCES `address_book` (`contact_id`);

--
-- Constraints for table `individualized_reminders`
--
ALTER TABLE `individualized_reminders`
  ADD CONSTRAINT `individualized_reminders_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`),
  ADD CONSTRAINT `individualized_reminders_ibfk_2` FOREIGN KEY (`contact_id`) REFERENCES `address_book` (`contact_id`);

--
-- Constraints for table `mobile_details`
--
ALTER TABLE `mobile_details`
  ADD CONSTRAINT `mobile_details_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `address_book` (`contact_id`);

--
-- Constraints for table `selected_days_of_delivery`
--
ALTER TABLE `selected_days_of_delivery`
  ADD CONSTRAINT `selected_days_of_delivery_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`);

--
-- Constraints for table `selected_time_of_delivery`
--
ALTER TABLE `selected_time_of_delivery`
  ADD CONSTRAINT `selected_time_of_delivery_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`);

--
-- Constraints for table `sms_campaign_targeted_groups`
--
ALTER TABLE `sms_campaign_targeted_groups`
  ADD CONSTRAINT `sms_campaign_targeted_groups_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  ADD CONSTRAINT `sms_campaign_targeted_groups_ibfk_2` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`);

--
-- Constraints for table `sms_templates`
--
ALTER TABLE `sms_templates`
  ADD CONSTRAINT `sms_templates_ibfk_1` FOREIGN KEY (`template_class_id`) REFERENCES `sms_template_categories` (`template_category_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
