#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年4月27日
@author: Irony."[讽刺]
@site: irony.iask.in
@email: 892768447@qq.com
@file: player3.py
@description: 
'''
import traceback

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2015 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

class LolitaPlayer(QMediaPlayer):
    """控制萝莉声音"""

    def __init__(self, playList = [], ddir = "data", parent = None):
        super(LolitaPlayer, self).__init__(parent)
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
            super(LolitaPlayer, self).play()    # 播放一次