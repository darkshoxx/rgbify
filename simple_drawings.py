from PIL import Image
import os
import math

HERE = os.path.abspath(os.path.dirname(__file__))
RES_FILE = os.path.join(HERE, "my_circle.png")
CIRCLE_FOLDER = os.path.join(HERE, "Circle")

circle_source_height = 627
radius = math.ceil(circle_source_height / 2)
image_width = 1920
image_height = 1080
my_circle = Image.new("RGBA", (image_width, image_height))
pixels = my_circle.load()

center_y = image_width / 2
center_x = image_height / 2

density = 10000 # number of divisions of the unit interval
thickness = 1
start = 0
end = 2*math.pi
divisions = [start + (step/density)*end for step in range(density+1)]

def interval_to_circle(division):
    return round(radius*math.cos(division) + center_x), round(radius*math.sin(division) + center_y)

def test_segment(division):
    for segment in range(6):
        if segment*end/6 <= division < (segment+1)*end/6:
            return segment, division - segment
    return 5, division - 5


number_of_shifts = 100
shift_indices = range(number_of_shifts)


for shift_index in shift_indices:
    shift = 2*math.pi*shift_index/number_of_shifts

    for division in divisions:
        segment, remainder = test_segment(division)
        # remainder is path from 0 to pi/3
        div_x, div_y = interval_to_circle((division + shift) % (2*math.pi))
        alpha = 255
        percentage = remainder/(math.pi/3)
        # percentage = percentage + shift % 1
        progression = round(255*percentage)
        if segment == 0:
            r_val = progression
            g_val = 0
            b_val = 255
        elif segment == 1:
            r_val = 255
            g_val = 0
            b_val = 255 - progression
        elif segment == 2:
            r_val = 255
            g_val = progression
            b_val = 0
        elif segment == 3:
            r_val = 255 - progression
            g_val = 255
            b_val = 0
        elif segment == 4:
            r_val = 0
            g_val = 255
            b_val = progression
        else:
            r_val = 0
            g_val = 255 - progression
            b_val = 255    
        for i in range(-thickness, thickness+1):
            for j in range(-thickness, thickness+1):
                if abs(i) + abs(j) <= thickness:
                    pixels[div_y + i,div_x+ j] = (r_val,g_val,b_val,alpha)
    my_circle.save(os.path.join(CIRCLE_FOLDER, f"Circle_{shift_index}.png"))

