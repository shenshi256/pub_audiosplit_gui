#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @Time    : 2025/7/16 16:50
# @Author  : WXY
# @File    : MainWindow
# @PROJECT_NAME: audiosplit_gui
# @PRODUCT_NAME: PyCharm
# -------------------------------------------------------------------------------
from gui.mainwindow_ui import Ui_MainWindow
from py.Demucs import DemucsProcessor
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox
from PySide6.QtCore import QThread, Slot, Signal, Qt
from GlobalExceptionHandler import GlobalExceptionHandler
from SingleInstanceManager import SingleInstanceManager
from LoggerManager import logger_manager
from datetime import datetime
import sys
import os
from utils import (setup_window_icon, setup_ffmpeg, show_info, show_warning,APPNAME,
                   show_error, show_confirm_exit, SCROLLBARSTYLE, DISABLED_CONTROL_STYLE,setup_window_title,format_timestamp_seconds, SELECTAUDIOVIDEO, DROPAUDIOVIDEO)
from SystemMonitorWorker import SystemMonitorWorker
from SettingsManager import settings_manager
from HelpModelWindow import HelpModelWindow
from HelpProjectWindow import  HelpProjectWindow

class WorkerThread(QThread):
    # ✅ 添加信号，让线程能够与主窗口通信
    finished_signal = Signal(bool, str)  # 处理完成信号

    def __init__(self, processor: DemucsProcessor, input_path, model_type, output_dir, selected_sources, audio_format="wav"):
        super().__init__()
        self.processor = processor
        self.input_path = input_path
        self.model_type = model_type
        self.output_dir = output_dir
        self.selected_sources = selected_sources
        self.audio_format = audio_format  # ✅ 新增音频格式参数
    def run(self):
        try:
            # ✅ 在线程中执行处理
            result = self.processor.process_audio(
                self.input_path,
                model_type=self.model_type,
                output_dir=self.output_dir,
                selected_sources=self.selected_sources,
                audio_format=self.audio_format  # ✅ 传递音频格式
            )
            # ✅ 发射成功信号
            if result:
                self.finished_signal.emit(True, f"成功处理 {len(result)} 个音频文件")
            else:
                self.finished_signal.emit(False, "处理失败，未生成任何文件")
        except Exception as e:
            # ✅ 发射失败信号
            self.finished_signal.emit(False, f"处理过程中发生错误: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self, is_trial_mode=False):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # with open("../gui/styles/mainwindow_ui.qss", "r", encoding="utf-8") as f:
        #     qss = f.read()
        # self.setStyleSheet(qss)
        # 保存试用模式状态
        self.is_trial_mode = is_trial_mode

        # ✅ 设置窗口标题 , 判断是否是试用模式
        if is_trial_mode:
            setup_window_title(self, subtitle="(试用)")
        else:
            setup_window_title(self)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        # 设置拖放事件处理
        self.setup_drag_drop_events()
        # ✅ 启用拖放功能
        self.ui.le_select_inputfile.setAcceptDrops(True)
        # ✅ 创建处理器（不需要moveToThread，因为我们使用自定义线程）
        self.processor = DemucsProcessor()
        # 初始化的时候, 设置为0
        self.ui.progressBar.setValue(0)
        # ✅ 移除不必要的线程变量
        # self.thread = QThread()
        # self.processor.moveToThread(self.thread)

        # 初始化模型帮助窗口
        self.help_model_dialog = None
        # 初始化项目帮助窗口
        self.help_dialog = None

        # 工作线程引用
        self.worker_thread = None
        # 设置日志管理器的UI文本框
        logger_manager.set_ui_text_edit(self.ui.te_msg)
        # self.ui.te_msg.verticalScrollBar(True)
        self.ui.te_msg.setStyleSheet(SCROLLBARSTYLE)

        # ✅ 连接日志管理器的UI更新信号
        logger_manager.ui_update_signal.connect(self.update_ui_log)
        logger_manager.batch_update_signal.connect(self.update_ui_log_batch)
        # 连接处理器信号
        self.processor.progress_updated.connect(self.update_progress)
        self.processor.log_updated.connect(self.update_log)
        self.processor.processing_finished.connect(self.on_processing_finished)
        # 连接按钮
        # 开始按钮
        self.ui.btn_start.clicked.connect(self.start_processing)
        self.ui.btn_select_file.clicked.connect(self.select_input_file)
        self.ui.btn_save.clicked.connect(self.select_output_dir)
        self.ui.btn_model_desc.clicked.connect(self.open_help_model_dialog)
        self.ui.btn_help.clicked.connect(self.open_help_dialog)
        # ✅ 连接调试模式复选框信号
        self.ui.chk_debug.stateChanged.connect(self.on_debug_mode_changed)

        # 处理状态标志
        self.is_processing = False

        # ✅ 连接模型选择单选按钮的信号
        self.ui.rbtn_htdemucs.toggled.connect(self.on_model_selection_changed)
        self.ui.rbtn_mdx_extra.toggled.connect(self.on_model_selection_changed)
        self.ui.rbtn_htdemucs_ft.toggled.connect(self.on_model_selection_changed)

        # ✅ 加载保存的设置并应用到界面
        self.load_saved_settings()
        # 创建系统监控工作线程
        self.monitor_worker = SystemMonitorWorker()
        self.monitor_worker.monitor_updated.connect(self.update_system_monitor_display)
        self.monitor_worker.start()


        # ✅ 添加初始化日志
        logger_manager.info("✅主窗口初始化完成", "main" )

    def on_model_selection_changed(self,  checked):
        """✅ 模型选择变化处理"""
        # 只在按钮被选中时处理，避免重复日志
        if checked and not self.is_processing:  # 只在非处理状态下且按钮被选中时响应
            self.update_audio_tracks_availability()

    def update_audio_tracks_availability(self):
        """✅ 根据选择的模型更新音轨复选框的可用性"""
        try:
            selected_model = self.get_selected_model()

            if selected_model == "mdx_extra":
                # MDX Extra 模型：只支持 vocals 和 other
                # 禁用 bass 和 drums
                self.ui.chk_bass.setEnabled(False)
                self.ui.chk_drums.setEnabled(False)

                # 取消选中 bass 和 drums
                self.ui.chk_bass.setChecked(False)
                self.ui.chk_drums.setChecked(False)

                # 确保 vocals 和 other 可用
                self.ui.chk_vocals.setEnabled(True)
                self.ui.chk_other.setEnabled(True)

                # 如果没有选中任何音轨，默认选中 vocals
                if not (self.ui.chk_vocals.isChecked() or self.ui.chk_other.isChecked()):
                    self.ui.chk_vocals.setChecked(True)

                logger_manager.info("🎵 MDX Extra 模型：只支持人声(vocals)和其他(other)音轨", "main", show_in_ui=True)

            else:
                # htdemucs 或 htdemucs_ft 模型：支持所有音轨
                self.ui.chk_vocals.setEnabled(True)
                self.ui.chk_drums.setEnabled(True)
                self.ui.chk_bass.setEnabled(True)
                self.ui.chk_other.setEnabled(True)

                # 如果没有选中任何音轨，默认选中所有音轨
                if not (self.ui.chk_vocals.isChecked() or self.ui.chk_drums.isChecked() or
                        self.ui.chk_bass.isChecked() or self.ui.chk_other.isChecked()):
                    self.ui.chk_vocals.setChecked(True)
                    self.ui.chk_drums.setChecked(True)
                    self.ui.chk_bass.setChecked(True)
                    self.ui.chk_other.setChecked(True)

                model_name = "HT-Demucs" if selected_model == "htdemucs" else "HT-Demucs FT"
                logger_manager.info(f"🎵 {model_name} 模型：支持所有音轨分离", "main", show_in_ui=True)

        except Exception as e:
            logger_manager.error(f"❌ 更新音轨可用性失败: {e}", "main", show_in_ui=True)

    def bring_to_front(self):
        """将主窗口置顶显示"""
        try:
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
            print("主窗口已置顶")
        except Exception as e:
            print(f"主窗口置顶失败: {e}")

    def setup_drag_drop_events(self):
        """设置拖放事件处理"""
        # 支持的音视频文件扩展名
        self.supported_extensions = set(DROPAUDIOVIDEO.split())
        #     {
        #     '.mp4', '.mov', '.mkv', '.avi', '.flv',  # 视频格式
        #     '.wav', '.mp3', '.ogg', '.flac'  # 音频格式
        # }
        # 重写拖放事件
        self.ui.le_select_inputfile.dragEnterEvent = self.QLineEdit_dragEnterEvent
        self.ui.le_select_inputfile.dragMoveEvent = self.QLineEdit_dragMoveEvent
        self.ui.le_select_inputfile.dropEvent = self.QLineEdit_dropEvent


    def QLineEdit_dragEnterEvent(self, event):
        """textEdit拖拽进入事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:  # 只允许拖拽一个文件
                file_path = urls[0].toLocalFile()
                if self.is_supported_file(file_path): # 判断是否支持的后缀
                    event.acceptProposedAction()
                    return
        event.ignore()

    def QLineEdit_dragMoveEvent(self, event):
        """textEdit拖拽移动事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                if self.is_supported_file(file_path):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def QLineEdit_dropEvent(self, event):
        """QLineEdit拖拽放下事件"""
        try:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if len(urls) == 1:
                    file_path = urls[0].toLocalFile()
                    if self.is_supported_file(file_path) and os.path.exists(file_path):
                        self.ui.le_select_inputfile.setText(file_path)
                        self.ui.le_select_inputfile.setCursorPosition(len(file_path)) # 让光标移动的最后的文本处, 如果是

                        # 保存目录路径
                        input_dir = os.path.dirname(file_path)

                        # 获取当前其他设置并更新输入路径
                        _, last_output_path, debug_open, select_model, audio_tracks = settings_manager.get_main_info()
                        settings_manager.save_main_info(
                            input_dir,
                            last_output_path,
                            debug_open,
                            select_model,
                            audio_tracks
                        )

                        # 记录日志
                        logger_manager.info(f"📄通过拖放选择文件: {os.path.basename(file_path)}", "main",
                                            show_in_ui=True)

                        event.acceptProposedAction()
                        return
                    else:
                        # ✅ 添加不支持文件格式的提示
                        if not self.is_supported_file(file_path):
                            logger_manager.warning(f"⚠️ 不支持的文件格式: {os.path.splitext(file_path)[1]}", "main",
                                                   show_in_ui=True)
                        elif not os.path.exists(file_path):
                            logger_manager.error(f"❌ 文件不存在: {file_path}", "main", show_in_ui=True)
                else:
                    # ✅ 添加多文件拖放的提示
                    logger_manager.warning("⚠️ 只支持拖放单个文件", "main", show_in_ui=True)

            event.ignore()

        except Exception as e:
            logger_manager.error(f"❌ 拖放处理失败: {e}", "main", show_in_ui=True)
            event.ignore()

    def is_supported_file(self, file_path):
        """检查文件是否为支持的音视频格式"""
        if not file_path:
            return False
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self.supported_extensions


    def on_debug_mode_changed(self, state):
        """✅ 调试模式切换处理"""
        try:
            is_debug_enabled = state == 2  # Qt.Checked = 2

            # ✅ 立即更新注册表
            self.update_debug_setting_in_registry(is_debug_enabled)

            # ✅ 启用或停止文件日志（使用默认路径）
            if is_debug_enabled:
                # 启用文件日志（使用默认路径）
                logger_manager.setup_file_logging(enable_debug=True)
                logger_manager.info("🔧 调试模式已开启，开始记录详细日志", "main", show_in_ui=True)
            else:
                # 停止文件日志
                logger_manager.setup_file_logging(enable_debug=False)
                logger_manager.info("🔧 调试模式已关闭，停止记录文件日志", "main", show_in_ui=True)

        except Exception as e:
            logger_manager.error(f"❌调试模式切换失败: {e}", "main", show_in_ui=True)

    def update_debug_setting_in_registry(self, is_debug_enabled):
        """✅ 更新注册表中的调试设置"""
        try:
            # 获取当前其他设置
            last_input_path, last_output_path, _, select_model, audio_tracks = settings_manager.get_main_info()

            # 更新调试设置
            debug_open = "1" if is_debug_enabled else "0"

            # 保存到注册表
            settings_manager.save_main_info(
                last_input_path,
                last_output_path,
                debug_open,  # 更新调试设置
                select_model,
                audio_tracks
            )

            logger_manager.debug(f"调试设置已更新到注册表: {debug_open}", "main")

        except Exception as e:
            logger_manager.error(f"❌更新注册表调试设置失败: {e}", "main", show_in_ui=True)

    # ✅ 新增：加载音频格式设置方法
    def load_audio_format_settings(self):
        """从注册表加载音频格式设置"""
        try:
            audio_format = settings_manager.get_audio_format()

            # 先取消所有选择
            self.ui.rbtn_wav.setChecked(False)
            self.ui.rbtn_mp3.setChecked(False)

            # 根据保存的格式设置对应的复选框
            if audio_format == "mp3":
                self.ui.rbtn_mp3.setChecked(True)
                logger_manager.info("✅加载音频格式设置: MP3", "main", show_in_ui=True)
            else:
                # 默认选择WAV
                self.ui.rbtn_wav.setChecked(True)
                logger_manager.info("✅加载音频格式设置: WAV", "main", show_in_ui=True)

        except Exception as e:
            logger_manager.error(f"❌加载音频格式设置失败: {e}", "main", show_in_ui=True)
            # 如果加载失败，默认选择WAV
            self.ui.rbtn_wav.setChecked(True)
            self.ui.rbtn_mp3.setChecked(False)

    def load_saved_settings(self):
        """✅ 加载保存的设置并应用到界面控件"""
        try:
            # 从设置管理器获取保存的信息
            last_input_path, last_output_path, debug_open, select_model, audio_tracks = settings_manager.get_main_info()

            # 设置输入文件路径
            if last_input_path and os.path.exists(last_input_path):
                self.ui.le_select_inputfile.setText(last_input_path)
                logger_manager.info(f"✅加载上次输入文件: {os.path.basename(last_input_path)}", "main", show_in_ui=True)

            # 设置输出目录路径
            if last_output_path and os.path.exists(last_output_path):
                self.ui.le_select_outputfile.setText(last_output_path)
                logger_manager.info(f"🟢加载上次输出目录: {last_output_path}", "main", show_in_ui=True)

            # ✅ 设置调试模式（文件日志已在LoggerManager初始化时自动设置）
            if debug_open == "1":
                self.ui.chk_debug.setChecked(True)
                logger_manager.info("✅调试模式已开启（文件日志已自动启用）", "main", show_in_ui=True)
            else:
                self.ui.chk_debug.setChecked(False)
                # 如果调试模式关闭，则禁用文件日志
                logger_manager.setup_file_logging(enable_debug=False)

            # 设置选择的模型
            self.set_selected_model(select_model)
            logger_manager.info(f"🟢加载上次选择模型: {select_model}", "main", show_in_ui=True)

            # 设置选择的音轨
            self.set_selected_audio_tracks(audio_tracks)
            logger_manager.info(f"✅加载上次选择音轨: {audio_tracks}", "main", show_in_ui=True)

            # ✅ 新增：加载音频格式设置
            self.load_audio_format_settings()

            logger_manager.info("🟢设置加载完成", "main", show_in_ui=True)

        except Exception as e:
            logger_manager.error(f"❌加载设置失败: {e}", "main", show_in_ui=True)
            # 如果加载失败，设置默认值
            self.set_default_settings()

    # ✅ 新增：获取当前选择的音频格式
    def get_selected_audio_format(self):
        """获取当前选择的音频格式"""
        if self.ui.rbtn_mp3.isChecked():
            return "mp3"
        else:
            return "wav"  # 默认返回wav

    # ✅ 新增：保存音频格式设置
    def save_audio_format_settings(self):
        """保存当前的音频格式设置到注册表"""
        try:
            audio_format = self.get_selected_audio_format()
            settings_manager.save_audio_format(audio_format)
            logger_manager.info(f"✅音频格式设置已保存: {audio_format.upper()}", "main", show_in_ui=True)
        except Exception as e:
            logger_manager.error(f"❌保存音频格式设置失败: {e}", "main", show_in_ui=True)



    def set_selected_model(self, model_name):
        """✅ 设置选择的模型"""
        self.ui.rbtn_htdemucs.setChecked(False)
        self.ui.rbtn_mdx_extra.setChecked(False)
        self.ui.rbtn_htdemucs_ft.setChecked(False)

        # 根据模型名称设置对应的单选按钮
        if model_name == "htdemucs":
            self.ui.rbtn_htdemucs.setChecked(True)
        elif model_name == "mdx_extra":
            self.ui.rbtn_mdx_extra.setChecked(True)
        elif model_name == "htdemucs_ft":
            self.ui.rbtn_htdemucs_ft.setChecked(True)
        else:
            # 默认选择 htdemucs
            self.ui.rbtn_htdemucs.setChecked(True)

    def set_selected_audio_tracks(self, audio_tracks):
        """✅ 设置选择的音轨"""
        # 先取消所有选择
        self.ui.chk_vocals.setChecked(False)
        self.ui.chk_drums.setChecked(False)
        self.ui.chk_bass.setChecked(False)
        self.ui.chk_other.setChecked(False)

        # 处理音轨字符串（可能是逗号分隔的多个值）
        if isinstance(audio_tracks, str):
            tracks = [track.strip() for track in audio_tracks.split(',') if track.strip()]
        else:
            tracks = [audio_tracks] if audio_tracks else ["vocals"]  # 默认选择vocals

        # 根据音轨名称设置对应的复选框
        for track in tracks:
            if track == "vocals":
                self.ui.chk_vocals.setChecked(True)
            elif track == "drums":
                self.ui.chk_drums.setChecked(True)
            elif track == "bass":
                self.ui.chk_bass.setChecked(True)
            elif track == "other":
                self.ui.chk_other.setChecked(True)

    def set_default_settings(self):
        """✅ 设置默认值"""
        # 设置默认模型
        self.ui.rbtn_htdemucs.setChecked(True)

        # 默认设置不选中
        self.ui.chk_debug.setChecked(False)

        # 设置默认音轨
        self.ui.chk_vocals.setChecked(True)

        # ✅ 新增：设置默认音频格式（WAV）
        self.ui.rbtn_wav.setChecked(True)
        self.ui.rbtn_mp3.setChecked(False)

        logger_manager.info("🎯 应用默认设置", "main", show_in_ui=True)
    def save_current_settings(self):
        """✅ 保存当前设置"""
        try:
            # 获取当前界面的值
            # input_file_path = self.ui.le_select_inputfile.text().strip()
            # input_path = os.path.dirname(input_file_path) if input_file_path else ""  # 只保存目录部分
            input_path = self.ui.le_select_inputfile.text().strip()
            output_path = self.ui.le_select_outputfile.text().strip()
            debug_open = "1" if self.ui.chk_debug.isChecked() else "0"
            select_model = self.get_selected_model()
            selected_sources = self.get_selected_sources()
            audio_tracks = ','.join(selected_sources) if selected_sources else "vocals"

            # 保存到设置管理器
            settings_manager.save_main_info(
                input_path,
                output_path,
                debug_open,
                select_model,
                audio_tracks
            )

            # ✅ 新增：保存音频格式设置
            self.save_audio_format_settings()

            logger_manager.info("✅设置已保存", "main", show_in_ui=True)

        except Exception as e:
            logger_manager.error(f"❌保存设置失败: {e}", "main", show_in_ui=True)

    def update_system_monitor_display(self, monitor_info):
        """在主线程中更新UI显示"""
        if 'error' in monitor_info:
            self.ui.memoryRate.setText(f"监控错误: {monitor_info['error']}")
            return

        monitor_text = (
            f"进程: 内存 {monitor_info['process_memory_text']}, CPU: {monitor_info['process_cpu']:.0f}%\n"
            f"系统: 内存 {monitor_info['system_memory_percent']:.0f}%, CPU: {monitor_info['system_cpu']:.0f}%"
        )
        self.ui.memoryRate.setText(monitor_text)

    def select_input_file(self):
        # 获取上次保存的路径作为起始目录
        last_input_path, _, _, _, _ = settings_manager.get_main_info()
        start_dir = last_input_path if last_input_path and os.path.exists(last_input_path) else ""

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择音视频文件",
            start_dir,  # 使用保存的路径作为起始目录
            f"音视频文件 ({SELECTAUDIOVIDEO});;所有文件 (*)"
        )
        if file_path:
            self.ui.le_select_inputfile.setText(file_path)
            self.ui.le_select_inputfile.setCursorPosition(len(file_path))
            # ✅ 立即保存新选择的目录路径到注册表
            new_input_dir = os.path.dirname(file_path)
            if new_input_dir != last_input_path:
                # 获取当前其他设置
                _, last_output_path, debug_open, select_model, audio_tracks = settings_manager.get_main_info()
                # 只更新输入路径，保持其他设置不变
                settings_manager.save_main_info(
                    new_input_dir,  # 保存目录路径
                    last_output_path,
                    debug_open,
                    select_model,
                    audio_tracks
                )

            # ✅ 添加文件选择日志
            logger_manager.info(f"🧬 已选择输入文件: {os.path.basename(file_path)}", "main", show_in_ui=True)

            # 输出文件时长, 使用
            duration_seconds = self.check_media_duration(file_path)
            logger_manager.info(f"🎬 音视频文件时长: {format_timestamp_seconds(duration_seconds)} 秒", "main", show_in_ui=True)

    def check_media_duration(self, file_path):
        """检查音视频文件时长"""
        """使用moviepy检查音视频文件时长"""
        try:
            from moviepy.editor import VideoFileClip

            # 使用 VideoFileClip 处理音视频文件
            with VideoFileClip(file_path) as clip:
                duration = clip.duration  # 返回秒数（浮点数）
                return duration

        except Exception as e:
            logger_manager.error(f"使用moviepy检查文件时长失败: {e}", "main")
            return None

    def select_output_dir(self):
        """选择输出目录"""
        # 获取上次保存的路径作为起始目录
        _, last_output_path, _, _, _ = settings_manager.get_main_info()
        start_dir = last_output_path if last_output_path and os.path.exists(last_output_path) else ""

        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录",
            start_dir  # 使用保存的路径作为起始目录
        )
        if dir_path:
            self.ui.le_select_outputfile.setText(dir_path)

            # ✅ 立即保存新选择的输出路径到注册表
            if dir_path != last_output_path:
                # 获取当前其他设置
                last_input_path, _, debug_open, select_model, audio_tracks = settings_manager.get_main_info()
                # 只更新输出路径，保持其他设置不变
                settings_manager.save_main_info(
                    last_input_path,
                    dir_path,  # 保存新的输出目录
                    debug_open,
                    select_model,
                    audio_tracks
                )

            # ✅ 添加目录选择日志
            logger_manager.info(f" ✅已选择输出目录: {dir_path}", "main", show_in_ui=True)
    def validate_inputs(self):
        """✅ 验证输入参数"""
        input_file = self.ui.le_select_inputfile.text().strip()

        if not input_file:
            logger_manager.error("[错误] ⚠️请先选择输入文件", "main", show_in_ui=True)

            # 选中输入框中的所有文本内容，方便用户重新输入
            self.ui.le_select_inputfile.selectAll()
            self.ui.le_select_inputfile.setFocus()  # 设置焦点到输入框
            return False

        if not os.path.exists(input_file):
            logger_manager.error("[错误] ❌输入文件不存在", "main", show_in_ui=True)

            # 选中输入框中的所有文本内容，方便用户重新输入
            self.ui.le_select_inputfile.selectAll()
            self.ui.le_select_inputfile.setFocus()  # 设置焦点到输入框
            return False


        # 检查是否选择了音轨
        selected_sources = self.get_selected_sources()
        if not selected_sources:
            logger_manager.error("[错误] ⚠️请至少选择一个音轨", "main", show_in_ui=True)
            return False

        return True

    def get_selected_model(self):
        """获取选择的模型"""
        if self.ui.rbtn_htdemucs.isChecked():
            return "htdemucs"
        elif self.ui.rbtn_mdx_extra.isChecked():
            return "mdx_extra"
        else:
            return "htdemucs_ft"

    def get_selected_sources(self):
        """获取选择的音轨"""
        selected_sources = []
        if self.ui.chk_vocals.isChecked():
            selected_sources.append("vocals")
        if self.ui.chk_drums.isChecked():
            selected_sources.append("drums")
        if self.ui.chk_bass.isChecked():
            selected_sources.append("bass")
        if self.ui.chk_other.isChecked():
            selected_sources.append("other")
        return selected_sources

    def ensure_models_available(self, model_type):
        """✅ 确保模型目录存在并检查所需模型文件"""
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

            # 确保models目录存在
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
                logger_manager.info(f" ✅已创建models目录: {model_dir}", "main", show_in_ui=True)
            else:
                logger_manager.debug(f"models目录已存在: {model_dir}", "main")

            # 根据模型类型检查所需的模型文件
            missing_models = []

            if model_type == "htdemucs":
                required_models = ["htdemucs.th"]
            elif model_type == "htdemucs_ft":
                required_models = ["htdemucs_ft_1.th", "htdemucs_ft_2.th", "htdemucs_ft_3.th", "htdemucs_ft_4.th"]
            elif model_type == "mdx_extra":
                required_models = ["mdx_extra_1.th", "mdx_extra_2.th", "mdx_extra_3.th", "mdx_extra_4.th"]
            else:
                logger_manager.error(f" ❌未知的模型类型: {model_type}", "main", show_in_ui=True)
                return False

            # 检查每个所需的模型文件
            for model_file in required_models:
                model_path = os.path.join(model_dir, model_file)
                if not os.path.exists(model_path):
                    missing_models.append(model_file)
                    logger_manager.warning(f" ⚠️缺少模型文件: {model_file}", "main", show_in_ui=True)

            if missing_models:
                missing_list = ", ".join(missing_models)
                logger_manager.error(f" ❌缺少必需的模型文件: {missing_list}", "main", show_in_ui=True)
                logger_manager.error(f" ❌请确保以下文件存在于 {model_dir} 目录中:", "main", show_in_ui=True)
                for model in missing_models:
                    logger_manager.error(f"   - {model}", "main", show_in_ui=True)
                return False

            logger_manager.info(f" ✅模型文件检查通过，使用模型: {model_type}", "main", show_in_ui=True)
            return True

        except Exception as e:
            logger_manager.error(f" ❌模型检查失败: {e}", "main", show_in_ui=True)
            return False

    def start_processing(self):
        """开始处理音频"""
        if self.is_processing:
            # 如果正在处理，显示确认停止对话框
            reply = show_confirm_exit(self, "确认停止", "确定要停止当前的音频处理吗？")

            if reply == QMessageBox.StandardButton.Yes:
                self.stop_processing()
            return

        # ✅ 验证输入
        if not self.validate_inputs():
            return

        input_file = self.ui.le_select_inputfile.text().strip()
                # ✅ 检查文件是否存在
        # if not os.path.exists(input_file):
        #     # 显示文件不存在的警告对话框
        #     show_warning(self, "文件不存在", f"指定的文件不存在：\n{input_file}\n\n请重新选择文件。")
        #     # 选中输入框中的所有文本内容，方便用户重新输入
        #     self.ui.le_select_inputfile.selectAll()
        #     self.ui.le_select_inputfile.setFocus()  # 设置焦点到输入框
        #     return
        output_dir = self.ui.le_select_outputfile.text().strip() or None
        model_type = self.get_selected_model()
        selected_sources = self.get_selected_sources()
        audio_format = self.get_selected_audio_format()  # ✅ 获取音频格式

        # ✅ 检查模型目录和模型文件
        if not self.ensure_models_available(model_type):
            show_warning(self, "模型文件缺失", f"缺少 {model_type} 模型所需的文件，请检查 models 目录")
            self.reset_ui_state()
            return

        # 检查文件时长
        duration_seconds = self.check_media_duration(input_file)
        if duration_seconds is None:
            show_warning(self, "错误", "无法获取文件时长，请确保文件格式正确")
            self.reset_ui_state()
            return

        # ✅ 试用模式下检查时长限制
        if self.is_trial_mode and duration_seconds > 600:  # 600秒 = 10分钟
            show_warning(self, "试用模式限制", "试用模式限制：音视频时长不超过10分钟")
            self.reset_ui_state()
            return

        # 清空te_msg的文本内容
        # self.ui.te_msg.clear()
        # 更新UI状态
        self.is_processing = True
        self.ui.btn_start.setText("停止处理")
        self.ui.progressBar.setValue(0)

        # ✅ 禁用相关控件，防止用户在处理过程中修改设置
        self.set_controls_enabled(False)

        # ✅ 记录开始处理的日志
        logger_manager.info(
            f"✅开始处理文件: {os.path.basename(input_file)}, 文件时长:{format_timestamp_seconds(duration_seconds)}",
            "main", show_in_ui=True)
        logger_manager.info(f"✅使用模型: {model_type}", "main", show_in_ui=True)
        logger_manager.info(f"🔊选择音轨: {', '.join(selected_sources)}", "main", show_in_ui=True)
        logger_manager.info(f"🎧输出格式: {audio_format.upper()}", "main", show_in_ui=True)  # ✅ 显示音频格式

        # ✅ 创建并启动工作线程
        self.worker_thread = WorkerThread(
            self.processor,
            input_path=input_file,
            model_type=model_type,
            output_dir=output_dir,
            selected_sources=selected_sources,
            audio_format=audio_format  # ✅ 传递音频格式
        )

        # ✅ 连接工作线程的完成信号
        self.worker_thread.finished_signal.connect(self.on_worker_finished)
        self.worker_thread.finished.connect(self.on_thread_finished)  # Qt内置的finished信号

        self.worker_thread.start()

    def stop_processing(self):
        """停止处理"""
        if self.is_processing and self.worker_thread:
            logger_manager.info("❌ 正在停止处理...", "main", show_in_ui=True)
            self.processor.stop_processing()

            # ✅ 等待线程结束
            if self.worker_thread.isRunning():
                self.worker_thread.quit()
                self.worker_thread.wait(5000)  # 最多等待5秒

            self.reset_ui_state()

    def set_controls_enabled(self, enabled: bool):
        """✅ 启用/禁用控件，并设置样式"""
        controls = [
            self.ui.btn_select_file,
            self.ui.btn_save,
            self.ui.rbtn_htdemucs,
            self.ui.rbtn_mdx_extra,
            self.ui.rbtn_htdemucs_ft,
            self.ui.le_select_inputfile,
            self.ui.le_select_outputfile
        ]

        # 音轨控件需要特殊处理
        audio_track_controls = [
            self.ui.chk_vocals,
            self.ui.chk_drums,
            self.ui.chk_bass,
            self.ui.chk_other
        ]

        for control in controls:
            control.setEnabled(enabled)

        # ✅ 音轨控件的启用/禁用需要考虑模型限制
        if enabled:
            # 重新启用时，根据当前模型设置音轨可用性
            self.update_audio_tracks_availability()
        else:
            # 禁用时，直接禁用所有音轨控件
            for control in audio_track_controls:
                control.setEnabled(False)

        # 设置禁用时的样式
        all_controls = controls + audio_track_controls
        if not enabled:
            # 应用禁用样式
            for control in all_controls:
                current_style = control.styleSheet()
                control.setStyleSheet(current_style + DISABLED_CONTROL_STYLE)
        else:
            # 恢复正常样式（移除禁用样式）
            for control in all_controls:
                current_style = control.styleSheet()
                # 移除禁用样式部分
                normal_style = current_style.replace(DISABLED_CONTROL_STYLE, "")
                control.setStyleSheet(normal_style)

    def reset_ui_state(self):
        """重置UI状态"""
        self.is_processing = False
        self.ui.btn_start.setText("开始处理")
        self.ui.progressBar.setValue(0) # 重置进度
        # ✅ 重新启用控件
        self.set_controls_enabled(True)

    @Slot(int)
    def update_progress(self, value):
        """更新进度条"""
        self.ui.progressBar.setValue(value)

    @Slot(str)
    def update_log(self, message):
        """更新日志显示（来自处理器的日志）"""
        self.ui.te_msg.append(message)

    @Slot(str)
    def update_ui_log(self, message):
        """更新UI日志（来自日志管理器的单条消息）"""
        self.ui.te_msg.append(message)

    @Slot(list)
    def update_ui_log_batch(self, messages):
        """批量更新UI日志（来自日志管理器的批量消息）"""
        for message in messages:
            self.ui.te_msg.append(message)

    @Slot(bool, str)
    def on_processing_finished(self, success, message):
        """处理完成回调（来自DemucsProcessor）"""
        if success:
            logger_manager.info(f"📊[DemucsProcessor] {message}", "main", show_in_ui=True)
        else:
            logger_manager.error(f"📊[DemucsProcessor] {message}", "main", show_in_ui=True)

    @Slot(bool, str)
    def on_worker_finished(self, success, message):
        """✅ 工作线程完成回调"""
        if success:
            logger_manager.info(f"[成功]✅ {message}", "main", show_in_ui=True)
            # ✅ 可选：显示成功消息框
            # QMessageBox.information(self, "处理完成", message)
        else:
            logger_manager.error(f"[失败]❌  {message}", "main", show_in_ui=True)
            # ✅ 可选：显示错误消息框
            # QMessageBox.critical(self, "处理失败", message)

    @Slot()
    def on_thread_finished(self):
        """✅ 线程结束回调"""
        self.reset_ui_state()
        self.worker_thread = None
        logger_manager.info("🟢处理线程已结束", "main", show_in_ui=True)

    def closeEvent(self, event):
        """✅ 窗口关闭事件处理"""
        # ✅ 在关闭前保存当前设置
        self.save_current_settings()

        if self.is_processing:
            reply = show_confirm_exit(self, "确认退出", "正在处理音频，确定要退出吗？")

            if reply == QMessageBox.StandardButton.Yes:
                # 停止系统监控工作线程
                if hasattr(self, 'monitor_worker') and self.monitor_worker:
                    logger_manager.info("🔄 正在停止系统监控线程...", "main", show_in_ui=True)
                    self.monitor_worker.stop()
                    logger_manager.info("✅ 系统监控线程已停止", "main", show_in_ui=True)

                self.stop_processing()

                # ✅ 清理模型缓存，释放内存
                try:
                    if hasattr(self, 'processor') and self.processor:
                        logger_manager.info("🧹 正在清理模型缓存...", "main", show_in_ui=True)
                        self.processor.clear_model_cache()
                        logger_manager.info("✅ 模型缓存清理完成", "main", show_in_ui=True)
                except Exception as e:
                    logger_manager.error(f"❌ 清理模型缓存失败: {e}", "main", show_in_ui=True)

                event.accept()
            else:
                event.ignore()
        else:
            # 即使没有在处理音频，也要停止系统监控线程
            if hasattr(self, 'monitor_worker') and self.monitor_worker:
                logger_manager.info("🔄 正在停止系统监控线程...", "main", show_in_ui=True)
                self.monitor_worker.stop()
                logger_manager.info("✅ 系统监控线程已停止", "main", show_in_ui=True)

            # ✅ 清理模型缓存，释放内存
            try:
                if hasattr(self, 'processor') and self.processor:
                    logger_manager.info("🧹 正在清理模型缓存...", "main", show_in_ui=True)
                    self.processor.clear_model_cache()
                    logger_manager.info("✅ 模型缓存清理完成", "main", show_in_ui=True)
            except Exception as e:
                logger_manager.error(f"❌ 清理模型缓存失败: {e}", "main", show_in_ui=True)

            event.accept()
    def open_help_dialog(self):
        """打开帮助窗体"""
        try:
            # 如果帮助窗口已经存在且可见，则将其置于前台
            if self.help_dialog and self.help_dialog.isVisible():
                self.help_dialog.raise_()
                self.help_dialog.activateWindow()
                return

            # 创建新的帮助窗口
            self.help_dialog = HelpProjectWindow()
            self.help_dialog.show()
            logger_manager.info("项目帮助窗口已打开", "main_window")

        except Exception as e:
            logger_manager.error(f"打开项目帮助窗口时发生错误: {str(e)}", "main_window")
            # QMessageBox.warning(self, "错误", f"无法打开帮助窗口: {str(e)}")
            show_error(self, "错误", f"无法打开帮助窗口: {str(e)}")
    def open_help_model_dialog(self):
        """打开帮助窗体"""
        try:
            # 如果帮助窗口已经存在且可见，则将其置于前台
            if self.help_model_dialog and self.help_model_dialog.isVisible():
                self.help_model_dialog.raise_()
                self.help_model_dialog.activateWindow()
                return

            # 创建新的帮助窗口
            self.help_model_dialog = HelpModelWindow()
            self.help_model_dialog.show()
            logger_manager.info("帮助窗口已打开", "main_window")

        except Exception as e:
            logger_manager.error(f"打开帮助窗口时发生错误: {str(e)}", "main_window")
            # QMessageBox.warning(self, "错误", f"无法打开帮助窗口: {str(e)}")
            show_error(self, "错误", f"无法打开帮助窗口: {str(e)}")

if __name__ == "__main__":
    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 设置中文语言环境
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

    # 注册全局异常处理器
    exception_handler = GlobalExceptionHandler()
    sys.excepthook = exception_handler.handle_exception

    # 创建单实例管理器
    instance_manager = SingleInstanceManager(APPNAME)

    # 检查是否已有实例在运行
    if instance_manager.is_running():
        logger_manager.info("应用程序已运行", "main")
        sys.exit(0)

    # 启动单实例服务器
    if not instance_manager.start_server():
        logger_manager.error("无法启动单实例服务", "main")
        sys.exit(1)

    try:
        # 创建并显示主窗口
        main_window = MainWindow()
        main_window.show()

        # 进入事件循环
        sys.exit(app.exec())
    except Exception as e:
        import traceback

        logger_manager.error(f"应用程序启动失败: {e}", "main")
        logger_manager.error(f"堆栈跟踪: {traceback.format_exc()}", "main")
        sys.exit(1)