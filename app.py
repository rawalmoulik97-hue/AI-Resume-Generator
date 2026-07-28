import streamlit as st
# streamlit: Web based app making 
# lite python framework

st.title("AI Resume Maker")

st.markdown("""##User can create or download AI created Resume based on High ATS Score""")

#====================AI AGENT ===========================

import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from PIL import image

# ==========================API KEY LOAD ==============================

GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type = "password")
GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY",type = "password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type = "password")

if not (GOOGLE_API_KEY) and not (GROQ_API_KEY) and not (TAVILY_API_KEY):
     st.sidebar.warning("PASS API KEY")
     st.stop()
else:
     st.success("API KEY LOADED")

# ==========================Model Building =============================

model = ChatGoogleGenerativeAI(
     google_api_key = GOOGLE_API_KEY,
     model = 'gemini-3.5-flash-lite',
)


def search_recent_news_jobs(query):
  """This function helps to search
  recent news or jobs related to
  given search query suppose user
  write Python Developer jobs
  it shopuld return trending news
  and job links"""
  client = TavilyClient(
      api_key = TAVILY_API_KEY
     )

  result = client.search(query)



# agent creation
from langchain.agents import create_agent

agent = create_agent(
    model = model,
    tools = [search_recent_news_jobs]
)

# ================================ PROMPT GENEARTOR =========================

def prompt_generator(agent):
  """This function helps to give detailed prompt
  followed by Chain of thoughts and persona based promoting,
  main task is to give detailed prompt to build Resume for
  students or Experienced person
  Based on their given personal information.
  """
  prompt = """You are a senior HR resume Analyzer,
  main task is to give detailed prompt to build Resume
  for Students or Experienced person based on their
  personal infromation. System Instruction I want Model
  to generate resume in HTML format, include that in prompt"""

  response = agent.invoke(prompt)
  file_name = 'prompt.py'
  with open(file_name, 'w') as f:
    f.write(response.content[-1]['text'])
  return "Prompt file generated Successfully, agent can read it"
prompt_generator(model)

  
# TOOL 2:

def resume_maker_prompt():
  """This function just gives updated prompt for model"""

  with open('prompt.py','r') as f:
    prompt = f.read()
  return prompt

resume_maker_prompt()

# ================================== UPLOAD IMAGE ================================

uploaded_file = st.sidebar.file_uploader(
     "Choose an image",
     type = ["jpg","jpeg","png","webp"]
)
if uploaded_file is not None:
     try:
          image = Image.open(uploaded_file)

          st.sidebar.image(image, caption = "UPLOADED IMAGE , use_container_width=True)

          if image.mode in ("RGBA" , "P"):
              image = image.convert("RGB")
          base_name = os.path.splitext)uploaded_file.name)[0]
          save_path = f"{base_name}.jpg"
          
          # 3. Save the image to the current working directory

          image.save(save_path, "JPEG")
          st.sidebar.success(f" Image Successfully saved as `{save_path}`!")

     except Execution as e:
          st.error(f"Error proccessing image: {e}")
          

# ==============================GENEERATE RESUME ===========================


prompt = """You are a helpful AI Assistant
with job resume maker , your task is to give
HTML format resume, with proper designing using recent CSS and JS
code, with professional design Format.
User will upload data and return HTML format resume
always use different color or styling"""

final_prompt = prompt + resume_maker_prompt()

user_details = """ user details: given below:
name is Moulik Rawal and i am a AI developer
my email is rawalmoulik97@gmail.com and i completed
my graduation from IITM College Janakpuri in BCA
I scored 90% in 12th class and scored  88% in 10th class
i have a experience of 3 Years in AI industry
my Skills are SQL, DBMS , PYTHON , Node.JS, React.JS
my hobbies are read,code,gaming,travelling
and give HR eye catching quates in my Resume
make my resume that effecting that it increases my
chances of selection"""

query = final_prompt + user_details

user_info = st.text_input("Enter your information")

user_details = f"""user details: given below:
Resume info: {user_info}
photo: {uploaded_file}
Photo present in current directory with name as
uploaded_file, and once resume generated give download button 
in same html code.
Default if not given : Give Python Developer Resume"""

if st.button("Genearate Resume"):
  with st.spinner("Running AGENT......"):

    response = agent.invoke({'messages':[{'role':'user','content': query}]})
    code = response['messages'][-1].content[-1]['text']

    # st.markdown(code)
    st.html(code, width="stretch", unsafe_allow_javascript=True)





