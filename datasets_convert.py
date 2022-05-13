import glob
import os
import cv2
import numpy as np

# change these if needed
dataset_path = "/home/orz/Projects/Datasets/BadSLAM/camera_shake_1"
output_path = "/home/orz/Projects/Datasets/BundleFusion/camera_shake_1"
color_name = "rgb"      # color, rgb
depth_name = "depth"    # filtered, depth
depth_scale = 5000      # default scale of BundleFusion is 1000
timestamp_name = "TIMESTAMP.txt"    # Pick one of two. Converting by reading timestamp.txt, see FastFusion datasets https://github.com/zhuzunjie17/FastFusion
image_format = "*.png"              # Pick one of two. Converting by traversing file name
resize = True
resize_type = "crop"    # scale, crop
resize_size = (456, 736)


def process(input_path, output_path, scale=-1):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    img = cv2.flip(img, 1)  # because BundleFusion flips image horizontally before reconstruction
    if img.shape[:2] != resize_size and resize:   # sale to 480*640(H*W)
        H, W = img.shape[:2]
        if resize_type == 'crop':
            img = img[:resize_size[0], :resize_size[1]]
            print("image is crop to {}, crop from top right".format(resize_size))
        elif resize_type == 'scale':
            img = cv2.resize(img, resize_size, interpolation=cv2.INTER_CUBIC)
            print("image is scaled to {}, scale factor is {:.5f} and {:.5f}".format(resize_size, H/480, W/640))
    if scale > 0 and scale is not 1000:     # convert scale to 1000
        img = (img / scale * 1000).astype(np.uint16)
        print("rescale to 1000")
    cv2.imwrite(output_path, img)


idx=0
os.makedirs(output_path, exist_ok=True)
timestamp_path = os.path.join(dataset_path, timestamp_name)
if not os.path.exists(timestamp_path):
    depth_paths = sorted(glob.glob(os.path.join(dataset_path, depth_name, image_format)))
    color_paths = sorted(glob.glob(os.path.join(dataset_path, color_name, image_format)))

    for i, (depth_input, color_input) in enumerate(zip(depth_paths, color_paths)):
        # color
        color_output = os.path.join(output_path, "frame-{:6d}.color.jpg".format(idx))
        img_color = cv2.imread(color_input, cv2.IMREAD_UNCHANGED)
        img_color = cv2.flip(img_color, 1)  # because BundleFusion flips image horizontally before reconstruction
        cv2.imwrite(color_output, img_color)

        # depth
        depth_output = os.path.join(output_path, "frame-{:6d}.depth.png".format(idx))
        img_depth = cv2.imread(depth_input, cv2.IMREAD_UNCHANGED)
        img_depth = cv2.flip(img_depth, 1)
        cv2.imwrite(depth_output, img_depth)

        idx += 1

else:
    with open(timestamp_path, 'r') as f:
        infos = f.read().splitlines()
        infos.pop(0)
        for info in infos:
            _, color_filename, depth_filename = info.split(',')
            # color
            color_input = os.path.join(dataset_path, color_name, color_filename)
            color_output = os.path.join(output_path, "frame-{:06d}.color.jpg".format(idx))
            process(color_input, color_output)

            # depth
            depth_input = os.path.join(dataset_path, depth_name, depth_filename)
            depth_output = os.path.join(output_path, "frame-{:06d}.depth.png".format(idx))
            process(depth_input, depth_output, depth_scale)

            idx += 1

print("done!")