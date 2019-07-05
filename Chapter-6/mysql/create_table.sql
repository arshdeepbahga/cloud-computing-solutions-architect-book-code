'''
MIT License

Copyright (c) 2019 Arshdeep Bahga and Vijay Madisetti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

CREATE TABLE department( 
number varchar(50) NOT NULL PRIMARY KEY, 
name varchar(200) NULL 
); 
 
CREATE TABLE employee ( 
number varchar(100) NOT NULL PRIMARY KEY, 
name varchar(100) NOT NULL, 
salary varchar(20) NOT NULL, 
department_id varchar(20) REFERENCES department (number), 
); 
 
CREATE TABLE project ( 
number varchar(20) NOT NULL PRIMARY KEY, 
name varchar(100) NOT NULL 
); 
 
CREATE TABLE workson ( 
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
employee_id varchar(20) NOT NULL REFERENCES employee (number), 
project_id varchar(20) NOT NULL REFERENCES project (number) 
);
