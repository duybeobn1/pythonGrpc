import cv2
import numpy as np

def apply_template_matching(main_image, template_image, method=cv2.TM_CCOEFF_NORMED):
    img = cv2.imread(main_image, 0)  # Read in grayscale
    template = cv2.imread(template_image, 0)  # Read in grayscale

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    offsetX = int(w * -0.01)
    offsetY = int(h * 0.35)
    widthNum = int(w * 0.65)
    heightNum = int(h * 0.45)

    new_top_left = (top_left[0] + offsetX, top_left[1] + offsetY)
    new_bottom_right = (new_top_left[0] + widthNum, new_top_left[1] + heightNum)

    cv2.rectangle(img, new_top_left, new_bottom_right, 150, 2)
    matched_region = img[max(0, new_top_left[1]):new_bottom_right[1], max(0, new_top_left[0]):new_bottom_right[0]]
    cv2.imwrite('D:/Stage Air 2024/spring/python-server/AutoExtract+Behavior/matched_region.png', matched_region)
    print("Matched region saved.")

main_image_path = 'D:/Stage Air 2024/spring/python-server/AutoExtract+Behavior/test6.png'
template_image_path = 'D:/Stage Air 2024/spring/python-server/AutoExtract+Behavior/test2.png'
apply_template_matching(main_image_path, template_image_path)
