import PyPDF2

# used to convert letter grades to a 4.0 gpa scale
grade_to_gpa = {"A+": 4.0, "A": 3.9, "A-": 3.7, "B+":3.3, "B":3, "B-": 2.7, "C+": 2.3, "C": 2, "C-":1.7, "D+":1.3, "D": 1, "D-": 0.7, "F": 0}
# words to filter in the parser
keywords = ['Course', 'Title','Term', 'Enrolment', 'Attm./Earned', 'Units']

class Course:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        self.high_grade = grade[0] == 'A'
        # print(self.grade)
        # if grade[0] == 'A':
            # print('high grade', grade)
          

    def get_name(self):
        return self.name
    def get_grade(self):
        return self.grade
    def __str__(self): # for printing
        return f"{self.name}: {self.grade}"

    # not sure if this is gonna be useful or not...
    def print_all_courses(self):
        return f"{self.name}"
    def print_all_grades(self):
        return f"{self.grade}"
    
    def to_dict(self):
        return {"name": self.name, "grade": self.grade, "high_grade": self.high_grade}

# a helper function that initializes all the courses in 'Course' type
# and returns a list of 'Course' object
def initalize_courses(course_list):
    courses = []
    for item in course_list:
        cur_name = ''
        # cur = Course(None, None)
        words = item.split()
        for word in words:
            if word in grade_to_gpa:
                grade = word
            else:
                if '/' not in word:
                    cur_name += word + ' '
                name = cur_name 
        courses.append(Course(name, grade))
    return courses

# -------------------------------------
#       parser + reader of the pdf
# -------------------------------------
def extract_course(pdf_file):
    # open the pdf file 
    reader = PyPDF2.PdfReader(pdf_file)

    # grab all contents in the pdf
    content = []
    start_collecting = False
    for page in reader.pages:
        start_collecting = False
        page_content = page.extract_text()
        lines = page_content.split('\n')
        for line in lines:
            # take all lines after 'Course' and before 'Totals'
            if line == "Course":
                start_collecting = True
            if line == "Totals":
                start_collecting = False
            if start_collecting:
                content.append(line)
    return content

# returns a list of all courses in separate string of the format:
# 'CourseID CourseName [Units] Grade'
def clean_course_list(data):
   flag_first = False
   merged_courses = []
   i = 0
   while i < len(data):
      item = data[i]
      if item == 'Course': 
          tmp = first_course(data, i)
          merged_courses.append(tmp[0])
          i = tmp[1] + 1
      else:
          merged_courses.append(item)
          i += 1
   return merged_courses[:-1] # the last string is courses with no grades -> thus dropped

# helper function to return the merged version of the first course for each table
def first_course(data, i):
    current_course = ''
    while i < len(data):
        # because I check for grades the courses with not grades are 
        # not parsed properly
        if data[i] in grade_to_gpa.keys():
            current_course += data[i]
            break
        words = data[i].split()
        for word in words:
            if word not in keywords:
                if 'Grade' not in word:
                    current_course += ''.join(word) + ' '
        i += 1
    return [current_course, i]

# -------------------------------------
#       Compute 4.0 scale cgpa
# -------------------------------------
def grade_converter(c): # takes in a list of Course object
    cgpa = 0
    valid_courses = 0
    for course in c:
        cur_grade = course.get_grade()
        if cur_grade:
            cgpa += grade_to_gpa[course.get_grade()]
            valid_courses += 1            
    return round(cgpa / valid_courses, 2)

def main():
    my_transcript = "transcript.pdf"
    timmy = "timmy.pdf"
    text = extract_course(my_transcript)
    c_list = clean_course_list(text)
    c = initalize_courses(c_list)

    # to print all the courses with grades, uncomment the following:
    for course in c: print(course)
    gpa = grade_converter(c)
    # print('cgpa is:', gpa)
    return 
# main()

def full_extract(pdf):
    text = extract_course(pdf)
    c_list = clean_course_list(text)
    c = initalize_courses(c_list)
    gpa = grade_converter(c)
    good_courses = [course for course in c if course.high_grade]
    # for course in good_courses: print(course)
    dict_c = [course.to_dict() for course in c]
    dict_good_courses = [course.to_dict() for course in good_courses]
    return {"gpa": gpa, "course_list": dict_c, "high_grade_course_list":dict_good_courses}


# print(full_extract('transcript.pdf'))