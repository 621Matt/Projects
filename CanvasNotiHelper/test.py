import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Canvas Helper")
        self.geometry("518x293")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,10), weight=1)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="a")
        self.checkbox_1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")



# test
# app = customtkinter.CTk()
# app.title("Canvas Helper")
# app.geometry("518x293")
# app.grid_columnconfigure((0,1), weight=1)
# app.grid_rowconfigure((0,10), weight=1)

# a = 10

# checkbox_1 = customtkinter.CTkCheckBox(app, text=f"{a}")
# checkbox_1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="ew")
# checkbox_2 = customtkinter.CTkCheckBox(app, text="checkbox 2")
# checkbox_2.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")


app = App()
app.mainloop()