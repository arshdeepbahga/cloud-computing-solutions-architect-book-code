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

CREATE TABLE employees ( 
    emp_no      INT             NOT NULL, 
    birth_date  VARCHAR(14)            NOT NULL, 
    first_name  VARCHAR(20)     NOT NULL, 
    last_name   VARCHAR(20)     NOT NULL, 
    gender      VARCHAR(10)     NOT NULL,    
    hire_date   VARCHAR(14)            NOT NULL, 
    PRIMARY KEY (emp_no) 
); 
CREATE TABLE departments ( 
    dept_no     VARCHAR(10)     NOT NULL, 
    dept_name   VARCHAR(40)     NOT NULL, 
    PRIMARY KEY (dept_no), 
    UNIQUE  (dept_name) 
); 
CREATE TABLE dept_manager ( 
    dept_no      VARCHAR(10)     NOT NULL, 
    emp_no       INT             NOT NULL, 
    from_date    VARCHAR(14)     NOT NULL, 
    to_date      VARCHAR(14)     NOT NULL, 
    FOREIGN KEY (emp_no)  REFERENCES employees (emp_no)  , 
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no), 
    PRIMARY KEY (emp_no,dept_no) 
);  
CREATE TABLE dept_emp ( 
    emp_no      INT             NOT NULL, 
    dept_no     VARCHAR(10)     NOT NULL, 
    from_date   VARCHAR(14)     NOT NULL, 
    to_date     VARCHAR(14)     NOT NULL, 
    FOREIGN KEY (emp_no)  REFERENCES employees   (emp_no) , 
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no), 
    PRIMARY KEY (emp_no,dept_no) 
); 
CREATE TABLE titles ( 
    emp_no      INT             NOT NULL, 
    title       VARCHAR(50)     NOT NULL, 
    from_date   VARCHAR(14)     NOT NULL, 
    to_date     VARCHAR(14), 
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no), 
    PRIMARY KEY (emp_no,title, from_date) 
);  
CREATE TABLE salaries ( 
    emp_no      INT             NOT NULL, 
    salary      INT             NOT NULL, 
    from_date   VARCHAR(14)     NOT NULL, 
    to_date     VARCHAR(14)     NOT NULL, 
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no), 
    PRIMARY KEY (emp_no, from_date) 
); 
