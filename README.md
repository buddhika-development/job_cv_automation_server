## CV Automation Platform - System Overview

This platform automates CV processing by utilizing AI-powered analysis and cloud-based storage. It is structured into multiple components, each playing a crucial role in handling, analyzing, and storing CVs.
In that project there use multiple technologies like,
1. Next js as frontend
2. Flask as backend
3. Langchain for interact with LLM

## Simple Explanation of the Process

Simple Explanation of the Process<br>
1️⃣ User Uploads CV → The user uploads their resume through the Next.js frontend.<br>
2️⃣ Data Sent to Backend → The Next.js server actions send the resume to the Flask backend.<br>
3️⃣ Storage & Processing → The Flask backend saves the CV to AWS S3 and prepares it for AI analysis.<br>
4️⃣ AI Analysis with Gemini LLM →
- The Flask backend sends the CV data to LangChain, which optimizes it.
- LangChain forwards it to Google Gemini LLM for AI processing.
- Gemini-2.0-flash-lite analyzes the resume and extracts key details (skills, experience, education).<br>

5️⃣ Storing Structured Data →
- The AI returns a JSON response with extracted information.
- The backend formats this data for better readability.<br>

6️⃣ Google Sheets Integration →
- The structured CV data is sent to Google Sheets via the Google API for record-keeping and further analysis.<br>

![image](https://github.com/user-attachments/assets/3046da8a-03d3-486d-bc26-f14cd34c6879)


## Use project locally

step 01 => Clone the project by using `git clone <repo-link>`

step 02 => Setup the python virtual enviorenment in command prompt `python -m venv <entiorenment_name>`

step 03 => Activate the created virtual enviorenment in command prompt `<enviorenment_name>\Scripts\activate`

step 04 => Install the necessery dependience `pip install -r requirenment.txt`

step 05 => Create .env file and include those provided values from your own credentials

  `
  aws_access_key_id
  aws_secret_access_key
  GOOGLE_API_KEY
  `
  
setp 06 => Run the server and check with the POSTMAN or connect directly into website frontend `python server.py`

step 07 => After all processes deactivate the virtual enviorenement `deactivate`

