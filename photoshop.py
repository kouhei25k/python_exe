import os
import sys
import cv2
import pytoshop
from pytoshop import layers
import numpy as np


class PhotoShop:
    def __init__(self,images,height,width):
        self.images = images
        self.height = height
        self.width =  width

    def _create_layer(self,image,layer_name):
        max_canvas = np.full(image.shape[:2], 255, dtype=np.uint8)

        layer_1 = layers.ChannelImageData(image=image[:, :, 3], compression=1)
        # RGB
        layer0 = layers.ChannelImageData(
            image=image[:, :, 2], compression=1)  # R
        layer1 = layers.ChannelImageData(
            image=image[:, :, 1], compression=1)  # G
        layer2 = layers.ChannelImageData(
            image=image[:, :, 0], compression=1)  # B
        new_layer = layers.LayerRecord(channels={-1: layer_1, 0: layer0, 1: layer1, 2: layer2},  # RGB画像
                                       # 位置
                                       top=0, bottom=image.shape[0], left=0, right=image.shape[1],
                                       name=layer_name,  # 名前
                                       opacity=255,  # レイヤーの不透明度
                                       )

        return new_layer


    def psd(self,save_dir):
        psd = pytoshop.core.PsdFile(
            num_channels=3, height=self.height, width=self.width)
        
        
        for i,image in  enumerate(self.images):
            layer_name = f'layer_{i}'
            new_layer = self._create_layer(image,layer_name)  
            psd.layer_and_mask_info.layer_info.layer_records.append(new_layer)

    
        with open(f'{save_dir}/output.psd', 'wb') as fd2:
            psd.write(fd2)
        return

