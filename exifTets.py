# photo time correction 
# 2021.04 @Wendell
# 需求：一些照片exif里面没有日期信息，传到手机就会显示在上传的这一天，导致时间线错乱
# 发现文件名包含日期，根据文件名修改照片日期，这样在手机里就可以按照时间线排列了

import os

import piexif


def checkFormat(photoPwd):
    # 检查文件类型是否为图片格式

    (root, ext) = os.path.splitext(photoPwd)
    return str.upper(ext[1:])  # 返回文件后缀类型


def getTime(photoName):
    '''
    根据文件名特征提取照片拍摄日期，转换为Exif时间格式
    from 'IMG_20210422_075810.jpg' to '2024:04:22 07:58:10'
    '''
    pN = photoName
    # from IMG_20210422_075810.jpg to 2024:04:22 07:58:10
    # 假设更新微'2024:04:22 07:58:10'
    imgTime = '2024:04:22 07:58:10'
    return imgTime


def setDate(photoName, photoPwd):
    '''
    给没有时间的照片加上时间
    '''
    imgTime = getTime(photoName)
    # 设置Exif信息
    exif_dict = piexif.load(photoPwd)  # 读取现有Exif信息
    print(exif_dict)
    print(exif_dict['0th'][piexif.ImageIFD.DateTime])
    exif_dict['0th'][piexif.ImageIFD.DateTime] = "9999:09:09 09:09:09".encode()  # 注意DateTime在ImageIFD里面
    print(exif_dict['0th'][piexif.ImageIFD.DateTime])
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = "9999:09:09 09:09:09".encode()
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = "9999:09:09 09:09:09".encode()
    print(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
    exif_bytes = piexif.dump(exif_dict)
    # 插入Exif信息
    piexif.insert(exif_bytes, photoPwd)


def changePhotoTime(folder):
    """
    修改该路径下的所有JPG照片的时间
    """
    for photoName in os.listdir(folder):
        photoPwd = os.path.join(folder, photoName)  # 照片的绝对路径
        if checkFormat(photoPwd) == 'JPG':  # 如果是JPG
            setDate(photoName, photoPwd)
            print(photoPwd)


if __name__ == '__main__':
    '''
    folder: 文件夹路径
    '''
    folder = r"C:\Users\鲁新\PycharmProjects\SlicesCompress"
    changePhotoTime(folder)
