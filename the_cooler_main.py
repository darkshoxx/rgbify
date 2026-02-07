import math
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).parent
SOURCE_FOLDER = HERE / "SourceImages"
FINAL_FOLDER = HERE / "FinalImages"
MYST_FOLDER = FINAL_FOLDER / "CoolMyst"

TEST_FILE = SOURCE_FOLDER / "mystbg.png"

def get_matrix(angle: float = None):
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

def mulitply(point: list, rot_mat) -> list:
    return np.matmul(rot_mat, point)

def rotate(point: list, angle: float):
    rot_mat = get_matrix(angle)
    mytup =  tuple(mulitply(point, rot_mat).getA1())
    return tuple(int(co) for co in mytup)

parts = 100
primitive = math.pi * 2 / parts
angles = [i * primitive for i in range(parts + 1)]
testim = Image.open(TEST_FILE)
out = testim.copy()
pixels = out.load()
for index in range(parts):
    for i in range(testim.size[0]):
        for j in range(testim.size[1]):
            pixels[i, j] = (*rotate(pixels[i, j][0:3], angles[index]), pixels[i, j][3])
    digits = len(str(index))
    zeroes = 3 - digits
    filename = "output" + "0"*zeroes + str(index) + ".png"
    out.save(MYST_FOLDER / filename)
    out = testim.copy()
    pixels = out.load()
