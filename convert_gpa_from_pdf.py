import PyPDF2

def grade_converter(pdf_file):

    # used to convert letter grades to a 4.0 gpa scale
    grade_to_gpa = {"A+": 4.0, "A": 3.9, "A-": 3.7, "B+":3.3, "B":3, "B-": 2.7, "C+": 2.3, "C": 2, "C-":1.7, "D+":1.3, "D": 1, "D-": 0.7, "F": 0}
    cgpa = 0
    grades = []

    # open the pdf file 
    reader = PyPDF2.PdfReader(pdf_file)

    # grab all contents in the pdf
    page_content = ''

    for page in reader.pages:
        # flag to start collecting grades after encountering "Grade" keyword
        start_collecting = False

        page_content = page.extract_text()
        # convert it into a list separated by words
        words = page_content.split()

        for word in words:
            # check if the word contains "Grade" and set the flag to True
            if "Grade" in word:
                start_collecting = True
                continue 

             # if the flag is True, collect the grades
            if start_collecting and word in grade_to_gpa.keys():
                cgpa += grade_to_gpa[word]
                grades.append(word)
    return round(cgpa / len(grades), 2)

def main():
    my_transcript = "transcript.pdf"
    my_gpa = grade_converter(my_transcript)
    print(my_gpa)
    return 
main()