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
import re
lineformat = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\ \
                        .\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3} \
                        \/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] \
                        ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) \
                        (?P<statuscode>\d{3}) (?P<bytessent>\d+) \
                        (?P<refferer>-|"([^"]+)") (["] \
                        (?P<useragent>[^"]+)["])""", re.IGNORECASE)

class MRVisitCounter(MRJob):
    def mapper(self, key, line): 
        try:       
            data=re.search(lineformat, line)
            datadict = data.groupdict()        
            yield datadict['ipaddress'], 1
        except:
            pass

    def reducer(self, address, visits):                
        yield address, sum(visits)

if __name__ == '__main__':
    MRVisitCounter.run()