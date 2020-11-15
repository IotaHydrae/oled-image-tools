from PIL import Image


class IMGprepare():

    def __init__(self):
        self.OLED_WIDTH = 128
        self.OLED_HEIGHT = 64
        pass

    def resolution_change(self, file_path):
        # 图像分辨率更改
        filename = file_path.split('/')[-1]
        print(filename)
        file_out = f'./output/img/reschg-{filename}'

        img = Image.open(file_path)
        out = img.resize((self.OLED_WIDTH, self.OLED_HEIGHT), Image.ANTIALIAS)
        out.save(file_out)
        return file_out

    def image_crop(self, file_path, width, height):
        # 图像裁剪
        pass


if __name__ == '__main__':
    file_in = './images/test.png'
    handle = IMGprepare()
    handle.resolution_change(file_in)
