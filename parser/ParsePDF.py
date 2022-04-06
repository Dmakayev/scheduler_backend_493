import re
from tika import parser
import pprint
import json

def parsePDF (deptInfo, outFile):
   classes = {}
   for entry in deptInfo:
      raw = parser.from_file (entry['fileName'])
      text = raw['content']
      lines = text.split("\n")
      #print (len(lines))
   
      index = 0
      while index < len(lines):
         while len(lines[index].strip()) == 0:
            del (lines[index])
            if index >= len(lines):
               break 
      #   if index < len(lines):
      #      print (format (index, "3d"), lines[index])
         index += 1
   
   
      classPattern = format (entry['prefix'], "4s") + " \d\d\d"  #'CSCI \d\d\d'
      classPattern2 = "^" + format (entry['prefix'], "4s") + " \d\d\d"  #'^CSCI \d\d\d'
      #csClassMatcher = re.search (classPattern, text)
      #while csClassMatcher != None:
         #print ("class starts at ", csClassMatcher.start())   
         #print ("class ends   at ", csClassMatcher.end())   
         #print ("class name      ", text[csClassMatcher.span()[0] : csClassMatcher.span()[1]])
         #print ("class name      ", csClassMatcher.group())
         #csClassMatcher = re.search (csClassPattern, text)
   
      #for c in re.finditer (csClassPattern, text):
         #print ("class starts at ", c.start())   
         #print ("class ends   at ", c.end())   
      #   print ("class name      ", c.group(0))
   
      #
      index = 0
      while index < len(lines):
         if re.search(classPattern2, lines[index]) != None:
            #print (lines[index])
            #classNumber = lines[index][0:8].strip() #excludes lab sections as a separate class
            classNumber = lines[index][0:9].strip() #included lab sections as a separate class
            className = lines[index][12:43].strip()
            credits = lines[index][44]
            if classes.get (classNumber) == None:
               classes[classNumber] = {}
               classes[classNumber]['classNumber'] = classNumber
               classes[classNumber]['className'] = className
               classes[classNumber]['credits'] = credits
            index = index + 1
            classes[classNumber]['sections'] = []
            while re.search ('^\s{10}', lines[index]) != None:
               #print (lines[index])
               index += 1
            while index < len(lines) and re.search ('^L?\d\d', lines[index]) != None:
               #print (lines[index])
               section = lines[index][0:4].strip()
               number = lines[index][4:9].strip()
               time = lines[index][12:27].strip()
               days = lines[index][27:35].strip()
               room = lines[index][36:50].strip()
               instructor = lines[index][58:76].strip()
               capacity = lines[index][79:82].strip()
               enrollment = lines[index][86:89].strip()
               waitSize = lines[index][93:96].strip()
               classes[classNumber]['sections'].append({'sectionNumber:': section, 'capacity': capacity, 'room:':room, 'waitSize': waitSize, 'enrollment':enrollment, 'days:':days,
                                                       'number:': number, 'time': time, 'instructor': instructor})
               index = index + 3
               while index < len(lines) and lines[index][0:5] == "     ":
                  index = index + 1
            #print ()
                  
         else:   
            index = index + 1   
   outFile =   open (outFile, "w")
   json.dump(classes, outFile)
   outFile.close()
   
def main ():
   deptInfo = [
               {'fileName' : 'CS-Spring 2022-2022-01-04.pdf', 'prefix' : 'CSCI'}, 
               {'fileName' : 'EE-Spring 2022-2022-01-04.pdf', 'prefix' : 'EE'}
              ]
   parsePDF (deptInfo, "seesc-classes-spring2022-4.json")
   print ("Done")

main()   