import numpy as np
import cv2
import time

line = False
N = 0
COLOUR = (100, 100, 255)


def get_points(im, number_of_lines):

    # Set up data to send to mouse handler
    data = {'image': im, 'number_of_lines': number_of_lines, 'lines': []}

    # Set the callback function for any mouse event
    cv2.imshow("Image", im)
    cv2.setMouseCallback("Image", mouse_handler, data)

    # Wait
    while N < number_of_lines:
        cv2.waitKey(1)
    time.sleep(1)

    # Convert array to np.array in shape n,2,2
    points = np.uint8(data['lines'])

    return points, data['image']


def mouse_handler(event, x, y, flags, data):

    global line, N

    if event == cv2.EVENT_LBUTTONDOWN and len(data['lines']) < data['number_of_lines']:
        # Draw the first Point
        line = True
        data['lines'].insert(0, [(x, y)])  # prepend the point
        cv2.circle(data['image'], (x, y), 2, COLOUR, 5, 16)
        cv2.imshow("Image", data['image'])

    elif event == cv2.EVENT_MOUSEMOVE and line:
        # thi is just for a ine visualization
        image = data['image'].copy()
        cv2.line(image, data['lines'][0][0], (x, y), COLOUR, 1)
        cv2.imshow("Image", image)

    elif event == cv2.EVENT_LBUTTONDOWN and line:
        line = False
        data['lines'][0].append((x, y))  # append the second point
        cv2.circle(data['image'], (x, y), 2, COLOUR, 5)
        cv2.line(data['image'], data['lines'][0][0], data['lines'][0][1], COLOUR, 2)
        cv2.imshow("Image", data['image'])
        N += 1


# Running the code
img = cv2.imread('image.jpg')
pts, final_image = get_points(img, 2)
print(pts)
