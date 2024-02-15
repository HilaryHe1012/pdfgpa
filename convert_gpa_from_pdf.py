import PyPDF2

def grade_converter(pdf_file):

    # used to convert letter grades to a 4.0 gpa scale
    grade_to_gpa = {"A+": 4.0, "A": 3.9, "A-": 3.7, "B+":3.3, "B":3, "B-": 2.7, "C+": 2.3, "C": 2, "C-":1.7, "D+":1.3, "D": 1, "D-": 0.7, "F": 0}
    cgpa = 0
    grades = []

    # open the pdf file 
    reader = PyPDF2.PdfReader(pdf_file)

    # grab all contents in the pdf
    contents = ""
    for page in reader.pages:
        contents += page.extract_text()

    # convert it into a list separated by words
    words = contents.split()

    for word in words:
        if word in grade_to_gpa.keys():
            cgpa += grade_to_gpa[word]
            grades.append(word)
    return round(cgpa / len(grades), 2)

def main():
    pdf_url = "MCM_TS_MCOFF-Year3-Fall.pdf"
    kush = "kush_transcript.pdf"
    timmy = "timmy_transcript.pdf"
    my_cgpa = grade_converter(timmy)
    print(my_cgpa)


main()
