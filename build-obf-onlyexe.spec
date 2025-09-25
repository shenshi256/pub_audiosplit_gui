# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 项目根目录
project_root = os.path.dirname(os.path.abspath(SPEC))
obfuscated_root = os.path.join(project_root, 'obfuscated')

# 添加项目路径
sys.path.insert(0, os.path.join(project_root, 'py'))
sys.path.insert(0, os.path.join(project_root, 'gui'))

# 创建运行时钩子来修复 PyArmor 路径问题
runtime_hook_content = '''
import sys
import os

# 修复 PyArmor 运行时路径问题
if hasattr(sys, '_MEIPASS'):
    # PyInstaller 打包环境
    base_path = sys._MEIPASS

    # 添加 py 和 gui 目录到 sys.path
    py_path = os.path.join(base_path, 'py')
    gui_path = os.path.join(base_path, 'gui')

    if py_path not in sys.path:
        sys.path.insert(0, py_path)
    if gui_path not in sys.path:
        sys.path.insert(0, gui_path)

    # 确保 pytransform 可以被找到
    pytransform_py = os.path.join(base_path, 'py', 'pytransform')
    
    if os.path.exists(pytransform_py):
        if pytransform_py not in sys.path:
            sys.path.insert(0, pytransform_py)
        
        # 设置 PyArmor 运行时环境变量
        os.environ['PYARMOR_RUNTIME'] = pytransform_py
        
        # 确保 _pytransform.dll 可以被找到
        dll_path = os.path.join(pytransform_py, '_pytransform.dll')
        if os.path.exists(dll_path):
            # 将 DLL 路径添加到 PATH 环境变量
            current_path = os.environ.get('PATH', '')
            if pytransform_py not in current_path:
                os.environ['PATH'] = pytransform_py + os.pathsep + current_path
        
        # 尝试预加载 pytransform 模块
        try:
            import pytransform
        except ImportError:
            pass
'''

# 写入运行时钩子文件
runtime_hook_path = os.path.join(project_root, 'pyarmor_runtime_hook.py')
with open(runtime_hook_path, 'w', encoding='utf-8') as f:
    f.write(runtime_hook_content)

print(f"✅ 创建运行时钩子: {runtime_hook_path}")
print(f"✅ 项目根目录: {project_root}")
print(f"✅ 混淆根目录: {obfuscated_root}")

# 收集数据文件
datas = []
binaries = []

# PyArmor 项目模式的混淆文件在 dist 子目录下
obfuscated_py_dist = os.path.join(obfuscated_root, 'py', 'dist')
pytransform_py_dir = os.path.join(obfuscated_py_dist, 'pytransform')

# 添加 PyArmor 运行时文件（包括 DLL）
if os.path.exists(pytransform_py_dir):
    # 添加 py 目录下的 pytransform
    for root, dirs, files in os.walk(pytransform_py_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, obfuscated_py_dist)
            
            if file.endswith('.dll'):
                # DLL 文件作为二进制文件添加到根目录和 py/pytransform 目录
                binaries.append((src_path, '.'))  # 添加到根目录
                binaries.append((src_path, os.path.join('py', os.path.dirname(rel_path))))  # 添加到原位置
                print(f"✅ 添加 PyArmor DLL 到根目录和原位置: {file}")
            else:
                # 其他文件作为数据文件添加
                datas.append((src_path, os.path.join('py', os.path.dirname(rel_path))))
                print(f"✅ 添加 PyArmor 运行时文件: py/{rel_path}")

# 添加混淆后的 py 文件（从 dist 目录）
py_files = []
if os.path.exists(obfuscated_py_dist):
    for file in os.listdir(obfuscated_py_dist):
        if file.endswith('.py') and file != '__init__.py':
            src_path = os.path.join(obfuscated_py_dist, file)
            datas.append((src_path, 'py'))
            py_files.append(file)
            print(f"✅ 添加混淆后的 py 文件: {file}")

# 添加GUI资源文件（整个 gui 目录都直接复制，无需区分混淆/原始）
gui_dir = os.path.join(project_root, 'gui')
obfuscated_gui_dir = os.path.join(obfuscated_root, 'gui')

if os.path.exists(obfuscated_gui_dir):
    # 添加整个 gui 目录
    for root, dirs, files in os.walk(obfuscated_gui_dir):
        for file in files:
            if file.endswith('.py') or file.endswith('.qss'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, obfuscated_root)
                datas.append((src_path, os.path.dirname(rel_path)))
                print(f"✅ 添加 GUI 文件: {rel_path}")

# 添加图片资源
img_files = [
    ('customer_service.png', 'qt/img'),
    ('favicon.ico', 'qt/img'),
    ('logo.jpg', 'qt/img'),
]

for src, dst in img_files:
    # 优先使用混淆目录的文件，如果不存在则使用原文件
    obfuscated_path = os.path.join(obfuscated_root, 'qt', 'img', src)
    original_path = os.path.join(project_root, 'qt', 'img', src)

    if os.path.exists(obfuscated_path):
        datas.append((obfuscated_path, dst))
        print(f"✅ 添加图片资源: {src} (混淆目录)")
    elif os.path.exists(original_path):
        datas.append((original_path, dst))
        print(f"✅ 添加图片资源: {src} (原始目录)")

# 添加ffmpeg.exe（作为二进制文件）
ffmpeg_path = os.path.join(obfuscated_root, 'py', 'ffmpeg.exe')
if os.path.exists(ffmpeg_path):
    #binaries.append((ffmpeg_path, 'py'))
    binaries.append((ffmpeg_path, '.'))
    print(f"✅ 添加 ffmpeg.exe (混淆目录)")
