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

# Parition records by Quarter 
 
from mrjob.job import MRJob 
 
class MRmyjob(MRJob): 
    def mapper(self, _, line): 
        #Split the line with tab separated fields 
        data=line.split('\t') 
 
        #Parse line 
        date = data[0].strip() 
        time = data[1].strip() 
        url = data[2].strip() 
        ip = data[3].strip() 
        visit_len=int(data[4].strip()) 
         
        #Extract year from date 
        year=date[0:4] 
        month=int(date[5:7]) 
         
        #Emit url and 1 if year is 2014 
        if year=='2014': 
            if month<=3: 
                yield "Q1", (date, time, url, ip, visit_len) 
            elif month<=6: 
                yield "Q2", (date, time, url, ip, visit_len) 
            elif month<=9: 
                yield "Q3", (date, time, url, ip, visit_len) 
            else: 
                yield "Q4", (date, time, url, ip, visit_len) 
 
     
if __name__ == '__main__': 
    MRmyjob.run()
