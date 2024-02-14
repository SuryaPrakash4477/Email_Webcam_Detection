import os
import cv2
import time
from email_ import send_email
import glob
from threading import Thread # To create thread class

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 0

def clean_folder():
    print("clean_folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended")


while True:
    status = 0
    check, frame = video.read()

    # Preprocessing the frames
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    # To make calculation efficient is we used guassian blur method
    # Tuple is the amount of blurness and providing standard deviation
    gray_frame_gua = cv2.GaussianBlur(gray_frame, (21, 21), 0) 

    # Making differences between preprocessed frames
    if first_frame is None:
        first_frame = gray_frame_gua
    
    delta_frame = cv2.absdiff(first_frame, gray_frame_gua)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # To remove noise
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    # To find the contours
    contours, check = cv2.findContours(dil_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y,), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            # To write Image
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]



    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:

        #Preparing the Thread
        email_thread = Thread(target = send_email, args = (image_with_object, )) #To parse this argument in send_email function which asign to target 
        email_thread.daemon = True #This line should allow the send_email function to execute in the BG
        clean_thread = Thread(target = clean_folder)
        clean_thread.daemon = True

        #Making andExecuting the thraed
        email_thread.start()
        clean_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()

# Wait until the user presses 'q' or closes the window
clean_thread.start()