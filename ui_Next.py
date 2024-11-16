# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Next.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)
import Next_rc

class Ui_Start(object):
    def setupUi(self, Start):
        if not Start.objectName():
            Start.setObjectName(u"Start")
        Start.resize(791, 536)
        icon = QIcon()
        icon.addFile(u":/icon/icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Start.setWindowIcon(icon)
        self.label = QLabel(Start)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 90, 301, 91))
        font = QFont()
        font.setFamilies([u"\u971e\u9e5c\u65b0\u6670\u9ed1"])
        font.setPointSize(24)
        self.label.setFont(font)
        self.label_2 = QLabel(Start)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(240, 90, 101, 21))
        font1 = QFont()
        font1.setFamilies([u"\u971e\u9e5c\u65b0\u6670\u9ed1"])
        self.label_2.setFont(font1)
        self.label_3 = QLabel(Start)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 40, 61, 61))
        self.label_3.setPixmap(QPixmap(u":/icon/icon.png"))
        self.label_3.setScaledContents(True)
        self.label_4 = QLabel(Start)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(50, 180, 201, 41))
        font2 = QFont()
        font2.setFamilies([u"\u971e\u9e5c\u65b0\u6670\u9ed1"])
        font2.setPointSize(11)
        self.label_4.setFont(font2)

        self.retranslateUi(Start)

        QMetaObject.connectSlotsByName(Start)
    # setupUi

    def retranslateUi(self, Start):
        Start.setWindowTitle(QCoreApplication.translate("Start", u"\u5c0f\u6811\u58c1\u7eb8 Next", None))
        self.label.setText(QCoreApplication.translate("Start", u"\u5c0f\u6811\u58c1\u7eb8 Next", None))
        self.label_2.setText(QCoreApplication.translate("Start", u"\u03b1 test", None))
        self.label_3.setText("")
        self.label_4.setText(QCoreApplication.translate("Start", u"\u4ece\u5de6\u4fa7\u9009\u62e9\u4e00\u4e2a\u9875\u9762\u4ee5\u5f00\u59cb", None))
    # retranslateUi

