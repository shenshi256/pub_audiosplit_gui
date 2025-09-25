#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @Time    : 2025/7/16 16:39
# @Author  : WXY
# @File    : Demucs
# @PROJECT_NAME: audiosplit_gui
# @PRODUCT_NAME: PyCharm
# -------------------------------------------------------------------------------
import sys
import librosa
import soundfile
from scipy.io.wavfile import write as wav_write
from demucs.apply import apply_model
import threading, time, os, subprocess
from scipy.io import wavfile
import numpy as np
from PySide6.QtCore import QObject, Signal
from utils import setup_ffmpeg, format_timestamp_seconds#, setup_ffprobe  # ✅ 导入 ffmpeg 设置函数
import torch
import torchaudio
from LoggerManager import logger_manager
from moviepy.editor import VideoFileClip

# ✅ 设置 ffmpeg 路径
ffmpeg_path = setup_ffmpeg()
if ffmpeg_path:
    logger_manager.info(f"✅ 使用 ffmpeg 路径: {ffmpeg_path}", module_name="DemucsProcessor",show_in_ui=True)
else:
    logger_manager.warning("⚠️ 未找到 ffmpeg.exe，将使用系统 PATH 中的 ffmpeg, 如果系统没有ffmpeg，请自行安装, 并配置环境变量PATH")

print(torch.__version__)
print(torchaudio.__version__)

