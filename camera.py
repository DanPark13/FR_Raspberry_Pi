# Original Author: smartbuilds.io
# Modified: Daniel Park
# Date: 7.12.21
# Desc: This scrtipt is running a face recongition of a live webcam stream.

import face_recognition
import cv2
import numpy as np
import os
import re
from datetime import datetime
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

# Store objects in array
known_person=[] # List of name of people
known_image=[] # Image object
known_face_encodings=[] # Encoding object

# Initialize some variables
face_locations = [] # Face locations Coordinates
face_encodings = [] # Face Encodings
face_names = [] # Face Associated with Name
process_this_frame = True

# Add images to the folder
for file in os.listdir("picture_ids"):
    try:
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("picture_ids/", file)
        known_image = face_recognition.load_image_file(file)
        known_face_encodings.append(face_recognition.face_encodings(known_image)[0])

    except Exception as e:
        pass

print(known_person)

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


# Create Video Camera Object to open camera and detect faces
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        process_this_frame = True

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

       # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            global name_gui, code_gui;
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                print(matches)

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_person[best_match_index]
                
                name_code = name.split("_")
                full_name = re.sub("([A-Z])"," \\1", name_code[0]).strip()
                code = "N/A"
                print(name_code)
                
                if(name!="Unknown"):
                    code = name_code[1]
                
                face_names.append(name)
        
                name_gui = full_name
                code_gui = code

        process_this_frame = not process_this_frame
            
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with a name and code below the face
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, f"Name: {name_gui}", (left + 10, bottom - 10), font, 1, (0, 0, 0), 1)
            cv2.putText(image, f"Code: {code_gui}", (left + 10, bottom + 20), font, 1, (0, 0, 0), 1)
            
            mark_attendance(name_gui)


        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
