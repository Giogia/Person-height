from draw_lines import *
from vanishing_line import *
from camera_calibration import *

PATH = 'test.jpg'
OBJECT_HEIGHT = 80

# Read image
image = cv2.imread(PATH, 33)
image = remove_radial_distortion(image)

# Get Base object and Person
reference_object = get_lines(image, 1, "One Line for Base Object")
draw_line(image, reference_object, COLOUR_GREEN)

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
base_line = np.array([reference_object[0], person[0]], dtype=int)
draw_line(image, base_line, COLOUR_WHITE)

# Intersection of plane line with vanishing line
base_line_vanishing_point = intersection_point(base_line, vanishing_line)
draw_point(image, base_line_vanishing_point, COLOUR_GREEN)

# Project object on person from vanishing line
object_projection_line = np.array([reference_object[1], base_line_vanishing_point], dtype=int)
object_projection = intersection_point(person, object_projection_line)

# Line between object and person tops
top_line = np.array([reference_object[1], person[1]], dtype=int)
draw_line(image, top_line, COLOUR_WHITE)

# Person line parallel to object line
parallel_object_top = np.subtract(person[0], np.subtract(reference_object[0], reference_object[1]))
parallel_object = np.array([person[0], parallel_object_top])
parallel_person_top = intersection_point(top_line, parallel_object)
draw_point(image, parallel_person_top, COLOUR_BLUE)
parallel_person = np.array([parallel_person_top, person[0]])
draw_line(image, parallel_person, COLOUR_BLUE)

# Object projection on parallel person line
parallel_object_projection = intersection_point(parallel_person, object_projection_line)
draw_point(image, parallel_object_projection, COLOUR_GREEN)
object_height = np.array([parallel_object_projection, person[0]])
draw_line(image, object_height, COLOUR_GREEN)

# Compute ration between the two heights
person_height = OBJECT_HEIGHT * np.linalg.norm(person[0] - parallel_person_top) \
                / np.linalg.norm(person[0] - parallel_object_projection)
write_message(image, str(person_height))

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Image", image)

NAME = 'result.jpg'
cv2.imwrite(NAME, image)
print("Image saved with name: " + NAME)

cv2.waitKey()
cv2.destroyAllWindows()
