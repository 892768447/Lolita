#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年4月27日
@author: Irony."[讽刺]
@site: irony.iask.in
@email: 892768447@qq.com
@file: player2.py
@description: 
'''
import traceback

from PyQt4.QtCore import QUrl
from PyQt4.phonon import Phonon


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2015 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

class LolitaPlayer(object):
    """控制萝莉声音"""

    def __init__(self, playList = [], ddir = "data"):
        self._currentIndex = 0
        try:
            self._playList = playList
            # 播放列表
            self.playList = [Phonon.MediaSource(QUrl(item[1].format(DATA_DIR = ddir))) for item in self._playList]
            # 播放器
            self.player = Phonon.createPlayer(Phonon.MusicCategory)
            self.player.setTickInterval(1000)
        except Exception as e:
            traceback.print_exc(e)

    def __del__(self):
        if hasattr(self, "playList"):
            del self.playList
        if hasattr(self, "player"):
            del self.player

    def currentIndex(self):
        return self._currentIndex

    def mediaCount(self):
        if hasattr(self, "playList"):
            return len(self.playList)
        return 0

    def setCurrentIndex(self, i):
        self._currentIndex = i

    def getText(self, i):
        """获取当前歌曲对应的文字"""
        if hasattr(self, "_playList"):
            try: return self._playList[i][0]
            except Exception as e: traceback.print_exc(e)
        return ""

    def play(self, i):
        """播放指定的歌曲"""
        if hasattr(self, "playList") and hasattr(self, "player"):
            self.player.stop()
            self.setCurrentIndex(i)
            self.player.setCurrentSource(self.playList[i])    # 切换到第几首
            self.player.play()    # 播放一次

    def stop(self):
        if hasattr(self, "player"):
            self.player.stop()
