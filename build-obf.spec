# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import shutil
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
    pytransform_paths = [
        os.path.join(base_path, 'pytransform'),  # 直接在 _internal 目录下
        os.path.join(base_path, 'py', 'pytransform'),
        os.path.join(base_path, 'gui', 'pytransform'),
        base_path  # _pytransform.dll 直接在 _internal 目录下
    ]
    
    for pytransform_path in pytransform_paths:
        if os.path.exists(pytransform_path):
            if pytransform_path not in sys.path:
                sys.path.insert(0, pytransform_path)
            
            # 设置 PyArmor 运行时环境变量
            os.environ['PYARMOR_RUNTIME'] = pytransform_path
            
            # 确保 _pytransform.dll 可以被找到
            dll_paths = [
                os.path.join(pytransform_path, '_pytransform.dll'),
                os.path.join(base_path, '_pytransform.dll')
            ]
            
            for dll_path in dll_paths:
                if os.path.exists(dll_path):
                    dll_dir = os.path.dirname(dll_path)
                    # 将 DLL 路径添加到 PATH 环境变量
                    current_path = os.environ.get('PATH', '')
                    if dll_dir not in current_path:
                        os.environ['PATH'] = dll_dir + os.pathsep + current_path
                    break
    
    # 尝试预加载 pytransform 模块
    try:
        import pytransform
    except ImportError as e:
        # 如果导入失败，尝试从不同路径导入
        for path in pytransform_paths:
            if os.path.exists(os.path.join(path, 'pytransform.py')):
                sys.path.insert(0, path)
                try:
                    import pytransform
                    break
                except ImportError:
                    continue
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

# 用于存储模型文件信息，稍后移动到exe同级目录
model_files = []

# PyArmor 项目模式的混淆文件在 dist 子目录下
obfuscated_py_dist = os.path.join(obfuscated_root, 'py', 'dist')
pytransform_py_dir = os.path.join(obfuscated_py_dist, 'pytransform')

# 添加 PyArmor 运行时文件（包括 DLL）- 关键修复
if os.path.exists(pytransform_py_dir):
    print(f"✅ 找到 PyArmor 运行时目录: {pytransform_py_dir}")
    
    # 添加 py 目录下的 pytransform
    for root, dirs, files in os.walk(pytransform_py_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, pytransform_py_dir)
            
            if file.endswith('.dll'):
                # DLL 文件直接放到 _internal 根目录，这样更容易被找到
                binaries.append((src_path, '.'))
                print(f"✅ 添加 PyArmor DLL 到根目录: {file}")
                
                # 同时也放到 pytransform 子目录
                binaries.append((src_path, 'pytransform'))
                print(f"✅ 添加 PyArmor DLL 到 pytransform: {file}")
            else:
                # 其他文件放到 pytransform 目录
                target_dir = 'pytransform' if rel_path == file else os.path.join('pytransform', os.path.dirname(rel_path))
                datas.append((src_path, target_dir))
                print(f"✅ 添加 PyArmor 运行时文件: {target_dir}/{file}")
                
                # 如果是 pytransform.py，也放一份到根目录
                if file == 'pytransform.py':
                    datas.append((src_path, '.'))
                    print(f"✅ 添加 pytransform.py 到根目录")
else:
    print(f"❌ 未找到 PyArmor 运行时目录: {pytransform_py_dir}")
    print("⚠️  这将导致运行时错误，请确保 PyArmor 混淆成功")

# 检查GUI目录的pytransform（如果存在）
pytransform_gui_dir = os.path.join(obfuscated_root, 'gui', 'pytransform')
if os.path.exists(pytransform_gui_dir):
    for root, dirs, files in os.walk(pytransform_gui_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, obfuscated_root)
            
            if file.endswith('.dll'):
                binaries.append((src_path, '.'))
                print(f"✅ 添加 GUI PyArmor DLL 到根目录: {file}")
            else:
                datas.append((src_path, os.path.dirname(rel_path)))
                print(f"✅ 添加 GUI PyArmor 运行时文件: {rel_path}")

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
            # 排除 styles 目录
        if 'styles' in root:
            print(f"⚠️  跳过 styles 目录: {root}")
            continue
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

