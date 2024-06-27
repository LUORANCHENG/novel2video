import torchaudio
import torch
from ChatTTS import ChatTTS
import soundfile
from IPython.display import Audio

chat = ChatTTS.Chat()

# 加载默认下载的模型
chat.load_models(compile=False) # 设置为Flase获得更快速度，设置为True获得更佳效果

# 使用随机音色
# speaker = chat.sample_random_speaker()

# 载入保存好的音色
speaker = torch.load('素材/speaker/speaker_5_girl.pth', map_location=torch.device('cpu'))


def generate_audio(text, oral=3, laugh=3, bk=3):
    '''
    输入文本，输出音频
    '''

    # 句子全局设置：讲话人音色和速度
    params_infer_code = {
        'spk_emb': speaker,
        # 'prompt': '[speed_{}]'.format(speed)
    }

    # 句子全局设置：口语连接、笑声、停顿程度
    # oral：连接词，AI可能会自己加字，取值范围 0-9，比如：卡壳、嘴瓢、嗯、啊、就是之类的词。不宜调的过高。
    # laugh：笑，取值范围 0-9
    # break：停顿，取值范围 0-9
    params_refine_text = {
        'prompt': '[oral_{}][laugh_{}][break_{}]'.format(oral, laugh, bk)
    }

    refine_text = chat.infer(text, refine_text_only=True)
    print(refine_text)
    wavs = chat.infer(refine_text, params_refine_text=params_refine_text, params_infer_code=params_infer_code)

    return wavs

# text ='不习惯吗。男人轻声问，那只手顺着她的腰肢往上，覆在她的左胸'
# wavs = zihao_tts(text,oral=2, laugh=9, bk=3)
# torchaudio.save("output/output_e2.wav", torch.from_numpy(wavs[0]), 24000)