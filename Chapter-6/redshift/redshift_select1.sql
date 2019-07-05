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


SELECT first_name, last_name, salary, from_date, to_date FROM employees, salaries WHERE employees.emp_no=salaries.emp_no AND employees.emp_no='10009'; 
 
'Sumant'    'Peac'    60929    '1985-02-18'    '1986-02-18' 
'Sumant'    'Peac'    64780    '1987-02-18'    '1988-02-18' 
'Sumant'    'Peac'    69042    '1989-02-17'    '1990-02-17' 
'Sumant'    'Peac'    71434    '1991-02-17'    '1992-02-17' 
'Sumant'    'Peac'    76518    '1993-02-16'    '1994-02-16' 
'Sumant'    'Peac'    80944    '1995-02-16'    '1996-02-16' 
'Sumant'    'Peac'    85875    '1997-02-15'    '1998-02-15' 
'Sumant'    'Peac'    90668    '1999-02-15'    '2000-02-15' 
'Sumant'    'Peac'    94443    '2001-02-14'    '2002-02-14' 
'Sumant'    'Peac'    64604    '1986-02-18'    '1987-02-18' 
'Sumant'    'Peac'    66302    '1988-02-18'    '1989-02-17' 
'Sumant'    'Peac'    70889    '1990-02-17'    '1991-02-17' 
'Sumant'    'Peac'    74612    '1992-02-17'    '1993-02-16' 
'Sumant'    'Peac'    78335    '1994-02-16'    '1995-02-16' 
'Sumant'    'Peac'    82507    '1996-02-16'    '1997-02-15' 
'Sumant'    'Peac'    89324    '1998-02-15'    '1999-02-15' 
'Sumant'    'Peac'    93507    '2000-02-15'    '2001-02-14' 
'Sumant'    'Peac'    94409    '2002-02-14'    '9999-01-01'
