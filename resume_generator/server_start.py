import os
import subprocess



project_path = r"C:\Users\vinay\Desktop\resume_maker_node_twocolumn"

os.chdir(project_path)
subprocess.run("npm start", shell=True)
