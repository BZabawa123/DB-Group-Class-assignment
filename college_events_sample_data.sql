USE CollegeEvents;

-- Insert sample Universities
INSERT INTO Universities (name, location, description, number_of_students) VALUES
('UCF', 'Orlando, FL', 'University of Central Florida', 68000),
('FSU', 'Tallahassee, FL', 'Florida State University', 42000);

-- Insert sample Users (SuperAdmins, Admins, Students)
INSERT INTO Users (username, email, password, user_type) VALUES
('superadmin1', 'sa1@ucf.edu', 'hashed_password', 'SuperAdmin'),
('superadmin2', 'sa2@fsu.edu', 'hashed_password', 'SuperAdmin'),
('admin1', 'admin1@ucf.edu', 'hashed_password', 'Admin'),
('admin2', 'admin2@fsu.edu', 'hashed_password', 'Admin'),
('student1', 'student1@ucf.edu', 'hashed_password', 'Student'),
('student2', 'student2@fsu.edu', 'hashed_password', 'Student'),
('student3', 'student3@ucf.edu', 'hashed_password', 'Student'),
('student4', 'student4@fsu.edu', 'hashed_password', 'Student');

-- Insert sample RSOs
INSERT INTO RSOs (name, university_id, admin_id, status) VALUES
('Hackers Club', 1, 3, 'inactive'),
('Art Society', 1, 3, 'inactive'),
('Gaming Knights', 1, 3, 'inactive'),
('FSU Tech', 2, 4, 'inactive'),
('FSU Outreach', 2, 4, 'inactive');

-- Insert sample Locations
INSERT INTO Locations (lname, address, longitude, latitude) VALUES
('Union Hall', '123 University Blvd', -81.200, 28.601),
('Tech Center', '456 College Ave', -81.300, 28.602),
('Library', '789 Academic Rd', -81.250, 28.603);

-- Insert sample Events (Superclass)
INSERT INTO Events (event_name, category, description, event_date, start_time, end_time, lname)
VALUES
('Hackathon 2025', 'Tech Talk', '24-hour hackathon.', '2025-05-10', '10:00:00', '12:00:00', 'Tech Center'),
('Art Expo', 'Social', 'Showcase of student art.', '2025-05-11', '12:00:00', '13:00:00', 'Union Hall'),
('Game Night', 'Social', 'Gaming tournament.', '2025-05-12', '17:00:00', '19:00:00', 'Library'),
('FSU Robotics Demo', 'Tech Talk', 'Robotics demo.', '2025-05-10', '10:00:00', '11:00:00', 'Tech Center'),
('Fundraiser Fair', 'Fundraising', 'Community fundraiser.', '2025-05-13', '14:00:00', '15:00:00', 'Union Hall'),
('Open Mic', 'Social', 'Music and performances.', '2025-05-14', '18:00:00', '20:00:00', 'Union Hall'),
('STEM Talk', 'Tech Talk', 'STEM outreach event.', '2025-05-15', '13:00:00', '14:00:00', 'Tech Center'),
('UCF Info Session', 'Fundraising', 'Student services info.', '2025-05-16', '11:00:00', '12:00:00', 'Library'),
('FSU BBQ', 'Social', 'Welcome BBQ.', '2025-05-17', '15:00:00', '16:00:00', 'Union Hall'),
('RSO Summit', 'Tech Talk', 'Leaders meet-up.', '2025-05-18', '09:00:00', '11:00:00', 'Tech Center');

-- Insert sample Event_Creation for Public/Private events.
INSERT INTO Event_Creation (event_id, admin_id, superadmin_id, privacy) VALUES
(1, 3, 1, 'Private'),
(2, 3, 1, 'Public'),
(3, 3, 1, 'Public'),
(4, 4, 2, 'Private'),
(5, 4, 2, 'Public'),
(6, 3, 1, 'Public'),
(7, 3, 1, 'Private'),
(8, 4, 2, 'Private'),
(9, 4, 2, 'Public');

-- Insert sample RSO_Events (those events associated with an RSO)
-- Let's say event 10 (we'll add one more event) is an RSO event.
INSERT INTO Events (event_name, category, description, event_date, start_time, end_time, lname)
VALUES ('RSO Party', 'Social', 'RSO exclusive party.', '2025-05-20', '20:00:00', '22:00:00', 'Union Hall');
SET @new_event_id = LAST_INSERT_ID();
INSERT INTO RSO_Events (event_id, rso_id) VALUES (@new_event_id, 1);

-- Insert sample Comments
INSERT INTO Comments (uid, event_id, rating, content) VALUES
(5, 1, 5, 'Awesome event!'),
(6, 1, 4, 'Very fun!'),
(7, 2, 3, 'Good effort.'),
(8, 3, 5, 'Loved it!'),
(3, 4, 4, 'Informative.'),
(4, 5, 2, 'Could be better.'),
(5, 6, 5, 'I had a great time.'),
(6, 7, 4, 'Nice speakers.'),
(7, 8, 3, 'Average.'),
(8, 9, 5, 'Food was great!');

-- Insert sample Students_RSOs (RSO membership)
INSERT INTO Students_RSOs (uid, rso_id) VALUES
(5, 1), (6, 1), (7, 1), (8, 1), (3, 1),
(5, 2), (6, 2), (7, 2), (8, 2), (3, 2),
(5, 3), (6, 3), (7, 3), (8, 3), (3, 3),
(5, 4), (6, 4), (7, 4), (8, 4), (4, 4),
(5, 5), (6, 5), (7, 5), (8, 5), (4, 5);
