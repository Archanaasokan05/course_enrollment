-- Database name: course_enrollment

create database course_enrollment;
use course_enrollment;

-- Table name: enrollments
-- Required table fields: enrollment_id, student_name, course_name, duration_months, enrollment_date, fee, status

create table enrollments(enrollment_id int primary key auto_increment,
						student_name varchar(30),
                        course_name varchar(30),
                        duration_months int,
                        enrollment_date date,
                        fee int,
                        status varchar(20));
                         
