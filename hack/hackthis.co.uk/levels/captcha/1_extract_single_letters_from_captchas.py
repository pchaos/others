import os
# import os.path
import cv2
import glob
import imutils


CAPTCHA_IMAGE_FOLDER = "captcha"
OUTPUT_FOLDER = "/tmp/extracted_letter_images"


# Get a list of all the captcha images we need to process
captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*.png"))
counts = {}

# loop over the image paths
for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))

    # Since the filename contains the captcha text (i.e. "2A2X.png" has the text "2A2X"),
    # grab the base filename as the text
    filename = os.path.basename(captcha_image_file)
    if filename.startwith('tmp'):
        # 忽略图片文件名以‘tmp'开头的文件
        continue;
    captcha_correct_text = os.path.splitext(filename)[0] # 文件名长度 40

    # Load the image and convert it to grayscale
    image = cv2.imread(captcha_image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)