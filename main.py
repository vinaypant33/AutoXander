# Libraries Import  :
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import ttkbootstrap as btk
from pubsub import pub
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap import tooltip
from PIL import Image
from customtkinter import CTkImage




# Import Scripts : 






def llm_message():
    current_message  = prompt_box.get("1.0" , "end")
    prompt_box.delete("1.0" , "end")
    pub.sendMessage("prompt_message" , prompt_message  = current_message)
    return "break"


## laod the assets from the files : 
try:
    upload_image  = Image.open(r'assets\ui_images\upload_button.png')
    upload_image_clip = Image.open(r'assets\ui_images\upload_button_clip.png')

    upload_image = upload_image.resize((25 , 25))
except Exception as image_load_error: 
    print(f"Unable to load the Images : {image_load_error}")


# Get the imges for the button : 
upload_image = CTkImage(upload_image)
upload_image_clip  = CTkImage(upload_image_clip)





ctk.set_appearance_mode('dark')
# ctk.set_default_color_theme('green')
main_application  = ctk.CTk()
main_application.title("AutoXander")

# Configure the application for the main application  : 
window_height  = main_application.winfo_screenheight()
window_width  = main_application.winfo_screenwidth()

width  = 700
height  = 400

x_location  = (window_width // 2) - (width // 2)
y_location  = (window_height // 2) - (height // 2)

main_application.geometry(f"{width}x{height}+{x_location}+{y_location}")
main_application.resizable(0 , 0)




# Boxes for the controls : 
frame_1  = ctk.CTkFrame(main_application , width=width   , height=height // 2 ,  corner_radius=1  )
frame_2 = ctk.CTkFrame(main_application , width=width , height= height // 2.6 , corner_radius=1 )
frame_3 = ctk.CTkFrame(main_application , width= width , height= height // 3 , corner_radius=1 )

log_box  = ctk.CTkTextbox(frame_1 , height=height  // 1.9 , width=width , corner_radius=0 )
divider = ctk.CTkFrame(main_application , height=2 , width=width , fg_color="white")
prompt_box  = ctk.CTkTextbox(frame_2 , height=height // 2.5 , width=width  , corner_radius= 0)
enter_button = ctk.CTkButton(frame_3 , image=upload_image , text=""  , height=3 , width=3 , bg_color="black" , corner_radius=10)
mood_selector  = ctk.CTkComboBox(frame_3 , values=['Chat' , 'Resume' , 'Job Application' , 'Search' , 'General'] , width=200)
upload_file_button  = ctk.CTkButton(frame_3 , image=upload_image_clip , text="" , height=2 , width=2 , corner_radius=10)


# Configure the Control : 
frame_1.pack_propagate(False)
frame_2.pack_propagate(False)
frame_3.pack_propagate(False)

prompt_box.insert("1.0", "Enter Prompt to Start.....")
log_box.insert("1.0" , "Current Status...........")
log_box.configure(state = "disabled")



# Bind the Controls : 
prompt_box.bind("<FocusIn>" , lambda x : prompt_box.delete("1.0" , "end"))
# prompt_box.bind("<FocusOut>" , lambda x:prompt_box.insert("1.0" , "Enter Prompt to start....."))
prompt_box.bind("<Shift-Return>", lambda event: llm_message())



# Pack the controls : 
frame_1.pack(pady = (0 , 1))
divider.pack()
frame_2.pack(pady = (1 , 0))
frame_3.pack()

log_box.pack()
prompt_box.pack()


enter_button.place(x = 4 , y = 8)
mood_selector.place(x = 40 , y = 8)
upload_file_button.place(x = 660 , y = 8)









if __name__ == '__main__':
    main_application.mainloop()