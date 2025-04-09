<<<<<<< HEAD
# DB-Group-Class-assignment
=======
# College-Event-Website
Purpose: Allow students to view and interact with events hosted by universities, RSOs (Registered Student Organizations), clubs, and more. Support different user roles with varying permissions (super admin, admin, student).

Project Description Mark 2
Purpose
The purpose of this second draft is to clarify what we have to do for our project. It breaks apart
the document into easier to read sections, and ensures we are on track. In addition,
it provides a section that has a plan of what we need to do, to tackle this project and finish it
early or on-time. Also, used ChatGPT to clarify my original first draft to make it even easier
to read so I'm cross checking what it wrote with what I wrote to make sure everything's
consistent.

Project Overview
Application: College Event Website
Purpose:
Requirements
1. User Registration & Roles
A. Registration Process
B. User Levels
 Allow students to view and interact with events hosted by universities, RSOs (Registered
Student Organizations), clubs, and more.
 Support different user roles with varying permissions (super admin, admin, student).
 Students (users) must register to obtain a user ID and password.
 Super Admin:
 Creates and manages university profiles.
 Profile details include:
 Name
 Location
2. Event Creation & Management
    A. Event Attributes
    B. Event Visibility
     Description
     Number of students
     Pictures
     (Additional details as needed)
     Approves events made without RSO (public events)
 Admin:
     Owns RSOs and can host events.
     Can create events (see Event Management section).
     Must be affiliated with one university and at least one RSO.
     Student:
     Uses the application to look up event information.
     Can request to create a new RSO or join an existing one.
  New RSO Requirement:
     At least 4 students with the same email domain (e.g., @knights.ucf.edu)
     One student is assigned as the RSO administrator.
     Once logged in, can view events relevant to their university (private and public) and
    RSOs.
     Cannot create events, but can:
     Rate events (1-5 stars)
     Comment on events (add, remove, edit)
     Mandatory Fields:
     Name
     Event Category (e.g., social, fundraising, tech talks)
     Description
     Time & Date
     Location (set using a map: Bing, Google, or OpenStreetMap with details like name,
    latitude, longitude)
     Contact details (phone, email)
       Public Events:
C. Post-Publishing Interactions
D. Social Network Integration
3. Data Population & Integration
Technical Requirements
A. Database Design & Implementation
1. Design Process
 Visible to everyone.
 If created without an RSO, must be approved by the super admin.
 Private Events:
 Visible only to students at the host university.
 RSO Events:
 Visible only to members of the specific RSO.
 After an event is published, students can:
 Add, remove, and edit comments.
 Rate the event (scale of 1-5 stars).
 Incorporate sharing capabilities via platforms such as Facebook and Google.

 Data Feed:
 Utilize RSS/XML feeds from the university events system (e.g., events.ucf.edu) to
populate the database.

 Follow a structured design process:
 Business operations/constraints analysis
 ER-model creation
 Conversion to the relational model
 Normalization
 Implementation (SQL scripts for creation and population)
 Indexing and performance considerations
2. Database Specifications
3. Sample Data Requirements
B. Application & User Interface
1. Front-End
2. Technologies Allowed
3. Constraint Enforcement
>>>>>>> 17d38d9 (Initial commit of my DB group assignment files)
