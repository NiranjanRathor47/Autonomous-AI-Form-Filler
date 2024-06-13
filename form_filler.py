import os
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# OpenAI API Key (replace with your new key if you have one)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the form URL
form_url = "https://form.jotform.com/241635027272149"
driver.get(form_url)

# Wait for the page to load completely
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

# Fill in the form fields with dummy data
try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'q11_fullName[first]')))
    driver.find_element(By.NAME, 'q11_fullName[first]').send_keys('John')
    driver.find_element(By.NAME, 'q11_fullName[middle]').send_keys('Doe')
    driver.find_element(By.NAME, 'q11_fullName[last]').send_keys('Smith')
    driver.find_element(By.NAME, 'q16_currentAddress[addr_line1]').send_keys('123 Main St')
    driver.find_element(By.NAME, 'q16_currentAddress[addr_line2]').send_keys('Apt 4B')
    driver.find_element(By.NAME, 'q16_currentAddress[city]').send_keys('Anytown')
    driver.find_element(By.NAME, 'q16_currentAddress[state]').send_keys('CA')
    driver.find_element(By.NAME, 'q16_currentAddress[postal]').send_keys('12345')
    driver.find_element(By.NAME, 'q12_emailAddress').send_keys('john.doe@example.com')
    driver.find_element(By.NAME, 'q13_phoneNumber13[full]').send_keys('(123) 456-7890')
    driver.find_element(By.NAME, 'q19_linkedin').send_keys('https://linkedin.com/in/johndoe')
except Exception as e:
    print(f"An error occurred while filling in personal information: {e}")

# Define prompt texts for OpenAI API
prompts = [
    "Write something interesting about AI Agents/LLMs",
    "Write something interesting about Web Automation",
    "Explain how to reverse a LinkedList"
]

# Generate content using OpenAI API
generated_texts = []
for prompt in prompts:
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Use gpt-3.5-turbo model
            prompt=prompt,
            max_tokens=150
        )
        generated_texts.append(response['choices'][0]['text'].strip())
    except Exception as e:
        print(f"An error occurred while generating text for prompt '{prompt}': {e}")
        generated_texts.append("")  # Add empty string to maintain list structure

# Fill the generated texts into the form fields
try:
    driver.find_element(By.NAME, 'q23_pleaseSpecify').send_keys(generated_texts[0])
    driver.find_element(By.NAME, 'q24_writeSomething').send_keys(generated_texts[1])
    driver.find_element(By.NAME, 'q25_reverseA').send_keys(generated_texts[2])
except Exception as e:
    print(f"An error occurred while filling in generated content: {e}")

# Upload the resume file (ensure the path to your resume is correct)
resume_path = "D:\\Resumes\\NiranjanRathorSRM_1.pdf"
try:
    driver.find_element(By.NAME, 'file').send_keys(resume_path)
except Exception as e:
    print(f"An error occurred while uploading the resume: {e}")

# Fill the cover letter field if it exists
try:
    driver.find_element(By.NAME, 'q22_coverLetter').send_keys("""Dear [Recruiter Name],

I came across your post for the [Job Title] position at [Company Name] and was very interested in applying my skills and experience to this opportunity.

In my previous role as a data science intern, I developed a customer churn prediction model with 83% accuracy using Python and scikit-learn. I'm also proficient in NLP and deployed a text summarization model on AWS.

My resume details my qualifications further, but I wanted to express my strong interest in Company's work. I'm a fast learner and eager to contribute meaningfully.

Thank you for your time and consideration.

Sincerely,

Niranjan Rathor""")
except Exception as e:
    print(f"An error occurred while filling in the cover letter: {e}")

# Submit the form
try:
    driver.find_element(By.ID, 'input_9').click()
    time.sleep(10)  # Allow time for the form to be submitted
except Exception as e:
    print(f"An error occurred while submitting the form: {e}")

# Close the browser
driver.quit()
