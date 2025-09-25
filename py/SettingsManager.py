#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @Time    : 2025/7/10 15:18
# @Author  : WXY
# @File    : SettingsManager
# @PROJECT_NAME: audiosplit_gui
# @PRODUCT_NAME: PyCharm
# -------------------------------------------------------------------------------
from PySide6.QtCore import QSettings


class SettingsManager:
    _instance = None
    _settings = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._settings = QSettings("wxy", "DemucsGUI")
        return cls._instance

    @property
    def settings(self):
        return self._settings

    def save_auth_info(self, machine_code, auth_time):
        """保存授权信息"""
        #self._settings.setValue("auth/machine_code", machine_code)
        self._settings.setValue("auth/auth_time", auth_time)
        self._settings.sync()

    def get_auth_info(self):
        """获取授权信息"""
        # machine_code = self._settings.value("auth/machine_code", "")
        auth_time = self._settings.value("auth/auth_time", "")
        last_auth_code = self._settings.value("auth/last_auth_code")

        # print("获取授权信息", machine_code, auth_time, last_auth_code)
        #return machine_code, auth_time, last_auth_code

        return   auth_time, last_auth_code




    def save_main_info(self, last_input_path,  last_output_path,debug_open,select_model, audio_tracks):
        """保存授权信息"""
        self._settings.setValue("main/last_input_path", last_input_path)# 输入路径, 包含文件名
        self._settings.setValue("main/last_output_path", last_output_path) # 输出路径
        self._settings.setValue("main/debug_open", debug_open) # 是否开启调试
        self._settings.setValue("main/select_model", select_model) # 选择模型, 只有一个
        self._settings.setValue("main/audio_tracks", audio_tracks) #多个音轨
        self._settings.sync()

    def get_main_info(self):
        """获取授权信息"""
        last_input_path = self._settings.value("main/last_input_path", "")
        last_output_path = self._settings.value("main/last_output_path", "")
        debug_open = self._settings.value("main/debug_open","0")# 0默认表示不开启调试
        select_model  = self._settings.value("main/select_model", "htdemucs") # 默认使用htdemucs模型
        audio_tracks = self._settings.value("main/audio_tracks", "vocals") # 默认选中chk_vocals
        # print("获取授权信息", machine_code, auth_time, last_auth_code)
        return last_input_path, last_output_path, debug_open, select_model, audio_tracks

    def save_main_only_main(self,key='last_input_path', value=""):
        """保存授权信息, 只处理一个值"""
        self._settings.setValue(f"main/{key}", value)#  只处理一个值
        self._settings.sync()

    def get_main_only_main(self,key='last_input_path' ):
        """保存授权信息, 只获取一个值"""
        _value = self._settings.value(f"main/{key}", "")#  只处理一个值
        return _value


    def save_ui_settings(self, output_type, debug_enabled, simple_enabled):
        """保存UI设置"""
        self._settings.setValue("ui/output_type", output_type)
        self._settings.setValue("ui/debug_enabled", debug_enabled)
        self._settings.setValue("ui/simple_enabled", simple_enabled)
        self._settings.sync()

    def get_ui_settings(self):
        """获取UI设置，如果读取失败则返回默认值"""
        try:
            output_type = self._settings.value("ui/output_type", "srt")  # 默认srt
            debug_enabled = self._settings.value("ui/debug_enabled", False, type=bool)  # 默认否
            simple_enabled = self._settings.value("ui/simple_enabled", False, type=bool)  # 默认否
            return output_type, debug_enabled, simple_enabled
        except Exception as e:
            # 如果读取失败，返回默认值
            print(f"读取UI设置失败: {e}，使用默认值")
            return "srt", False, False

    def save_selected_model(self, model_name):
        """保存选中的模型名称（只保存.pt文件名，提示文本时清空设置）"""
        if model_name and model_name.endswith(".pt"):
            # 选择了实际的.pt文件，保存选择
            self._settings.setValue("ui/selected_model", model_name)
        else:
            # 选择了提示文本或空值，清空之前的选择
            self._settings.setValue("ui/selected_model", "")
        self._settings.sync()

    def get_selected_model(self):
        """获取上次选中的模型名称"""
        return self._settings.value("ui/selected_model", "")

    # ✅ 新增：保存音频格式设置
    def save_audio_format(self, audio_format):
        """保存音频输出格式设置"""
        self._settings.setValue("main/audio_format", audio_format)
        self._settings.sync()

    # ✅ 新增：获取音频格式设置
    def get_audio_format(self):
        """获取音频输出格式设置，默认返回wav"""
        return self._settings.value("main/audio_format", "wav")


# 创建全局实例
settings_manager = SettingsManager()