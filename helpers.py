# Original Author: Daniel park
# Date: 7.12.21
# Desc: Helper functions used in processing main and camera

from datetime import datetime

def mark_attendance(person_name):
    """
    Write the person's name down in the attendance sheet when identified on webcam
    
    Args:
        (String) person_name: person's name
    
    Returns:
        N/A
    """
    with open("attendance_sheet.csv", "r+") as sheet:
        current_data_list = sheet.readlines()
        name_list = []
        
        # Create a new entry
        for line in current_data_list:
            entry = line.split(",")
            name_list.append(entry[0])
            
        # If person detected is not in the attendance sheet, mark them in the sheet
        if person_name not in name_list:
            time_now = datetime.now()
            date = time_now.strftime("%x")
            time = time_now.strftime("%H:%M:%S")
            sheet.writelines(f"\n{person_name},{date},{time}")
