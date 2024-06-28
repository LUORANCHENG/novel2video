# novel2video

本项目是基于[holk-h/MoneyProducer_txt2video](https://github.com/holk-h/MoneyProducer_txt2video)为基础进行的二次开发，主要优化了文件的存储目录和加入了超逼真的文本转语音模型Chattts。

## 项目简介

通过文生图工具stable-diffusion和文本转语音模型Chattts，实现将小说文本自动转换成AI配图的有声小说视频

示例视频：

https://github.com/LUORANCHENG/novel2video/assets/80999506/6ff66fd0-9251-47ce-ae87-2cb0e383a352


整体工作流程:

![process](https://github.com/LUORANCHENG/novel2video/assets/80999506/f326840f-3437-4c00-81f9-a455529f1ef2)


## 功能特色

- **超逼真的语音合成效果**：采用了目前文字转语音模型的天花板Chattts，支持固定音色、设置语速、添加停顿词、口头语、笑声。
- **多语言支持**：支持中文和英文小说的转换，满足不同用户的需求。

## 安装指南

### 前置准备

1.确保你的电脑正确安装了CUDA和CUDNN

2.安装stable-diffusion-web-ui，具体安装教程请参考官方的仓库: [stable-diffusion-web-ui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

3.获取到一个GPT3.5的api_key


### 配置环境

1. **克隆仓库**

```bash
git clone https://github.com/LUORANCHENG/novel2video.git
```

2. **使用conda创建并激活虚拟环境**
```bash
conda create -n myenv python=3.10
```

```bash
conda activate myenv
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

因为Chattts的作者默认使用的是cpu版本的torch，如果使用GPU版torch，安装如下依赖进行替换

```bash
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
```

由于pynini这个模块直接使用pip安装容易报错，所以需要额外使用conda进行安装

```bash
conda install -c conda-forge pynini=2.1.5
```

在成功安装pynini这个模块后，就可以继续安装后续的模块了
```bash
pip install soundfile nemo_text_processing gradio WeTextProcessing
```

## 使用说明

1.在`utils/llm.py`中填入自己GPT3.5的api_key。

2.启动stable-diffusion-web-ui（启动的时候需要加上 `--api --listen` 参数），然后修改 `utils/sd.py` 中的url地址。

3.运行test目录下的 `Chattts_test.py`和 `stable_diffusion_test.py`,以检查环境是否配置正确。

4.运行`utils/novel_spider.py` 爬取指定的小说内容，爬取到的内容将会存放在`素材/小说原文`的文件夹下,`utils/novel_spider.py` 的具体使用教程请查看这里：[使用教程](https://github.com/LUORANCHENG/novel2video/wiki/novel_spider.py%E7%9A%84%E5%85%B7%E4%BD%93%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)

5.修改根目录中main.py最底下的generate_videos函数，填上自己的小说所在文件夹目录和小说名称，并修改要生成视频的起始章节数和终止章节数。

6.运行根目录下的main.py文件，所有的输出均保存在`output`目录中

7.英文字幕会生成在 `subtitle` 文件夹里（中文字幕直接就是原始文本），可以使用剪映等软件识别并创建字幕

## 进阶用法

1.可通过修改`utils/tts_pro.py`来实现固定音色、设置语速、添加停顿词、口头语、笑声等功能，具体参数设置可参考Chattts的官方仓库：[Chattts官方仓库](https://github.com/2noise/ChatTTS)

2.可通过修改`utils/sd.py`中的`sd_model_checkpoint`参数来更换不同的stable_diffusion文生图模型，模型的下载可自行上浏览器查找。
