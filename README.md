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
在运行前可以先打开测试按钮进行测试，测试所得信息会在控制台输出

### 设置页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/setting.png)  
系统设置页面  
对主页面的图像处理程序进行设置，各种参数会影响到匹配结果。如果不会设置，可以选择默认选项

### 摄像头页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/camera.png)  
摄像头设置页面

### 校准页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/check_setting.png)  
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/check_setting2.png)  

### 标记页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/point_setting.png)  

### 运行页面
- - -
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test1.png)  
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test2.png)  
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test3.png)  
![picture not loaded](https://github.com/SputnikPH/machine/blob/master/show/test4.png)  
