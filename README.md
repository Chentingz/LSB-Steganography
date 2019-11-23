# LSB-Steganography
## 简介
[基于LSB隐写术将文本隐藏于320x240的灰度图像](https://chentingz.github.io/2019/11/23/基于LSB算法实现信息隐藏/)
## 目录结构
- LSB.py：秘密信息嵌入和提取算法的实现
- Noise.py：对嵌有秘密信息的载体图像进行加噪处理的实现
- test
  - raw_img.bmp：原始载体图像
  - input_secret_text.txt：输入的秘密信息（一段文本）
  
## 使用方法
- 文本隐藏于载体图像中
  - 在test/secret_text.txt中输入秘密信息
  - 运行LSB.py
  - 在test目录下将生成mod_img.bmp（嵌有秘密信息的载体图像）、img_raw_and_mod_compare.png（原始载体图像与嵌有秘密信息的载体图像的对比图）、output_secret_text.txt（从载体图像中提取的结果）
  - 也可以在控制台上查看秘密信息提取的结果

- 加噪处理
  - 运行Noise.py
  - 在test目录下将生成img_gaussian.bmp（加高斯噪声后的嵌有秘密信息的图像）、img_sp.bmp（加椒盐噪声后的嵌有秘密信息的图像）、img_mod_and_noises_compare.png（加噪前后的图像对比）

## 依赖
- Pillow (Python Imaging Library)：用于秘密信息嵌入和提取时的图像处理
- CV2：用来存储加噪处理后的图像
- Matplotlib：用于绘制对比图
- Skimage：用于图像加噪处理

