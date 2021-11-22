/*
IS211 - Assignment 13 - schema.sql
*/

DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS results;

CREATE TABLE IF NOT EXISTS students (
id INT PRIMARY KEY NOT NULL,
first_name VARCHAR(255) NOT NULL,
last_name VARCHAR(255) NOT NULL);

INSERT INTO students VALUES(1, 'John', 'Smith');

CREATE TABLE IF NOT EXISTS quizzes (
id INT PRIMARY KEY NOT NULL,
subject VARCHAR(255),
num_questions INT,
quiz_date VARCHAR(255);

INSERT INTO quizzes VALUES(1, 'Python Basics', 5, 'February 5th, 2015');

CREATE TABLE IF NOT EXISTS results (
stu_id INT PRIMARY KEY NOT NULL,
quiz_id INT NOT NULL,
score INT NOT NULL);

INSERT INTO results VALUES(1, 1, 85 );

