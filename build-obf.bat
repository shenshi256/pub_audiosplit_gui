@echo off
chcp 65001 >nul
echo 🚀 开始构建带混淆的可执行文件...

:: 检查 PyArmor 是否安装
python -c "import pyarmor" 2>nul
if errorlevel 1 (
    echo ❌ PyArmor 未安装，请先安装: pip install pyarmor==7.7.4
    pause
    exit /b 1
)

:: 检查 PyInstaller 是否安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller 未安装，请先安装: pip install pyinstaller
    pause
    exit /b 1
)

echo ✅ 依赖检查完成

:: 清理旧的构建文件
echo 🧹 清理旧的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "obfuscated" rmdir /s /q "obfuscated"

:: 清理 __pycache__ 目录
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

echo ✅ 清理完成

:: 创建混淆输出目录
mkdir "obfuscated"
mkdir "obfuscated\py"
mkdir "obfuscated\gui"

:: 初始化 PyArmor 项目（这是关键步骤）
echo 🔧 初始化 PyArmor 项目...
pyarmor init --src=py --entry=main.py obfuscated\py
if errorlevel 1 (
    echo ❌ PyArmor 项目初始化失败
    pause
    exit /b 1
)
echo ✅ PyArmor 项目初始化完成

:: 混淆 py 目录（使用项目模式）
echo 🔒 混淆 py 目录...
cd obfuscated\py
pyarmor build
if errorlevel 1 (
    echo ❌ py目录混淆失败
    cd ..\..
    pause
    exit /b 1
)
cd ..\..
echo ✅ py目录混淆完成

:: 复制整个 gui 目录（跳过所有 UI 文件混淆以避免 PyArmor 试用版限制）
echo 📁 复制 gui 目录...
echo ⚠️  跳过所有 GUI 文件混淆（避免 PyArmor 试用版 32KB 限制）
echo    原因: 所有 UI 文件都导入 resource_rc.py，会触发代码对象大小限制

xcopy "gui" "obfuscated\gui\" /E /I /Y
echo ✅ gui 目录复制完成

:: 检查 PyArmor 运行时文件
echo 🔍 检查 PyArmor 运行时文件...
if exist "obfuscated\py\dist\pytransform" (
    echo ✅ 找到 py\dist\pytransform 目录
    dir "obfuscated\py\dist\pytransform" /B
) else (
    echo ❌ 未找到 py\dist\pytransform 目录，PyArmor 混淆可能失败
    pause
    exit /b 1
)

:: 检查关键的 PyArmor 运行时文件
if exist "obfuscated\py\dist\pytransform\_pytransform.dll" (
    echo ✅ 找到 _pytransform.dll
) else (
    echo ❌ 未找到 _pytransform.dll，这会导致运行时错误
    pause
    exit /b 1
)

:: 复制资源文件
echo 📁 复制资源文件...

if exist "models" (
    xcopy "models" "obfuscated\models\" /E /I /Y
    echo ✅ models 目录复制完成
)

if exist "qt\img" (
    xcopy "qt\img" "obfuscated\qt\img\" /E /I /Y
    echo ✅ qt\img 目录复制完成
)

if exist "py\ffmpeg.exe" (
    copy "py\ffmpeg.exe" "obfuscated\py\"
    echo ✅ ffmpeg.exe 复制完成
)

:: 使用 PyInstaller 打包（使用 build-obf.spec）
echo 📦 使用 PyInstaller 打包...
pyinstaller --clean "build-obf.spec"
if errorlevel 1 (
    echo ❌ PyInstaller 打包失败
    echo 💡 保留混淆文件用于调试，请检查 obfuscated 目录
    pause
    exit /b 1
) else (
    echo ✅ PyInstaller 打包成功
    
    :: 验证 PyArmor 运行时文件是否被正确包含
    echo 🔍 验证 PyArmor 运行时文件...
    if exist "dist\音频分离器\_internal\_pytransform.dll" (
        echo ✅ _pytransform.dll 已正确包含到 _internal 目录
    ) else (
        echo ❌ _pytransform.dll 未包含到 _internal 目录
        echo 💡 手动复制 PyArmor 运行时文件...
        
        :: 手动复制 PyArmor 运行时文件到 _internal 目录
        if exist "obfuscated\py\dist\pytransform\_pytransform.dll" (
            copy "obfuscated\py\dist\pytransform\_pytransform.dll" "dist\音频分离器\_internal\"
            echo ✅ 手动复制 _pytransform.dll 完成
        )
        
        if exist "obfuscated\py\dist\pytransform\pytransform.py" (
            copy "obfuscated\py\dist\pytransform\pytransform.py" "dist\音频分离器\_internal\"
            echo ✅ 手动复制 pytransform.py 完成
        )
        
        :: 复制整个 pytransform 目录
        if exist "obfuscated\py\dist\pytransform" (
            xcopy "obfuscated\py\dist\pytransform" "dist\音频分离器\_internal\pytransform\" /E /I /Y
            echo ✅ 手动复制 pytransform 目录完成
        )
    )
    
    :: 最终验证
    echo 🔍 最终验证...
    if exist "dist\音频分离器\_internal\_pytransform.dll" (
        echo ✅ 验证通过: _pytransform.dll 存在于 _internal 目录
    ) else (
        echo ❌ 验证失败: _pytransform.dll 仍然缺失
        echo 💡 保留混淆文件用于手动调试
        pause
        exit /b 1
    )
    
    :: 只有在验证通过后才清理混淆文件
    echo 🧹 清理混淆文件...
    if exist "obfuscated" rmdir /s /q "obfuscated"
    echo ✅ 清理完成
)

echo ✅ 构建完成！
echo 📁 输出目录: dist\音频分离器\
echo 🚀 可执行文件: dist\音频分离器\音频分离器.exe
echo.
echo 📋 使用说明:
echo 1. 运行 build-obf.bat 开始打包
echo 2. 等待混淆和打包完成
echo 3. 在 dist\音频分离器\ 目录找到可执行文件
echo.
echo 🔒 混淆特性:
echo - 多文件分发: 可执行文件 + 依赖库文件夹
echo - py 目录: 完全混淆（使用项目模式）
echo - gui 目录: 跳过混淆（避免 PyArmor 试用版限制）
echo - gui/styles: 自动包含所有 QSS 样式文件
echo - PyArmor 运行时: 自动包含并验证
echo - 资源文件: 自动包含
echo - GUI 资源: 图标和界面文件
echo - 包含 ffmpeg: 音频处理工具
echo - 第三方库: 自动包含
echo.
echo 💡 说明: 由于 PyArmor 试用版有 32KB 代码对象限制，所有 GUI 文件都跳过了混淆。
echo    这些文件主要是界面定义，不包含核心业务逻辑。
echo    核心业务逻辑在 py 目录中已完全混淆保护。
echo.
pause