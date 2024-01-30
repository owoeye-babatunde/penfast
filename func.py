import cv2
import numpy as np

def measure_length_width(image):
    # Convert the UploadedFile object to a numpy array
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    # Load the image
    #img = cv2.imread(image)
    #print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    # Get the bounding rectangle
    x, y, w, h = cv2.boundingRect(largest_contour)
    # Draw the bounding rectangle on the original image
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Extract the image within the bounding box
    roi = img[y:y+h, x:x+w]

    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to create a mask
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Create a mask for the background
    background_mask = cv2.bitwise_not(thresh)
    
    # Apply the mask to the original ROI
    roi_without_background = cv2.bitwise_and(roi, roi, mask=background_mask)

    # Find the exact widths at different points
    widths = []
    for i in range(roi_without_background.shape[1]):
        non_zero_pixels = np.count_nonzero(roi_without_background[:, i])
        widths.append(non_zero_pixels)
    
    width = sum(widths)/len(widths)
    
    max_width = max(widths)
    length = max_width
    #print("The length of the image:", max_width  )
    #print("The width is: ", width)
    return length * 1.05 * 0.0264583333, width * 0.6 * 0.0264583333


if __name__ == "__main__":
    measure_length_width(image="penis.jpg")

