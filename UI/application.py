import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


from pubsub import pub  # For Message Passing

from ttkbootstrap.toast import ToastNotification # For the toast notification. 





ctk.set_appearance_mode('dark')
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
frame_1  = ctk.CTkFrame(main_application , width=width   , height=height // 1.9 ,  corner_radius=1  , fg_color="red")
frame_2 = ctk.CTkFrame(main_application , width=width , height= height // 2.5 , corner_radius=1 , fg_color="white")
frame_3 = ctk.CTkFrame(main_application , width= width , height= height // 12 , corner_radius=1 , fg_color="green")

log_box  = ctk.CTkTextbox(frame_1 , height=height  // 1.9 , width=width , corner_radius=0 )
prompt_box  = ctk.CTkTextbox(frame_2 , height=height // 2.5 , width=width  , corner_radius= 0  )

# Configure the Control : 
frame_1.pack_propagate(False)
frame_2.pack_propagate(False)
frame_3.pack_propagate(False)
log_box.configure(state = "disabled")
prompt_box.insert("1.0", "Please Enter Prompt.....")


# Bind the Controls : 
prompt_box.bind("<FocusIn>" , lambda x : prompt_box.delete("1.0" , "end"))



# Pack the controls : 
frame_1.pack()
frame_2.pack()
frame_3.pack()

log_box.pack()
prompt_box.pack()




# Call the main application 
main_application.mainloop()