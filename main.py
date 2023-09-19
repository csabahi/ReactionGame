import cv2
import math
import random
import pickle
import time
from cvzone.HandTrackingModule import HandDetector

width = 1080
height = 760
hand_radius = 40
target_radius = 40  
border_size = 15  
hit_target=False
target_count = 0
t_start = time.time()
time_array = []



class Circle:

    def __init__(self, coordinates, radius, color, thickness):
        self.coordinates=  coordinates
        self.radius = radius
        self.color = color
        self.thickness = thickness

    def draw( self, _frame):
        cv2.circle(_frame, self.coordinates, self.radius, self.color, self.thickness)

    def check_intersections(self, other_coordinates, other_radius): 

        distance = math.sqrt(math.pow(other_coordinates[0] - self.coordinates[0], 2) 
                    + math.pow(other_coordinates[1] - self.coordinates[1], 2))
        if distance <= self.radius + other_radius: 
            return True
        else: 
            return False  

def create_random_target(current_target_pos=[]):
    if current_target_pos:
        possible_x = []

        x_limit = [target_radius + border_size + 20, width - target_radius - border_size - 15]
        y_limit = [target_radius + border_size + 20, height - target_radius - border_size - 15]

        for i in range(x_limit[0], x_limit[1]):
            if i + 200 < current_target_pos[0] or i - 200 > current_target_pos[0]:
                possible_x.append(i)

        possible_y = []
        for i in range(y_limit[0], y_limit[1]):
            if i + 200 < current_target_pos[1] or i - 200 > current_target_pos[1]:
                possible_y.append(i)

        if not possible_x:
            possible_x = range(x_limit[0], x_limit[1])

        if not possible_y:
            possible_y = range(y_limit[0], y_limit[1])

    else:
        possible_x = range(target_radius + border_size, width - target_radius - border_size)
        possible_y = range(target_radius + border_size, height - target_radius - border_size)
    # pick a random coordinate
    random_x = random.choice(possible_x)
    random_y = random.choice(possible_y)
    # pick a random color
    random_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 256)]
    _target = Circle([random_x, random_y], target_radius, random_color, -1)

    return _target



target = create_random_target()

cap = cv2.VideoCapture(0)  # Use 0 for the default camera
# Set the frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = HandDetector(detectionCon=0.2, maxHands=2)
target = Circle((int(width/2), int(height/2)), 50, (0, 0, 255), -1)


##This while statement is for the general hand tracking
while True:
    elapsed_time = time.time() - t_start
    frame = cap.read()[1]  # Read the frame directly, without using ret

    hands, frame = detector.findHands(frame, flipType=True)
    # frame = cv2.flip(frame, 1)

    cv2.imshow("Reaction Game", frame)

    target.draw(frame)

    hands = detector.findHands(frame, flipType=True, draw=False)

    if hands:
        for i in range(len(hands)):
            hand_position = hands[i]["center"]
            hand_circle = Circle(hand_position, hand_radius, (0, 0, 0), -1)
            
            if target.check_intersections(hand_circle.coordinates, hand_circle.radius): 
                hit_target = True
                hand_circle.color = (0, 255, 0)
                print("hit a target")
                time_array.append(elapsed_time)
                # print(time_array)
    
            else: 

                hand_circle.color = (0,0,255)
        
            hand_circle.draw(frame)

    if hit_target:
        target_count += 1
        if target_count == 5:
            with open('output.txt', 'w') as file: 
                for time in time_array: 
                    file.write(str(time) + '\n')
          
        # print("count =", target_count)
        target = create_random_target(target.coordinates)
        print(target.coordinates)
        hit_target = False
    
    target.draw(frame)

    cv2.imshow("Reaction Game", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break