class DemucsProcessor(QObject):
    """Demucs 音频分离处理器类"""
    # 信号定义
    progress_updated = Signal(int)  # 进度更新信号
    status_updated = Signal(str)  # 状态更新信号
    log_updated = Signal(str)  # 日志更新信号
    processing_finished = Signal(bool, str)  # 处理完成信号 (成功/失败, 消息)

    def __init__(self, model_dir=None, output_dir=None, sample_rate=44100):
        """

        :param model_dir:
        :param output_dir:
        :param sample_rate:
        - 自动检测运行环境（开发环境 vs 打包环境）
        - 设置模型目录和输出目录路径
        - 初始化采样率、停止标志、进度模拟器相关属性
        - 创建模型缓存字典
        """
        super().__init__()
        # self.model_dir = model_dir or os.path.join(os.getcwd(), "../models")
        # self.output_dir = output_dir or os.path.join(os.getcwd(), "demucs_output")
        # ✅ 修复模型目录路径问题
        if model_dir is None:
            # 检测是否在 PyInstaller 打包环境中
            if getattr(sys, 'frozen', False):
                # 打包环境：使用 EXE 所在目录下的 models
                exe_dir = os.path.dirname(sys.executable)
                self.model_dir = os.path.join(exe_dir, "models")
            else:
                # 开发环境：使用项目根目录下的 models
                self.model_dir = os.path.join(os.getcwd(), "../models")
        else:
            self.model_dir = model_dir

        # ✅ 修复输出目录路径问题
        if output_dir is None:
            # 检测是否在 PyInstaller 打包环境中
            if getattr(sys, 'frozen', False):
                # 打包环境：使用 EXE 所在目录下的 demucs_output
                exe_dir = os.path.dirname(sys.executable)
                self.output_dir = os.path.join(exe_dir, "demucs_output")
            else:
                # 开发环境：使用当前工作目录下的 demucs_output
                self.output_dir = os.path.join(os.getcwd(), "demucs_output")
        else:
            self.output_dir = output_dir


        self.sample_rate = sample_rate
        self.stop_flag = threading.Event()

        # ✅ 添加进度模拟器相关属性
        self.progress_simulator_stop = threading.Event()
        self.current_progress = 0
        self.progress_lock = threading.Lock()

        # 确保输出目录存在 , 不在这里创建输出目录, 因为这样的话, 程序一启动就会被创建, 因为mainwindow会调用它
        #  os.makedirs(self.output_dir, exist_ok=True)

        # 模型缓存
        self._cached_models = {}

    def ensure_output_directory(self, output_dir=None):
        """确保输出目录存在（只在需要时创建）"""
        target_dir = output_dir or self.output_dir
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            logger_manager.info(f"已创建输出目录: {target_dir}", "DemucsProcessor", show_in_ui=True)
        return target_dir
    def start_progress_simulation(self, start_progress, end_progress, duration_estimate=60):
        """
        启动进度模拟器
        :param start_progress: 起始进度
        :param end_progress: 目标进度（不会超过这个值）
        :param duration_estimate: 预估处理时间（秒），用于计算模拟速度
        """
        self.progress_simulator_stop.clear()

        def simulate_progress():
            with self.progress_lock:
                current_progress = start_progress
                self.current_progress = current_progress

            # ✅ 设置最大模拟进度，不会达到end_progress
            max_simulated_progress = end_progress - 5  # 最多到75%（如果end_progress是80%）

            while not self.progress_simulator_stop.is_set() and not self.stop_flag.is_set():
                # ✅ 每次循环随机生成5-10秒的更新间隔
                update_interval = np.random.uniform(5, 10)

                # ✅ 等待随机时间间隔
                if self.progress_simulator_stop.wait(update_interval):
                    break  # 如果被停止，立即退出

                # ✅ 检查是否还能继续递增
                with self.progress_lock:
                    if self.current_progress < max_simulated_progress:
                        # ✅ 每次只递增1%
                        self.current_progress += 1
                        new_progress = self.current_progress

                        self.progress_updated.emit(new_progress)
                        logger_manager.debug(f"模拟进度递增: {new_progress}% (+1%, 间隔: {update_interval:.1f}s)",
                                             "DemucsProcessor")
                    else:
                        # ✅ 已达到最大模拟进度，不再递增
                        logger_manager.debug(f"已达到最大模拟进度: {max_simulated_progress}%，停止递增",
                                             "DemucsProcessor")
                        break

        # 启动模拟线程
        simulator_thread = threading.Thread(target=simulate_progress, daemon=True)
        simulator_thread.start()
        logger_manager.info(f"🎯 启动进度模拟器: {start_progress}% → 最多{end_progress - 5}% (每次+1%, 间隔: 5-10秒)",
                            "DemucsProcessor" )
    def stop_progress_simulation(self, final_progress=None):
        """
        停止进度模拟器
        :param final_progress: 最终进度值，如果提供则立即跳转到该进度
        """
        self.progress_simulator_stop.set()

        if final_progress is not None:
            with self.progress_lock:
                self.current_progress = final_progress
                self.progress_updated.emit(final_progress)
                # logger_manager.debug(f"停止模拟器并跳转到: {final_progress}%", "DemucsProcessor")

        # logger_manager.info("⏹️ 停止进度模拟器", "DemucsProcessor")

    def safe_progress_update(self, progress):
        """
        安全的进度更新，确保不会被模拟器覆盖
        """
        with self.progress_lock:
            if progress > self.current_progress:
                self.current_progress = progress
                self.progress_updated.emit(progress)

    def extract_waveform(self, input_path, temp_wav_path="temp_audio.wav"):
        """提取音频波形, 使用FFmpeg从音视频文件中提取音频, 转成PCM16位立体声格式"""
        """提取音频波形, 使用FFmpeg从音视频文件中提取音频, 转成PCM16位立体声格式"""
        logger_manager.info("[INFO]♻️ 调用 ffmpeg 提取音频...", module_name="DemucsProcessor", show_in_ui=True)
        try:
            # 获取 FFmpeg 可执行文件路径
            ffmpeg_binary = os.environ.get("FFMPEG_BINARY", "ffmpeg")

            # subprocess.run([
            #     ffmpeg_binary, '-y', '-i', input_path,
            #     '-vn', '-acodec', 'pcm_s16le', '-ar', str(self.sample_rate), '-ac', '2',
            #     temp_wav_path
            # ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            subprocess.run([
                ffmpeg_binary, '-y', '-i', input_path,
                '-vn', '-acodec', 'pcm_s16le', '-ar', str(self.sample_rate), '-ac', '2',
                temp_wav_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)  # Windows 下隐藏窗口

            # 使用 librosa 加载到内存并转换为 PyTorch 张量
            y, sr = librosa.load(temp_wav_path, sr=self.sample_rate, mono=False)
            os.remove(temp_wav_path)

            if y.ndim == 1:
                y = np.stack([y, y])  # 单声道转双声道

            logger_manager.info("[INFO]✅ 音频提取完成", module_name="DemucsProcessor", show_in_ui=True)
            return torch.tensor(y).float(), sr

        except subprocess.CalledProcessError as e:
            error_msg = f"[ERROR]❌ FFmpeg 处理失败: {str(e)}"
            logger_manager.error(error_msg, module_name="DemucsProcessor", show_in_ui=True)
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"[ERROR]❌ 音频提取失败: {str(e)}"
            logger_manager.error(error_msg, module_name="DemucsProcessor", show_in_ui=True)
            raise RuntimeError(error_msg)

    def load_single_model(self, model_name):
        """加载单个模型"""
        # 1. 检查缓存中是否已有该模型， 用到哪个模型加载哪个模型
        if model_name in self._cached_models:  
            # 这里是从缓存中加载模型, 那是什么时候把模型放到缓存里面的呢? 这里的缓存是不是指的就是内存? 
            # 是程序一启动就加载到内存里面的吗?
            # 如果是程序一启动就加载到内存里面,那是把models目录下的所有模型都加载了, 还是用到哪个加载哪个?
            #如果是用到哪个加载哪个, 那么之前的模型会释放吗? 
            return self._cached_models[model_name]# 直接返回缓存的模型
        # 第2步：缓存中没有，从磁盘加载, 这里加载的是整个模型对象, 而不是模型的路径
        model_path = os.path.join(self.model_dir, f"{model_name}.th")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"⚠️模型文件不存在: {model_path}")

        try:
            logger_manager.info(f"[INFO]♻️加载模型: {model_name}", module_name="DemucsProcessor",show_in_ui=True)
            pkg = torch.load(model_path, map_location="cpu")

            if "klass" in pkg and "kwargs" in pkg and "state" in pkg:
                ModelClass = pkg["klass"]
                model = ModelClass(**pkg["kwargs"])
                model.load_state_dict(pkg["state"])
                model.eval()
                # 第3步：加载成功后，存入缓存
                self._cached_models[model_name] = model
                return model
            else:
                logger_manager.error(f"[ERROR]❌ 模型文件格式不正确，缺少 klass/kwargs/state 字段", module_name="DemucsProcessor",show_in_ui=True)
                raise RuntimeError("模型文件格式不正确，缺少 klass/kwargs/state 字段")

        except Exception as e:
            error_msg = f"[ERROR] ❌加载模型失败: {str(e)}"
            #self.log_updated.emit(error_msg)
            logger_manager.error(error_msg, module_name="DemucsProcessor",show_in_ui=True)
            raise RuntimeError(error_msg)

    def load_ensemble_models(self, prefix):
        """加载多个模型文件（通常4个：prefix_1.th 到 prefix_4.th）"""
        logger_manager.info(f"[INFO]💡加载集成模型: {prefix}", module_name="DemucsProcessor",show_in_ui=True)
        cache_key = f"{prefix}_ensemble"
        if cache_key in self._cached_models:
            return self._cached_models[cache_key]

        models = []
        for i in range(1, 5):
            model_path = os.path.join(self.model_dir, f"{prefix}_{i}.th")

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"❌集成模型文件不存在: {model_path}")

            try:
                pkg = torch.load(model_path, map_location="cpu")
                ModelClass = pkg["klass"]
                kwargs = pkg.get("kwargs", {})
                model = ModelClass(**kwargs)
                model.load_state_dict(pkg["state"])
                model.eval()
                models.append(model)

            except Exception as e:
                error_msg = f"[ERROR]❌加载集成模型 {i} 失败: {str(e)}"
                self.log_updated.emit(error_msg)
                raise RuntimeError(error_msg)

        self._cached_models[cache_key] = models
        return models

    def separate_with_model(self, model, waveform, output_dir=None, silence_threshold=1e-4, selected_sources=None, input_path=None, audio_format="wav"):
        """使用单个模型分离音频"""
        if output_dir is None:
            output_dir = self.ensure_output_directory()
        else:
            output_dir = self.ensure_output_directory(output_dir)

        # self.log_updated.emit("[INFO] 正在分离音频...")
        logger_manager.info("[INFO]♻️ 正在分离音频...", module_name="DemucsProcessor",show_in_ui=True)
        self.status_updated.emit("正在分离音频...")

        start_time = time.time()
        timer_stop = threading.Event()

        def timer_printer():
            while not timer_stop.is_set() and not self.stop_flag.is_set():
                elapsed = int(time.time() - start_time)
                format_elapsed = format_timestamp_seconds(elapsed)

                self.status_updated.emit(f"✨ 正在分离音频... 已耗时 {format_elapsed}...")
                #self.log_updated.emit(f"[INFO] 已耗时 {format_elapsed}...")
                logger_manager.info(f"[INFO] 🕐已耗时 {format_elapsed}...", module_name="DemucsProcessor",show_in_ui=True)

                timer_stop.wait(5)

        timer_thread = threading.Thread(target=timer_printer, daemon=True)
        timer_thread.start()

        try:
            with torch.no_grad():
                sources = apply_model(model, waveform.unsqueeze(0), device="cpu")
        except Exception as e:
            timer_stop.set()
            error_msg = f"[ERROR] ❌ 模型分离失败: {str(e)}"
            self.log_updated.emit(error_msg)
            raise RuntimeError(error_msg)
        finally:
            timer_stop.set()
            timer_thread.join()

        elapsed = time.time() - start_time
        format_elapsed = format_timestamp_seconds(elapsed)
        logger_manager.info(f"[INFO]✅ 模型分离完成，总耗时 {format_elapsed}", module_name="DemucsProcessor",show_in_ui=True)
        #self.log_updated.emit(f"[INFO] 分离完成，耗时 {format_elapsed}")

        # 保存音频文件
        os.makedirs(output_dir, exist_ok=True)
        saved_count = 0
        saved_files = []
        # 从输入路径获取文件名（不含扩展名）
        if input_path:
            input_filename = os.path.splitext(os.path.basename(input_path))[0]
        else:
            input_filename = "output"

        for name, audio in zip(model.sources, sources[0]):
            # 检查是否选择了该音轨
            if selected_sources and name not in selected_sources:
                continue

            peak = audio.abs().max().item()
            if peak < silence_threshold:
                #self.log_updated.emit(f"[跳过] {name} 轨道静音（峰值 {peak:.5f}），未保存。")
                logger_manager.info(f"[跳过]➡️ {name} 轨道静音（峰值 {peak:.5f}），未保存。", module_name="DemucsProcessor",show_in_ui=True)
                continue

            try:
                # print(soundfile.available_formats())
                # print(soundfile.available_subtypes("WAV"))
                # ✅ 统一音频数据处理方式
                # 1. 将 tensor 转为 numpy
                audio_np = audio.cpu().numpy()

                # 2. 检查维度并转置（如果需要）
                if len(audio_np.shape) == 2 and audio_np.shape[0] < audio_np.shape[1]:
                    # 如果是 (channels, samples) 格式，转置为 (samples, channels)
                    audio_np = audio_np.T

                # 3. 确保数据在有效范围内
                audio_np = np.clip(audio_np, -1.0, 1.0)

                # 4. 转换为 float32
                audio_np = audio_np.astype(np.float32)

                # 5. 处理单声道情况
                if len(audio_np.shape) == 2 and audio_np.shape[1] == 1:
                    audio_np = audio_np.squeeze()

                # 根据音频格式保存
                if audio_format.lower() == "mp3":
                    out_path = os.path.join(output_dir, f"{input_filename}_{name}.mp3")
                    self._save_as_mp3(audio_np, out_path)
                else:
                    # 默认保存为 WAV
                    out_path = os.path.join(output_dir, f"{input_filename}_{name}.wav")
                    soundfile.write(out_path, audio_np, samplerate=self.sample_rate, format="WAV", subtype="FLOAT")

                logger_manager.info(f"[保存] {name} → {out_path}", module_name="DemucsProcessor", show_in_ui=True)
                saved_files.append(out_path)
                saved_count += 1

            except Exception as e:
                #self.log_updated.emit(f"[ERROR] 保存 {name} 失败: {str(e)}")
                logger_manager.error(f"[ERROR]❌ 保存 {name} 失败: {str(e)}", module_name="DemucsProcessor",show_in_ui=True)

        if saved_count == 0:
            #self.log_updated.emit("[警告] 所有音频均为静音，未保存任何文件。")
            logger_manager.warning("[警告]⚠️  所有音频均为静音，未保存任何文件。", module_name="DemucsProcessor",show_in_ui=True)
        else:
            #self.log_updated.emit(f"[完成] 共保存 {saved_count} 个音轨，输出目录：{output_dir}")
            logger_manager.info(f"[完成] ✅ 共保存 {saved_count} 个音轨，输出目录：{output_dir}", module_name="DemucsProcessor",show_in_ui=True)

        return saved_files

    def separate_with_ensemble(self, models, waveform, output_dir=None, silence_threshold=1e-4, selected_sources=None, input_path=None,audio_format="wav"):
        """使用集成模型分离音频
        - 使用多个模型进行集成分离，提高质量
        - 对多个模型的输出结果取平均值
        - 包含详细的进度更新
        - 支持中途停止处理
        """
        if output_dir is None:
            output_dir = self.output_dir

        logger_manager.info("[INFO]♻️ 正在使用 ensemble 模型分离音频...", module_name="DemucsProcessor",show_in_ui=True)
        self.status_updated.emit("正在使用集成模型分离音频...")

        start_time = time.time()
        timer_stop = threading.Event()

        def timer():
            while not timer_stop.is_set() and not self.stop_flag.is_set():
                format_elapsed = format_timestamp_seconds(int(time.time() - start_time))
                logger_manager.info(f"[INFO] 🕐已耗时 {format_elapsed}...", module_name="DemucsProcessor",show_in_ui=True)
                timer_stop.wait(5)

        threading.Thread(target=timer, daemon=True).start()

        try:
            with torch.no_grad():
                estimates = []
                total_models = len(models)

                for idx, model in enumerate(models):
                    if self.stop_flag.is_set():
                        break

                    # ✅ 模型开始处理
                    progress_start = 30 + int((idx / total_models) * 50)
                    self.progress_updated.emit(progress_start)
                    logger_manager.info(f"[INFO] ➡️运行第 {idx + 1}/{total_models} 个模型...",
                                        module_name="DemucsProcessor", show_in_ui=True)

                    out = apply_model(model, waveform.unsqueeze(0), device="cpu")
                    estimates.append(out[0])

                    # ✅ 模型完成处理
                    progress_end = 30 + int(((idx + 1) / total_models) * 50)
                    self.progress_updated.emit(progress_end)

                if not self.stop_flag.is_set():
                    sources = torch.stack(estimates).mean(0)
                else:
                    timer_stop.set()
                    return []

        except Exception as e:
            timer_stop.set()
            error_msg = f"[ERROR]❌ 集成模型分离失败: {str(e)}"
            logger_manager.error(error_msg, module_name="DemucsProcessor",show_in_ui=True)
            raise RuntimeError(error_msg)
        finally:
            timer_stop.set()

        elapsed = time.time() - start_time
        logger_manager.info(f"[INFO]🕐 模型分离完成，总耗时 {elapsed:.2f} 秒", module_name="DemucsProcessor",show_in_ui=True)

        # 保存音频文件
        os.makedirs(output_dir, exist_ok=True)
        saved_count = 0
        saved_files = []
        # 从输入路径获取文件名（不含扩展名）
        if input_path:
            input_filename = os.path.splitext(os.path.basename(input_path))[0]
        else:
            input_filename = "output"

        for idx, (name, audio) in enumerate(zip(models[0].sources, sources)):
            if self.stop_flag.is_set():
                break

            # 检查是否选择了该音轨
            if selected_sources and name not in selected_sources:
                continue

            peak = audio.abs().max().item()
            if peak < silence_threshold:
                logger_manager.info(f"[跳过]➡️ {name} 轨道静音（峰值 {peak:.5f}），未保存。", module_name="DemucsProcessor",
                                    show_in_ui=True)
                continue

            try:
                # ✅ 修改为 float32 保存方式
                # 1. 将 tensor 转为 numpy，并转置到正确的维度
                audio_np = audio.cpu().numpy().T  # (channels, time) -> (time, channels)

                # 2. 确保数据在有效范围内
                audio_np = np.clip(audio_np, -1.0, 1.0)

                # 3. 转换为 float32
                audio_np = audio_np.astype(np.float32)

                # 4. 处理单声道情况
                if audio_np.shape[1] == 1:
                    audio_np = audio_np.squeeze()

                #out_path = os.path.join(output_dir, f"output_{name}.wav")
                # 修改文件命名：使用输入文件名_音轨名.wav
                # out_path = os.path.join(output_dir, f"{input_filename}_{name}.wav")
                # # 5. 使用 soundfile 保存 float32 格式
                # soundfile.write(out_path, audio_np, samplerate=self.sample_rate, subtype="FLOAT")

                # 根据音频格式保存
                if audio_format.lower() == "mp3":
                    out_path = os.path.join(output_dir, f"{input_filename}_{name}.mp3")
                    self._save_as_mp3(audio_np, out_path)
                else:
                    # 默认保存为 WAV
                    out_path = os.path.join(output_dir, f"{input_filename}_{name}.wav")
                    soundfile.write(out_path, audio_np, samplerate=self.sample_rate, subtype="FLOAT")

                logger_manager.info(f"[保存] {name} → {out_path}", module_name="DemucsProcessor", show_in_ui=True)
                saved_files.append(out_path)
                saved_count += 1

                # 更新进度
                progress = 80 + int((idx + 1) / len(sources) * 20)  # 剩余20%用于保存
                self.progress_updated.emit(progress)

            except Exception as e:
                logger_manager.error(f"[ERROR] ❌ 保存 {name} 失败: {str(e)}", module_name="DemucsProcessor",
                                     show_in_ui=True)

        if saved_count == 0:
            self.log_updated.emit("[警告]⚠️  所有音频均为静音，未保存任何文件。")
        else:
            self.log_updated.emit(f"[完成]✅共保存 {saved_count} 个音轨，输出目录：{output_dir}")

        return saved_files

    def _save_as_mp3(self, audio_data, output_path, sample_rate=None):
        """
        将音频数据保存为 MP3 格式
        先保存为临时 WAV 文件，然后使用 FFmpeg 转换为 MP3
        """
        import uuid
        import tempfile

        temp_wav = None
        try:
            # 使用安全的临时文件名
            temp_filename = f"temp_{uuid.uuid4().hex[:8]}.wav"
            temp_wav = os.path.join(tempfile.gettempdir(), temp_filename)

            # 确保音频数据格式正确
            if isinstance(audio_data, torch.Tensor):
                audio_np = audio_data.detach().cpu().numpy()
            else:
                audio_np = np.array(audio_data)

            logger_manager.debug(f"原始音频数据形状: {audio_np.shape}, 数据类型: {audio_np.dtype}",
                                 "DemucsProcessor")

            # 处理音频数据维度
            if audio_np.ndim == 1:
                # 单声道，转换为 (samples, 1)
                processed_audio = audio_np.reshape(-1, 1)
            elif audio_np.ndim == 2:
                if audio_np.shape[0] < audio_np.shape[1]:
                    # 如果是 (channels, samples) 格式，需要转置
                    processed_audio = audio_np.T
                else:
                    # 已经是 (samples, channels) 格式
                    processed_audio = audio_np
            else:
                raise ValueError(f"不支持的音频数据维度: {audio_np.shape}")

            # 确保数据在有效范围内
            processed_audio = np.clip(processed_audio, -1.0, 1.0)

            # 转换为 float32
            processed_audio = processed_audio.astype(np.float32)

            logger_manager.debug(f"处理后音频数据形状: {processed_audio.shape}, 数据类型: {processed_audio.dtype}",
                                 "DemucsProcessor")

            # 先保存为 WAV
            soundfile.write(temp_wav, processed_audio, samplerate=self.sample_rate, subtype="FLOAT")

            logger_manager.debug(f"临时 WAV 文件已创建: {temp_wav}", "DemucsProcessor")

            # 获取 FFmpeg 可执行文件路径
            ffmpeg_binary = os.environ.get("FFMPEG_BINARY", "ffmpeg")

            # 使用 FFmpeg 转换为 MP3
            ffmpeg_cmd = [
                ffmpeg_binary, "-y",  # -y 覆盖输出文件
                "-i", temp_wav,  # 输入文件
                "-codec:a", "libmp3lame",  # 使用 MP3 编码器
                "-b:a", "320k",  # 比特率 320kbps
                "-loglevel", "error",  # 只输出错误信息，减少输出
                output_path  # 输出文件
            ]

            logger_manager.debug(f"执行 FFmpeg 命令: {' '.join(ffmpeg_cmd)}", "DemucsProcessor")

            # 修复编码问题：使用 bytes 模式而不是 text 模式
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=False,  # 使用 bytes 模式
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0  # Windows 下隐藏窗口
            )

            if result.returncode != 0:
                # 安全地解码错误信息
                try:
                    stderr_msg = result.stderr.decode('utf-8', errors='replace')
                except:
                    try:
                        stderr_msg = result.stderr.decode('gbk', errors='replace')
                    except:
                        stderr_msg = str(result.stderr)

                raise RuntimeError(f"FFmpeg 转换失败 (返回码: {result.returncode}): {stderr_msg}")

            logger_manager.debug(f"MP3 转换成功: {output_path}", "DemucsProcessor")

            # 删除临时文件
            if temp_wav and os.path.exists(temp_wav):
                os.remove(temp_wav)
                logger_manager.debug(f"临时文件已删除: {temp_wav}", "DemucsProcessor")

        except Exception as e:
            # 如果转换失败，删除临时文件
            if temp_wav and os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                    logger_manager.debug(f"清理临时文件: {temp_wav}", "DemucsProcessor")
                except:
                    pass

            # 重新抛出异常，但提供更详细的错误信息
            error_msg = f"MP3 转换失败: {str(e)}"
            logger_manager.error(error_msg, "DemucsProcessor")
            raise RuntimeError(error_msg)

    def smooth_progress_update(self, start_progress, end_progress, duration=0.5, steps=10):
        """平滑更新进度条"""
        if self.stop_flag.is_set():
            return
        # duration = 20.0
        step_size = (end_progress - start_progress) / steps
        step_duration = duration / steps

        for i in range(steps + 1):
            if self.stop_flag.is_set():
                break
            current_progress = int(start_progress + (step_size * i))
            self.progress_updated.emit(current_progress)
            if i < steps:  # 最后一步不需要等待
                time.sleep(step_duration)

    def process_audio(self, input_path, model_type="htdemucs", output_dir=None, selected_sources=None, audio_format="wav"):
        """
        处理音频的主要方法
        - 支持三种模型类型：
        - htdemucs ：单模型，4轨分离
        - mdx_extra ：集成模型，2轨分离（人声+伴奏）
        - htdemucs_ft ：集成模型，4轨分离
        - 包含完整的错误处理和进度管理
        - 处理完成后自动打开输出文件夹（Windows）
        """
        self.stop_flag.clear()
        self.progress_simulator_stop.set()  # 确保之前的模拟器已停止

        try:
            # 检查输入文件
            if not os.path.isfile(input_path):
                raise FileNotFoundError(f"❌ 输入文件不存在: {input_path}")

            # ✅ 平滑更新到10%
            self.smooth_progress_update(0, 10, duration=0.3)

            # 提取音频
            waveform, sr = self.extract_waveform(input_path)
            # ✅ 平滑更新到20%
            self.smooth_progress_update(10, 20, duration=0.3)

            # 根据模型类型处理
            if model_type == "htdemucs":
                model = self.load_single_model("htdemucs")
                # ✅ 平滑更新到30%
                self.smooth_progress_update(20, 30, duration=0.5)

                # ✅ 启动进度模拟器 (30% → 80%)
                # 单模型处理时间相对较短，预估30秒
                self.start_progress_simulation(30, 80, duration_estimate=30)

                saved_files = self.separate_with_model(model, waveform, output_dir, selected_sources=selected_sources, input_path=input_path, audio_format=audio_format)

                # ✅ 停止模拟器并跳转到80%
                self.stop_progress_simulation(80)

            elif model_type == "mdx_extra":
                models = self.load_ensemble_models("mdx_extra")
                # ✅ 平滑更新到30%
                self.smooth_progress_update(20, 30, duration=0.5)

                # ✅ 启动进度模拟器 (30% → 80%)
                # 集成模型处理时间较长，预估60秒
                self.start_progress_simulation(30, 80, duration_estimate=60)

                saved_files = self.separate_with_ensemble(models, waveform, output_dir,
                                                          selected_sources=selected_sources, input_path=input_path, audio_format=audio_format)

                # ✅ 停止模拟器并跳转到80%
                self.stop_progress_simulation(80)

            elif model_type == "htdemucs_ft":
                models = self.load_ensemble_models("htdemucs_ft")
                # ✅ 平滑更新到30%
                self.smooth_progress_update(20, 30, duration=0.5)

                # ✅ 启动进度模拟器 (30% → 80%)
                # 集成模型处理时间较长，预估60秒
                self.start_progress_simulation(30, 80, duration_estimate=60)

                saved_files = self.separate_with_ensemble(models, waveform, output_dir,
                                                          selected_sources=selected_sources, input_path=input_path, audio_format=audio_format)

                # ✅ 停止模拟器并跳转到80%
                self.stop_progress_simulation(80)

            else:
                raise ValueError(f"⚠️ 不支持的模型类型: {model_type}")

            # ✅ 平滑更新到100%
            self.smooth_progress_update(80, 100, duration=0.3)
            self.status_updated.emit("处理完成")

            self.processing_finished.emit(True, f"✅成功保存 {len(saved_files)} 个音频文件")

            # 自动打开输出文件夹（Windows）
            if saved_files and os.name == "nt":
                output_folder = output_dir or self.output_dir
                subprocess.run(["explorer", os.path.abspath(output_folder)], shell=True)

            return saved_files

        except Exception as e:
            # ✅ 发生错误时停止模拟器
            self.stop_progress_simulation()

            error_msg = str(e)
            self.log_updated.emit(f"[ERROR] ❌ 处理失败: {error_msg}")
            self.status_updated.emit("处理失败")
            self.processing_finished.emit(False, error_msg)
            return []

    def stop_processing(self):
        """停止处理
        - 设置停止标志，中断正在进行的处理
        - 停止进度模拟器
        - 更新状态为已取消
        """
        self.stop_flag.set()
        # ✅ 停止进度模拟器
        self.stop_progress_simulation()

        self.log_updated.emit("[INFO] 📊用户取消处理")
        self.status_updated.emit("已取消")

    def clear_model_cache(self):
        """清理所有模型缓存，释放内存"""
        if self._cached_models:
            logger_manager.info(f"正在清理 {len(self._cached_models)} 个缓存模型...",
                                "DemucsProcessor", show_in_ui=True)

            # 逐个删除模型对象
            for model_name in list(self._cached_models.keys()):
                del self._cached_models[model_name]

            self._cached_models.clear()

            # 强制垃圾回收
            import gc
            gc.collect()

            logger_manager.info("✅ 模型缓存已清理完成", "DemucsProcessor", show_in_ui=True)

    def clear_specific_model(self, model_name):
        """清理特定模型缓存"""
        if model_name in self._cached_models:
            del self._cached_models[model_name]
            import gc
            gc.collect()
            logger_manager.info(f"✅ 已清理模型: {model_name}", "DemucsProcessor", show_in_ui=True)

    # def __del__(self):
    #     """析构函数，对象销毁时自动清理"""
    #     self.clear_model_cache()


def main():
    """命令行主函数"""
    print("""
    可用模型：
    1. htdemucs (单模型，4轨分离)
    2. mdx_extra (ensemble，2轨：人声+伴奏)
    3. htdemucs_ft (ensemble，4轨分离)
    """)
    choice = input("请选择模型 [1/2/3]: ").strip()
    input_path = input("请输入音视频文件路径: ").strip().strip('"')

    if not os.path.isfile(input_path):
        print("[ERROR]❌  输入文件无效。")
        return

    # 创建处理器实例
    processor = DemucsProcessor()

    # 连接信号到打印函数
    processor.log_updated.connect(print)
    processor.status_updated.connect(lambda msg: print(f"状态: {msg}"))
    processor.progress_updated.connect(lambda p: print(f"进度: {p}%"))

    # 根据选择处理
    model_map = {"1": "htdemucs", "2": "mdx_extra", "3": "htdemucs_ft"}
    if choice in model_map:
        processor.process_audio(input_path, model_map[choice])
    else:
        print("[ERROR] ❌ 无效选择。")


if __name__ == "__main__":
    main()