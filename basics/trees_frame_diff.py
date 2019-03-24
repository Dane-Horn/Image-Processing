import os
from image import Image

counter = 1000
directory = 'Campus_pnm'
target = 'Campus_frame_res'
curr = Image(filename=f'{directory}/trees1000.pnm').weighted_avg_gray()
for f in os.listdir(directory):
    prev = curr
    curr = Image(filename=f'{directory}/{f}')
    gray = curr.weighted_avg_gray()
    res = gray.diff(prev, 100)
    res.write_to_file(f'{target}/{f}')
    print(f)
