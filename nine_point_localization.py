###
# input：matrix after denoising and matrixing(image)
# TO_DO:
# one way of boosting up: use only 9*7*7 data
###
# sample_points: 1/4, 2/4, 3/4
import numpy as np
import time


def signalling(image):
    ###
    #  input : image matrix
    #  output: 9 values of pixels
    #  use average to further denoise
    width, height = image.size
    x = [0]*3
    y = [0]*3
    for i in range(3):
        x[i] = float(i + 1) / 4.0 * float(width)
        x[i] = int(x[i])
        y[i] = float(i + 1) / 4.0 * float(height)
        y[i] = int(y[i])
    m = np.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            # averaging: 5*5
            for k in range(5):
                for l in range(5):
                    k = k-2
                    l = l-2
                    m[i][j] += image[x[i]+k][y[j]+l]
    m = m / 25.
    return m


threshold = 0.2  # gray scale threshold for white line: need adjusting; consider one of RGB instead
pixels_status_front_rear = np.zeros(3, 3)
x_status = [0]*3
x_timer = [0]*3
pixels_status_left_right = np.zeros(3, 3)
y_status = [0]*3
y_timer = [0]*3


def clear_counter_x():
    global pixels_status_front_rear
    global x_status
    global x_timer
    pixels_status_front_rear = np.zeros(3, 3)
    x_status = [0] * 3
    x_timer = [0] * 3


def clear_counter_y():
    global pixels_status_left_right
    global y_status
    global y_timer
    pixels_status_left_right = np.zeros(3, 3)
    y_status = [0] * 3
    y_timer = [0] * 3


def check_timeout(pixels, n, timer, pixels_status, status):
    # use time to eliminate perpendicular line's effect:
    # if time>1s clear relevant counters
    flag = 0  # flag uif any change: do overall judgement(pass in three pixels or pass perpendicular line)
    for i in range(3):
        if pixels[1][i] < threshold:
            pixels_status[n][i] = 1
            flag = 1
    if timer == 0 and flag == 1:
        timer = time.time()
    if timer != 0 and time.time() - timer > 1:  # timeout
        timer = 0
        pixels_status = np.zeros(3, 3)
        status = 0
    elif flag == 1 and pixels_status[1][0] == 1 and pixels_status[1][1] == 1 and pixels_status[1][2] == 1:
        status = 1
        timer = 0
    return timer, status, pixels_status


# first detect the centre three;if they has been 1, register x/y_status with 1
def front_rear_processing(pixels):
    global x_timer
    global x_status
    global pixels_status_front_rear
    if x_status[1] == 1:
        x_timer[0], x_status[0], pixels_status_front_rear = check_timeout(pixels, 0, x_timer[0],
                                                                          pixels_status_front_rear, x_status[0])
        x_timer[2], x_status[2], pixels_status_front_rear = check_timeout(pixels, 2, x_timer[2],
                                                                          pixels_status_front_rear, x_status[2])
        if x_status[2] == 1:
            clear_counter_x()
            return -1
        elif x_status[0] == 1:
            clear_counter_x()
            return 1
        else:
            return 0
    elif x_status == 0:
        # check if passing the central line;
        x_timer[1], x_status[1], pixels_status_front_rear = check_timeout(pixels, 1, x_timer[1],
                                                                          pixels_status_front_rear, x_status[1])
        return 0


def left_right_processing(pixels):
    global y_timer
    global y_status
    global pixels_status_left_right
    if y_status[1] == 1:
        y_timer[0], y_status[0], pixels_status_left_right = check_timeout(pixels, 0, y_timer[0],
                                                                          pixels_status_left_right, y_status[0])
        y_timer[2], y_status[2], pixels_status_left_right = check_timeout(pixels, 2, y_timer[2],
                                                                          pixels_status_left_right, y_status[2])
        if y_status[2] == 1:
            clear_counter_y()
            return -1
        elif y_status[0] == 1:
            clear_counter_y()
            return 1
        else:
            return 0
    elif y_status == 0:
        # check if passing the central line;
        y_timer[1], y_status[1], pixels_status_left_right = check_timeout(pixels, 1, y_timer[1],
                                                                          pixels_status_left_right, y_status[1])
        return 0


###
# need to be tested
# front: x_change= +1
# right: y_change= +1
###
def processing(image):
    pixels = signalling(image)
    x_change = front_rear_processing(pixels)
    # same process but in left_right direction
    pixels_transpose = np.transpose(pixels)
    y_change = left_right_processing(pixels_transpose)
    return x_change, y_change


x_index = 0
y_index = 0


def local_positioning(image):
    global x_index
    global y_index
    x_change, y_change = processing(image)
    x_index += x_change
    y_index += y_change
    return x_index, y_index, time.time()
