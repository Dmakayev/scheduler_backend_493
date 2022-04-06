import re
from tika import parser
import pprint
import json


def listIntersection(lst1, lst2):
   return list(set(lst1) & set(lst2))


def listUnion(lst1, lst2):
   final_list = sorted(lst1 + lst2)
   return final_list


def classesAtTime (days, time):
   classList = set()
   for classNumber in classes:
      for section in classes[classNumber]['sections']:
         if classes[classNumber]['sections'][section]['days'] == days and classes[classNumber]['sections'][section]['time'] == time:
            classList.add (classNumber)
   return sorted (list (classList))
   
def getInstructor (className, section='01'):
   
   if className in classes:
      if section in classes[className]['sections']:
         return classes[className]['sections'][section]['instructor']
      else:
         return None
   else:
      return None

def getTime (className, section='01'):
   if className in classes:
      if section in classes[className]['sections']:
         return classes[className]['sections'][section]['time']
      else:
         return None
   else:
      return None

      
def getDays (className, section='01'):
   if className in classes:
      if section in classes[className]['sections']:
         return classes[className]['sections'][section]['days']
      else:
         return None
   else:
      return None

      
def getSections (className, ignoreLabsAndTBAs=True):
   sectionsToReturn = []
   if className in classes:
      for section in classes[className]['sections']:
         time = getTime (className, section) 
         if not ignoreLabsAndTBAs or (section.find("L") == -1 and time  != "TBA"):
            sectionsToReturn.append (section)
      return sectionsToReturn      
   else:
      return None
   
def getInstructorSections (className, instructor, ignoreLabsAndTBAs=True):
   sectionsToReturn = []
   if className in classes:
      for section in classes[className]['sections']:
         if classes[classNumber]['sections'][section]['instructor'] == instructor:
            time = getTime (className, section) 
            if not ignoreLabsAndTBAs or (section.find("L") == -1 and time  != "TBA"):
               sectionsToReturn.append (section)
      return sectionsToReturn         
   else:
      return None
   
def getClasses (instructor):
   classList = set()
   for classNumber in classes:
      for section in classes[classNumber]['sections']:
         if classes[classNumber]['sections'][section]['instructor'] == instructor:
            classList.add (classNumber)
   return sorted (list (classList))


def sortableTime(time):
   colonAt = time.find (":")
   dashAt = time.find('-')
   hour = int(time[0:colonAt])
   minute = time[colonAt + 1:dashAt]
   if minute[-1] == 'p':
      hour += 12
   return format (hour, "02d") + ":" + minute 

def timeToMinutes (classTime):
   colonAt = classTime.find(":")
   hour = int(classTime[:colonAt])
   minutes = int(classTime[colonAt + 1:colonAt + 3])
   if hour < 8:
      hour = hour + 12
   elif hour == 8:
      if classTime[-1] == 'p':
         hour = hour + 12
   return hour * 60 + minutes

def minutesToTime (minutes):
   hours = int (minutes // 60) 
   if hours > 12:
      hours = hours - 12
   minutes = minutes % 60
   return str(hours) + ":" + format (minutes, "02d")

def addMinutes (classTime, duration):
   classTimeDays, classTimeTime = classTime.split (" ")
   minutes = timeToMinutes (classTimeTime) + duration
   return classTimeDays + " " + minutesToTime (minutes)

def timeConflict (classTime, timeToCheck, leeway=0):
   classTimeDays, classTimeTime = classTime.split (" ")
   timeToCheckDays, timeToCheckTime = timeToCheck.split (" ")
   if timeToCheckDays not in classTimeDays:
      return False
   classStartTime, classEndTime = classTimeTime.split ("-")
   startTimeMinutes = timeToMinutes (classStartTime) + leeway
   endTimeMinutes = timeToMinutes (classEndTime) - leeway 
   timeToCheckMinutes = timeToMinutes (timeToCheckTime)
   return startTimeMinutes <= timeToCheckMinutes <= endTimeMinutes

def getTeachingTimes (instructor, ignoreLabsAndTBAs=True):   
   theirTimes = []
   theirClasses = getClasses (instructor)
   for classNumber in theirClasses:
      sections = getSections(classNumber)
      for section in sections:
         days = getDays (classNumber, section) 
         time = getTime (classNumber, section) 
         if not ignoreLabsAndTBAs or (section.find("L") == -1 and time  != "TBA"):
            theirTimes.append (days +  " " + time)
            #print ("Stokke has class at ", days , time)
   return theirTimes
   
def getInstructors():
   instructors = set()
   for classNumber in classes:
      for section in classes[classNumber]['sections']:
         instructor = classes[classNumber]['sections'][section]['instructor']
         if instructor != '':
            instructors.add (instructor)
         #else:
         #   x = 10
   return sorted (list (instructors))


undergradCommittee = ['Stokke, T', 'Hu, W', 'Adams, R', 'Elderini, T']
gradCommittee = ['Grant, E', 'Adams, R', 'Kim, M', 'Salehfar, H']
meetingStartTimes = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "1:00", "2:30", "3:00", "3:30" ]

