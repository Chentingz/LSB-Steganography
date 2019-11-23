# -*- coding: UTF-8 -*-
from PIL import Image
import matplotlib.pyplot as plt

input_secret_text_path = "./test/input_secret_text.txt"
output_secret_text_path = "./test/output_secret_text.txt"
raw_img_path = "./test/raw_img.bmp"
mod_img_path = "./test/mod_img.bmp"
img_raw_and_mod_compare_path = "./test/img_raw_and_mod_compare.png"
eof_str = "00000000"
eof = chr(int(eof_str, 2))

"""
从文件中读取秘密信息
"""
def get_text_from_file():
    file = open(input_secret_text_path, "r")
    text = file.read()
    file.close()
    return text
"""
读取载体图像
@return: 图像
"""
def get_raw_img():
    raw_img = Image.open(raw_img_path)
    width = raw_img.size[0]
    height = raw_img.size[1]
    if width != 320 and height != 240:
        raw_img = raw_img.resize((320, 240))
    if raw_img.mode != "L":
        raw_img = raw_img.convert("L")
    return raw_img
"""
将秘密信息嵌入到载体图像中
首先将秘密信息转换成二进制字符串，如"a" -> "0110 0001"
在二进制字符串的末尾添加两个0x0000的ASCII码作为结束标志，如"0110 0001" -> "0110 0001 0000 0000 0000 0000"
按照图像从上到下，从左到右的顺序，将串的每一位依次插入到像素的最低位中，每一个像素用一个字节表示
@param text: string类型的秘密信息
@param raw_img: image类型原始载体图像
@return: image类型嵌入秘密信息后的图像
"""
def insert_text_to_image(text, raw_img):
    mod_img = raw_img.copy()
    width = mod_img.size[0]
    height = mod_img.size[1]
    binstr = text2binarystring(text)
    binstr += eof_str + eof_str
    #print(binstr)
    i = 0
    for w in range(width):
        for h in range(height):
            if i == len(binstr):
                break
            value = mod_img.getpixel((w,h))
            #print("before mod value:%d" %(value))
            #print("binstr[%d]:%s" %(i,binstr[i]))
            value = mod_lsb(value, binstr[i])
            #print("after mod value:%d" %(value))
            mod_img.putpixel((w,h), value)
            i=i+1
    return mod_img

"""
将value的最低位替换成bit,返回修改后的value
@param value: int类型表示的像素值
@param bit: string类型表示的嵌入位
@return: int类型表示的修改后的像素值
"""
def mod_lsb(value, bit):
    str = bin(value).replace('0b', '').zfill(8)
    lsb = str[len(str)-1]
    #print("lsb:%s" %lsb)
    #print("bit:%s" %bit)
    if lsb != bit :
        str = str[0:len(str)-1] + bit
    #print(str)
    return int(str, 2)


"""
将秘密信息转换成二进制串
先将字符转换成对应的ASCII码，然后转二进制，最后8位对齐，不足的前面用0填充
@param text: string类型表示的秘密信息
@return: string类型表示的二进制串
"""
def text2binarystring(text):
    binstr = ""
    for ch in text :
        # ord(ch): 将ch转换成十进制数 bin():转换成0b开头的二进制字符串 zfill:返回指定长度字符串，不足的前面填充0
        binstr += bin(ord(ch)).replace('0b', '').zfill(8)
    return binstr

"""
从图像中提取秘密信息，返回string类型的秘密信息
@param mod_img: 嵌入秘密信息后的图像
@return: string类型表示的秘密信息
"""
def get_text_from_image(mod_img):
    width = mod_img.size[0]
    height = mod_img.size[1]
    bytestr = ""
    text = ""
    countEOF = 0
    for w in range(width):
        for h in range(height):
            value = mod_img.getpixel((w,h))
            bytestr += get_lsb(value)
            if len(bytestr) == 8 :
                # 转换成ASCII码
                # 例："0110 0001" -> 97 -> 'a'
                ch = chr(int(bytestr, 2))
                if ch == eof :
                    countEOF = countEOF + 1
                if countEOF == 2 :
                    break
                text += ch
                bytestr = ""
    return text

"""
返回像素值的lsb
@param value: int类型表示的像素值
@return: string类型表示的像素值最低位
"""
def get_lsb(value):
    str = bin(value).replace('0b', '').zfill(8)
    lsb = str[len(str)-1]
    return lsb

"""
将文本写入文件
@param text: 文本
"""
def write_text_to_file(text):
    file = open(output_secret_text_path, "w")
    file.write(text)
    file.close()

"""
秘密信息嵌入和提取
"""
def main():
    text = get_text_from_file()
    raw_img = get_raw_img()
    mod_img = insert_text_to_image(text, raw_img)
    mod_img.save(mod_img_path)
    hidden_text = get_text_from_image(mod_img)
    print(hidden_text)
    write_text_to_file(hidden_text)

    # 构造对比图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置
    plt.rcParams['axes.unicode_minus'] = False
    plt.subplot(121)
    plt.title("原始载体图像")
    plt.imshow(raw_img, cmap='gray')
    plt.subplot(122)
    plt.title("嵌有秘密信息的载体图像")
    plt.imshow(mod_img, cmap='gray')
    # 保存对比图
    plt.savefig(img_raw_and_mod_compare_path)
    # 显示对比图
    plt.show()

# 调用
if __name__ == '__main__':
    main()