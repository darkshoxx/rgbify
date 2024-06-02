import os
from PIL import Image
import math
import numpy as np
HERE = os.path.abspath(os.path.dirname(__file__))
SOURCE_FOLDER = os.path.join(HERE, "SourceImages")
FINAL_FOLDER = os.path.join(HERE, "FinalImages")

TEST_FILE = os.path.join(SOURCE_FOLDER, "myst123.bmp")
TEST_OUTPUT = os.path.join(FINAL_FOLDER, "ColourOutput.bmp")

num_tol = 0.00001

testim = Image.open(TEST_FILE)

def maxer(value:float):
    return max(0,value)

def minner(value:float):
    return min(255,value)

def dimmer(pixel, shift = 70):
    r,g,b,a = pixel
    return (maxer(r-shift), maxer( g-shift), maxer(b-shift), a)

def get_matrix(angle:float=None):
    if angle is None:
         angle = 0 # math.pi*2
    u = 1/math.sqrt(3)
    usq = 1/3
    cosa = math.cos(angle)
    acosa = 1 - cosa
    sina = math.sin(angle)
    # m11 = cosa + usq*acosa
    # m12 = usq*acosa - u*sina
    # m13 = usq*acosa + u*sina
    # m21 = usq*acosa + u*sina
    # m22 = cosa + usq*acosa
    # m23 = usq*acosa - u*sina
    # m31 = usq*acosa - u*sina
    # m32 = usq*acosa + u*sina
    # m33 = cosa + usq*acosa

    diff = usq*acosa - u*sina
    summ = usq*acosa + u*sina
    other = cosa + usq*acosa

    rot_matrix = np.matrix([[other, diff, summ], [summ, other, diff], [diff, summ, other]])
    return rot_matrix

def extract_data_from_point(point:list):
    # find height h
    h = sum(point)/3
    H = [h, h, h]
    if np.linalg.norm(point-H) < num_tol:
        return 0, h
    # define A and its length L
    A = point - H
    L = np.linalg.norm(A)
    # define C = H + c*A
    # find intersections
    one_part = [(1-h)/(p_part-h) for p_part in point if abs(p_part-h)>num_tol]
    zero_part = [(-h)/(p_part-h) for p_part in point if abs(p_part-h)>num_tol]
    intersection_candidates = one_part + zero_part
    # determine correct intersection B
    sorted_candidates = sorted(intersection_candidates)
    c = None
    for candidate in sorted_candidates:
        c = candidate
        if candidate > 0:
            break
    t = c / L

    # find percentage t
    return t, h

def transform_point(point, t, h, rot_mat):
    # 0. rule out h:
    H = [h, h, h]
    if np.linalg.norm(point-H) < num_tol:
        return H
    # 1. rotate point p to q
    q = np.matmul(rot_mat,point)
    # 2. determine intersection of r*q with six planes
    one_part = [(1-h)/(p_part-h) for p_part in np.nditer(q) if abs(p_part-h)>num_tol]
    zero_part = [(-h)/(p_part-h) for p_part in np.nditer(q) if abs(p_part-h)>num_tol]
    intersection_candidates = one_part + zero_part
    sorted_candidates = sorted(intersection_candidates)
    candidate = None
    for candidate in sorted_candidates:
        if candidate > 0:
            break
    # 3. scale q up by factor of t
    L_2 = np.linalg.norm(H + candidate*(q-H))
    r = (t*L_2)**2 / np.linalg.norm(q-H)
    # 4. return or set point = q
    return_values = [None, None, None]
    for index, value in enumerate(np.nditer(H + r*(q-H))):
        return_values[index] = value
    return return_values
# transformator = dimmer

def transform_pixel(pixel, angle=None):
    transparency = pixel[3]
    point = np.array(pixel[0:3])
    rot_mat = get_matrix(angle=angle)
    t,h = extract_data_from_point(point)
    r,g,b = transform_point(point, t, h, rot_mat)
    r,g,b = limiter(r), limiter(g), limiter(b)
    return  math.floor(r), math.floor(g), math.floor(b),transparency

def limiter(value):
    return minner(maxer(value))

from functools import partial

parts = 200
part_iterator = range(parts)
angles = [part*math.pi*2/parts for part in part_iterator]

pixels = testim.load()
for angle in angles:
    transformator = partial(transform_pixel, angle=angle)
    for i in range(testim.size[0]):
        for j in range(testim.size[1]):
            pixels[i,j] =transformator(pixels[i,j])
    filename = "output" + str(angle) + ".bmp"
    pathname = os.path.join(FINAL_FOLDER, filename)
    testim.save(pathname)


print(testim)