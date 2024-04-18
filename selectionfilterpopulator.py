#############################################################
###### Infinite Campus Selection Filter Populator ###########
###### Created By: C. Eide, Tech Integrator       ###########
###### Trumbull Public Schools, Trumbull, CT      ###########
###### Direct Inquiries to: ceide@trumbullps.org  ###########
#############################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv, os

# GLOBAL CONSTANTS (CONFIG)
DISTRICTICLOGINURL = "https://trumbullct.infinitecampus.org/campus/trumbull.jsp" # URL for District's IC Login Page
DEFAULTCOLUMNNAME = "student_studentNumber"

script_dir = os.path.dirname(__file__)

# create the driver, navigate to IC, and wait for the user to get to the correct screen
driver = webdriver.Chrome()
driver.get(DISTRICTICLOGINURL)

loop = True
while (loop):

     # prompt user for filename
    valid = False
    while not valid:
        filename = input("Please type the filename you wish to use: ")
        if not '.' in filename:
            print("INVALID FILENAME! Please enter a filename with extension")
            continue
        if filename.rsplit('.', 1)[1] != 'csv':
            print("INVALID INPUT! Please enter a CSV file")
            continue
        if not os.path.exists(script_dir + "/" + filename):
            print("FILE NOT FOUND! Please try again")
            continue
        valid = True
    
    columnname = input("Please type the column name containing student numbers (Press Enter for IC Default): ")
    if columnname == "":
        columnname = DEFAULTCOLUMNNAME
        
    # wait for user to be ready to populate
    input("Press Enter To Select Values")

    # holder for student numbers from CSV file
    studentstoselect = []

    # load up the CSV values
    try:
        with open(script_dir + '/' + filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                print(row[columnname])
                studentstoselect.append(row[columnname])
    except:
        print("ERROR: Could not open file.  Please check filename and ensure it's in the proper location.\n")
        continue

    try:
        #shift view to iFrame and locate <select> element
        driver.switch_to.default_content()
        frame = driver.find_element(By.ID, "frameWorkspace")
        driver.switch_to.frame(frame)
        studentListSelect = Select(driver.find_element(By.ID, "allListID"))

        # find the button used to move values to right
        movebutton = driver.find_element(By.ID, "addSelection")

        # iterate through options and select ones in the list of students, then move them to the right
        for option in studentListSelect.options:

            optionStudentNumber = option.text.split('#',1)[1]
            print("Option Student Number: " + optionStudentNumber)

            if(optionStudentNumber in studentstoselect):
                option.click()
                movebutton.click()
    except:
        print("ERROR: Please ensure you are at the proper screen!\n")
        continue
    
    loopinput = input("Would you like to try again? (Y/N)")
    if (loopinput == 'N'):
        loop = False

print("Script Execution Complete")
driver.quit()