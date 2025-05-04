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
from tkinter import filedialog
from datetime import datetime
from llm import llm_model
from threading import Thread
from resume_generator.two_column import server_start
import webbrowser #  Check for the main browser preferably chrome :: or firefox which ever is installed. 
from time import sleep 
from controllers import playwright_main



current_date  = datetime.today().date()
## App Constants: 
file_names  = []
current_status  = []
chat_data = {}
file_content  = []
chat_data['chat'] = []
chat_data['answer'] = []




def status_updater(text):
    log_box.configure(state='normal')
    log_box.delete("1.0", "end")

    current_status.append(log_box.get("1.0", "end"))
    # current_status.append("Starting the LLM model for automation.....")
    current_status.append(text)

    log_box.delete("1.0", "end")

    for each in current_status:
        log_box.insert("end", each + "\n")
    log_box.configure(state="disabled")



def llm_message():
    print("LLM Model Started......")
    # current_message  = prompt_box.get("1.0" , "end").strip()
    # prompt_box.delete("1.0" , "end")
    # chat_data['chat'].append(current_message)
    # pub.sendMessage("prompt_message" , prompt_message  = current_message)
    # # answer  = llm_model.single_chat(current_message , number_control=2048 , number_batch=512 , number_threads=12)
    # answer = llm_model.single_chat(current_message)
    # print(answer)
    # chat_data
    # status_updater("Entered Prompt :: " + current_message)
    # prompt_box.delete("1.0" , "end")
    # return "break"
    current_message = prompt_box.get("1.0", "end").strip()
    prompt_box.delete("1.0", "end")
    chat_data['chat'].append(current_message)
    # pub.sendMessage("prompt_message", prompt_message=current_message)



    if llm_model is None:
        status_updater("Model is still loading. Please wait...")
        return "break"

    answer = llm_model.single_chat(current_message)
    print(answer)
    status_updater("Entered Prompt :: " + current_message)
    status_updater("Result :: " + answer)
    return "break"


# def start_model_loading():
#     # server_start.start_node_server()  # To start the node server and then get the server open in one notepad : 
#     Thread(target=server_start.start_node_server, daemon=True).start()
#     sleep(100)
#     print("Server Started....")
#     # webbrowser.open("http://localhost:3000")
#     Thread(target=llm_message, daemon=True).start()

def start_model_loading():
    def model_loader():
        try:
            server_start.start_node_server()
            status_updater("Node server started.")
        except Exception as e:
            status_updater(f"Server Error: {e}")

    def delayed_llm_start():
        sleep(2)  # Light delay to avoid race
        llm_message()

    def playwright_working():
        sleep(1)
        playwright_main.main_working()


    Thread(target=model_loader, daemon=True).start()
    Thread(target=delayed_llm_start, daemon=True).start()
    Thread(target=playwright_working , daemon=True).start()



def file_reader():
    text  = llm_model.fileOpener()
    file_content.append(text)

def reset_function():
    file_content.clear()
    log_box.configure(state="normal") 
    log_box.delete("1.0" , "end")
    log_box.insert("1.0" , "Current Status......")


## laod the assets from the files : 
try:
    upload_image  = Image.open(r'assets\ui_images\upload_button.png')
    upload_image_clip = Image.open(r'assets\ui_images\upload_button_clip.png')
    restart_button_image = Image.open(r'assets\ui_images\restart.png')

    # Other Icons to laod ;
    pdf_image  = Image.open(r'assets\icons\pdf.png')


    upload_image = upload_image.resize((25 , 25))

except Exception as image_load_error: 
    print(f"Unable to load the Images : {image_load_error}")


# Get the imges for the button : 
upload_image = CTkImage(upload_image)
upload_image_clip  = CTkImage(upload_image_clip)
restart_button_image = CTkImage(restart_button_image)

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
enter_button = ctk.CTkButton(frame_3 , image=upload_image , text=""  , height=3 , width=3 , bg_color="black" , corner_radius=10 , command=start_model_loading)
mood_selector  = ctk.CTkComboBox(frame_3 , values=['Chat' , 'Resume' , 'Job Application' , 'Search' , 'General'] , width=200)
upload_file_button  = ctk.CTkButton(frame_3 , image=upload_image_clip , text="" , height=2 , width=2 , corner_radius=10 , command=file_reader)
restart_button = ctk.CTkButton(frame_3 , image=restart_button_image , text="" , height=2 , width=2 , corner_radius=10 , command=reset_function)


# Configure the Control : 
frame_1.pack_propagate(False)
frame_2.pack_propagate(False)
frame_3.pack_propagate(False)

prompt_box.insert("1.0", "Enter Prompt to Start.....")
log_box.insert("1.0" , "Current Status")
log_box.configure(state = "disabled")


# Bind the Controls : 
prompt_box.bind("<FocusIn>" , lambda x : prompt_box.delete("1.0" , "end"))
# prompt_box.bind("<FocusOut>" , lambda x:prompt_box.insert("1.0" , "Enter Prompt to start....."))
prompt_box.bind("<Shift-Return>", lambda enter: start_model_loading)


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
restart_button.place(x = 250 , y = 8)


if __name__ == '__main__':
    main_application.mainloop()