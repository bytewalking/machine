# machine
项目名称：基于机器视觉柔性加工辅助系统  
开发语言：python2.7  
图像处理工具：openCV  
图像界面开发工具：TKinter  
开发环境数据库：sqlite3
当前版本：1.5  
上一版本完成日期：2018/5/13  

## 主要功能
* 从摄像头获取图片
* 识别出图片的轮廓
* 对轮廓相似的图片进行匹配
* 识别标记点，在其它图片中对标记点进行还原
* 将像素坐标转换成厘米坐标

### 登录页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/index.png)  
验证完账号密码后可以进入系统

### 主页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/home.png)  
系统主页面  
在运行前可以先打开测试按钮进行测试，测试所得信息会在控制台输出，会得到图像匹配率、标记点坐标、匹配成功图形的序号。图形的序号会被自动标记。

### 设置页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/setting.png)  
系统设置页面  
对主页面的图像处理程序进行设置，各种参数会影响到匹配结果。如果不会设置，可以选择默认选项。保存后的参数会以配置文件的方式存储。

### 摄像头页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/camera.png)  
摄像头设置页面  
可以选择笔记本自带摄像头或其它摄像头。因为tkinter库里没有视频模块，所有我自己写这个功能。获取视频时，我采用了多线程的方式来实现实时视频的效果，但python的多线程优化很差，将来打算用其它方式实现实时视频。

### 校准页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/check_setting.png)  
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/check_setting2.png)  
用来校准的图片一定要是两个不相连的物体。也可以使用默认的图片，只需手动输入物理距离，系统便可以自动计算出物体间的像素距离、物理距离、图片大小等数据。用来完成坐标换算。

### 标记页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/point_setting.png)  
在标记页面选择待加工点后，便可以回到主页面进行加工点坐标还原测试。机器学习的功能正在努力学习中，将来打算加入这部分功能，用来帮助系统判断加工物体是否符合要求。

### 运行页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test1.png)  
系统会找到物体轮廓，在物体上找出做小外接矩形，以此来建立坐标系。然后以标记页面得到的坐标为目标，在这张图片上找到相应的位置。
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test2.png)  
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test3.png)  
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test4.png)  

