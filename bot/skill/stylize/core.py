# author: Paul Galatic
#
# Program to perform K-means image cartoonization, integrated as a Bot Skill
# source: https://www.pyimagesearch.com/2018/08/27/neural-style-transfer-with-opencv/
#

# standard lib
import argparse
import random
import time
import pdb
import os

# required lib
import imageio
import imutils
import cv2

# project lib

MODEL_DIR = 'bot/skill/stylize/models/'

def parse_args():
    '''construct the argument parser and parse the arguments'''
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=False,
        help="neural style transfer model")
    ap.add_argument("-i", "--im_name", required=True,
        help="name of input image to apply neural style transfer to")
    return ap.parse_args()

def style_transfer(image, ckpt):
    '''
    Applies style tranfer.
    
    args
        im_name : the name of an input image
        chkpt   : the name of the model to use for style transfer
    '''
    # if no model is chosen, then choose a random one
    pdb.set_trace()
    if not ckpt:
        models = os.listdir(MODEL_DIR)
        ckpt = MODEL_DIR + random.choice(models)
    
    # load the neural style transfer model from disk
    # print("[INFO] loading style transfer model...")
    net = cv2.dnn.readNetFromTorch(ckpt)
    
    # resize the image to have a width of 600 pixels, and
    # then grab the image dimensions

    imutils.resize(image, width=600)
    
    (h, w) = image.shape[:2]
    
    # construct a blob from the image, set the input, and then perform a
    # forward pass of the network
    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
        (103.939, 116.779, 123.680), swapRB=False, crop=False)
    net.setInput(blob)
    output = net.forward()

    # reshape the output tensor, add back in the mean subtraction, and
    # then swap the channel ordering
    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.680
    output /= 255.0
    output = output.transpose(1, 2, 0)
    
    # print("[INFO] neural style transfer took {:.4f} seconds".format(end - start))
    
    return image * 255, output * 255

def main():
    args = parse_args()
    
    img_in = cv2.imread(args.im_name)
    
    image, output = style_transfer(img_in, args.model)
    
    cv2.imwrite('out.png', output)
    
    # show the images
    cv2.imshow("Input", image)
    cv2.imshow("Output", output)

    cv2.waitKey(0)
    
if __name__ == '__main__':
    main()
        