classes = {}
classTimes = set()
classTimesNotAvailable = set()

inFile = open ("seesc-classes-spring2022-4.json", "r")
data = inFile.read()
inFile.close
classes = json.loads(data)
instructors = getInstructors()

#pp = pprint.PrettyPrinter(indent=3)
#pp.pprint(classes)   

print ("Instructors")
print (instructors)

print("classes taught by Stokke")
for classNumber in getClasses ("Stokke, T"): 
   for section in getInstructorSections (classNumber, "Stokke, T"):
      print (classNumber, section)
print()         
print("classes/labs taught by Stokke")
for classNumber in getClasses ("Stokke, T"): 
   for section in getInstructorSections (classNumber, "Stokke, T", False):
      print (classNumber, section)
print()         

for classNumber in classes:
   for section in classes[classNumber]['sections']:
      if classes[classNumber]['sections'][section]['instructor'] in undergradCommittee:
         tempSection = classes[classNumber]['sections'][section]
         if tempSection['time'].find('TBA') == -1:
            classTimesNotAvailable.add (tempSection['days'] + " " + tempSection['time'])
sortedClassTimesNotAvailable = list (classTimesNotAvailable)
sortedClassTimesNotAvailable.sort()
print ("Times not available")
for timeInfo in sortedClassTimesNotAvailable:
   days, time = timeInfo.split (" ")
   conflictClasses = classesAtTime (days, time)
   for conflictClass in conflictClasses:
      instructor = getInstructor (conflictClass)
      if instructor in undergradCommittee:
         print (days, time, getInstructor (conflictClass))
print ()

classesPerDay = {}
print ("Monday classes")   
for classNumber in classes:
   for section in classes[classNumber]['sections']:
      if classes[classNumber]['sections'][section]['days'].find('M') > -1:
         print (classNumber, section, classes[classNumber]['sections'][section]['time'])
         classesPerDay[classNumber+'-'+section]=classes[classNumber]['sections'][section]['time']

print ("\n\nMonday classes - time, class")
times = list(classesPerDay.keys())
times.sort (key=lambda n:sortableTime(classesPerDay[n]))
for className in times:
   name, section = className.split('-')
   print (classesPerDay[className], className, getInstructor (name, section))
   
print()
csci160sections = getSections ('CSCI 160')
csci160sections.sort()
print ("Sections for CS160", getSections ('CSCI 160'))
for section in csci160sections:
   print (section, getTime('CSCI 160', section))

myClasses = getClasses ('Stokke, T')
print (myClasses)
print()

print ()
print ("Undergraduate Committee")

overallTeachingTimes = []
for instructor in undergradCommittee:
   teachingTimes = getTeachingTimes (instructor)
   print (instructor)
   print (teachingTimes)
   print ()
   overallTeachingTimes = listUnion (overallTeachingTimes, teachingTimes)
   
print ()
   
timesAvailable = []
for day in "MTWRF":
   for startTime in meetingStartTimes: 
      duration = 60
      startTimeToTest = day + " " + startTime
      #middleTimeToTest= addMinutes (startTimeToTest, duration // 2)
      #endTimeToTest = addMinutes (startTimeToTest, duration)
      noConflict = True
      for className in overallTeachingTimes:
         startTimeConflict = False
         for times in range (duration // 30 + 1):
            startTimeConflict = startTimeConflict or timeConflict (className, addMinutes (startTimeToTest, times * 30))
         #startTimeConflict = timeConflict (className, startTimeToTest) or timeConflict (className, middleTimeToTest) or timeConflict (className, endTimeToTest)
         if startTimeConflict:
            noConflict = False
            break
      #   timesAvailable.append (timeToTest)
      if noConflict:
         print (startTimeToTest, " potential start time")

print ()
print ()
print ("Graduate Committee")
overallTeachingTimes = []
for instructor in gradCommittee:
   teachingTimes = getTeachingTimes (instructor)
   print (instructor)
   print (teachingTimes)
   print ()
   overallTeachingTimes = listUnion (overallTeachingTimes, teachingTimes)
   
print ()
  
timesAvailable = []
for day in "MTWRF":
   for startTime in meetingStartTimes: 
      duration = 80
      startTimeToTest = day + " " + startTime
      noConflict = True
      for className in overallTeachingTimes:
         startTimeConflict = False
         for times in range (duration // 30 + 1):
            startTimeConflict = startTimeConflict or timeConflict (className, addMinutes (startTimeToTest, times * 30), 5)
         if startTimeConflict:
            noConflict = False
            break
      #   timesAvailable.append (timeToTest)
      if noConflict:
         print (startTimeToTest, "potential start time for grad committee")
               

#input()