# 收集模型文件信息（暂时添加到_internal，稍后移动）
models_dir = os.path.join(obfuscated_root, 'models')
if os.path.exists(models_dir):
    for file in os.listdir(models_dir):
        if file.endswith('.th'):
            src_path = os.path.join(models_dir, file)
            # 暂时添加到_internal的models目录
            datas.append((src_path, 'models'))
            # 记录模型文件信息，稍后移动
            model_files.append((src_path, file))
            print(f"✅ 添加模型文件（将移动到exe同级）: {file} (混淆目录)")
else:
    # 如果混淆目录不存在，使用原目录
    original_models_dir = os.path.join(project_root, 'models')
    if os.path.exists(original_models_dir):
        for file in os.listdir(original_models_dir):
            if file.endswith('.th'):
                src_path = os.path.join(original_models_dir, file)
                # 暂时添加到_internal的models目录
                datas.append((src_path, 'models'))
                # 记录模型文件信息，稍后移动
                model_files.append((src_path, file))
                print(f"✅ 添加模型文件（将移动到exe同级）: {file} (原始目录)")

# 添加ffmpeg.exe（作为二进制文件）
ffmpeg_path = os.path.join(obfuscated_root, 'py', 'ffmpeg.exe')
if os.path.exists(ffmpeg_path):
    binaries.append((ffmpeg_path, 'py'))
    print(f"✅ 添加 ffmpeg.exe (混淆目录)")
else:
    # 如果混淆目录不存在，使用原文件
    original_ffmpeg_path = os.path.join(project_root, 'py', 'ffmpeg.exe')
    if os.path.exists(original_ffmpeg_path):
        binaries.append((original_ffmpeg_path, 'py'))
        print(f"✅ 添加 ffmpeg.exe (原始目录)")

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
        pytransform_py_dir,  # 添加 pytransform 目录
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
    [],
    exclude_binaries=True,
    name='音频分离器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 设置为False隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'qt', 'img', 'favicon.ico'),  # 设置应用图标
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='音频分离器',
)

# 自定义后处理：将模型文件移动到exe同级目录
print("🔄 开始后处理：移动模型文件到exe同级目录...")

dist_dir = os.path.join(project_root, 'dist', '音频分离器')
internal_models_dir = os.path.join(dist_dir, '_internal', 'models')
external_models_dir = os.path.join(dist_dir, 'models')

if os.path.exists(internal_models_dir) and model_files:
    # 创建exe同级的models目录
    if not os.path.exists(external_models_dir):
        os.makedirs(external_models_dir)
        print(f"✅ 创建exe同级models目录: {external_models_dir}")
    
    # 移动模型文件
    for src_path, filename in model_files:
        internal_file = os.path.join(internal_models_dir, filename)
        external_file = os.path.join(external_models_dir, filename)
        
        if os.path.exists(internal_file):
            try:
                shutil.move(internal_file, external_file)
                print(f"✅ 移动模型文件: {filename} -> exe同级/models/")
            except Exception as e:
                print(f"⚠️  移动模型文件失败 {filename}: {e}")
                # 如果移动失败，尝试复制
                try:
                    shutil.copy2(internal_file, external_file)
                    os.remove(internal_file)
                    print(f"✅ 复制并删除模型文件: {filename}")
                except Exception as e2:
                    print(f"❌ 复制模型文件也失败 {filename}: {e2}")
    
    # 如果_internal/models目录为空，删除它
    try:
        if os.path.exists(internal_models_dir) and not os.listdir(internal_models_dir):
            os.rmdir(internal_models_dir)
            print("✅ 删除空的_internal/models目录")
    except Exception as e:
        print(f"⚠️  删除空目录失败: {e}")

print("✅ 模型文件后处理完成")

# 清理临时文件
try:
    if os.path.exists(runtime_hook_path):
        os.remove(runtime_hook_path)
        print(f"✅ 清理运行时钩子文件: {runtime_hook_path}")
except:
    pass

print("✅ 混淆多文件打包配置完成")
print("🔍 关键修复:")
print("  - PyArmor DLL 文件同时放置在根目录和 pytransform 子目录")
print("  - 增强的运行时钩子处理多种 DLL 路径")
print("  - 添加手动复制 PyArmor 文件的备用机制")
print("  - 构建过程中验证关键文件存在")
print("  - 模型文件通过后处理移动到exe同级目录")
print("📁 最终目录结构:")
print("  dist/音频分离器/")
print("  ├── 音频分离器.exe")
print("  ├── _internal/          # 其他依赖文件")
print("  └── models/             # 模型文件（与exe同级）")