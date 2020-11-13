"""
author: ASCKSV a.k.a A. S. Cedric KUASSIVI
"""
import numpy as np
import cv2
import os

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

wrapper_step = 1
wrapper_speed = 1

cv2.namedWindow("Time Warp Filter", cv2.WINDOW_AUTOSIZE)


def time_warp(orientation=0):

    wrapper_height = 0
    count = 0
    final_image = np.zeros((height, width, 3), np.uint8)
    use_cam = True

    while True:
        count += 1
        # Capture frame-by-frame
        if use_cam:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

        # Our operations on the frame come here
        if count % wrapper_speed == wrapper_speed - 1:
            wrapper_height_before = wrapper_height
            wrapper_height += wrapper_step

            if orientation == 0:
                frame_freeze = frame[wrapper_height_before: wrapper_height][:][:]
                frame_remaining = frame[wrapper_height:][:][:]
                final_image[wrapper_height_before: wrapper_height, :width, :3] = frame_freeze
                final_image[wrapper_height:, :width, :3] = frame_remaining
                if wrapper_height > height:
                    use_cam = False
                    cv2.imshow('Time Warp Filter', final_image)
            else:
                frame_freeze = frame[:height, wrapper_height_before: wrapper_height, :3]
                frame_remaining = frame[:height, wrapper_height:, :3]
                final_image[:height, wrapper_height_before: wrapper_height, :3] = frame_freeze
                final_image[:height, wrapper_height:, :3] = frame_remaining
                if wrapper_height > width:
                    use_cam = False
                    cv2.imshow('Time Warp Filter', final_image)

        moving_wrapper = draw_wrapper(final_image, wrapper_height, orientation)

        cv2.imshow("Time Warp Filter", moving_wrapper)

        # key bindings
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        if k == ord('r'):
            use_cam = True
            wrapper_height = 0
        if k == ord('i'):
            use_cam = True
            wrapper_height = 0
            orientation = (orientation + 1) % 2
        if k == ord('s'):
            path = './'
            cv2.imwrite(os.path.join(path, 'timeWarp.jpg'), final_image)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return final_image


def draw_wrapper(bg_image, wrapper_height, orientation):
    if orientation == 0:
        start_point = (0, wrapper_height)
        end_point = (width, wrapper_height)
    else:
        start_point = (wrapper_height, 0)
        end_point = (wrapper_height, height)
    line_thickness = 1
    color = (255, 0, 0)
    cv2.line(bg_image, start_point, end_point, color, thickness=line_thickness)
    return bg_image


if __name__ == "__main__":

    image = time_warp(orientation=1)

