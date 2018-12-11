10/12/2018
finish framework. need further tests and adjustments

raspberrypi_camera.py
   -capture_image_and_processing: 
          get vedio stream; 
          pass the captured image to image_process function
   -image_process:
          integrate other three files' functions:
          1. clear noise(if necessary)
          2. gaussian blur and convert to matrix
          3. detect lines using nine pixels, get localized coordinates and time

possibly return: x_positioning, y_positioning, run_time
still need: communication protocol