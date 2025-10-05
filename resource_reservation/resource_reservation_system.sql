-- Create the database
CREATE DATABASE IF NOT EXISTS resource_reservation_system;
USE resource_reservation_system;

-- Table structure for Location
CREATE TABLE `Location` (
  `location_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table Location
INSERT INTO `Location` VALUES (1,'Main Library','123 Library St'),(2,'Science Building','456 Science Ave'),(3,'Tech Park','789 Tech Blvd');

-- Table structure for User
CREATE TABLE `User` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phno` varchar(20) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table User
INSERT INTO `User` VALUES (1,'John Doe','123-456-7890','admin'),(2,'Jane Smith','987-654-3210','user'),(3,'Peter Jones','555-555-5555','user');

-- Table structure for Resource
CREATE TABLE `Resource` (
  `resource_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location_id` int DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  PRIMARY KEY (`resource_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `Resource_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `Location` (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table Resource
INSERT INTO `Resource` VALUES (1,'Lab','Computer Lab A',1,30),(2,'Equipment','Projector 1',2,1),(3,'Classroom','Room 101',3,50);

-- Table structure for ReservationStatus
CREATE TABLE `ReservationStatus` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `status_name` varchar(255) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ReservationStatus
INSERT INTO `ReservationStatus` VALUES (1,'Confirmed'),(2,'Pending'),(3,'Cancelled');

-- Table structure for Reservation
CREATE TABLE `Reservation` (
  `Reservation_ID` int NOT NULL AUTO_INCREMENT,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `resource_id` int DEFAULT NULL,
  `userid` int DEFAULT NULL,
  `status_id` int DEFAULT NULL,
  `attendees` int DEFAULT NULL,
  PRIMARY KEY (`Reservation_ID`),
  KEY `resource_id` (`resource_id`),
  KEY `userid` (`userid`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `Reservation_ibfk_1` FOREIGN KEY (`resource_id`) REFERENCES `Resource` (`resource_id`),
  CONSTRAINT `Reservation_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `User` (`userid`),
  CONSTRAINT `Reservation_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `ReservationStatus` (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table Reservation
INSERT INTO `Reservation` VALUES (1,'2024-01-01 10:00:00','2024-01-01 12:00:00',1,1,1,25),(2,'2024-01-02 14:00:00','2024-01-02 15:00:00',2,2,2,1),(3,'2024-01-03 09:00:00','2024-01-03 11:00:00',3,3,3,40);

-- Stored Procedures
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateReservationStatus`(
    IN p_reservation_id INT,
    IN p_new_status_id INT
)
BEGIN
    UPDATE Reservation
    SET status_id = p_new_status_id
    WHERE Reservation_ID = p_reservation_id;
END$$
DELIMITER ;

-- Functions
DELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `GetUserRole`(p_user_id INT) RETURNS varchar(255) CHARSET utf8mb4
    DETERMINISTIC
BEGIN
    DECLARE user_role_value VARCHAR(255);
    SELECT role INTO user_role_value FROM User WHERE userid = p_user_id;
    RETURN user_role_value;
END$$
DELIMITER ;