else:
    # 如果混淆目录不存在，使用原文件
    original_ffmpeg_path = os.path.join(project_root, 'py', 'ffmpeg.exe')
    if os.path.exists(original_ffmpeg_path):
        #binaries.append((original_ffmpeg_path, 'py'))
        binaries.append((original_ffmpeg_path, '.'))
        print(f"✅ 添加 ffmpeg.exe (原始目录)")

# 不添加模型文件 - 用户要求不包含
print("⚠️  跳过模型文件 - 需要用户单独下载")

# 收集第三方库的数据文件
try:
    # 收集demucs相关数据
    demucs_datas = collect_data_files('demucs')
    datas.extend(demucs_datas)
    print(f"✅ 收集 demucs 数据文件: {len(demucs_datas)} 个")
except Exception as e:
    print(f"⚠️  收集 demucs 数据文件失败: {e}")

try:
    # 收集torch相关数据
    torch_datas = collect_data_files('torch')
    datas.extend(torch_datas)
    print(f"✅ 收集 torch 数据文件: {len(torch_datas)} 个")
except Exception as e:
    print(f"⚠️  收集 torch 数据文件失败: {e}")

try:
    # 收集PySide6相关数据
    pyside6_datas = collect_data_files('PySide6')
    datas.extend(pyside6_datas)
    print(f"✅ 收集 PySide6 数据文件: {len(pyside6_datas)} 个")
except Exception as e:
    print(f"⚠️  收集 PySide6 数据文件失败: {e}")

# 隐藏导入
hiddenimports = [
    # PySide6 相关
    'PySide6.QtCore',
    'PySide6.QtWidgets',
    'PySide6.QtGui',
    
    # 音频处理相关
    'demucs',
    'demucs.api',
    'demucs.separate',
    'torch',
    'torchaudio',
    'numpy',
    'librosa',
    'soundfile',
    'moviepy',
    'moviepy.editor',
    
    # 系统相关
    'psutil',
    'win32api',
    'win32con',
    'win32gui',
    'win32process',
    'pywintypes',
    
    # 标准库
    'logging.handlers',
    'threading',
    'queue',
    'json',
    'sqlite3',
    'winreg',
    'subprocess',
    'multiprocessing',
    'concurrent.futures',
    'asyncio',
    'ssl',
    'certifi',
    'urllib3',
    'requests',
    'charset_normalizer',
    'idna',
    
    # 科学计算
    'scipy',
    'resampy',
    'julius',
    'openunmix',
    'diffq',
    'einops',
    'hydra',
    'omegaconf',
    'submitit',
    'dora',
    'xformers',
    'flashy',
    'treetable',
    'retrying',
    'colorama',
    'tqdm',
    
    # 加密相关 (pycryptodome)
    'Crypto',
    'Crypto.Cipher',
    'Crypto.Cipher.AES',
    'Crypto.Util',
    'Crypto.Util.Padding',
    'Crypto.Random',
    'Crypto.Hash',
    'Crypto.PublicKey',
    'Crypto.Signature',
    
    # PyArmor 运行时
    'pytransform'
]

# 收集子模块
try:
    demucs_submodules = collect_submodules('demucs')
    hiddenimports.extend(demucs_submodules)
    print(f"✅ 收集 demucs 子模块: {len(demucs_submodules)} 个")
except Exception as e:
    print(f"⚠️  收集 demucs 子模块失败: {e}")

try:
    torch_submodules = collect_submodules('torch')
    hiddenimports.extend(torch_submodules)
    print(f"✅ 收集 torch 子模块: {len(torch_submodules)} 个")
except Exception as e:
    print(f"⚠️  收集 torch 子模块失败: {e}")

try:
    # 收集 Crypto 子模块
    crypto_submodules = collect_submodules('Crypto')
    hiddenimports.extend(crypto_submodules)
    print(f"✅ 收集 Crypto 子模块: {len(crypto_submodules)} 个")
except Exception as e:
    print(f"⚠️  收集 Crypto 子模块失败: {e}")

# 排除不需要的模块
excludes = [
    'tkinter',
    'matplotlib',
    'IPython',
    'jupyter',
    'notebook',
    'pytest',
    'sphinx',
    'setuptools',
    'distutils',
]

# PyArmor混淆配置
block_cipher = None

# 使用混淆后的主文件（PyArmor 项目模式生成在 dist 子目录）
main_py_path = os.path.join(obfuscated_py_dist, 'main.py')
if not os.path.exists(main_py_path):
    raise FileNotFoundError(f'混淆后的主文件未找到: {main_py_path}，请先运行混淆脚本')

print(f"✅ 使用混淆后的主文件: {main_py_path}")

a = Analysis(
    [main_py_path],
    pathex=[
        project_root,
        obfuscated_root,
        obfuscated_py_dist,  # 添加混淆后的 py dist 目录
        os.path.join(obfuscated_root, 'gui'),
        os.path.join(project_root, 'py'),
        os.path.join(project_root, 'gui'),
    ],
    binaries=binaries,  # 使用我们收集的二进制文件
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[runtime_hook_path],  # 添加运行时钩子
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 过滤重复文件
a.datas = list(set(a.datas))
a.binaries = list(set(a.binaries))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='音频分离器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'qt', 'img', 'favicon.ico'),  # 设置应用图标
)

# 清理临时文件
try:
    if os.path.exists(runtime_hook_path):
        os.remove(runtime_hook_path)
        print(f"✅ 清理运行时钩子文件: {runtime_hook_path}")
except:
    pass

print("✅ 混淆单 EXE 打包配置完成")