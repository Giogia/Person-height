from draw_lines import *
from vanishing_line import *
from camera_calibration import *

PATH = 'test.jpg'
OBJECT_HEIGHT = 80

# Read image
image = cv2.imread(PATH, 33)
image = remove_radial_distortion(image)

# Get Base object and Person
base_object = get_lines(image, 1, "One Line for Base Object")
draw_line(image, base_object, COLOUR_GREEN)

person = get_lines(image, 1, "One Line for Person")
draw_line(image, person, COLOUR_BLUE)

# Get lines for plane vanishing line
vanishing_line = []
for i in range(2):
    horizontal_lines = get_lines(image, 2, "Two plane lines")
    horizontal_vanishing_point = intersection_point(horizontal_lines[0], horizontal_lines[1])

    while vanishing_line is None:
        horizontal_lines = get_lines(image, 2, "Two More Lines, Those were Parallel")
        horizontal_vanishing_point = intersection_point(horizontal_lines[0], horizontal_lines[1])

    vanishing_line.append(horizontal_vanishing_point)

vanishing_line = np.asarray(vanishing_line, dtype=int)
draw_line(image, vanishing_line, COLOUR_WHITE)

# Line between object and person bottoms
plane_line = np.array([base_object[0], person[0]], dtype=int)
draw_line(image, plane_line, COLOUR_WHITE)

# Intersection of plane line with vanishing line
vanishing_line_intersection = intersection_point(plane_line, vanishing_line)
draw_point(image, vanishing_line_intersection, COLOUR_GREEN)

# Project object on person from vanishing line
object_projection = np.array([base_object[1], vanishing_line_intersection], dtype=int)
object_height = intersection_point(person, object_projection)

# Line between object and person tops
top_line = np.array([base_object[1], person[1]], dtype=int)
draw_line(image, top_line, COLOUR_WHITE)

# Person line parallel to object line
parallel_person_top = np.subtract(person[0], np.subtract(base_object[0], base_object[1]))
parallel_person = np.array([person[0], parallel_person_top])
person_height_point = intersection_point(top_line, parallel_person)
draw_point(image, person_height_point, COLOUR_BLUE)
person_height_line = np.array([person_height_point, person[0]])
draw_line(image, person_height_line, COLOUR_BLUE)

# Object projection on parallel person line
parallel_object_height = intersection_point(parallel_person, object_projection)
draw_point(image, parallel_object_height, COLOUR_GREEN)
parallel_object_line = np.array([parallel_object_height, person[0]])
draw_line(image, parallel_object_line, COLOUR_GREEN)

# Compute ration between the two heights
person_height = OBJECT_HEIGHT * np.linalg.norm(person[0] - person_height_point) \
                / np.linalg.norm(person[0] - parallel_object_height)
write_message(image, str(person_height))

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Image", image)

NAME = 'result.jpg'
cv2.imwrite(NAME, image)
print("Image saved with name: " + NAME)

cv2.waitKey()
cv2.destroyAllWindows()
