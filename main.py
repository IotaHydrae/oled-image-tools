from PIL import Image
import numpy as np

from prepare import IMGprepare
import numpy as np

class IMGtools():

    def __init__(self):
        self.OUTPUT_PATH = './output/img/'
        pass

    def color_transform(self, file_path):
        filename = file_path.split('/')[-1]
        file_out = self.OUTPUT_PATH + 'monochrome-' + filename

        img = Image.open(file_path)
        # thresh = np.mean(img)
        # fn = lambda x: 255 if x > thresh else 0

        img = img.convert('1')
        # img = img.convert('L').point(fn, mode='1')
        img.save(file_out)
        return file_out

    def origin_data2hex(self, data_list):
        print(data_list)
        out_data = 0x00

        # update list
        for bit in range(8):
            if data_list[bit]:
                data_list[bit] = 0
            else:
                data_list[bit] = 1
        print(data_list)
        for offset in range(8):
            out_data |= (data_list[offset] << offset)
        print(hex(out_data))
        out_data = hex(out_data)
        return out_data

    def dot_matrix_output_hex(self, file_path):
        img = Image.open(file_path)
        print(img)
        img_array = np.array(img)
        print("size: ", img_array.size)
        print("shape: ", img_array.shape)

        # 准备输出数据到文件
        data_output = []
        # 写入上部分
        data_output.append('#ifndef _OLEDPIC_H\n')
        data_output.append('#define _OLEDPIC_H\n')
        data_output.append('unsigned char code oled_pic_data[]={\n')

        # 写入主要数据
        for page_index in range(8):
            row_start = page_index * 8;
            row_end = row_start + 8
            # print(row_start, row_end)

            for col_index in range(128):
                temp_data_list = []
                for pic_line in range(row_start, row_end):
                    # print(img_array[row][127])
                    temp_data = img_array[pic_line][col_index]

                    temp_data_list.append(temp_data)
                result = self.origin_data2hex(temp_data_list)
                print(result)
                data_output.append(result + ',')

                # 将单行数据划为16个一行
                if not (col_index % 16) and col_index != 0:
                    data_output.append('\n')

            # 页输出完成，换行
            data_output.append('\n')
            print(col_index)

        # 数据写入完成
        data_output.append('};')

        data = open('./data/oled_pic_data.h', 'w')
        data.writelines(data_output)

        pass

    def dot_matrix_output(self, file_path, type='normal'):
        img = Image.open(file_path)
        print(img)
        img_array = np.array(img)
        print("size: ", img_array.size)
        print("shape: ", img_array.shape)

        # 准备输出数据到文件
        data_output = []
        data_output.append('#ifndef _OLEDPIC_H')
        data_output.append('#define _OLEDPIC_H')
        data_output.append('unsigned char code oled_pic_data[]=')
        data_output.append('{')

        data = open('./data/oled_pic_data.h', 'w')
        data.writelines(data_output)
        row_count = 0
        for pic__line in img_array:

            # 64行
            data.writelines("    {")
            # 列计数
            count = 0
            for x_pixel in pic__line:
                if x_pixel:
                    data.writelines('1')
                else:
                    data.writelines('0')
                count += 1
                # print(x_pixel)
                if count < 64:
                    data.writelines(',')
                else:
                    break
            row_count += 1

            data.writelines("},\n")
            if row_count >= 32:
                break
        # 主要数据写入完成
        data.writelines("};\n")
        data.writelines("#endif")
        data.close()
        pass


if __name__ == '__main__':
    origin_pic = './images/nihao.png'
    pre_tool = IMGprepare()
    pre_tool.resolution_change(origin_pic)

    pic_path = './output/img/reschg-nihao.png'
    handle = IMGtools()

    # 图像色彩转换
    single_color = handle.color_transform(pic_path)
    print(single_color)
    # 点阵数据输出
    handle.dot_matrix_output_hex(single_color)
