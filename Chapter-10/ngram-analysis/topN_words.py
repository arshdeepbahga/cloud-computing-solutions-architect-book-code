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

from mrjob.job import MRJob 
 
class MyMRJob(MRJob): 
    def mapper(self, _, line): 
        line = line.strip() 
        words = line.split() 
        for word in words: 
            yield (word, 1) 
 
    def reducer(self, key, list_of_values): 
        word = key 
        total_count = sum(list_of_values) 
        yield None, (total_count, word) 
 
    def reducer2(self, _, list_of_values): 
        N = 3 
        list_of_values = sorted(list(list_of_values), reverse=True) 
        return list_of_values[:N] 
 
    def steps(self): 
        return [self.mr(mapper=self.mapper,  
        reducer=self.reducer), self.mr(reducer=self.reducer2)] 
         
if __name__ == '__main__': 
    MyMRJob.run()
