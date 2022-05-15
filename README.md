
- Environment:
  - freeimage: `sudo apt install libfreeimage-dev`
  - Pangolin: version 0.8
  - CUDA: version 11.6
  - OpenCV: version 4.5.5, with opencv_contrib
- Note:
  - If you want to use different dataset, you need first crop the image size to a multiple of 4
    - use `datasets_convert.py` to convert ETH3D-type datasets into what BundleFusion needs
    - BundleFusion will horizontal flip rgb and depth images, so that I flip rgb and depth images horizontally beforehand in `datasets_convert.py`
    - I cannot find where to specify the depth scale, so that I convert origin depth scale (5000 for ETH3D datasets) to 1000 in `datasets_convert.py`  
    - If you do not change the image size, you might get error message "ERROR: image width must be a multiple of 4" from SiftGPU.cpp 
    - Scaling is not recommended, because I feel that the reconstructed model will also scale after images are scaled
    - After cropping images, $c_x$ and $c_y$ of camera intrinsic should be changed:
      - suppose, the image size before and after cropping is (Ho, Wo) and (Hn, Wn), then updated $c_x$ and $c_y$ are
        $$$ c_x' = c_x - (Wo-Wn)/2 $$$
        $$$ c_y' = c_y - (Ho-Hn)/2 $$$
      - $f_x$ and $f_y$ are unchanged
    - Change zParametersBundlingDefault.txt:
      - line 44~47, to a quarter of the image size
    - Change zParametersDefault.txt
      - line 114-115, to the image size
      - line 118-121, to the updated camera intrinsic (depth and rgb are same)
  - If you want to debug, e.g. break point, you must comment out `set(CMAKE_BUILD_TYPE Release)` in CMakeLists.txt (line 4)
  - If you want to save model, you **cannot** comment out `set(CMAKE_BUILD_TYPE Release)` in CMakeLists.txt (line 4)
    

---- 
Origin README

# BundleFusion_Ubuntu_Pangolin
This is an ubuntu porting project for [https://github.com/niessner/BundleFusion](https://github.com/niessner/BundleFusion), a GPU-based 3D reconstruction method. 
<br>
<b>Youtube Demo:</b>[https://www.youtube.com/watch?v=QOHhFObUprA](https://www.youtube.com/watch?v=QOHhFObUprA)
<p align="center">
<a href="https://www.youtube.com/watch?v=QOHhFObUprA
" target="_blank"><img src="asset/demo_office2.png"
alt="demo for BundleFusion_Ubuntu" width="720" height="540" /></a>
</p>



```
@article{dai2017bundlefusion,
  title={BundleFusion: Real-time Globally Consistent 3D Reconstruction using On-the-fly Surface Re-integration},
  author={Dai, Angela and Nie{\ss}ner, Matthias and Zoll{\"o}fer, Michael and Izadi, Shahram and Theobalt, Christian},
  journal={ACM Transactions on Graphics 2017 (TOG)},
  year={2017}
}
```

## Installation

This code is tested under ubuntu16.04/GCC7/CUDA10.1 (GPU: RTX2060).

Requirements:

* CMake
* Eigen 3.1.0
* NVIDIA CUDA 9.0/10.+
* OpenCV

Optional:

* Pangolin

```
mkdir build && cd build
cmake -DVISUALIZATION=ON ..
make -j8
```

We use -DVISUALIZATION=OFF/ON to switch visualization plug.

## Usage

* Download datasets from BundleFusion project mainpage [http://graphics.stanford.edu/projects/bundlefusion/](http://graphics.stanford.edu/projects/bundlefusion/) and unzip it.
* Run Commands:

```
cd build
./bundle_fusion_example ../zParametersDefault.txt ../zParametersBundlingDefault.txt /PATH/TO/dataset/office2
```

A pangolin window will show up and get real time reconstruction  result.

* Save Mesh:

we provide save mesh button at pangoln GUI, you need to specify the save path at zParametersDefault.txt for item "s_generateMeshDir".



## Result

We provide a reconstruction result of dataset [office2](http://graphics.stanford.edu/projects/bundlefusion/data/office2/office2.zip) with Google Drive: [https://drive.google.com/file/d/121rR0_6H_xTpsSsYAHIHV_sZqJjHdN5R/view?usp=sharing](https://drive.google.com/file/d/121rR0_6H_xTpsSsYAHIHV_sZqJjHdN5R/view?usp=sharing)



## Issues

* Pangolin OpenGL error:

<b>Problem:</b>

```
/usr/local/include/pangolin/gl/glsl.h:709:70: error: ‘glUniformMatrix3dv’ was not declared in this scope
     glUniformMatrix3dv( GetUniformHandle(name), 1, GL_FALSE, m.data());
                                                                      ^
/usr/local/include/pangolin/gl/glsl.h: In member function ‘void pangolin::GlSlProgram::SetUniform(const string&, const Matrix4d&)’:
/usr/local/include/pangolin/gl/glsl.h:713:70: error: ‘glUniformMatrix4dv’ was not declared in this scope
     glUniformMatrix4dv( GetUniformHandle(name), 1, GL_FALSE, m.data());
```

<b>Solution:</b>

```
sudo vim /usr/local/include/pangolin/gl/glplatform.h
#goto line#58
#replace "GL/glew.h" with "/usr/include/GL/glew.h"
```

## Contact

contact with fangasfrank #at gmail.com for porting issues.
