<<<<<<< HEAD
# Libraries Needed
from google import genai # How I can communicate with Google Gemini using python
from google.genai.types import Tool, UrlContext, GenerateContentConfig # Not sure what this is for but it is listed in the Google Gemini Developer Docs
import sqlite3 # For the Database
import os # Where I can extract the API key and execute terminal commands such as creating a SQL Database
import re # Used for string cleaning and validation
from urllib.parse import urlparse # Checks if website is a valid website
import requests


# I want to make this a callable module so that I can run it from a GUI without the 'scary black box', aka a terminal appearing
def sub_list_gen(website: str, name: str, api_key_param:str):
    # Validation
    INVALID_CHARS = set(r'\/:*?"<>|') | {'\0'}
    errors = [] # List to hold all the errors to be output
    
    # Checks if they are strings
    if not isinstance(website, str):
        errors.append("Website must be a string")
    if not isinstance(name, str):
        errors.append("Name must be a string")
        
    if not errors:
        # This ensures that it does not continue if there are type errors
        INVALID_CHARS.add('/')
        
        # Now checks if name follows the rules to be saved as a file
        for char in name:
            if char in INVALID_CHARS:
                errors.append(
                    f"Names cannot contain {INVALID_CHARS}"
                )
                break
        
        # Windows Specific - checks if name starts or ends with space or dot
        if name and (name[0]in {' ','.'} or name [-1] in {' ', '.'}):
            errors.append("Name cannot start or end with a space or dot")

        if not website.startswith("https://") or not website.lower().endswith(".pdf"):
            errors.append("Website must start with 'https://' and end with '.pdf'")
            
        if website.startswith("https://cdn"):
            errors.append("CDNs are currently unsupported right now as Gemini does not fully support it")
        
        parsed_url = urlparse(website)
        if not (parsed_url.scheme and parsed_url.netloc):
            errors.append("Website is not a well formed url") # A well formed URL means that it follows the rules and standards of the layout of a URL (protocol://domain/resource), it does not guarantee whether it actually exists.
            
        if not errors: 
            try:
                resp = requests.head(website, allow_redirects=True, timeout=5)
                if  resp.status_code >= 400:
                    errors.append(
                       f"The URL could not be reached (status code {resp.status_code})." 
                    )
            except Exception as e:
                errors.append(f"Error trying to reach the URL: {str(e)}")
    
    if not errors:       
        tools = [
            {"url_context": UrlContext()}
        ]
        
        def strip_code_fences_inline(text: str) -> str:
        # Remove triple backticks + any attached language tag [sometimes it comes as sql other times sqlite]
            text = re.sub(r"```[^\n]*\n?", "", text)
            return text
        
        # API_KEY = os.environ["GEMINI_API_KEY"]
        API_KEY = api_key_param
        print(API_KEY)
        client = genai.Client(api_key=API_KEY)

        # Prepares the url part by putting URL string in prompt
        sql_file = name+".sql"
        db_file = name+".db"

        # Stores a copy of the contents of website in case anything goes wrong
        web_part = website

        # Step 2: Prepare prompt with URL for specification and instructions (f-strings are so useful here)
        prompt = f"Extract all **section headings and sub‑headings** from the specification text provided at {web_part} and generate only valid SQLite SQL code that creates a table called Topics (TopicID INT PRIMARY KEY AUTOINCREMENT, MainCategory TEXT NOT NULL, SubCategory TEXT NOT NULL, TopicDetail TEXT NOT NULL, Grade INT, Difficulty REAL, Stability REAL, DateReviewed TEXT, DateToReview TEXT) and inserts all extracted topics exactly as they appear in the spec text; do **not** include anything not literally present in the specification text; use only the provided spec content however you can make them useful for a student as a revision checklist and do not make it hyper-specific, I just want the topics and subtopics (for example, in the topic 'Exponentials and logs', I only want to see subtopics like 'Laws of logarithms' or 'logarithmic graphs', not stuff like 'know how to plot a logarithmic graph'); output only SQL code. Create blank columns called Grade, Difficulty, Stability, DateReviewed and DateToReview where a student can input integers 1-4 for Grade and a program can add review dates as well as difficulty and stability. If a subject has optional units, do not include them. If a specification has both A Level and AS Level, just make the database for A Level. Last but definitely not least, do not add your own commentary or your thoughts, just the SQL Code as this fed directly into SQLite and you dont want SQLite to error out."


        # Step 3: Generate summary with Gemini 2.5 (only model available from the free tier, might change in the next few months so still needs frequent review)
        response = client.models.generate_content(
            model = "gemini-3-flash-preview",
            contents = prompt,
            config = GenerateContentConfig(tools=tools)
            )

        # Step 4: Extract the generated SQL code
        sql_output = response.text
        conn = sqlite3.connect(db_file)
        # Step 5: Create a local SQLite Database using the terminal (abstracted from the end user)
        with open(sql_file, 'w', encoding="utf-8") as sql:
            try:
                #sql_output = sql_output.strip("`")
                sql.write(sql_output)
                #print(sql_output[:4])
                sql_output3 = strip_code_fences_inline(sql_output)
                #print(sql_output3)
                sql.write(str(sql))
                conn.executescript(sql_output3)
                print(f"{db_file} was created")
                conn.commit()
                conn.close()
                sql.close()
            except sqlite3.Error as er:
                errors.append(f"SQLite Error {er.sqlite_errorcode}: {er.sqlite_errorname}, please try again") 
    return errors

