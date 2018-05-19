# coding=utf-8\

# 多图形下的圆形匹配算法
import cv2
import numpy as np
import ConfigParser
import math
import os

class  imageProcessing():
    def __init__(self):
        # 初始化,方便自己查看
        self.matchingmsensitivity = None
        self.imagereadingmode = None
        self.contourretrievalmode = None
        self.contourapproximationmethod = None
        self.valueprocessingmethod = None
        self.newvalvevalueaftertreatment = None
        self.thethresholdoftheclassification = None
        self.tagcolor = None
        self.thethicknessofthetag = None

        # 预留变量名
        self.customtargetimageaddress = None
        self.customcolorrgb = None

        self.confinit()

    def confinit(self):
        # 读取配置文件
        cf = ConfigParser.ConfigParser()
        cf.read("setting.ini")
        temp = cf.get("set", "imagereadingmode")
        if temp == '以彩色模式读取':
            self.imagereadingmode = 1
        elif temp == '以灰度模式读取':
            self.imagereadingmode = 0
        else:
            self.imagereadingmode = -1
        temp = cf.get("set", "contourretrievalmode")
        if temp == '建立一个等级树结构的轮廓':
            self.contourretrievalmode = 3
        elif temp == '只检测外轮廓':
            self.contourretrievalmode = 0
        elif temp == '检测的轮廓不建立等级关系':
            self.contourretrievalmode = 1
        else:
            self.contourretrievalmode = 2
        temp = cf.get("set", "contourapproximationmethod")
        if temp == '存储所有的轮廓点':
            self.contourapproximationmethod = 1
        else:
            self.contourapproximationmethod = 2
        temp = cf.get("set", "valueprocessingmethod")
        if temp == 'BINARY_INV':
            self.valueprocessingmethod = 1
        elif temp == 'BINARY':
            self.valueprocessingmethod = 0
        elif temp == 'TRUNC':
            self.valueprocessingmethod = 2
        elif temp == 'TOZERO':
            self.valueprocessingmethod = 3
        else:
            self.valueprocessingmethod = 4

        self.newvalvevalueaftertreatment = cf.getint("set", "newvalvevalueaftertreatment")
        self.thethresholdoftheclassification = cf.getint("set", "thethresholdoftheclassification")

    def patterMatching(self, target, testImage):

        # 读取图片
        targetImg = cv2.imread(target, self.imagereadingmode)
        contrastImg = cv2.imread(testImage, self.imagereadingmode)

        # 阀值处理
        targetRet, targetBinary = cv2.threshold(cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY), 127, 255,
                                                cv2.THRESH_BINARY_INV)
        contrastImgRet, contrastImgBinary = cv2.threshold(cv2.cvtColor(contrastImg, cv2.COLOR_BGR2GRAY),
                                                          self.newvalvevalueaftertreatment,
                                                          self.thethresholdoftheclassification,
                                                          self.valueprocessingmethod)

        # 识别轮廓
        targetImage, targetContours, targetHierarchy = cv2.findContours(targetBinary, cv2.RETR_EXTERNAL,
                                                                        self.contourapproximationmethod)
        contrastmage, contrastContours, contrastHierarchy = cv2.findContours(contrastImgBinary,
                                                                             self.contourretrievalmode,
                                                                             self.contourapproximationmethod)

        cnt1 = targetContours[0]
        right = []
        ret = []

        # 结果处理
        for i in range(0, len(contrastContours)):
            cnt2 = contrastContours[i]
            ret.append(cv2.matchShapes(cnt1, cnt2, 1, 0.0))
            # print '第%d号图的匹配度：%f' % (i, ret)
            if (ret[i] < 0.01):
                right.append(i)
                print '匹配的圆形为：', i, '号'

        return right, ret

    def imageMark(self, testImage):
        # 这段程序的作用是给每个轮廓做上标记
        contrastImg = cv2.imread(testImage, self.imagereadingmode)
        contrastImgRet, contrastImgBinary = cv2.threshold(cv2.cvtColor(contrastImg, cv2.COLOR_BGR2GRAY),
                                                          self.newvalvevalueaftertreatment,
                                                          self.thethresholdoftheclassification,
                                                          self.valueprocessingmethod)
        contrastmage, contrastContours, contrastHierarchy = cv2.findContours(contrastImgBinary,
                                                                             self.contourretrievalmode,
                                                                             self.contourapproximationmethod)

        # 算出质心
        def Centroid(cnt):
            M = cv2.moments(cnt)
            try:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return (cx, cy)
            except:
                return None

        # 写上标签
        def Mark(centroid, num):

            cv2.putText(contrastImg, str(num), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        for i in range(0, len(contrastContours)):
            cnt = contrastContours[i]
            flag = Centroid(cnt)
            if flag == None:
                pass
            else:
                Mark(flag, i)

        cv2.imwrite(os.getcwd()+'\img\Mark.jpg', contrastImg)
        print '标记完成'

    def takePhoto(self):
        pass

    def distancecheck(self,testImage):
        contrastImg = cv2.imread(testImage, self.imagereadingmode)
        contrastImgRet, contrastImgBinary = cv2.threshold(cv2.cvtColor(contrastImg, cv2.COLOR_BGR2GRAY),
                                                          self.newvalvevalueaftertreatment,
                                                          self.thethresholdoftheclassification,
                                                          self.valueprocessingmethod)
        contrastmage, contrastContours, contrastHierarchy = cv2.findContours(contrastImgBinary,
                                                                             cv2.RETR_EXTERNAL,
                                                                             self.contourapproximationmethod)

        # 算出质心
        def Centroid(cnt):
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy)

        x1, y1 = Centroid(contrastContours[0])
        x2, y2 = Centroid(contrastContours[1])

        return math.sqrt(math.pow(abs(y2-y1), 2)+math.pow(abs(x2-x1), 2))

    def dotest(self, testImage, page):
        img = cv2.imread(testImage)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, self.newvalvevalueaftertreatment,
                                    self.thethresholdoftheclassification,
                                    cv2.THRESH_BINARY_INV)

        image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
        cv2.imwrite(os.getcwd()+'\img\Result'+str(page)+'.jpg', img)

        # 算出质心
        def Centroid(cnt):
            M = cv2.moments(cnt)
            try:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return (cx, cy)
            except:
                return None

        return Centroid(contours[0])

    def markMost(self, testImage, page):
        img = cv2.imread(testImage)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray,
                                    self.newvalvevalueaftertreatment,
                                    self.thethresholdoftheclassification,
                                    cv2.THRESH_BINARY_INV)

        image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]

        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

        cv2.circle(img, leftmost, 10, (0, 0, 255), -1)
        cv2.circle(img, rightmost, 10, (0, 0, 255), -1)
        cv2.circle(img, topmost, 10, (0, 0, 255), -1)
        cv2.circle(img, bottommost, 10, (0, 0, 255), -1)
        cv2.imwrite(os.getcwd()+'\img\RmustResult'+str(page)+'.jpg', img)
        print leftmost

        return [leftmost, rightmost, topmost, bottommost]

    # 算出高
    def height(self, a, b, bottom):
        p = (a+b+bottom)/2
        s = math.sqrt(p*(p-a)*(p-b)*(p-bottom))
        return 2*s/bottom

    #算出两点距离
    def distance(self, a1, b1, a2, b2):
        return math.sqrt(math.pow(abs(b2 - b1), 2) + math.pow(abs(a2 - a1), 2))

    # 注：各参数已经写死，后期记得改回来
    def boundingRectangle(self, test_image, x, y):

        img = cv2.imread(test_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnt = contours[0]

        rect = cv2.minAreaRect(cnt)
        # rect得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # box获取最小外接矩形的4个顶点
        # box = np.int0(box)
        traget_x = self.height(self.distance(x, y, box[2][0], box[2][1]),
                               self.distance(x, y, box[3][0], box[3][1]),
                               self.distance(box[2][0], box[2][1], box[3][0], box[3][1]))
        traget_y = self.height(self.distance(x, y, box[0][0], box[0][1]),
                               self.distance(x, y, box[3][0], box[3][1]),
                               self.distance(box[0][0], box[0][1], box[3][0], box[3][1]))

        # 返回距宽、高的距离和矩形宽高
        return traget_x, traget_y, rect[1][0], rect[1][1]

    def reduction_of_coordinates(self, test_image, org_x, org_y, or_width, or_height, page):
        # print ('org_x = %d org_y = %d' % (org_x, org_y))
        img = cv2.imread(test_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnt = contours[0]

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        org_x = org_x*rect[1][0]/or_width
        org_y = org_y*rect[1][0]/or_width
        # 获得3点坐标
        x0, y0 = box[0][0], -box[0][1]
        x2, y2 = box[2][0], -box[2][1]
        x3, y3 = box[3][0], -box[3][1]
        # print ('x0=%d y0=%d x2=%d y2=%d x3=%d y3=%d' % (x0, y0, x2, y2, x3, y3))
        # 方程1(b3-b2)
        a1 = y3-y2
        b1 = x2-x3
        oc1 = y2 * (x3 - x2) - (y3 - y2) * x2
        c1 = (oc1 - org_x * (math.sqrt(a1 * a1 + b1 * b1)))
        # print 'a1=%d, b1=%d, c1=%d' % (a1, b1, c1)
        # 方程2(b0-b3)
        a2 = y3-y0
        b2 = x0-x3
        oc2 = y0 * (x3 - x0) - (y3 - y0) * x0
        c2 = oc2 + org_y * (math.sqrt(a2 * a2 + b2 * b2))
        # print 'a2=%d, b2=%d, c2=%d' % (a2, b2, c2)

        final_x = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1)
        final_y = (a1 * c2 - a2 * c1) / (a1 * b2 - a2 * b1)

        # final_x = final_x*rect[1][0]/or_width
        # final_y = final_y*rect[1][0]/or_width
        one = tuple([int(final_x), int(final_y)])
        cv2.circle(img, one, 5, (0, 255, 0), -1)
        cv2.imwrite(os.getcwd() + '\img\cash\RmustResult' + str(page) + '.jpg', img)
        print '标记完成'
        print 'final_x=%d final_y=%d' % (final_x, final_y)
        return final_x, final_y

