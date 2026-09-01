import os
import requests
import customtkinter
import re
import threading
import time
from datetime import datetime
from dotenv import load_dotenv 

#load env reading module
load_dotenv()
token = os.getenv("CANVAS_TOKEN")
url = os.getenv("CANVAS_URL")
header = {"Authorization": f"Bearer {token}"}

class ScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.checkboxes = []

        # Theme
        self.configure(
            scrollbar_button_color="#564D65",
            label_fg_color="#564D65",
            label_font = ("Courier", 18, "bold")
        )

        # Temp loading message
        self.loading_label = customtkinter.CTkLabel(self, text="Loading Assignments...")
        self.loading_label.grid(row=0, column=0, pady=20)

        # Start checkbox creation
        threading.Thread(target=self.data_fetcher, daemon=True).start()


    def data_fetcher(self):
         time.sleep(2)

         data = get_current_assignments()

         self.after(0, self.checkbox_creator, data)

    def checkbox_creator(self, data):
        self.loading_label.destroy()

        for row, i in enumerate(data):
                    text = f"{i.get('name')} - {i.get('course')} - {i.get('due_date')}"
                    checkbox = customtkinter.CTkCheckBox(self, text=text, corner_radius=11, hover_color="#564D65")
                    checkbox.original_text = text
                    checkbox.configure(command=lambda cb=checkbox: self.event(cb))
        
                    checkbox.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")
                    self.checkboxes.append(checkbox)
     

    def event(self, checkbox):
            if checkbox.get() == 1:
                checkbox.configure(text="Assignment Complete!", text_color="green")
            else:
                checkbox.configure(text=checkbox.original_text, text_color="white")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Canvas Helper")
        self.geometry("500x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(False,False)

        # Theme
        self.configure(
            fg_color="#D1D1D1"

        )

        # CheckBox Frame
        self.scrollable_checkbox_frame = ScrollableCheckboxFrame(self, title="Assignments")
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")

        # CheckBox Frame Theme
        # self.scrollable_checkbox_frame.configure(
        #      label_font=("Courier", 18, "bold")
        # )

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
    return assignments

# Main Function
def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
