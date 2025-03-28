
# import necesery packages
import os
import json
import gspread
from pypdf import PdfReader
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from google.oauth2.service_account import Credentials

load_dotenv()


# cread pdf file
def pdf_content_extract(file):

    cv_content = ""

    # access the pdf file
    cv = PdfReader(file)
    cv_page_count = len(cv.pages)

    print(cv_page_count)

    # read pdf file and append content
    for i in range(0, cv_page_count):
        cv_page_content = cv.pages[i].extract_text().strip().replace("\n", "")
        cv_content += cv_page_content

    return cv_content


# generate prompt template for get response from the LLM model
def generate_prompt_template(content):

    # make promt with the system information
    template = """
        You need to acts as compnay HR manage. Your task is filter | extract details from the given cv content. You need to provide details about,
            applicant_name,
            applicant_contact_number,
            applicant_email_address,
            applicant_linkedin_profile,
            applicant_github_profile,
            other_links
            applicant_education_experience,
            projects,
            applicant_job_experience
        
        those details need to provide from the json format. in project need to provide details in,
            project_name,
            project_description,
            related_links,
            used_technological_stack
        that data paragraphic manager, but make line sperator when provide details about another project . also in educational qualification,
            educational_qualification,
            educational_institute,
            year have done
        in that data paragraphic manager, but make line sperator when provide details about another educational qualification. Also there are past_experiences,
            company_name,
            working_duration,
            position_worked
        in that data paragraphic manager, but make line sperator when provide details about another experience.In applicant projects can be what are the things they are build and what are the project they are interacted with. FIlter it from the things in the cv.

        if there is no any provided value for specific field provide null
        
        cv content : {cv_content}
    """

    # prepare the prompt with the provided details
    prompt_template = PromptTemplate.from_template(template)
    prompt = prompt_template.invoke({"cv_content" : content})

    return prompt


def get_response_from_llm(prompt) :

    try:
        # define llm
        model = ChatGoogleGenerativeAI(
            model= "gemini-2.0-flash",
            temperature= 0
        )

        # get analyzed response from the llm
        response = model.invoke(prompt).content

        # organize the response and wrap with json objext
        organized_response = response.replace("```", "").replace("json","")
        json_response = json.loads(organized_response)
        
        return json_response
    except Exception as e:
        print(f"Something went wrong in llm response process.... {e}")


# update google sheet with the llm analyze detail
def update_data_google_sheet(applicant_data):

    scopes = [ "https://www.googleapis.com/auth/spreadsheets" ]
    credentials_document = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
    print(credentials_document)
    
    # connect with the relevent specific spread sheet
    try :
        credentials = Credentials.from_service_account_file(credentials_document, scopes = scopes)
        clinet = gspread.authorize(credentials)           

        sheet_id = "1Wy_ExShLnIkm3qu3WMcNkff_Edu7AhahDJ17Lub5fpw"

        work_book = clinet.open_by_key(sheet_id)
    except Exception as e:
        print(f"Something went wrong while connectiong to spreadsheet... : {e}")
        
    
    work_sheet_list = map(lambda x : x.title, work_book.worksheets())
    working_worksheet = "Apllicant Details"

    # access the working sheet if it exist, other wise create the spread sheet
    try:
        if working_worksheet in work_sheet_list:
            sheet = work_book.worksheet(working_worksheet)
        else :
            sheet = work_book.add_worksheet(working_worksheet, cols = 10, rows = 5000)

            # setup the spreadsheet headers
            sheet.update_cell(1,2, "Applicant contact")
            sheet.update_cell(1,1, "Applicant name")
            sheet.update_cell(1,3, "Applicant email address")
            sheet.update_cell(1,4, "Applicant linkedin profile")
            sheet.update_cell(1,5, "Applicant github profile")
            sheet.update_cell(1,6, "Applicant edycation")
            sheet.update_cell(1,7, "Applicant projects")
            sheet.update_cell(1,8, "Applicant past experience")
            sheet.update_cell(1,9, "Applicant other links")
    except:
        print("Something went wrong while woring data sheet accessing....")
    

    spread_sheet_data = sheet.get_all_values()
    spread_sheet_data_row_count = len(spread_sheet_data)

    # data insertion process
    try:
        currently_updating_row = spread_sheet_data_row_count + 1
        sheet.update_cell(currently_updating_row, 1, applicant_data["applicant_name"])
        sheet.update_cell(currently_updating_row, 2, applicant_data["applicant_contact_number"])
        sheet.update_cell(currently_updating_row, 3, applicant_data["applicant_email_address"])
        sheet.update_cell(currently_updating_row, 4, applicant_data["applicant_linkedin_profile"])
        sheet.update_cell(currently_updating_row, 5, applicant_data["applicant_github_profile"])
        sheet.update_cell(currently_updating_row, 6, applicant_data["applicant_education_experience"])
        sheet.update_cell(currently_updating_row, 7, applicant_data["projects"])
        sheet.update_cell(currently_updating_row, 8, applicant_data["applicant_job_experience"])
        sheet.update_cell(currently_updating_row, 9, applicant_data["other_links"])

    except:
        print("Somethign went wrong while data wring in the spreadsheet..")


