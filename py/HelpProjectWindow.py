#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @Time    : 2025/7/17 19:03
# @Author  : WXY
# @File    : HelpModelWindow
# @PROJECT_NAME: audiosplit_gui
# @PRODUCT_NAME: PyCharm
# -------------------------------------------------------------------------------
from PySide6.QtWidgets import QMainWindow
from gui.helpwindow_ui import Ui_HelpWindow
from utils import setup_window_icon, VERSION, SCROLLBARSTYLE
import base64
import os

class HelpProjectWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_HelpWindow()
        # with open("../gui/styles/helpwindow_ui.qss", "r", encoding="utf-8") as f:
        #     qss = f.read()
        # self.setStyleSheet(qss)
        self.ui.setupUi(self)
        setup_window_icon(self)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        # 设置标题栏文本（可选）
        self.setWindowTitle(f"项目使用帮助 {VERSION}")
        self.ui.lblHelp.setText("📘 项目使用帮助")
        # 填入帮助信息
        self.ui.textBrowser.setHtml(self.get_help_html())
        # 配置链接在外部浏览器中打开
        self.ui.textBrowser.setOpenExternalLinks(True)
        # 连接关闭按钮
        self.ui.pushButton.clicked.connect(self.close)

        self.ui.textBrowser.setStyleSheet(SCROLLBARSTYLE)

    def get_customer_service_image_base64(self):
        """从文件系统获取客服图片并转换为Base64"""
        try:
            # 获取当前脚本的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建图片路径
            img_path = os.path.join(current_dir, "..", "qt", "img", "customer_service.png")
            img_path = os.path.normpath(img_path)

            print(f"尝试加载图片: {img_path}")  # 调试信息

            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    image_data = f.read()
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    print("图片加载成功")  # 调试信息
                    return f"data:image/png;base64,{base64_data}"
            else:
                print(f"图片文件不存在: {img_path}")  # 调试信息
                return ""
        except Exception as e:
            print(f"加载客服图片失败: {e}")
            return ""

    def get_help_html(self):
            """返回 HTML 格式的帮助内容"""
            # 获取客服图片的Base64数据
            customer_service_img = self.get_customer_service_image_base64()

            return f"""
           <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{
          background-color: #1e1e1e;
          color: #e0e0e0;
          font-family: Consolas, Courier New, monospace;
          padding: 20px;
        }}
        h1 {{
          color: #00d8ff;
          font-size: 24px;
          margin-bottom: 20px;
        }}
        h2 {{
          color: #89ddff;
          font-size: 20px;
          margin-top: 30px;
          margin-bottom: 15px;
        }}
        .section {{
          margin-top: 20px;
        }}
        .ascii-box {{
          background-color: #2a2a2a;
          padding: 12px;
          border-left: 4px solid #00d8ff;
          white-space: pre;
          font-size: 12px;
          margin-bottom: 20px;
        }}
        .model-list {{
          background-color: #2e2e2e;
          padding: 12px;
          border-radius: 8px;
          line-height: 1.6;
          font-size: 13px;
          border: 1px solid #444;
        }}
        .highlight {{
          color: #89ddff;
        }}
        .bold {{
          font-weight: bold;
        }}
        a {{
          color: #4fc3f7;
          text-decoration: none;
        }}
        a:hover {{
          text-decoration: underline;
        }}
        ul {{
          line-height: 1.8;
          margin-top: 15px;
        }}
        ol {{
          line-height: 1.8;
          margin-top: 15px;
        }}
        li {{
          margin-bottom: 8px;
        }}
        hr {{
          margin: 30px 0;
          border: none;
          border-top: 1px solid #444;
        }}
        .disclaimer {{
          font-size: 0.9em;
          color: #777;
          background-color: #2a2a2a;
          padding: 15px;
          border-radius: 8px;
          border-left: 4px solid #ff6b6b;
          margin-top: 20px;
        }}
        .usage-box {{
          background-color: #2e2e2e;
          padding: 15px;
          border-radius: 8px;
          border: 1px solid #444;
          margin: 15px 0;
        }}
      </style>
    </head>
    <body>

    <h1>🎯 Whisper Demucs 音频分离工具使用指南</h1>

    <div class="section">
      <p>欢迎使用 <span class="highlight bold">Whisper Demucs</span> 音频分离工具。本工具支持将音频文件分离为人声、伴奏、鼓等音轨，方便后期处理和音频增强。</p>
    </div>

    <div class="usage-box">
      <p><span class="bold">🎵 主要功能：</span></p>
      <ul>
        <li>🎤 制作卡拉OK伴奏</li>
        <li>🎧 音频后期处理</li>
        <li>🎬 视频配音分离</li>
        <li>🎼 多音轨分离（人声/鼓/贝斯/其他）</li>
      </ul>
    </div>

    <div class="section">
      <p><span class="bold">🔧 支持特性：</span></p>
      <ul>
        <li>支持三种模型（htdemucs, mdx_extra, htdemucs_ft）</li>
        <li>支持拖入 MP3/WAV 文件</li>
        <li>可选择分离后的输出格式</li>
        <li>实时进度显示和状态监控</li>
      </ul>
    </div>

    <h2>📋 使用步骤</h2>

    <div class="usage-box">
      <ol>
        <li><span class="highlight">选择音频文件</span> - 点击"选择文件"或直接拖拽音频文件到程序窗口</li>
        <li><span class="highlight">选择分离模型</span> - 根据需要选择合适的模型（推荐使用 htdemucs）</li>
        <li><span class="highlight">设置输出选项</span> - 选择输出格式和保存路径</li>
        <li><span class="highlight">开始分离</span> - 点击"开始分离"按钮并等待处理完成</li>
        <li><span class="highlight">查看结果</span> - 分离完成后可在输出目录查看生成的音轨文件</li>
      </ol>
    </div>

    <div class="section">
      <p><span class="bold">🔗 下载地址：</span>如你尚未下载模型，可前往以下地址获取：</p>
      <ul>
        <li>🧬 官网地址: <a href="https://github.com/facebookresearch/demucs" target="_blank">https://github.com/facebookresearch/demucs</a></li>
        <li>📦 百度网盘：<a href="https://pan.baidu.com/s/1mNNWBpeq8Lk19-q3JPqrmA?pwd=b6xx" class="link">https://pan.baidu.com/s/1mNNWBpeq8Lk19-q3JPqrmA?pwd=b6xx</a> <span class="link">提取码: b6xx</span></li>
      </ul>
    </div>

    <div class="section">
      <p><span class="bold">☕ 如有帮助, 感谢打赏:</span></p>
      <p>
      {f'<img src="{customer_service_img}" alt="客服二维码" style="max-width: 400px; height: 300px; display: block; margin: 10px auto; border: 1px solid #444; border-radius: 8px;"/>' if customer_service_img else '<p style="color: #ff6b6b;">客服图片加载失败，请检查图片文件是否存在</p>'}
      </p>
      
    </div>

    <hr>

    <div class="disclaimer">
      <p><span class="bold">⚠️ 免责声明：</span></p>
      <p>本软件仅供学习和研究使用，禁止用于任何侵犯版权的用途。用户对使用结果承担全部责任。</p>
    </div>

    </body>
    </html>
            """