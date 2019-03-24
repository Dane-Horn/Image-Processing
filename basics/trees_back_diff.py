import os
from image import Image

counter = 1000
directory = 'Campus_pnm'
target = 'Campus_back_res'
bg = Image(filename=f'{directory}/trees1000.pnm').weighted_avg_gray()
for f in os.listdir(directory):
    curr = Image(filename=f'{directory}/{f}').weighted_avg_gray()
    res = curr.diff(bg, 90)
    res.write_to_file(f'{target}/{f}')
    print(f)
