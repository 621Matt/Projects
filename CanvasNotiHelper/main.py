import os
import requests
import customtkinter
import re
from datetime import datetime
from dotenv import load_dotenv 

#load env reading module
load_dotenv()
token = os.getenv("CANVAS_TOKEN")
url = os.getenv("CANVAS_URL")
header = {"Authorization": f"Bearer {token}"}

# Create test variable of assignments
# Create app screen
# Create function that makes new checkboxes based on assignments
# create function that checks for new assignments
    # use threads to prevent freezing of UI

app = customtkinter.CTk()
app.title("Canvas Helped")
app.geometry("518x293")
app.grid_columnconfigure((0,1), weight=1)
checkbox_vars = []

b = "ITSC-3144"
a = "Assignment 3"
c = "Sept 05"

# checkbox_1 = customtkinter.CTkCheckBox(app, text=(f"{a} - {b} - {c}"))
# checkbox_1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="ew")

# app.mainloop()












# Gets assignments from canvas api and puts into list
def get_current_assignments():
    # Assignments
    assignments = []


    #Requests courses and stores in json file
    course_request = requests.get(f"{url}/api/v1/courses", headers=header, params={"enrollment_state": "active"})
    courses = course_request.json()

    # print(courses)

    for course in courses:
        course_id = course.get("id")
        course_name = course.get("name")   

        if course_id is None or course_name is None:
            continue

        #get assignments for specific course
        course_assignments_url = f"{url}/api/v1/courses/{course_id}/assignments"
        course_assignments_request = requests.get(course_assignments_url, headers=header, params={"bucket":"upcoming"})

        if course_assignments_request.status_code == 200:
            # print("yes")

            course_assignments = course_assignments_request.json()
            # print(course_name)

            for i in course_assignments:

                # Vibe Code Begin / Cleans and removes unwanted chars from date, course, and assignment name 
                date = i.get("due_at", "No Due Date")
                if date:
                    date_obj = datetime.fromisoformat(date.replace("Z", "+00:00"))
                    formatted_date = date_obj.strftime("%b %d")
                else:
                    formatted_date = "No Due Date"

                course = str(course_name)
                # Regex is weird, finds 2 to 4 capital letters, matches - between letters and numbers, and 4 digits
                match = re.search(r'([A-Z]{2,4})[-]?(\d{4})', course)
                if match:
                    cleaned_course = f"{match.group(1)}-{match.group(2)}"
                else:
                    cleaned_course = course

                assignment_name = str(i['name']).encode('cp1252', errors='replace').decode('cp1252')
                # End

                assignment = {
                    "course" : cleaned_course,
                    "name" : assignment_name,
                    "due_date" : formatted_date,
                }

                assignments.append(assignment)
               

# didnt wirk on printed last assignment
# probs cuz screen wasnt updating idk
    for i in assignments:
        # print(i.get("course"))
        checkbox_1 = customtkinter.CTkCheckBox(app, text=(f"{i.get('course')} - {i.get('name')} - {i.get('due_date')}"))
        checkbox_1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="ew")
      
         # call function that makes checkboxs


#Step 3:
get_current_assignments()
app.mainloop()