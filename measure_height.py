from draw_lines import *
from utils import *
from vanishing_line import *

PATH = 'img1.jpg'

# Read image
image = read_image(PATH)

# Get lines for plane vanishing line
horizontal_vanishing_points = []

for i in range (2):
    horizontal_lines = get_lines(image, 2)
    horizontal_vanishing_point = intersection_point(horizontal_lines[0], horizontal_lines[1])
    horizontal_vanishing_points.append(horizontal_vanishing_point)
    draw_vanishing_point(image, horizontal_vanishing_point)

draw_vanishing_line(image,horizontal_vanishing_points)

# Get lines for vertical vanishing point
vertical_lines = get_lines(image, 2)
vertical_vanishing_point = intersection_point(vertical_lines[0], vertical_lines[1])
draw_vanishing_point(image, vertical_vanishing_point)

cv2.waitKey()