# Stores the errors, if there are none, it just proceeds as usual
# errors = sub_list_gen("https://qualifications.pearson.com/content/dam/pdf/A%20Level/Mathematics/2017/specification-and-sample-assesment/a-level-l3-further-mathematics-specification.pdf","further_maths_for_me")

# This is just for the purpose of debugging, it will be removed in the final code
""" if len(errors) > 0:
    counter = 0
    for counter in range (0, len(errors)):
=======
# Libraries Needed
from google import genai # How I can communicate with Google Gemini using python
from google.genai.types import Tool, UrlContext, GenerateContentConfig # Not sure what this is for but it is listed in the Google Gemini Developer Docs
import sqlite3 # For the Database
import os # Where I can extract the API key and execute terminal commands such as creating a SQL Database
import re # Used for string cleaning and validation
from urllib.parse import urlparse # Checks if website is a valid website
import requests


# I want to make this a callable module so that I can run it from a GUI without the 'scary black box', aka a terminal appearing
def sub_list_gen(website: str, name: str, api_key_param:str):
    # Validation
    INVALID_CHARS = set(r'\/:*?"<>|') | {'\0'}
    errors = [] # List to hold all the errors to be output
    
    # Checks if they are strings
    if not isinstance(website, str):
        errors.append("Website must be a string")
    if not isinstance(name, str):
        errors.append("Name must be a string")
        
    if not errors:
        # This ensures that it does not continue if there are type errors
        INVALID_CHARS.add('/')
        
        # Now checks if name follows the rules to be saved as a file
        for char in name:
            if char in INVALID_CHARS:
                errors.append(
                    f"Names cannot contain {INVALID_CHARS}"
                )
                break
        
        # Windows Specific - checks if name starts or ends with space or dot
        if name and (name[0]in {' ','.'} or name [-1] in {' ', '.'}):
            errors.append("Name cannot start or end with a space or dot")

        if not website.startswith("https://") or not website.lower().endswith(".pdf"):
            errors.append("Website must start with 'https://' and end with '.pdf'")
            
        if website.startswith("https://cdn"):
            errors.append("CDNs are currently unsupported right now as Gemini does not fully support it")
        
        parsed_url = urlparse(website)
        if not (parsed_url.scheme and parsed_url.netloc):
            errors.append("Website is not a well formed url") # A well formed URL means that it follows the rules and standards of the layout of a URL (protocol://domain/resource), it does not guarantee whether it actually exists.
            
        if not errors: 
            try:
                resp = requests.head(website, allow_redirects=True, timeout=5)
                if  resp.status_code >= 400:
                    errors.append(
                       f"The URL could not be reached (status code {resp.status_code})." 
                    )
            except Exception as e:
                errors.append(f"Error trying to reach the URL: {str(e)}")
    
    if not errors:       
        tools = [
            {"url_context": UrlContext()}
        ]
        
        def strip_code_fences_inline(text: str) -> str:
        # Remove triple backticks + any attached language tag [sometimes it comes as sql other times sqlite]
            text = re.sub(r"```[^\n]*\n?", "", text)
            return text
        
        # API_KEY = os.environ["GEMINI_API_KEY"]
        API_KEY = api_key_param
        print(API_KEY)
        client = genai.Client(api_key=API_KEY)

        # Prepares the url part by putting URL string in prompt
        sql_file = name+".sql"
        db_file = name+".db"

        # Stores a copy of the contents of website in case anything goes wrong
        web_part = website

        # Step 2: Prepare prompt with URL for specification and instructions (f-strings are so useful here)
        prompt = f"Extract all **section headings and sub‑headings** from the specification text provided at {web_part} and generate only valid SQLite SQL code that creates a table called Topics (TopicID INT PRIMARY KEY AUTOINCREMENT, MainCategory TEXT NOT NULL, SubCategory TEXT NOT NULL, TopicDetail TEXT NOT NULL, Grade INT, Difficulty REAL, Stability REAL, DateReviewed TEXT, DateToReview TEXT) and inserts all extracted topics exactly as they appear in the spec text; do **not** include anything not literally present in the specification text; use only the provided spec content however you can make them useful for a student as a revision checklist and do not make it hyper-specific, I just want the topics and subtopics (for example, in the topic 'Exponentials and logs', I only want to see subtopics like 'Laws of logarithms' or 'logarithmic graphs', not stuff like 'know how to plot a logarithmic graph'); output only SQL code. Create blank columns called Grade, Difficulty, Stability, DateReviewed and DateToReview where a student can input integers 1-4 for Grade and a program can add review dates as well as difficulty and stability. If a subject has optional units, do not include them. If a specification has both A Level and AS Level, just make the database for A Level. Last but definitely not least, do not add your own commentary or your thoughts, just the SQL Code as this fed directly into SQLite and you dont want SQLite to error out."


        # Step 3: Generate summary with Gemini 2.5 (only model available from the free tier, might change in the next few months so still needs frequent review)
        response = client.models.generate_content(
            model = "gemini-3-flash-preview",
            contents = prompt,
            config = GenerateContentConfig(tools=tools)
            )

        # Step 4: Extract the generated SQL code
        sql_output = response.text
        conn = sqlite3.connect(db_file)
        # Step 5: Create a local SQLite Database using the terminal (abstracted from the end user)
        with open(sql_file, 'w', encoding="utf-8") as sql:
            try:
                #sql_output = sql_output.strip("`")
                sql.write(sql_output)
                #print(sql_output[:4])
                sql_output3 = strip_code_fences_inline(sql_output)
                #print(sql_output3)
                sql.write(str(sql))
                conn.executescript(sql_output3)
                print(f"{db_file} was created")
                conn.commit()
                conn.close()
                sql.close()
            except sqlite3.Error as er:
                errors.append(f"SQLite Error {er.sqlite_errorcode}: {er.sqlite_errorname}, please try again") 
    return errors

# Stores the errors, if there are none, it just proceeds as usual
# errors = sub_list_gen("https://qualifications.pearson.com/content/dam/pdf/A%20Level/Mathematics/2017/specification-and-sample-assesment/a-level-l3-further-mathematics-specification.pdf","further_maths_for_me")

# This is just for the purpose of debugging, it will be removed in the final code
""" if len(errors) > 0:
    counter = 0
    for counter in range (0, len(errors)):
>>>>>>> master
        print(errors[counter]) """