import copy
import math
import random


class Image(object):
    @staticmethod
    def flatPixels(img):
        arr = []
        for y in range(img.rows):
            for x in range(img.cols):
                r, g, b = img.pixels[y][x]
                arr.append(r)
                arr.append(g)
                arr.append(b)
        return arr

    def __init__(self, image=None, filename=None):
        if filename != None:
            self.filename = filename
            f = open(filename, 'r')
            self.type = f.readline().strip()
            cols, rows = f.readline().strip().split(' ')
            self.rows, self.cols = int(rows), int(cols)
            self.max_val = int(f.readline().strip())
            self.pixels = self.make_pixels(f.readline().strip().split(' '))
            f.close()
        elif image != None:
            self.rows, self.cols = image.rows, image.cols
            self.max_val = image.max_val
            self.pixels = copy.deepcopy(image.pixels)
            self.type = image.type
            self.filename = ''
        else:
            self.rows = 0
            self.cols = 0
            self.pixels = []
            self.max_val = 255
            self.type = 'P3'
            self.filename = ''

    def write_to_file(self, filename):
        f = open(f'{filename}.ppm', 'w')
        f.write(f'{self.type}\n{self.cols} {self.rows}\n{self.max_val}\n')
        for row in range(self.rows):
            for col in range(self.cols):
                r, g, b = self.pixels[row][col]
                f.write(f'{r} {g} {b} ')
        f.close()

    def make_pixels(self, arr):
        pixel_arr = []
        image = []
        for i in range(0, len(arr), 3):
            pixel_arr.append((int(arr[i]), int(arr[i+1]), int(arr[i+2])))
        for y in range(self.rows):
            image.append([])
            for x in range(self.cols):
                image[y].append(pixel_arr[y*self.cols + x])
        return image

    def single_channel_gray(self, chan):
        new_image = Image(self)
        for row in range(new_image.rows):
            for col in range(new_image.cols):
                val = new_image.pixels[row][col][chan]
                new_image.pixels[row][col] = (val, val, val)
        return new_image

    def avg_gray(self):
        new = Image(self)
        for row in range(new.rows):
            for col in range(new.cols):
                r, g, b = new.pixels[row][col]
                val = (r + b + g) // 3
                new.pixels[row][col] = (val, val, val)
        return new

    def weighted_avg_gray(self):
        new = Image(self)
        for row in range(new.rows):
            for col in range(new.cols):
                r, g, b = new.pixels[row][col]
                val = int(r*0.3 + b*0.59 + g*0.11)
                new.pixels[row][col] = (val, val, val)
        return new

    def nnScale(self, new_rows, new_cols):
        new = Image()
        new.pixels = []
        new.cols = new_cols
        new.rows = new_rows
        cols_r = self.cols / float(new_cols)
        rows_r = self.rows / float(new_rows)
        for y in range(new_rows):
            new.pixels.append([])
            for x in range(new_cols):
                srcx = math.floor(x*cols_r)
                srcy = math.floor(y*rows_r)
                new.pixels[y].append(self.pixels[srcy][srcx])
        return new

    def bilinearScale(self, new_rows, new_cols):
        new = Image()
        new.cols = new_cols
        new.rows = new_rows
        cols_r = (self.cols - 1) / float(new_cols)
        rows_r = (self.rows - 1) / float(new_rows)

        for y in range(new_rows):
            new.pixels.append([])
            for x in range(new_cols):
                srcy = int(rows_r * y)
                srcx = int(cols_r * x)
                y_diff = (rows_r * y) - srcy
                x_diff = (cols_r * x) - srcx
                a = self.pixels[srcy][srcx]
                b = self.pixels[srcy][srcx+1]
                c = self.pixels[srcy+1][srcx]
                d = self.pixels[srcy+1][srcx+1]

                r = (a[0]) * (1 - x_diff) * (1 - y_diff) + \
                    (b[0]) * (1 - x_diff) * (y_diff) + \
                    (c[0]) * (x_diff) * (1 - y_diff) + \
                    (d[0]) * (x_diff) * (y_diff)

                g = (a[1]) * (1 - x_diff) * (1 - y_diff) + \
                    (b[1]) * (1 - x_diff) * (y_diff) + \
                    (c[1]) * (x_diff) * (1 - y_diff) + \
                    (d[1]) * (x_diff) * (y_diff)

                b = (a[2]) * (1 - x_diff) * (1 - y_diff) + \
                    (b[2]) * (1 - x_diff) * (y_diff) + \
                    (c[2]) * (x_diff) * (1 - y_diff) + \
                    (d[2]) * (x_diff) * (y_diff)

                new.pixels[y].append((int(r), int(g), int(b)))
        return new

    def rotateBad(self, degrees):
        new = Image(self)
        for y in range(new.rows):
            for x in range(new.cols):
                new.pixels[y][x] = (0, 0, 0)

        radians = math.radians(degrees)
        sin = math.sin(radians)
        cos = math.cos(radians)
        mid_row = self.rows / 2
        mid_col = self.cols / 2
        for y in range(new.rows):
            for x in range(new.cols):
                dsty = int(sin*(x-mid_col) + cos*(y-mid_row) + mid_row)
                dstx = int(cos*(x-mid_col) - sin*(y-mid_row) + mid_col)
                if dsty >= 0 and dstx >= 0 and dsty < self.rows and dstx < self.cols:
                    new.pixels[dsty][dstx] = self.pixels[y][x]
        return new

    def rotateBest(self, degrees):
        new = Image()
        radians = math.radians(degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        # calculate new three rotated corners
        # using the power of **maths**
        x1 = int(-self.rows * sin)
        y1 = int(self.rows * cos)
        x2 = int(self.cols * cos - self.rows * sin)
        y2 = int(self.rows * cos + self.cols * sin)
        x3 = int(self.cols * cos)
        y3 = int(self.cols * sin)
        minx = min((0, x1, x2, x3))
        miny = min((0, y1, y2, y3))
        maxx = max((x1, x2, x3))
        maxy = max((y1, y2, y3))

        new.cols = maxx - minx
        new.rows = maxy - miny

        for y in range(miny, maxy):
            new.pixels.append([])
            for x in range(minx, maxx):
                srcx = int(x*cos + y*sin)
                srcy = int(y*cos - x*sin)
                if (srcx < 0 or srcy < 0 or srcx >= self.cols or srcy >= self.rows):
                    new.pixels[y].append((0, 0, 0))
                else:
                    new.pixels[y].append(self.pixels[srcy][srcx])
        return new

    def diff(self, other, thresh):
        res = Image(self)

        for y in range(res.rows):
            for x in range(res.cols):
                if abs(self.pixels[y][x][0] - other.pixels[y][x][0]) > thresh:
                    res.pixels[y][x] = (255, 255, 255)
                else:
                    res.pixels[y][x] = (0, 0, 0)
        return res

    def threshed(self, thresh):
        new = Image(self)
        for y in range(new.rows):
            for x in range(new.cols):
                if new.pixels[y][x][0] < thresh:
                    new.pixels[y][x] = (0, 0, 0)
                else:
                    new.pixels[y][x] = (255, 255, 255)
        return new

    def mask_and(self, other):
        new = Image(self)
        for y in range(self.rows):
            for x in range(self.cols):
                sp = self.pixels[y][x][0]
                op = other.pixels[y][x][0]
                if sp == 255 and op == 255:
                    new.pixels[y][x] = (255, 255, 255)
                else:
                    new.pixels[y][x] = (0, 0, 0)
        return new

    def update_running_back(self, frame, alpha):
        new = Image(self)
        for y in range(new.rows):
            for x in range(new.cols):
                fr, fg, fb = frame.pixels[y][x]
                br, bg, bb = self.pixels[y][x]
                new.pixels[y][x] = \
                    (int(alpha*fr + (1-alpha)*br),
                     int(alpha*fg + (1-alpha)*bg),
                     int(alpha*fb + (1-alpha)*bb))
        return new

    def cryptFiend(self):
        new1 = Image()
        new1.pixels = [[(0, 0, 0) for _ in range(self.cols * 2)]
                       for _ in range(self.rows * 2)]
        new1.cols = self.cols * 2
        new1.rows = self.rows * 2
        new2 = Image(new1)

        for y in range(self.rows):
            for x in range(self.cols):
                ny, nx = 2*y, 2*x
                ran = random.randint(1, 6)
                if self.pixels[y][x][0] == 0:
                    if ran == 1:
                        new1.pixels[ny][nx] = (0, 0, 0)
                        new1.pixels[ny][nx+1] = (255, 255, 255)
                        new1.pixels[ny+1][nx] = (255, 255, 255)
                        new1.pixels[ny+1][nx+1] = (0, 0, 0)

                        new2.pixels[ny][nx] = (255, 255, 255)
                        new2.pixels[ny][nx+1] = (0, 0, 0)
                        new2.pixels[ny+1][nx] = (0, 0, 0)
                        new2.pixels[ny+1][nx+1] = (255, 255, 255)
                    if ran == 2:
                        new1.pixels[ny][nx] = (255, 255, 255)
                        new1.pixels[ny][nx+1] = (0, 0, 0)
                        new1.pixels[ny+1][nx] = (0, 0, 0)
                        new1.pixels[ny+1][nx+1] = (255, 255, 255)

                        new2.pixels[ny][nx] = (0, 0, 0)
                        new2.pixels[ny][nx+1] = (255, 255, 255)
                        new2.pixels[ny+1][nx] = (255, 255, 255)
                        new2.pixels[ny+1][nx+1] = (0, 0, 0)
                    if ran == 3:
                        new1.pixels[ny][nx] = (255, 255, 255)
                        new1.pixels[ny][nx+1] = (0, 0, 0)
                        new1.pixels[ny+1][nx] = (255, 255, 255)
                        new1.pixels[ny+1][nx+1] = (0, 0, 0)

                        new2.pixels[ny][nx] = (0, 0, 0)
                        new2.pixels[ny][nx+1] = (255, 255, 255)
                        new2.pixels[ny+1][nx] = (0, 0, 0)
                        new2.pixels[ny+1][nx+1] = (255, 255, 255)
                    if ran == 4:
                        new1.pixels[ny][nx] = (0, 0, 0)
                        new1.pixels[ny][nx+1] = (255, 255, 255)
                        new1.pixels[ny+1][nx] = (0, 0, 0)
                        new1.pixels[ny+1][nx+1] = (255, 255, 255)

                        new2.pixels[ny][nx] = (255, 255, 255)
                        new2.pixels[ny][nx+1] = (0, 0, 0)
                        new2.pixels[ny+1][nx] = (255, 255, 255)
                        new2.pixels[ny+1][nx+1] = (0, 0, 0)
                    if ran == 5:
                        new1.pixels[ny][nx] = (0, 0, 0)
                        new1.pixels[ny][nx+1] = (0, 0, 0)
                        new1.pixels[ny+1][nx] = (255, 255, 255)
                        new1.pixels[ny+1][nx+1] = (255, 255, 255)

                        new2.pixels[ny][nx] = (255, 255, 255)
                        new2.pixels[ny][nx+1] = (255, 255, 255)
                        new2.pixels[ny+1][nx] = (0, 0, 0)
                        new2.pixels[ny+1][nx+1] = (0, 0, 0)
                    if ran == 6:
                        new1.pixels[ny][nx] = (255, 255, 255)
                        new1.pixels[ny][nx+1] = (255, 255, 255)
                        new1.pixels[ny+1][nx] = (0, 0, 0)
                        new1.pixels[ny+1][nx+1] = (0, 0, 0)

                        new2.pixels[ny][nx] = (0, 0, 0)
                        new2.pixels[ny][nx+1] = (0, 0, 0)
                        new2.pixels[ny+1][nx] = (255, 255, 255)
                        new2.pixels[ny+1][nx+1] = (255, 255, 255)
                else:
                    if ran == 1:
                        new1.pixels[ny][nx] = (0, 0, 0)
                        new1.pixels[ny][nx+1] = (255, 255, 255)
                        new1.pixels[ny+1][nx] = (255, 255, 255)
                        new1.pixels[ny+1][nx+1] = (0, 0, 0)

                        new2.pixels[ny][nx] = (0, 0, 0)
                        new2.pixels[ny][nx+1] = (255, 255, 255)
                        new2.pixels[ny+1][nx] = (255, 255, 255)
                        new2.pixels[ny+1][nx+1] = (0, 0, 0)
                    if ran == 2:
                        new1.pixels[ny][nx] = (255, 255, 255)
                        new1.pixels[ny][nx+1] = (0, 0, 0)
                        new1.pixels[ny+1][nx] = (0, 0, 0)
                        new1.pixels[ny+1][nx+1] = (255, 255, 255)

                        new2.pixels[ny][nx] = (255, 255, 255)
                        new2.pixels[ny][nx+1] = (0, 0, 0)
                        new2.pixels[ny+1][nx] = (0, 0, 0)
                        new2.pixels[ny+1][nx+1] = (255, 255, 255)
                    if ran == 3:
                        new1.pixels[ny][nx] = (255, 255, 255)
                        new1.pixels[ny][nx+1] = (0, 0, 0)
                        new1.pixels[ny+1][nx] = (255, 255, 255)
                        new1.pixels[ny+1][nx+1] = (0, 0, 0)

                        new2.pixels[ny][nx] = (255, 255, 255)
                        new2.pixels[ny][nx+1] = (0, 0, 0)
                        new2.pixels[ny+1][nx] = (255, 255, 255)
                        new2.pixels[ny+1][nx+1] = (0, 0, 0)
                    if ran == 4:
                        new1.pixels[ny][nx] = (0, 0, 0)
                        new1.pixels[ny][nx+1] = (255, 255, 255)
                        new1.pixels[ny+1][nx] = (0, 0, 0)
                        new1.pixels[ny+1][nx+1] = (255, 255, 255)

                        new2.pixels[ny][nx] = (0, 0, 0)
                        new2.pixels[ny][nx+1] = (255, 255, 255)
                        new2.pixels[ny+1][nx] = (0, 0, 0)
                        new2.pixels[ny+1][nx+1] = (255, 255, 255)
                    if ran == 5:
                        new1.pixels[ny][nx] = (0, 0, 0)
                        new1.pixels[ny][nx+1] = (0, 0, 0)
                        new1.pixels[ny+1][nx] = (255, 255, 255)
                        new1.pixels[ny+1][nx+1] = (255, 255, 255)

                        new2.pixels[ny][nx] = (0, 0, 0)
                        new2.pixels[ny][nx+1] = (0, 0, 0)
                        new2.pixels[ny+1][nx] = (255, 255, 255)
                        new2.pixels[ny+1][nx+1] = (255, 255, 255)
                    if ran == 6:
                        new1.pixels[ny][nx] = (255, 255, 255)
                        new1.pixels[ny][nx+1] = (255, 255, 255)
                        new1.pixels[ny+1][nx] = (0, 0, 0)
                        new1.pixels[ny+1][nx+1] = (0, 0, 0)

                        new2.pixels[ny][nx] = (255, 255, 255)
                        new2.pixels[ny][nx+1] = (255, 255, 255)
                        new2.pixels[ny+1][nx] = (0, 0, 0)
                        new2.pixels[ny+1][nx+1] = (0, 0, 0)
        return new1, new2

    def hideMessage(self, message):
        def changeVal(v):
            return v - 1 if v == 255 else v + 1
        new = Image(self)
        binary = ''.join(format(ord(x), 'b').zfill(8) for x in message)
        for y in range(self.rows):
            for x in range(self.cols):
                r, g, b = self.pixels[y][x]
                if len(binary) >= 3:
                    if binary[0] == '1':
                        r = changeVal(r)
                    binary = binary[1:]
                    if binary[0] == '1':
                        g = changeVal(g)
                    binary = binary[1:]
                    if binary[0] == '1':
                        b = changeVal(b)
                    binary = binary[1:]
                elif len(binary) == 2:
                    if binary[0] == '1':
                        r = changeVal(r)
                    binary = binary[1:]
                    if binary[0] == '1':
                        g = changeVal(g)
                    binary = binary[1:]
                elif len(binary) == 1:
                    if binary[0] == '1':
                        r = changeVal(r)
                    binary = binary[1:]
                else:
                    return new
                new.pixels[y][x] = (r, g, b)

    def getMessage(self, other):
        message = []
        self_pixels = Image.flatPixels(self)
        other_pixels = Image.flatPixels(other)
        for i in range(0, len(self_pixels)-8, 8):
            char = list(
                map(
                    lambda x, y: '0' if x == y else '1',
                    self_pixels[i:i+8], other_pixels[i:i+8]
                )
            )
            char = ''.join(char)
            if char == '00000000':
                break
            message.append(char)
        message = ''.join(map(lambda c: chr(int(c, 2)), message))
        return message
