import os
import requests
from dotenv import load_dotenv

#load env reading module
load_dotenv()

# print(os.getenv("CANVAS_URL"))

#Step 1:
token = os.getenv("CANVAS_TOKEN")
url = os.getenv("CANVAS_URL")
header = {"Authorization": f"Bearer {token}"}

#Step 2:
def get_new_assignments():
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
            print(course_name)

            for i in course_assignments:
                due_date = i.get("due_at", "No Due Date")
                sub_type = i.get("submission_types", [])

                print(f"{i['name']}, {due_date}, {sub_type}")

                # use external tools to find hidden assignments and put / parse into json / dict / repeat steps above

        



#Step 3:
get_new_assignments()