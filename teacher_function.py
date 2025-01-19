from mistralai import Mistral
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract
import subprocess
from PIL import Image
AI71_API_KEY = "api71-api-652e5c6c-8edf-41d0-9c34-28522b07bef9"

subprocess.run(['apt-get','update'])
subprocess.run(['apt-get','install','-y','tesseract-ocr'])
API_KEY = 'xQ2Zhfsp4cLar4lvBRDWZKljvp0Ej427'
MODEL = "mistral-large-latest"
client = Mistral(api_key=API_KEY)
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_questions_from_text(text, no_of_questions, marks_per_part, no_parts):
    chat_response = client.chat.complete(
            model=MODEL,
            messages = [
        {"role": "system", "content": "You are a teaching assistant"},
        {"role": "user",
         "content": f"Give your own {no_of_questions} questions under each part for {no_parts} parts with {marks_per_part} marks for each part. Note that all questions must be from the topics of {text}"}
            ]

        )
    response_content = chat_response.choices[0].message.content
    return response_content
    

def extract_text_from_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Ensure the image was loaded correctly
    if img is None:
        raise ValueError("Image not found or unable to load")

    # Convert the image to RGB format
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Extract text from the image
    text = pytesseract.image_to_string(img_rgb)
    
    return text


def evaluate(question, answer, max_marks):
    prompt = f"""Questions: {question}
    Answer: {answer}.
    Evaluate answers strictly one by one(if there are multiple) for each question and assign marks out of {max_marks} based on below guidelines.
guidelines:
- If the answer is wrong or incorrect or irrelevent to topic, give 0 marks.

- If the answer is somewhat accurate, give total marks minus 2, and so on.
- If the answer is very accurate and complete, give total marks.
- If the answer is good but not completely accurate, give total marks minus 1.


Note:Provide only marks for each answers. dont provide anything other than that.
Format:
1.Question no: Marks,etc"""
    chat_response = client.chat.complete(
            model=MODEL,
            messages =[
        {"role": "system", "content": "You are a strict answer evaluator. "},
        {"role": "user", "content": prompt}
    ]
        )
    response_content = chat_response.choices[0].message.content
    return response_content
    

def generate_student_report(name, age, cgpa, course, assigned_test, ai_test, interests, difficulty, courses_taken):
    prompt = f"""
    Name: {name}
    Age: {age}
    CGPA: {cgpa}
    Course: {course}
    Assigned Test Score: {assigned_test}
    AI generated Test Score: {ai_test}
    Interests: {interests}
    Difficulty in: {difficulty}
    Courses Taken: {courses_taken}
    Use the above student data to generate a neat personalized report and suggested teaching methods."""
    chat_response = client.chat.complete(
            model=MODEL,
            messages=[
            {"role": "system", "content": "You are a student report generator."},
            {"role": "user", "content": prompt}
        ]
        )
    response_content = chat_response.choices[0].message.content
    return response_content
    
def generate_timetable_module(data,hours_per_day,days_per_week,semester_end_date,subjects):
    chat_response = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Create a timetable starting from Monday based on the following inputs:\n"
                                            f"- Number of hours per day: {hours_per_day}\n"
                                            f"- Number of days per week: {days_per_week}\n"
                                            f"- Semester end date: {semester_end_date}\n"
                                            f"- Subjects: {', '.join(subjects)}\n"}
            ]
        )
    response_content = chat_response.choices[0].message.content
    return response_content
    
   
def cluster_topics(academic_topics):
    prompt = (
            "Please cluster the following academic topics into their respective subjects such as Mathematics, Physics, etc.: "
            + ", ".join(academic_topics))
    response = ""
    chat_response = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
    response_content = chat_response.choices[0].message.content
    return response_content
    

def generate_timetable_weak(clustered_subjects, hours_per_day):
    prompt = (
        f"Using the following subjects and topics:\n{clustered_subjects}\n"
        f"Generate a special class timetable for {hours_per_day} hours per day.\n"
        f"Also provide reference books and methods to teach the slow learners for each subject"
    )
    response = ""
    chat_response = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
    response_content = chat_response.choices[0].message.content
    return response_content
    
    