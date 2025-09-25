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
from gui.helpmodelwindow_ui import Ui_HelpModelWindow
from utils import setup_window_icon, VERSION, SCROLLBARSTYLE
import base64
import os


class HelpModelWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_HelpModelWindow()
        self.ui.setupUi(self)
        # with open("../gui/styles/helpmodelwindow_ui.qss", "r", encoding="utf-8") as f:
        #     qss = f.read()
        # self.setStyleSheet(qss)
        setup_window_icon(self)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        # 设置标题栏文本（可选）
        self.setWindowTitle(f"模型使用帮助 {VERSION}")
        self.ui.lblProjectHelp.setText("📘 模型使用帮助")
        # 填入帮助信息
        self.ui.textBrowser.setHtml(self.get_help_html())
        # 配置链接在外部浏览器中打开
        self.ui.textBrowser.setOpenExternalLinks(True)
        # 连接关闭按钮
        self.ui.btnClose.clicked.connect(self.close)

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

      table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #2e2e2e;
        }}
        th, td {{
            padding: 8px 10px;
            border-bottom: 1px solid #444;
        }}
        th {{
            background-color: #3a3a3a;
            color: #ffd700;
            text-align: left;
        }}
        td {{
            color: #c0c0c0;
        }}
  </style>
</head>
<body>

<h1>🎯 demucs 模型下载与使用指南</h1>

<div class="section">
  <p>以下是当前支持的 <span class="highlight bold">Demucs</span> 模型文件，已存放在模型目录中：</p>
</div>


<table>
    <tr>
        <th>模型文件</th>
        <th>大小</th>
        <th>描述</th>
    </tr>
    <tr>
        <td>htdemucs.th</td>
        <td>84.1 MB</td>
        <td>"标准人声分离" Demucs 模型, <span class="highlight bold">最常用, 也是最推荐的模型,</span> 基于 Hybrid Transformer Demucs，可分离为 4 个轨道（人声/鼓/贝斯/其他）。适用于多乐器分离。</td>
    </tr>
    <tr>
        <td>htdemucs_ft_1.th</td>
        <td>84.1 MB</td>
        <td>fine-tune 模型 1, 在CPU下极慢, 且效果并不是很好, htdemucs 的增强版本，Fine-tune 后效果更佳，适用于高精度音轨还原需求。</td>
    </tr>
    <tr>
        <td>htdemucs_ft_2.th</td>
        <td>84.1 MB</td>
        <td>fine-tune 模型 2</td>
    </tr>
    <tr>
        <td>htdemucs_ft_3.th</td>
        <td>84.1 MB</td>
        <td>fine-tune 模型 3</td>
    </tr>
    <tr>
        <td>htdemucs_ft_4.th</td>
        <td>84.1 MB</td>
        <td>fine-tune 模型 4</td>
    </tr>
    <tr>
        <td>mdx_extra_1.th</td>
        <td>167.4 MB</td>
        <td>增强型 MDX 模型 1, 
"高精度混合分离（推荐）,适合人声提取和伴奏提取，模型较轻量，速度较快。适合卡拉OK场景。</td>
    </tr>
    <tr>
        <td>mdx_extra_2.th</td>
        <td>167.4 MB</td>
        <td>增强型 MDX 模型 2</td>
    </tr>
    <tr>
        <td>mdx_extra_3.th</td>
        <td>167.4 MB</td>
        <td>增强型 MDX 模型 3</td>
    </tr>
    <tr>
        <td>mdx_extra_4.th</td>
        <td>167.4 MB</td>
        <td>增强型 MDX 模型 4</td>
    </tr>
</table> 

<div class="section">

  <p><span class="bold">📌 使用说明:</span></p>
  <ul>
    <li>🔄 标注为1 , 2, 3, 4的模型, 必须全部下载 。</li>
    <li>📁 存放路径:确保以上模型文件放在程序默认的模型目录（<code>models/</code>）下。</li>

  </ul>
</div>

<div class="section">
  <p><span class="bold">🔗 下载地址：</span>如你尚未下载模型，可前往以下地址获取：</p>
  <ul>
  <li>🧬 官网地址: <a href="https://github.com/facebookresearch/demucs" target="_blank">https://github.com/facebookresearch/demucs</a> </li>
    <li>📦 百度网盘：<a href="https://pan.baidu.com/s/1mNNWBpeq8Lk19-q3JPqrmA?pwd=b6xx"  class="link" >https://pan.baidu.com/s/1mNNWBpeq8Lk19-q3JPqrmA?pwd=b6xx</a> <span  class="link">提取码: b6xx</span></li>
                       <li>👉 如嫌网盘限速, 可以联系客服, 发邮箱超大附件 </li>
   </ul>

</div>

<div class="section">
  <p><span class="bold">📍 常见问题:</span></p>
  <ul>
    <li>模型文件必须完整下载，带 1/2/3/4 的必须4个都下载, 且不能被改名。</li>
    <li>若某模型缺失，程序将在启动时提示错误。</li>
  </ul>
</div> 

<div class="section">
  <p><span class="bold">📞 联系客服:</span></p>
  <p>
  {f'<img src="{customer_service_img}" alt="客服二维码" style="max-width: 200px; height: auto; display: block; margin: 10px 0; border: 1px solid #444; border-radius: 8px;"/>' if customer_service_img else '<p style="color: #ff6b6b;">客服图片加载失败，请检查图片文件是否存在</p>'}
  </p>
  <p>扫描上方二维码联系客服获取技术支持</p>
</div>

</body>
</html>
        """