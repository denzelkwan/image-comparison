#!/usr/bin/env python
from skimage.measure import compare_ssim
import cv2
import csv
import time


def compare_images(image1, image2):
    start_time = time.time()
    similar = 1- compare_ssim(image1, image2) ## Structural Similiarity Index has 1 signifying identical images, not 0
    elapsed = time.time() - start_time

    return similar, elapsed
    
## appending to the results.csv file with the paths, similiarity index, and time elapsed for the comparison
def output_file(pathA, pathB, similar, elapsed):
    with open('results.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([pathA, pathB, similar, elapsed])



## read in csv containing all images that are being compared
with open('image-comparison.csv') as csvfile:

## creating new file and setting the headers
    with open('results.csv', 'w') as newcsv:
        writer = csv.writer(newcsv, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['image1', 'image2', 'similar', 'elapsed'])

## skipping the first line because they are headers
    firstLine = True
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if firstLine:
            firstLine = False
            continue

        path1, path2 = row[0], row[1]
        
        image1 = cv2.cvtColor(cv2.imread(row[0]), cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(cv2.imread(row[1]), cv2.COLOR_BGR2GRAY)

        similar, elapsed = compare_images(image1, image2)
        
        output_file(path1, path2, similar, elapsed)


