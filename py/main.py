#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @Time    : 2025/7/18 17:36
# @Author  : WXY
# @File    : main.py
# @PROJECT_NAME: audiosplit_gui
# @PRODUCT_NAME: PyCharm
# -------------------------------------------------------------------------------
import sys
import os

# 添加py目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
py_dir = os.path.join(current_dir, "py")
sys.path.insert(0, py_dir)

from PySide6.QtWidgets import QApplication
from py.SplashScreen import SplashScreen
from py.GlobalExceptionHandler import GlobalExceptionHandler
from py.SingleInstanceManager import SingleInstanceManager
from py.LoggerManager import logger_manager
from utils import show_error,APPNAME
from gui import resource_rc

def main():
    """主函数"""
    try:
        # 创建应用程序实例
        app = QApplication(sys.argv)
        # 设置中文语言环境 - 必须在 QApplication 创建后立即设置
        from PySide6.QtCore import QLocale, QTranslator, QLibraryInfo

        locale = QLocale(QLocale.Language.Chinese, QLocale.Country.China)
        QLocale.setDefault(locale)

        translator = QTranslator()
        qt_translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if translator.load(locale, "qtbase", "_", qt_translations_path):
            app.installTranslator(translator)
        else:
            if translator.load(locale, "qt", "_", qt_translations_path):
                app.installTranslator(translator)
        # 设置应用程序信息
        # app.setApplicationName("AudioSplit GUI")
        # app.setApplicationVersion("1.0.0")
        # app.setOrganizationName("WXY")

        # 初始化单例管理器
        instance_manager = SingleInstanceManager(APPNAME)
        # if not instance_manager.is_single_instance():
        if instance_manager.is_running():
            # print("应用程序已在运行中...")
            show_error(None,"提示", "应用程序已运行。")
            return 0

        # 启动单例服务器
        if not instance_manager.start_server():
            show_error(None,"提示", "无法启动单例服务器")
            return 1

        # 设置全局异常处理器
        exception_handler = GlobalExceptionHandler()
        sys.excepthook = exception_handler.handle_exception

        # 初始化日志管理器
        logger_manager.info("应用程序启动", "main")

        # 创建并显示启动界面
        splash = SplashScreen()

        # 连接单例管理器的信号到启动界面的置顶方法
        instance_manager.show_window_signal.connect(splash.bring_to_front)

        splash.show()

        # 运行应用程序
        result = app.exec()

        logger_manager.info("应用程序退出", "main")
        return result

    except Exception as e:
        print(f"应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())