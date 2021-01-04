import cv2
import glob
import matplotlib.pyplot as plt
from os.path import splitext,basename
from local_utils import detect_lp
from transfer import load_model
from preprocessing import preprocess_image



def get_plate(wpod_net,image_path, Dmax=608, Dmin=256):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    return LpImg, cor


# test
'''
## Obtain plate image and its coordinates from an image

test_image = image_paths[2]
wpod_net_path = "wpod-net.json"
wpod_net = load_model(wpod_net_path)

LpImg,cor = get_plate(wpod_net,test_image)
print("Detect %i plate(s) in"%len(LpImg),splitext(basename(test_image))[0])
print("Coordinate of plate(s) in image: \n", cor)

## Visualize our result
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.axis(False)
plt.imshow(preprocess_image(test_image))
plt.subplot(1,2,2)
plt.axis(False)
plt.imshow(LpImg[0]) 
plt.show()
'''