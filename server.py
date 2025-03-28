from flask import Flask, request
from utills import validation, aws_s3, llm_reponse
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)

load_dotenv()

# cv holding folder
cv_container = "cv_container"

# check cv holder file already exits or not, if not exists create new folder
if not os.path.exists(cv_container):
    os.makedirs(cv_container)

# handle http request
@app.route('/api/form_data_handling', methods = ["POST"] )
def backend_form_handling():

    applicant_name = request.form.get('applicantName')
    applicant_contact_number = request.form.get('applicantContact')
    applicant_email = request.form.get('applicantEmail')
    applicant_cv = request.files.get('applicantCv')


    # validate the user form data
    applicant_name_validation = validation.applicant_name_validation(applicant_name)
    applicant_contact_number_validation = validation.applicant_phone_number_validation(applicant_contact_number)
    applicant_email_validation = validation.applicant_email_address_validation(applicant_email)
    applicant_cv_validation = validation.applicant_cv_validation(applicant_cv.filename)

    # exit from the process when some of validation false
    if not (applicant_name_validation or applicant_contact_number_validation or applicant_email_validation or applicant_cv_validation) :
        return {
            'message' : 'Please enter valid details...'
        }
    
    # store pdf in folder
    try:
        cv_container_file_path = 'cv_container'
        
        current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S");
        file_name = f"{current_date_time}_{applicant_name.replace(" ","_")}.pdf"

        cv_save_path = os.path.join(cv_container_file_path, file_name)
        applicant_cv.save(cv_save_path)
    except:
        print("Something went wrong in CV saving process....")

    

    # upload cv into aws s3 bucket
    try:
        aws_s3.store_cv_in_s3(cv_save_path, file_name)    
    except:
        print("Somethign went wrong in data s3 bucket uploading process")

    
    # scrape data, analyze and update google sheet
    try:
        content = llm_reponse.pdf_content_extract(applicant_cv)
        prompt = llm_reponse.generate_prompt_template(content)
        analuzed_applicant_details = llm_reponse.get_response_from_llm(prompt)
        llm_reponse.update_data_google_sheet(analuzed_applicant_details)

    except:
        print("Something went wrong data scraping process and data uploading process....")

    
    return {
        'message' : 'Success'
    }


app.run(debug=True, port=8000)