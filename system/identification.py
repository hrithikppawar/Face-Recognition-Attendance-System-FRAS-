import cv2
import os
import numpy as np
import PIL
import face_recognition as fr
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_dir = os.path.join(BASE_DIR, 'static/images/profile_picture')

#This function returns the dictionary of image file name and corresponding face encoding
def encoded_profile_pictures():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_dir = os.path.join(BASE_DIR, 'static/images/profile_picture')

    encoded_photos = {}
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            path = os.path.join(root, file)
            image = fr.load_image_file(path)
            if len(fr.face_encodings(image)) == 0:
                continue
            image_encoded = fr.face_encodings(image)[0]
            encoded_photos[file] = image_encoded
    return encoded_photos
        
dictionary = encoded_profile_pictures()

img='hrithik.jpg'

def most_frequent(List): 
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num

def check_for_match(dictionary, frame):
    # Resize the frame to the 1/4 th size for faster face recognition processing
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    # Convert the image from BGR color to RGB color
    rgb_small_frame = small_frame[:, :, ::-1]

    # find all the faces and face encodings in the frame
    face_locations = fr.face_locations(rgb_small_frame)
    face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

    known_name = list(dictionary.keys())
    known_name_encoding = list(dictionary.values())
    identified_names = []
    for face_encoding in face_encodings:
        # see if face is a match for known faces
        matches = fr.compare_faces(known_name_encoding, face_encoding)
        name = 'Unknown'

        face_distance = fr.face_distance(known_name_encoding, face_encoding)
        best_match_index = np.argmin(face_distance)
        if matches[best_match_index]:
            name = known_name[best_match_index]
            
        #t = datetime.datetime.now().strftime("%H:%M:%S")
        identified_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, identified_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Now return the list of name of person appeared in the frame.
    return identified_names

def start_detection():
    video_capture = cv2.VideoCapture(0)
    attendance = {}
    while True:
        match = []
        for i in range(30):
            ret, frame = video_capture.read()

            x = check_for_match(dictionary, frame)

            match.append(x)
            #for key in x.keys():
            #    if not key in match:
            #        match[key] = x[key]
                
            cv2.imshow('Press "Q" to stop Attendance', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        else:
            name = most_frequent(match)
            for person in name:
                person = person.replace('.jpg', '')
                if not person in attendance.keys():
                    attendance[person] = datetime.datetime.now().strftime("%H:%M:%S") 
            print(attendance)
            continue
        break
    video_capture.release()
    cv2.destroyAllWindows()
    return attendance

#attendance=start_detection()
#print('attendance=', attendance)



    
