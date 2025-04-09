-- Create the database and select it
CREATE DATABASE IF NOT EXISTS CollegeEvents;
USE CollegeEvents;

-- 1. Users: Contains all user types (SuperAdmin, Admin, Student)
CREATE TABLE `Users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `last_login` DATETIME NULL,
  `username` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `role` VARCHAR(50) NOT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `is_staff` TINYINT(1) NOT NULL DEFAULT 0,
  `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2. Universities: Stores university details
CREATE TABLE Universities (
  university_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  location VARCHAR(255),
  description TEXT,
  number_of_students INT
);

-- 3. RSOs: Registered Student Organizations
CREATE TABLE RSOs (
  rso_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  university_id INT,
  admin_id INT,
  status ENUM('active','inactive') DEFAULT 'inactive',
  FOREIGN KEY (university_id) REFERENCES Universities(university_id),
  FOREIGN KEY (admin_id) REFERENCES Users(uid)
);

-- 4. Locations: Used by events
CREATE TABLE Locations (
  lname VARCHAR(255) PRIMARY KEY,
  address VARCHAR(255),
  longitude REAL,
  latitude REAL
);

-- 5. Events: The superclass for all events.
--    (Event_name, Time, and Location combination is unique.)
CREATE TABLE Events (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  event_name VARCHAR(100),
  category ENUM('Social','Fundraising','Tech Talk'),
  description TEXT,
  event_date DATE,
  start_time TIME,
  end_time TIME,
  lname VARCHAR(255),
  UNIQUE(lname, event_date, start_time),
  FOREIGN KEY (lname) REFERENCES Locations(lname)
);

-- 6. Event_Creation: Maps events (Public/Private) to an Admin and a SuperAdmin.
--    This represents the ternary relationship "Creates" for events not associated with an RSO.
CREATE TABLE Event_Creation (
  event_id INT PRIMARY KEY,
  admin_id INT NOT NULL,
  superadmin_id INT NOT NULL,
  privacy ENUM('Public','Private') NOT NULL,
  FOREIGN KEY (event_id) REFERENCES Events(event_id),
  FOREIGN KEY (admin_id) REFERENCES Users(uid),
  FOREIGN KEY (superadmin_id) REFERENCES Users(uid)
);

-- 7. RSO_Events: Subclass table for events associated with an RSO.
--    Its primary key is also a foreign key to Events.
CREATE TABLE RSO_Events (
  event_id INT PRIMARY KEY,
  rso_id INT,
  FOREIGN KEY (event_id) REFERENCES Events(event_id),
  FOREIGN KEY (rso_id) REFERENCES RSOs(rso_id)
);

-- 8. Comments: User comments and ratings for events.
CREATE TABLE Comments (
  comment_id INT AUTO_INCREMENT PRIMARY KEY,
  uid INT,
  event_id INT,
  rating INT CHECK (rating BETWEEN 1 AND 5),
  content TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES Users(uid),
  FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

-- 9. Students_RSOs: Relationship table for students joining RSOs.
CREATE TABLE Students_RSOs (
  uid INT,
  rso_id INT,
  PRIMARY KEY(uid, rso_id),
  FOREIGN KEY(uid) REFERENCES Users(uid),
  FOREIGN KEY(rso_id) REFERENCES RSOs(rso_id)
);
