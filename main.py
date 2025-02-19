import customtkinter as ctk
import pystray
import sqlite3
import threading
import time
from dbhandler import DbHandler
from main import ElectroImporter  
from PIL import Image
from plyer import notification  
from pystray import MenuItem as item, Icon


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  
WIDTH, HEIGHT = 800, 400

class Widget(ctk.CTk):


    def __init__(self):
        super().__init__()
        self.title("Electrobuyer")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.grid_columnconfigure(0, weight=1)  
        
        self.fields = [] 

     
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

     
        self.add_button = ctk.CTkButton(self, text="+", command=self.add_text_field)
        self.add_button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        
     
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.start_submit_thread)
        self.submit_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.load_previous_data()

    def load_previous_data(self):
        db = DbHandler()
        previous_entries = db.get_last_price()
        db.close()
        
        for _, link, status, price in previous_entries:

            text_color = "red" if status == "Above Threshold" else "green" if status == "Below Threshold" else "gray"
            
            self.add_text_field(link, status, price, text_color)


    def add_text_field(self, link="", status="NA", price="0", text_color="gray"):
        field_frame = ctk.CTkFrame(self.input_frame)
        field_frame.grid(row=len(self.fields), column=0, padx=10, pady=5, sticky="ew")

        text_var = ctk.StringVar(value=link)  
        text_field = ctk.CTkEntry(field_frame, textvariable=text_var, width=400)
        text_field.grid(row=0, column=0, padx=5, pady=5)

        status_label = ctk.CTkLabel(field_frame, text=status, text_color=text_color, width=100)
        status_label.grid(row=0, column=1, padx=5, pady=5)

        delete_button = ctk.CTkButton(field_frame, text="Delete", 
                                    command=lambda: self.delete_field(field_frame))
        delete_button.grid(row=0, column=2, padx=5, pady=5)

        price_var = ctk.StringVar(value=str(price))
        price_field = ctk.CTkEntry(field_frame, textvariable=price_var, width=50)
        price_field.grid(row=0, column=3, padx=5, pady=5)

        self.fields.append((field_frame, text_var, status_label, price_field))

    def delete_field(self, field_frame):
        for i, (frame, link, _,price) in enumerate(self.fields):
            if frame == field_frame:
                frame.destroy() 
                del self.fields[i]
                DbHandler().delete(link=link.get())
                break

       
        self.reorganize_fields()
    
    def reorganize_fields(self):
        for i, (frame, _, _,_) in enumerate(self.fields):
            frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
    
    def start_submit_thread(self):
        threading.Thread(target=self.submit, daemon=True).start()

    def submit(self):
        for i, (_, text_var, status_label,price_w) in enumerate(self.fields):
            link = text_var.get()  
            try:
                start = time.time()
                price = ElectroImporter(link).run()  
                end = time.time()
                print(end-start)
                if price < float(price_w.get()):
                    status_label.configure(text="Below Threshold", text_color="green")
                    self.show_notification(f"ALERT ALERT ALERT", f"{link} = {price}!!!!")
                else:
                    status_label.configure(text="Above Threshold", text_color="red")
                
                DbHandler().input_price(link=link,status=status_label._text, price=price_w.get())
            except Exception as e:
                status_label.configure(text="Error", text_color="orange")
                print(f"Error fetching price for {link}: {e}")
    
    def auto_check_prices(self):
        while True:
            time.sleep(1200) 
            self.submit()

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )

    def hide_window(self):
        self.withdraw()  
        self.create_tray_icon()

    def create_tray_icon(self):
        def restore_app(icon):
            self.deiconify() 
            icon.stop()  

        def exit_app(icon):
            icon.stop() 
            self.quit()  

        icon_image = Image.open("icon.PNG")

        menu = (item("Restore", restore_app), item("Exit", exit_app))
        self.tray_icon = Icon("Electrobuyer", icon_image, "Electrobuyer", menu)

        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
if __name__ == "__main__":
    app = Widget()
    app.mainloop()
