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
import string 
 
stop_words = ["for","of","the","in","a",  
        "to","is","news", "breaking", "and",  
        "you", "by", "your", "on", "at",  
        "as", "this", "it", "with", "from"] 
 
exclude = set(string.punctuation) 
 
#-------- Load Ignore Words Dict ---- 
stopFile = open('StopWords.txt') 
lines = stopFile.readlines() 
for line in lines: 
    s = line.split("\t") 
    stop_words.append(s) 
stopFile.close() 
 
class MyMRJob(MRJob): 
    def mapper(self, _, line): 
        #Get data 
        data=line.split(',') 
        sentiment = data[0].strip() 
        headline = data[1].strip() 
        headline = headline.lower() 
        words = headline.split() 
 
        good_words = [] 
        for word in words: 
            good_words.append(word) 
 
        # Create phrases 
        phrases = [] 
        for i in range(0, len(good_words) - 1): 
            word1 = good_words[i] 
            word2 = good_words[i+1] 
            if word1 in stop_words: 
                continue 
            if word2 in stop_words: 
                continue 
 
            phrase = '%s %s' %(word1, word2) 
            phrases.append(phrase) 
 
        link = data[2].strip() 
        for phrase in phrases: 
            yield phrase, (1, sentiment, link) 

    def reducer(self, key, list_of_values): 
        totalCount = 0.0 
        totalSentiment = 0.0 
        list_of_links = [] 
        for item in list_of_values: 
            #Skip if the link has already been processed 
            if item[2] in list_of_links: 
                continue 
 
            #Add count 
            totalCount = totalCount + item[0] 
            #Add sentiment 
            totalSentiment = totalSentiment + float(item[1]) 
            #Append links 
            list_of_links.append(item[2]) 
 
        avgSentiment = totalSentiment / totalCount 
        yield None, (totalCount, key, avgSentiment, list_of_links) 
 
    def reducer2(self, _, list_of_values): 
        #Print top 25 
        count = 0 
        for item in sorted(list_of_values, reverse = True): 
            if count > 25: 
                break 
            print item 
            count = count + 1 
 
    def steps(self): 
        return [self.mr(mapper=self.mapper,  
        reducer=self.reducer), self.mr(reducer=self.reducer2)] 
 
if __name__ == '__main__': 
    MyMRJob.run()

