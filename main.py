'''
Author: shu-shu-1 3458222@qq.com
Date: 2024-10-26 17:07:33
LastEditors: shu-shu-1 3458222@qq.com
LastEditTime: 2024-11-16 13:57:33
FilePath: \A小树壁纸\7.0\main.py
Description: 

Copyright (c) 2024 by shu-shu-1 3458222@qq.com, All Rights Reserved. 
'''
# ExceedShareServer.exe
from pathlib import Path
import shutil
import subprocess
import threading
import time
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from PySide6.QtWidgets import QApplication,QHBoxLayout,QFrame,QSystemTrayIcon,QLabel
from PySide6.QtGui import QIcon,QFont,QPixmap
from PySide6.QtCore import *
from ui_Next import Ui_Start
import sys
import requests
import os
import io
import json
from PIL import Image

LONG_VER="Core.0.1.0.Alpha.20241116.2-Internal"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
class Feature:
    ...

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(SubtitleLabel(text))

        # 创建按钮并绑定 show_war 方法
        self.button = PushButton(text="进行提示测试")
        self.button.clicked.connect(self.show_war)  # 绑定按钮点击事件
        self.layout().addWidget(self.button)

    def show_war(self):
        InfoBar.info(
            title='info测试',
            content=f'测试消息',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
        InfoBar.warning(
            title='warning测试',
            content=f'测试消息',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
        InfoBar.error(
            title='error测试',
            content=f'测试消息',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
        InfoBar.success(
            title='success测试',
            content=f'测试消息',
            orient=Qt.Horizontal,
            isClosable=True,    
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='恭喜',
            content="消息弹窗测试执行完毕！",
            target=self.button,
            parent=self,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP
        )


class BingWallpaperThread(QThread):
    # 定义信号，用于在下载完成时发送结果
    finished = Signal(list)

    def __init__(self):
        super().__init__()
    def run(self):
        try:
            headers={
                'Content-Type':'application/json; charset=utf-8',
                'user-agent':UA
            }
            response = requests.get(
                "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=zh-CN",
                headers=headers, #请求头
            )
            response = json.loads(response.text) #转化为json
            imgList = []
            for item in response['images']:
                imgList.append({
                    'copyright':item['copyright'], #版权
                    'date':item['enddate'][0:4]+'-'+item['enddate'][4:6]+'-'+item['enddate'][6:], #时间
                    'urlbase':'https://cn.bing.com'+item['urlbase'], #原始图片链接
                    'url':'https://cn.bing.com'+item['url'], #图片链接
                    'title':item['title'], #标题
                    'copyrightlink':item['copyrightlink'], #版权链接
                })
            self.finished.emit(imgList) #返回一个数据数组
        except:
            self.finished.emit(["Error"])

class MainWindow(QFrame):

    def __init__(self):
        super().__init__()
        
        # 创建 Feature 实例
        self.feature = Feature()

        # 使用ui文件导入定义界面类
        self.ui = Ui_Start()
        # self.ui.spinner = IndeterminateProgressRing(self)

        # 调整大小
        # self.ui.spinner.setFixedSize(30, 30)

        # # 调整厚度
        # self.ui.spinner.setStrokeWidth(4)
        # self.ui.spinner.setGeometry(QRect(50, 350, 30, 30))

        self.ring = ProgressRing(self)
        # 设置进度环取值范围和当前值
        self.ring.setRange(0, 110)
        self.ring.setValue(0)
        self.ring.setGeometry(QRect(50, 350, 30, 30))
        self.ring.setFixedSize(30, 30)
        self.ring.setStrokeWidth(4)


        self.ui.infolabel = QLabel(self)
        self.ui.infolabel.setGeometry(QRect(100, 350, 200, 30))
        self.ui.infolabel.setText("正在从壁纸源获取数据...")
        font1 = QFont()
        font1.setFamilies([u"\u971e\u9e5c\u65b0\u6670\u9ed1"])
        font1.setPointSize(12)
        self.ui.infolabel.setFont(font1)

        self.today_view = ImageLabel(self)

        # 按比例缩放到指定高度
        

        # 圆角
        self.today_view.setBorderRadius(8, 8, 8, 8)
        self.today_view.setGeometry(QRect(0, 450, 200, 200))


        self.ui.download_button = PushButton(text="开始下载", parent=self)
        self.ui.download_button.setGeometry(QRect(300, 350, 100, 30))
        self.ui.download_button.clicked.connect(self.start_download)

        self.ui.test_text = QLabel(self)
        self.ui.test_text.setGeometry(QRect(0, 320, 300, 200))
        self.ui.test_text.setWordWrap(True)  # 启用自动换行
        self.ui.test_text.setText("数据获取中")
        font1 = QFont()
        font1.setFamilies([u"\u971e\u9e5c\u65b0\u6670\u9ed1"])
        font1.setPointSize(12)        

        self.ui.setupUi(self)

        self.setObjectName("home")
    def start_download(self):
        self.download_thread = BingWallpaperThread()
        self.download_thread.finished.connect(self.on_download_finished)
        self.ring.setValue(1)
        self.download_thread.start()

        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='测试启动成功',
            content="任务已经开始执行",
            target=self.ui.download_button,
            parent=self,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP
        )
        

    def on_download_finished(self, success):
        self.ring.setValue(10)
        if success and success[0] and "url" in success[0]:
            try:
                response = requests.get(success[0]["url"], stream=True)
                if response.status_code == 200:
                    total_length = response.headers.get('content-length')
                    if total_length is None:  # 如果没有 Content-Length，就无法显示进度
                        total_length = 1024*1024
                    else:
                        total_length = int(total_length)
                    
                    bytes_downloaded = 0
                    buffer = io.BytesIO()

                    for data in response.iter_content(chunk_size=1024):
                        bytes_downloaded += len(data)
                        buffer.write(data)
                        
                        # 计算并更新进度条
                        progress = int((bytes_downloaded / total_length) * 100) + 10
                        self.ring.setValue(progress)

                    # 使用 Pillow 打开二进制流来判断图片格式
                    buffer.seek(0)
                    image = Image.open(buffer)
                    format = image.format.lower()  # 获取图片格式，并转换为小写

                    # 保存图片到本地
                    image_path = f"./temp/today.{format}"
                    with open(image_path, 'wb') as file:
                        buffer.seek(0)
                        shutil.copyfileobj(buffer, file)

                    # 显示图片
                    pixmap = QPixmap(image_path)
                    self.today_view.setImage(pixmap)
                    self.today_view.scaledToHeight(200)


                    # 完成下载，更新进度条至100%
                    self.ring.setValue(110)

                    # 显示成功信息
                    InfoBar.success(
                        title='数据获取完成',
                        content=f'测试执行完成，成功获取数据',
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )
                    self.ui.test_text.setText(f"成功获取数据：{success[0]['url']}，格式：{format}")
                else:
                    # 处理请求失败的情况
                    InfoBar.error(
                        title='数据获取失败',
                        content=f'测试执行完成，数据获取失败：状态码 {response.status_code}',
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )
                    self.ui.test_text.setText("数据获取失败")
                    self.ring.setValue(0)
            except Exception as e:
                # 处理异常
                InfoBar.error(
                    title='数据获取异常',
                    content=f'测试执行过程中发生异常：{str(e)}',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                self.ui.test_text.setText("数据获取异常")
                self.ring.setValue(0)
        else:
            # 处理 success 数据不正确的情况
            InfoBar.error(
                title='数据获取完成',
                content=f'测试执行完成，数据获取失败',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            self.ui.test_text.setText("数据获取失败")
            self.ring.setValue(0)
        
class TodayWidget(QFrame):

    def __init__(self):
        super().__init__()
        
class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        self.homeInterface = MainWindow()
        self.todayInterface = Widget('每日一图', self)
        # self.videoInterface = Widget('Video Interface', self)
        self.settingInterface = Widget('Setting Interface', self)
        self.albumInterface = Widget('Album Interface', self)
        self.albumInterface1 = Widget('Album Interface 1', self)
        self.favoriteInterface = Widget('Favorite Interface', self)

        
        self.initWindow()
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        self.initNavigation()
        # self.splashScreen.finish()
        # 设置系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./icon.png"))  # 替换为你的图标路径
        
        # 创建托盘图标右键菜单
        tray_menu = RoundMenu()
        tray_menu.addActions([
            Action(FIF.LINK, '显示窗口', triggered=self.showNormal),
            Action(FIF.EMBED, '退出', triggered=self.quit_application),
        ])

        # 将右键菜单设置给托盘图标
        self.tray_icon.setContextMenu(tray_menu)
        
        # 连接托盘图标激活信号
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        # 显示托盘图标
        self.tray_icon.show()
        
        #TODO: 重写关闭事件

        # self.old_closeEvent = self.closeEvent
        # self.closeEvent = self.new_closeEvent

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()

    def new_closeEvent(self, event):
        # 当用户尝试关闭窗口时，将窗口隐藏并阻止默认关闭行为
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()

    def quit_application(self):
        self.tray_icon.hide()  # 隐藏托盘图标
        QApplication.quit()  # 关闭应用程序
    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')
        self.addSubInterface(self.todayInterface, FIF.HISTORY, '每日一图')
        self.addSubInterface(self.albumInterface, FIF.ALBUM, '壁纸源')
        self.addSubInterface(self.albumInterface1, FIF.ALBUM, '二次元源', parent=self.albumInterface)

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.favoriteInterface, FIF.HEART, '收藏')


        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

        InfoBar.warning(
            title='警告',
            content="早期测试版仅供展示和测试",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )
        InfoBar.info(
            title='版本号',
            content=LONG_VER,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )
        self.splashScreen.finish()
        

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/icon/icon.png'))
        self.setWindowTitle(f'小树壁纸 Next {LONG_VER}')


if __name__ == '__main__':
    config_path = Path('./config')
    # print(os.path.exists("./config/process.json"))
    if os.path.exists("./config/process.json") is not True:
        try:
            config_path.mkdir()
            print(f"文件夹 '{config_path}' 创建成功。")
        except FileExistsError:
            print(f"文件夹 '{config_path}' 已经存在。")
    temp_path = Path('./temp')
    if os.path.exists("./temp") is not True:
        try:
            temp_path.mkdir()
            print(f"文件夹 '{temp_path}' 创建成功。")
        except FileExistsError:
            print(f"文件夹 '{temp_path}' 已经存在。")

    #     with open("./config/process.json", "w+", encoding="utf-8") as f:
    #         json.dump(Default_process_config, f, ensure_ascii=False, indent=4)
    #     process_config = Default_process_config
    # else: 
    #     with open("./config/process.json", "r", encoding="utf-8") as f:
    #         process_config = json.load(f)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
