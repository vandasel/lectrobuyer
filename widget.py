import customtkinter as ctk
import re
from main import ElectroImporter

ctk.set_appearance_mode("dark")

def button_callback():
    input_text = text.get("1.0", "end-1c")  
    print(ElectroImporter(url=input_text).run())
    


app = ctk.CTk()
app.geometry("400x600")
app.title("URL")


text = ctk.CTkTextbox(app, width=300, height=200)
text.pack(padx=20, pady=20)


button = ctk.CTkButton(app, text="Add item", command=button_callback)
button.pack(padx=20, pady=20)


app.mainloop()
