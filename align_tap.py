import cv2
import numpy as np
import glob
import statistics
import math
import os
from photoshop import PhotoShop

class AlignTap:
    def __init__(self,images_path):
        self.images_path=images_path
        self.images = glob.glob(f'{images_path}/*.jpg')
        self.images.extend(glob.glob(f'{images_path}/*.png'))


    def _clip_tap_area(self,image,cx,cy):
        x1,y1,x2,y2 = cx-890,cy-50,cx+890,cy+50
        clip_image = image[y1 : y2, x1: x2]
        return clip_image

    def _correction_rotation(self,image,crop_image,cx,cy):
        gray = cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
        retval, binarized = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(binarized,50,150,apertureSize = 3)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        coordinate=[]
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour) 
            if 200 > w and  w > 120 and  20 < h and h < 50:
                coordinate.append([x,y])

        delta_x = coordinate[0][0]-coordinate[1][0]
        delta_y = coordinate[0][1]-coordinate[1][1]
        slope=(delta_y/delta_x)

        angle = math.degrees(math.atan(slope))
        center = cx,cy
        scale = 1.0
        height = image.shape[0]                         
        width = image.shape[1]  

        trans = cv2.getRotationMatrix2D(center, angle , scale)    
        modifying_image = cv2.warpAffine(image, trans, (width,height))

        return  modifying_image

    def _detect_circle(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ハフ変換で円検出する。
        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1.0, minDist=500, param1=100, param2=35,minRadius=20, maxRadius=50)

        if circles is not None:
            cx, cy, r = circles.squeeze(axis=0).astype(int)[0]
        
        return cx,cy

    def _format_image(self,image):
        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        height, width = img.shape[:2]
    
        cx,cy = self._detect_circle(img)
        tap_image = self._clip_tap_area(img,cx,cy) 
        modified_image = self._correction_rotation(img,tap_image,cx,cy)
        image_dict={"img":modified_image,"h":height,"w":width,"cx":cx,"cy":cy}

        return image_dict


    def align_tap(self,is_save_psd):

        image_list=[]
        for image in self.images:
            image_dict = self._format_image(image)
            image_list.append(image_dict)
        
        max_height= max(i['h'] for i in image_list)
        max_width= max(i['w'] for i in image_list)

        bg=np.zeros((max_height*2,max_width*2,4),np.uint8)

        aligned_image_list=[]
        for i in range(len(image_list)):
            moving_x=max_width-image_list[i]["cx"]
            moving_y=max_height-image_list[i]["cy"]
            
            bg[moving_y:image_list[i]["h"]+moving_y,moving_x:image_list[i]["w"]+moving_x] = image_list[i]["img"]

            bg_img = np.zeros((max_height*2,max_width*2,4),np.uint8)
            bg_img[moving_y:image_list[i]["h"]+moving_y,moving_x:image_list[i]["w"]+moving_x] = image_list[i]["img"]
            aligned_image_list.append(bg_img)

        y,x = bg[:,:,3].nonzero()
        minx = np.min(x)
        miny = np.min(y)
        maxx = np.max(x)
        maxy = np.max(y)
        
    

        new_dir_path = f'{self.images_path}/result'
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)

        result_image_list=[]
        for i,aligned_image in enumerate(aligned_image_list):
            result_image = aligned_image[miny:maxy, minx:maxx]
            cv2.imwrite(f'{new_dir_path}/result{i}.png',result_image)
            result_image_list.append(result_image)

        ps = PhotoShop(result_image_list,max_height,max_width,)
        ps.psd(new_dir_path)  

        return "多分成功"
