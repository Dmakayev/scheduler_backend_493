import re
from tika import parser
import json
from CourseTables.models import *


def parsePDF(deptInfo, outFile):
    classes = {}
    for entry in deptInfo:
        raw = parser.from_file(entry['fileName'])
        text = raw['content']
        lines = text.split("\n")
        # print (len(lines))

        index = 0
        while index < len(lines):
            while len(lines[index].strip()) == 0:
                del (lines[index])
                if index >= len(lines):
                    break
            index += 1

        classPattern = format(entry['prefix'], "4s") + " \d\d\d"  # 'CSCI \d\d\d'
        classPattern2 = "^" + format(entry['prefix'], "4s") + " \d\d\d"  # '^CSCI \d\d\d'

        index = 0
        while index < len(lines):
            if re.search(classPattern2, lines[index]) != None:
                # print (lines[index])
                # classNumber = lines[index][0:8].strip() `
                classNumber = lines[index][0:9].strip()  # included lab sections as a separate class
                className = lines[index][12:43].strip()
                credits = lines[index][44]
                classes[classNumber] = {}
                classes[classNumber]['classNumber'] = classNumber
                classes[classNumber]['className'] = className
                classes[classNumber]['credits'] = credits
                index = index + 1
                classes[classNumber]['sections'] = []
                while re.search('^\s{10}', lines[index]) != None:
                    # print (lines[index])
                    index += 1
                while index < len(lines) and re.search('^L?\d\d', lines[index]) != None:
                    # print (lines[index])
                    section = lines[index][0:4].strip()
                    number = lines[index][4:9].strip()
                    time = lines[index][12:27].strip()
                    days = lines[index][27:35].strip()
                    room = lines[index][36:50].strip()
                    instructor = lines[index][58:76].strip()
                    capacity = lines[index][79:82].strip()
                    enrollment = lines[index][86:89].strip()
                    waitSize = lines[index][93:96].strip()
                    classes[classNumber]['sections'].append(
                        {'sectionNumber': section, 'capacity': capacity, 'room': room, 'waitSize': waitSize,
                         'enrollment': enrollment, 'days': days,
                         'number': number, 'time': time, 'instructor': instructor})

                    sendCourse = TempCourse()
                    sendCourse.classNumber = classNumber
                    sendCourse.className = className
                    sendCourse.credits = credits
                    sendCourse.sectionNumber = section
                    sendCourse.capacity = capacity
                    sendCourse.room = room
                    sendCourse.waitSize = waitSize
                    sendCourse.enrollment = enrollment
                    sendCourse.days = days
                    sendCourse.uniqueCourseID = number
                    sendCourse.time = time
                    sendCourse.instructor = instructor
                    sendCourse.save()

                    index = index + 3
                    while index < len(lines) and lines[index][0:5] == "     ":
                        index = index + 1
                # print ()

            else:
                index = index + 1

    f = list(classes.keys())
    q = list(map(lambda field: classes[field], f))
    outFile = open(outFile, "w")
    json.dump(q, outFile)
    outFile.close()


def main(inFile):
    deptInfo = [
        {'fileName': inFile, 'prefix': 'CSCI'},
        {'fileName': inFile, 'prefix': 'EE'},
    ]
    parsePDF(deptInfo, inFile + "-output.json")
    print("Done")

# main()
