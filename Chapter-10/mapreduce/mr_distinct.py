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

# Distint IP addresses 
 
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
        visit_printlen=int(data[4].strip()) 
        yield ip, None 
        
   
    def reducer(self, key, list_of_values): 
        yield key, None 
 
     
if __name__ == '__main__': 
    MRmyjob.run()
