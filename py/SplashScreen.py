#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @Time    : 2025/7/10 16:59
# @Author  : WXY
# @File    : SplashScreen
# @PROJECT_NAME: audiosplit_gui
# @PRODUCT_NAME: PyCharm
# -------------------------------------------------------------------------------
import sys
import os
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QTimer, QThread, Signal, Qt
from gui.splashscreen_ui import Ui_SplashScreen
from utils import setup_label_icon, VERSION
import AuthWindow
from SettingsManager import settings_manager
from AESEncrypt import aes_decrypt
from datetime import datetime, timedelta
from MainWindow import MainWindow
from LoggerManager import logger_manager

class ModelLoadWorker(QThread):
    """模型加载工作线程"""
    progress_updated = Signal(int)
    finished = Signal()

    def run(self):
        """模拟模型加载过程"""
        # 模拟加载过程，分多个阶段
        stages = [
            ("初始化环境", 20),
            ("加载配置文件", 40),
            ("检查模型资源", 60),
            ("加载AI模型", 80),
            ("完成初始化", 100)
        ]

        for stage_name, progress in stages:
            # 模拟每个阶段的加载时间
            logger_manager.debug(f"模型加载阶段: {stage_name} ({progress}%)", "splash_screen")
            self.msleep(500)  # 等待500毫秒
            self.progress_updated.emit(progress)

        logger_manager.info("模型加载完成", "splash_screen")
        self.finished.emit()

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        # with open("../gui/styles/splashscreen_ui.qss", "r", encoding="utf-8") as f:
        #     qss = f.read()
        # self.setStyleSheet(qss)
        # 设置窗口属性以支持圆角和透明背景
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        # # ✅ 在启动时就设置文件日志, 否则日志文件还没有准备好, 那么就不会写日志
        # try:
        #     from datetime import datetime
        #     today = datetime.now().strftime("%Y%m%d")
        #     log_file_path = os.path.join(os.getcwd(), f"audiosplit_{today}_debug.log")
        #     logger_manager.setup_file_logging(log_file_path, enable_debug=True)
        #     logger_manager.info("启动界面日志系统已初始化", "splash_screen")
        # except Exception as e:
        #     logger_manager.error(f"启动界面日志系统初始化失败: {e}", "splash_screen")
        # 确保模型目录存在, 如果没有就创建
        self.ensure_model_directory()
        # 初始化UI
        self.init_ui()

        # 初始化模型加载线程
        self.model_worker = ModelLoadWorker()
        self.model_worker.progress_updated.connect(self.update_progress)
        self.model_worker.finished.connect(self.on_loading_finished)

        # 授权检查完成标志
        self.auth_ready = False
        self.model_ready = False
        self.next_window_shown = False  # 防止重复调用标志位, 重复调用就会重复显示2个main窗口

        # 主窗口引用
        self.main_window = None
        self.auth_window = None

        # 启动加载过程
        self.start_loading()

    def bring_to_front(self):
        """将当前活动窗口置顶显示"""
        try:
            # 如果主窗口已经显示，则置顶主窗口
            if self.main_window and self.main_window.isVisible():
                self.main_window.bring_to_front()
                logger_manager.info("主窗口已置顶", "splash_screen")
            # 如果授权窗口正在显示，则置顶授权窗口
            elif self.auth_window and self.auth_window.isVisible():
                self.auth_window.raise_()
                self.auth_window.activateWindow()
                self.auth_window.setWindowState(
                    (self.auth_window.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive
                )
                # 在Windows上强制置顶
                self.auth_window.setWindowFlags(self.auth_window.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                self.auth_window.show()
                self.auth_window.setWindowFlags(self.auth_window.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
                self.auth_window.show()
                logger_manager.info("授权窗口已置顶", "splash_screen")
            # 否则置顶启动界面
            elif self.isVisible():
                self.raise_()
                self.activateWindow()
                self.setWindowState(
                    (self.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive
                )
                # 在Windows上强制置顶
                self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                self.show()
                self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
                self.show()
                logger_manager.info("启动界面已置顶", "splash_screen")
        except Exception as e:
            logger_manager.error(f"窗口置顶失败: {e}", "splash_screen")

    def show_main_window(self, is_trial_mode=False):
        """显示主窗口"""
        try:
            # 使用预导入的MainWindow，避免延迟导入
            self.main_window = MainWindow(is_trial_mode=is_trial_mode)
            self.main_window.show()
            logger_manager.info(f"主窗口显示完成", "splash_screen")

        except Exception as e:
            logger_manager.error(f"显示主窗口失败: {e}", "splash_screen")
            import traceback
            logger_manager.error(f"堆栈跟踪: {traceback.format_exc()}", "splash_screen")

    def init_ui(self):
        """初始化UI界面"""
        # 设置窗口图标 , 不用设置了, 因为把标题栏隐藏了
        # setup_window_icon(self)
        self.ui.versionLabel.setText(VERSION)
        # 设置logoLabel的图标
        setup_label_icon(self.ui.logoLabel)

        # 连接关闭按钮事件
        # self.ui.closeButton.clicked.connect(self.close_application)
        # 为QLabel添加鼠标点击事件（替换原来的clicked.connect）
        self.ui.closeButton.mousePressEvent = lambda \
            event: self.close_application() if event.button() == Qt.MouseButton.LeftButton else None
        # 初始化进度条
        self.ui.progressBar.setValue(0)

        # 设置初始状态文本（如果有statusLabel的话）
        # self.ui.statusLabel.setText("正在初始化...")

    def close_application(self):
        """关闭整个应用程序"""
        # 如果还在加载过程中，终止加载线程
        if self.model_worker.isRunning():
            self.model_worker.terminate()
            self.model_worker.wait()
        logger_manager.info("正在关闭应用程序...", "splash_screen")
        # 退出应用程序
        QApplication.quit()

    def start_loading(self):
        """开始加载过程"""
        logger_manager.info("启动界面开始加载过程", "splash_screen")
        # 同时启动授权检查和模型加载
        self.check_authorization()
        self.model_worker.start()

    def check_authorization(self):
        """检查授权状态"""
        self.auth_ready = True  # 直接返回授权有效
        self.check_ready_state()
        return
        # #machine_code, auth_time='2025-08-04 12:33:30', last_auth_code='cS/6Z5LN8200Reg8C1dY0hiubQDx+A0rs3vVv4bhyLutRpPr4PTjrfc9GJAVjWO4o8GYPOKfDU3aepgWIxIl0lFtBqefaJIv/MPEmN254Zc='
        # auth_time, last_auth_code = settings_manager.get_auth_info()
        # # 检查授权信息完整性
        # #if not machine_code or not auth_time or not last_auth_code:
        # if not auth_time or not last_auth_code:
        #     self.auth_ready = True  # 需要显示授权窗口
        #     self.check_ready_state()
        #     return
        #
        # try:
        #     # 第一次解密
        #     auth_code_one_de = aes_decrypt(last_auth_code)
        #     if auth_code_one_de is None:
        #         raise ValueError("第一次解密失败")
        #
        #     # 检查分隔后的元素数量
        #     auth_parts = auth_code_one_de.split("|")
        #     if len(auth_parts) != 2:
        #         raise ValueError("授权码格式错误")
        #
        #     auth_code_en = auth_parts[0]
        #     temp_time = auth_parts[1]
        #
        #     # 第二次解密
        #     auth_code = aes_decrypt(auth_code_en)
        #     if auth_code is None:
        #         raise ValueError("第二次解密失败")
        #
        #     # 解析内层授权码
        #     auth_code_parts = auth_code.split("|")
        #     if len(auth_code_parts) != 2:
        #         raise ValueError("内层授权码格式错误")
        #
        #     auth_code_machine = auth_code_parts[0]
        #     auth_code_day = auth_code_parts[1]
        #
        #     # 验证机器码
        #     current_machine_code = AuthWindow.AuthWindow.generate_machine_code_static()
        #     if current_machine_code and auth_code_machine.replace('-', '') != current_machine_code.replace('-', ''):
        #         raise ValueError("机器码不匹配")
        #
        #     # 检查授权天数
        #     auth_days = int(auth_code_day)
        #
        #     if auth_days == 0:
        #         # 无限制授权
        #         self.auth_ready = True
        #         self.check_ready_state()
        #         return
        #
        #     # 检查授权是否过期
        #     auth_datetime = datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S")
        #     expire_datetime = auth_datetime + timedelta(days=auth_days)
        #     current_datetime = datetime.now()
        #
        #     if current_datetime < auth_datetime or current_datetime > expire_datetime:
        #         raise ValueError("授权已过期或时间异常")
        #
        #     # 授权有效
        #     self.auth_ready = True
        #     self.check_ready_state()
        #
        # except Exception as e:
        #     logger_manager.warning(f"授权检查失败: {e}，将显示授权窗口", "splash_screen")
        #     self.auth_ready = True  # 需要显示授权窗口
        #     self.check_ready_state()

    def update_progress(self, value):
        """更新进度条"""
        self.ui.progressBar.setValue(value)

    def on_loading_finished(self):
        """模型加载完成"""
        self.model_ready = True
        self.check_ready_state()

    def check_ready_state(self):
        """检查是否所有准备工作都完成"""
        if self.auth_ready and self.model_ready and not self.next_window_shown:
            self.next_window_shown = True  # 设置标志位
            # 减少延迟时间，从500ms改为200ms
            QTimer.singleShot(200, self.show_next_window)

    def show_next_window(self):
        """显示下一个窗口"""
        # 授权有效，直接显示主窗口
        self.show_main_window()
        # 关闭启动界面
        self.close()
        return
        # # 如果授权信息不完整或验证失败，显示授权窗口
        # if not self.is_auth_valid():
        #     logger_manager.info("授权无效，显示授权窗口", "splash_screen")
        #     self.show_auth_window()
        # else:
        #     # 授权有效，直接显示主窗口
        #     self.show_main_window()
        #     # 关闭启动界面
        #     self.close()

    def is_auth_valid(self):
        """检查授权是否有效"""
        try:
            # machine_code, auth_time, last_auth_code = settings_manager.get_auth_info()
            #
            # if not machine_code or not auth_time or not last_auth_code:
            #     return False

            auth_time, last_auth_code = settings_manager.get_auth_info()

            if not auth_time or not last_auth_code:
                return False

            # 重复授权验证逻辑（简化版）
            auth_code_one_de = aes_decrypt(last_auth_code)
            if not auth_code_one_de:
                return False

            auth_parts = auth_code_one_de.split("|")
            if len(auth_parts) != 2:
                return False

            auth_code = aes_decrypt(auth_parts[0])
            if not auth_code:
                return False

            auth_code_parts = auth_code.split("|")
            if len(auth_code_parts) != 2:
                return False

            # 验证机器码
            current_machine_code = AuthWindow.AuthWindow.generate_machine_code_static()
            if auth_code_parts[0].replace('-', '') != current_machine_code.replace('-', ''):
                return False

            # 检查授权天数
            auth_days = int(auth_code_parts[1])
            if auth_days == 0:
                return True  # 无限制授权

            # 检查是否过期
            auth_datetime = datetime.strptime(auth_parts[1], "%Y-%m-%d %H:%M:%S")
            expire_datetime = auth_datetime + timedelta(days=auth_days)
            current_datetime = datetime.now()

            return auth_datetime <= current_datetime <= expire_datetime

        except Exception:
            return False

    def show_auth_window(self):
        """显示授权窗口"""
        try:
            logger_manager.info("开始创建授权窗口", "splash_screen")
            self.auth_window = AuthWindow.AuthWindow(clear_registry=False)  # 不清空注册表
            # 连接授权成功信号
            self.auth_window.auth_success.connect(self.on_auth_success)
            # 连接试用模式成功信号
            self.auth_window.trial_mode_success.connect(self.on_trial_success)
            self.auth_window.show()
            # 授权窗口显示后关闭启动界面
            self.close()
            logger_manager.info("授权窗口已显示，启动界面已关闭", "splash_screen")
        except Exception as e:
            logger_manager.error(f"显示授权窗口失败: {e}", "splash_screen")
            import traceback
            logger_manager.error(f"堆栈跟踪: {traceback.format_exc()}", "splash_screen")

    def on_auth_success(self):
        """授权成功回调"""
        try:
            logger_manager.info("授权成功，准备显示主窗口", "splash_screen")
            if self.auth_window:
                self.auth_window.close()
            self.show_main_window()
            self.close()
        except Exception as e:
            logger_manager.error(f"授权成功处理失败: {e}", "splash_screen")
            import traceback
            logger_manager.error(f"堆栈跟踪: {traceback.format_exc()}", "splash_screen")

    def on_trial_success(self):
        """试用模式成功回调"""
        try:
            logger_manager.info("试用模式启动，准备显示主窗口", "splash_screen")
            if self.auth_window:
                self.auth_window.close()
            self.show_main_window(is_trial_mode=True)
            self.close()
        except Exception as e:
            logger_manager.error(f"试用模式处理失败: {e}", "splash_screen")
            import traceback
            logger_manager.error(f"堆栈跟踪: {traceback.format_exc()}", "splash_screen")

    def ensure_model_directory(self):
        """确保model目录存在"""
        try:
            # 检测是否在 PyInstaller 打包环境中
            if getattr(sys, 'frozen', False):
                # 打包环境：获取 EXE 所在目录
                exe_dir = os.path.dirname(sys.executable)
                model_dir = os.path.join(exe_dir, "models")
            else:
                # 开发环境：使用原来的逻辑
                current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前py目录
                project_root = os.path.dirname(current_dir)  # 项目根目录
                model_dir = os.path.join(project_root, "models")

            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
                logger_manager.info(f"已创建models目录: {model_dir}", "splash_screen")
            else:
                logger_manager.debug(f"models目录已存在: {model_dir}", "splash_screen")

            return model_dir
        except Exception as e:
            logger_manager.error(f"创建models目录失败: {e}", "splash_screen")
            return None

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        logger_manager.info("应用程序启动", "splash_screen")
        splash = SplashScreen()
        splash.show()
        sys.exit(app.exec())
    except Exception as e:
        logger_manager.critical(f"应用程序启动失败: {e}", "splash_screen")
        import traceback
        logger_manager.critical(f"堆栈跟踪: {traceback.format_exc()}", "splash_screen")
        input("按回车键退出...")  # 防止窗口立即关闭


# def ensure_model_directory_static():
#     """静态方法：确保model目录存在（用于main函数调用）"""
#     try:
#         # 获取项目根目录下的models目录路径
#         current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前py目录
#         project_root = os.path.dirname(current_dir)  # 项目根目录
#         model_dir = os.path.join(project_root, "models")
#
#         if not os.path.exists(model_dir):
#             os.makedirs(model_dir)
#             logger_manager.info(f"已创建models目录: {model_dir}", "splash_screen")
#         else:
#             logger_manager.debug(f"models目录已存在: {model_dir}", "splash_screen")
#
#         return model_dir
#     except Exception as e:
#         logger_manager.error(f"创建models目录失败: {e}", "splash_screen")
#         return None