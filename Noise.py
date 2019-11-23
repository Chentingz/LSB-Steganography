import cv2
import matplotlib.pyplot as plt
import skimage.util as ski
import LSB
from PIL import Image

mod_img_path = "./test/mod_img.bmp"
img_gaussian_path = "./test/img_gaussian.bmp"
img_sp_path = "./test/img_sp.bmp"
img_mod_and_noises_compare_path = "./test/img_mod_and_noises_compare.png"
"""
对嵌有秘密信息的载体图像加噪处理，并保存
"""
def noise():
    mod_img = cv2.imread(mod_img_path, cv2.IMREAD_GRAYSCALE)
    img_copy = mod_img.copy()
    # 高斯噪声处理后的嵌有秘密信息的载体图像
    img_gaussian = ski.random_noise(img_copy, mode="gaussian", seed=None, clip=True, mean=0,var=0.05)
    img_gaussian *= 255
    # 椒盐噪声处理后的嵌有秘密信息的载体图像
    img_sp = ski.random_noise(img_copy, mode="s&p", seed=None, clip=True, amount=0.1)
    img_sp *= 255

    # 保存加噪后的图像
    cv2.imwrite(img_gaussian_path, img_gaussian)
    cv2.imwrite(img_sp_path, img_sp)

    # 构造对比图
    plt.rcParams['font.sans-serif']=['SimHei']  # 中文字体设置
    plt.rcParams['axes.unicode_minus'] = False
    plt.subplot(131)
    plt.title("嵌有秘密信息的载体图像")
    plt.imshow(mod_img,cmap='gray')
    plt.subplot(132)
    plt.title("高斯噪声处理后图像")
    plt.imshow(img_gaussian, cmap='gray')
    plt.subplot(133)
    plt.title("椒盐噪声处理后的图像")
    plt.imshow(img_sp,cmap='gray')
    # 保存对比图
    plt.savefig(img_mod_and_noises_compare_path)
    # 显示对比图
    plt.show()

# 调用
if __name__ == "__main__":
    noise()
    mod_img = Image.open(mod_img_path)
    img_gaussian = Image.open(img_gaussian_path)
    img_sp = Image.open(img_sp_path)
    # 打印嵌有秘密信息的载体图像、加高斯噪声后图像、加椒盐噪声后图像中的秘密信息
    print("载体图像中提取的秘密信息：")
    print(LSB.get_text_from_image(mod_img))
    print("高斯噪声图像中提取的秘密信息：")
    print(LSB.get_text_from_image(img_gaussian))
    print("椒盐噪声图像中提取的秘密信息：")
    print(LSB.get_text_from_image(img_sp))