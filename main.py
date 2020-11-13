"""
author: ASCKSV a.k.a A. S. Cedric KUASSIVI
"""
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

wrapper_step = 3
wrapper_speed = 1


def time_warp():
    wrapper_height = 0
    count = 0
    final_image = np.zeros((height, width, 3), np.uint8)
    while True:
        count += 1
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Our operations on the frame come here
        if count % wrapper_speed == wrapper_speed - 1:
            wrapper_height_before = wrapper_height
            wrapper_height += wrapper_step
            frame_freeze = frame[wrapper_height_before: wrapper_height][:][:]
            frame_remaining = frame[wrapper_height:][:][:]
            final_image[wrapper_height_before: wrapper_height, :width, :3] = frame_freeze
            final_image[wrapper_height:, :width, :3] = frame_remaining
        moving_wrapper = draw_wrapper(final_image, wrapper_height)

        cv2.imshow('frame', moving_wrapper)

        # Conditions to release the cap
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if wrapper_height > height:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return final_image


def draw_wrapper(bg_image, wrapper_height):
    start_point = (0, wrapper_height)
    end_point = (width, wrapper_height)
    line_thickness = 1
    color = (255, 0, 0)
    cv2.line(bg_image, start_point, end_point, color, thickness=line_thickness)
    return bg_image


if __name__ == "__main__":

    image = time_warp()
    cv2.imshow('Final image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
