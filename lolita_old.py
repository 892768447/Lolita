#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年4月25日
@author: Irony."[讽刺]
@site: irony.iask.in
@email: 892768447@qq.com
@file: lolita.py
@description: 可拖动小萝莉
'''

from PyQt5.Qt import Qt
from PyQt5.QtCore import QUrl, QPoint
from PyQt5.QtGui import QImage, QMovie
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QLabel, QToolTip
import json
import sys, os
import traceback


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2015 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

class LolitaPlayer(QMediaPlayer):
    """控制萝莉声音"""

    def __init__(self, playList = [], ddir = "data", parent = None):
        """
        @param dfile: 萝莉的音乐配置文件
        """
        QMediaPlayer.__init__(self, parent)
        # super(LolitaMusic, self).__init__(parent)
        try:
            # 播放列表
            self.playList = QMediaPlaylist(parent)
            # 设置只播放一次
            self.playList.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
            # 读取配置文件中的音乐路径
            self._playList = playList
            # 添加到列表里
            self.playList.addMedia([QMediaContent(QUrl(item[1].format(DATA_DIR = ddir))) for item in self._playList])
            self.playList.setCurrentIndex(0)

            # 设置播放列表
            self.setPlaylist(self.playList)
            # 设置音量
            self.setVolume(100)
        except Exception as e:
            traceback.print_exc(e)

    def __del__(self):
        if hasattr(self, "playList"):
            del self.playList

    def currentIndex(self):
        if hasattr(self, "playList"):
            return self.playList.currentIndex()
        return 0

    def mediaCount(self):
        if hasattr(self, "_playList"):
            return len(self._playList)
        return 0

    def setCurrentIndex(self, i):
        if hasattr(self, "playList"):
            self.playList.setCurrentIndex(i)

    def getText(self, i):
        """获取当前歌曲对应的文字"""
        if hasattr(self, "_playList"):
            try: return self._playList[i][0]
            except Exception as e: traceback.print_exc(e)
        return ""

    def play(self, i):
        """播放指定的歌曲"""
        if hasattr(self, "playList"):
            self.playList.setCurrentIndex(i)    # 切换到第几首
            QMediaPlayer.play(self)    # 播放一次

    def stop(self):
        QMediaPlayer.stop(self)

class Lolita(QLabel):
    """小萝莉"""

    def __init__(self, ddir = "data", parent = None):
        QLabel.__init__(self, parent)
        # super(Lolita, self).__init__(parent)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框,不在任务栏显示
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)

        self.canPlay = True
        self.moveCanPlay = True    # 移动的时候可播放,用于控制一次
        self.cindex = 0    # 当前的歌曲序号为0
        self.init(ddir)

    def init(self, ddir):
        """加载lolita.dat配置"""
        try:
            conf = json.loads(open(ddir + "/lolita.dat", "rb").read().decode())
            normal = conf.get("normal", "").format(DATA_DIR = ddir)
            move = conf.get("move", "").format(DATA_DIR = ddir)
            hover = conf.get("hover", "").format(DATA_DIR = ddir)
            press = conf.get("press", "").format(DATA_DIR = ddir)

            image = QImage(normal)
            self.resize(image.size())    # 设置窗口的大小
            self.setMinimumSize(image.size())
            self.setMaximumSize((image.size()))
            del image

            self.movies = {
                "normal": QMovie(normal),    # 普通
                "move": QMovie(move),    # 移动
                "hover": QMovie(hover),    # 悬停(会动)
                "press": QMovie(press),    # 按下
            }

            self.setMovie(self.movies.get("normal")).start()    # 默认显示

            # 声音播放列表
            playList = conf.get("playList", [])
            self.player = LolitaPlayer(playList, ddir)
            self.player.setCurrentIndex(0)
        except Exception as e:
            self.close()
            traceback.print_exc(e)

    def exit(self):
        if hasattr(self, "movies"):
            for _, movie in self.movies.items():
                movie.stop()
            del self.movies
        if hasattr(self, "player"):
            self.player.stop()
            del self.player
        self.setMovie(None)
        # 如果主窗口加载该部件则不要调用exit函数。只调用close
        # 如果是该文件单独演示则调用exit
        QApplication.instance().quit()

    def setMovie(self, movie):
        QLabel.setMovie(self, movie)
        return movie

    def _change_image_(self, name):
        if not hasattr(self, "movies"): return
        if name not in self.movies: return
        _movies = self.movies.copy()
        _movie = _movies.pop(name)
        for _, movie in _movies.items(): movie.stop()    # 停止其他的
        _movie.stop()
        self.setMovie(_movie).start()    # 切换到这个

    def mousePressEvent(self, event):
        """鼠标按下"""
        if event.button() == Qt.LeftButton:
            self.moveCanPlay = True
            self._change_image_("press")
            self.mpos = event.globalPos() - self.pos()    # 记录坐标
        QLabel.mousePressEvent(self, event)
        # super(Lolita, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """鼠标拖动"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.mpos)
            self.canPlay = False
            if self.moveCanPlay:
                self.moveCanPlay = False
                self.player.stop()
                self.player.play(0)    # 播放drag的声音
            self._change_image_("move")
        QLabel.mouseMoveEvent(self, event)
        # super(Lolita, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        if event.button() == Qt.LeftButton:
            self._change_image_("normal")
            self.moveCanPlay = False
            if not self.canPlay:    # 移动了,不播放
                self.canPlay = True
                return
            # 只是点击才播放
            self.cindex = self.cindex + 1
            # 当当前序号大于了排除drag的个数或者是当前序号为drag的序号0时,改为1
            if self.cindex > self.player.mediaCount() - 1: self.cindex = 1
            self.player.play(self.cindex)    # 播放
            text = self.player.getText(self.cindex)
            QToolTip.showText(self.pos() + QPoint(0, -50), text, self)
        QLabel.mouseReleaseEvent(self, event)
        # super(Lolita, self).mouseReleaseEvent(event)

    def enterEvent(self, event):
        """鼠标进入"""
        self._change_image_("hover")
        return QLabel.enterEvent(self, event)

    def leaveEvent(self, event):
        """鼠标离开"""
        self._change_image_("normal")
        return QLabel.leaveEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
            self.exit()
        # 如果主窗口加载该部件则不要调用exit函数。只调用close
        # 如果是该文件单独演示则调用exit
        QLabel.mouseDoubleClickEvent(self, event)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Lolita(ddir = os.path.abspath("data"))
    w.show()
    w.setStyleSheet("""
    QToolTip {
        border: 2px solid white;
        padding: 1px;
        border-radius: 3px;
        opacity: 200;
        background-color: white;
    }
    """)
    sys.exit(app.exec_())
