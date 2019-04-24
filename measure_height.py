from draw_lines import *
from vanishing_line import *

PATH = 'image.png'
OBJECT_HEIGHT = 1

# Read image
image = cv2.imread(PATH)

# Get Base object and Person

object = get_lines(image, 1, "One Line for Base Object")
draw_line(image, object, COLOUR_RED)
person = get_lines(image, 1, "One Line for Person")
draw_line(image, person, COLOUR_RED)
# Get lines for plane vanishing line
vanishing_line = []

for i in range(2):
    horizontal_lines = get_lines(image, 2, "Two plane lines")
    horizontal_vanishing_point = intersection_point(horizontal_lines[0], horizontal_lines[1])

    while vanishing_line is None:
        horizontal_lines = get_lines(image, 2, "Two More Lines, Those were Parallel")
        horizontal_vanishing_point = intersection_point(horizontal_lines[0], horizontal_lines[1])

    vanishing_line.append(horizontal_vanishing_point)
    draw_point(image, horizontal_vanishing_point)

vanishing_line = np.asarray(vanishing_line, dtype=int)
draw_line(image, vanishing_line)

#vertical_vanishing_point = intersection_point(object, person)
# Get lines for vertical vanishing point
#vertical_lines = get_lines(image, 2, "Two Vertical Lines")
#vertical_vanishing_point = intersection_point(vertical_lines[0], vertical_lines[1])

#while vertical_vanishing_point is None:
  #  vertical_lines = get_lines(image, 2, "Two More Lines, Those were Parallel")
  #  vertical_vanishing_point = intersection_point(vertical_lines[0], vertical_lines[1])
#draw_point(image, vertical_vanishing_point)

plane_line = np.array([object[0], person[0]], dtype=int)
draw_line(image, plane_line, COLOUR_BLUE)

vanishing_line_intersection = intersection_point(plane_line, vanishing_line)
draw_point(image, vanishing_line_intersection)

object_projection = np.array([object[1], vanishing_line_intersection], dtype=int)
#draw_line(image, object_projection, COLOUR_BLUE)

object_height = intersection_point(person, object_projection)
#draw_point(image, object_height)

# Line linking the top of the object and the person
top_line = np.array([object[1], person[1]], dtype=int)

parallel_person_top = np.subtract(person[0], np.subtract(object[0], object[1]))
parallel_person = np.array([person[0], parallel_person_top])
person_height_point = intersection_point(top_line, parallel_person)
person_height_line = np.array([person_height_point, person[0]])
draw_line(image, person_height_line, COLOUR_BLUE)

parallel_object_height = intersection_point(parallel_person, object_projection)
draw_point(image, parallel_object_height)

parallel_object_line = np.array([parallel_object_height, person[0]])
draw_line(image, parallel_object_line, COLOUR_GREEN)

person_height = OBJECT_HEIGHT * np.linalg.norm(person[0] - person_height_point) \
                / np.linalg.norm(person[0] - parallel_object_height)
write_message(image, str(person_height))

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Image", image)

cv2.waitKey()
cv2.destroyAllWindows()
