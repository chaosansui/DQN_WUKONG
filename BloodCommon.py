# coding=utf-8
import cv2
import grabscreen

class GrayWindow(object):
    def __init__(self, sx, sy, ex, ey):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.mistake = 3 # 图像尺寸误差
        self.image = grabscreen.grab_screen(self)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def get_tuple(self):
        return (self.sx, self.sy, self.ex, self.ey)
    
    def __iter__(self):
        return iter((self.sx, self.sy, self.ex, self.ey))

    def __repr__(self):
        return f"BloodWindow(sx={self.sx}, sy={self.sy}, ex={self.ex}, ey={self.ey})"

class BloodWindow(GrayWindow):
    def __init__(self, sx, sy, ex, ey):
        super().__init__(sx, sy, ex, ey)
        # 剩余血量的灰度值范围, 即血条白色部分的灰度值
        self.blood_gray_max = 220
        self.blood_gray_min = 180
        
        self.blood_gray_min = 80

    def blood_count(self) -> int:
        total_length = self.image.shape[1]  # 血条的总长度是图像的宽度
        max_find_cnt = 2
        while max_find_cnt > 0:
            max_find_cnt -= 1
            # 二值化图像
            _, binary = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY)

            # 查找轮廓
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # 有概率找不到轮廓
            if not contours:
                continue
                raise ValueError("未找到任何轮廓，请检查图像和阈值设置")
                # self_blood = 0
                # for self_bd_num in self.gray[(self.gray.shape[0]) // 2]: # 取中间这一行值作为血量计算
                #     if self.blood_gray_min <= self_bd_num <= self.blood_gray_max:
                #         self_blood += 1
                # print('total_length:%d' % total_length)
                # return (self_blood / total_length) * 100
            
            # 血条是最大的白色区域
            max_contour = max(contours, key=cv2.contourArea)

            # 获取血条的边界框
            x, y, w, h = cv2.boundingRect(max_contour)

            # 计算血量百分比
            
            current_health_length = w
            health_percentage = (current_health_length / total_length) * 100
            return health_percentage
        return 0
    
class EnergyWindow(BloodWindow):
    def __init__(self, sx, sy, ex, ey):
        super().__init__(sx, sy, ex, ey)
        # 剩余体力的灰度值范围
        self.blood_gray_max = 165
        self.blood_gray_min = 135

def get_self_blood_window():
    # return BloodWindow(210, 980, 572, 995)
    return BloodWindow(210, 980, 360, 995)

# 体力值
def get_self_energy_window():
    return EnergyWindow(210, 1015, 350, 1023)

def get_boss_blood_window():
    return BloodWindow(685, 912, 1260, 924)

def get_main_screen_window():
    # 主要窗口, 不收集全屏数据, 只关心能看到自己和boss这部分画面, 减少训练量
    return GrayWindow(600, 300, 1400, 900)
    return GrayWindow(600, 0, 1500, 1000)

init_self_blood = get_self_blood_window().blood_count()
init_medicine_nums = 4 