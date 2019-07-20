# Image Comparison

## The Problem
We want to figure out how to compare two different images and measure their similarity.

### The Business Problem
Instead of having Bjorn manually open up two pairs of images and give a "Bjorn Score" for their similarities, we want to automate this process by iterating through an entire list of images pairs and calculating a score. This will be outputted into a results file so it will be nicely aggregated.

## The Solution
In a nutshell, this python script reads-in a csv file that contains (absolute) paths to images that are to be compared. Once the pair of images are known, it calculates the Structural Similarity Index, which is a method of evaluating the pixels in given windows of the image.
Information regarding the algorithm can be found here: https://en.wikipedia.org/wiki/Structural_similarity

## Assumptions
1. Valid CSV file
* The headers, rows, and columns are valid
* The order of the columns are: image1, image2
* The paths of the images lead to an existing image

2. Python is already installed (I'm using version 3.6)
* ```pip``` is already installed
* If Windows is being used, I assume Anaconda is already installed

3. The original csv file with the list of images is named `image-comparison.csv` and is in the same directory as `main.py`.

## Libraries Required 
- If using Windows, perform these commands in Anaconda.
#### cv2 (opencv.python version 4.1.0.25 at the time of development)

``` pip install opencv-python ```

#### scikit.image (version 0.15.0 at the time of development)

``` pip install scikit-image ```

## Design 

### Comparison Libraries
First looked into a few python libraries that handled image comparison. There were two methods that stood out: MSE, SSIM.

#### Mean Squared Error (MSE)
MSE performs its calculation by comparing each pixel, thus measuring absolute errors.

We then take the difference between the images by subtracting the pixel intensities. Next up, we square these difference (hence mean squared error, and finally sum them up.
In order to calculate the mean, all we are doing is dividing our sum of squares by the total number of pixels in the image.

<img src="http://www.sciweavers.org/tex2img.php?eq=%20%5Cfrac%7B1%7D%7B%28m%2B1%29%28n%2B1%29%7D%20%20%20%5Csum_0%5Em%20%20%5Csum_0%5En%20%28%5BI%28i%2C%20j%29%20-%20K%28i%2C%20j%29%5D%5E%7B2%7D%29&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt=" \frac{1}{(m+1)(n+1)}   \sum_0^m  \sum_0^n ([I(i, j) - K(i, j)]^{2})" width="315" height="50" />

#### Structural Similarity Index (SSIM)

SSIM is a method for predicting perceived quality of digital images, videos, etc. It was designed to improve traditional methods, such as MSE.
"SSIM is a perception-based model that considers image degradation as perceived change in structural information", also taking considerations to both luminance masking and contrast masking terms.

More information can be found on the wiki: https://en.wikipedia.org/wiki/Structural_similarity

##### The SSIM index is calculated on various windows of an image. The measure between two windows x and y of common size N×N is:

<img src="http://www.sciweavers.org/tex2img.php?eq=%20%5Cfrac%7B%20%20%20%282%5Cmu%20_%7Bx%7D%5Cmu%20_%7By%7D%20%2B%20%20c_%7B1%7D%29%282%20%20%5Csigma%20_%7Bxy%7D%20%2B%20%20c_%7B2%7D%29%20%7D%7B%28%5Cmu%5E%7B2%7D_%7Bx%7D%20%2B%20%5Cmu%5E%7B2%7D_%7By%7D%20%2B%20%20c_%7B1%7D%29%28%5Csigma%5E%7B2%7D_%7Bx%7D%20%2B%20%5Csigma%5E%7B2%7D_%7By%7D%20%2B%20%20c_%7B2%7D%29%7D%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt=" \frac{   (2\mu _{x}\mu _{y} +  c_{1})(2  \sigma _{xy} +  c_{2}) }{(\mu^{2}_{x} + \mu^{2}_{y} +  c_{1})(\sigma^{2}_{x} + \sigma^{2}_{y} +  c_{2})} " width="228" height="53" />


__where:__

<img src="http://www.sciweavers.org/tex2img.php?eq=%20c_%7B1%7D%20%3D%20%28k_%7B1%7DL%29%5E2&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt=" c_{1} = (k_{1}L)^2" width="94" height="21" />
<img src="http://www.sciweavers.org/tex2img.php?eq=%20c_%7B2%7D%20%3D%20%28k_%7B2%7DL%29%5E2&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt=" c_{2} = (k_{2}L)^2" width="94" height="21" />

L is the dynamic range of the pixels



__and__
<img src="http://www.sciweavers.org/tex2img.php?eq=%20k_%7B1%7D%20%3D%200.01%0A&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt=" k_{1} = 0.01" width="82" height="18" />
<img src="http://www.sciweavers.org/tex2img.php?eq=%20k_%7B2%7D%20%3D%200.03%0A&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt=" k_{2} = 0.03" width="82" height="18" />
__by default__


 ##### Since SSIM is undisputed to be an improved method of MSE, SSIM was chosen over MSE.
 
 Once the method was chosen, I then had to break down the rest of the script.
 
 ### Parsing an inputted CSV file
 
 Using the built-in __csv__ libraries, reading in CSV files were straightforward. 
 
 ### Using the Image Comparison library
 
 Each time a row from the csv file is read, it passes the two images into the function and does its magic.
 However, because SSIM requires the images to be of the same dimension, there is extra work prior to the calculation where the images are resized to a default value of 640x480 unless specified.
 Differing file types (tested with .jpg and .png) can be compared.
 
 ### Outputting Results into new CSV
 
 As each pair of images are compared, the similarity results and the elapsed time of the comparison are stored and outputted into a new csv file, in the required format from the assignment.
 
 The new csv file will have headers: image1, image2, similar, elapsed
 
 Once all the images are compared, the csv file should have the same amount of rows as the original csv file with the list of images to compare.
 
 
