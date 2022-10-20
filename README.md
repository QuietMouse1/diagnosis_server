# Diagnosis folder 

Python script to start a simple server to serve and automatically generate latest report/images from the logs folder. The logs folder contains .csv values such as position, cpu usage, ram usage, etc.
# Bugs 

- Creating an new folder inside Logs/Mavroslogs and pressing generate latest logs (there is no check to see if files exist when generating images and report)
- Needs python3

flask run --host=0.0.0.0

# Server images

Main landing page

![](/img/main_page.png)

Inside the report page, there are images of the graphs that is generated from the .csv files

![](/img/report_page.png)