import torchaudio
import torch
from ChatTTS import ChatTTS
import soundfile
from IPython.display import Audio
import asyncio
import os


chat = ChatTTS.Chat()

# 加载默认下载的模型
chat.load_models(compile=False) # 设置为Flase获得更快速度，设置为True获得更佳效果

# 使用随机音色
# speaker = chat.sample_random_speaker()

# 载入保存好的音色
speaker = torch.load('./素材/speaker/speaker_5_girl.pth')


def generate_audio(text, language:str, txt_name:str, order:int, oral=3, laugh=3, bk=3):
    max_retries = 10
    retry_delay = 2
    attempt = 0

    while attempt <max_retries:
        try:
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
            wavs = chat.infer(refine_text, params_refine_text=params_refine_text, params_infer_code=params_infer_code)

            save_path = f"./output/audios/{txt_name}/{language}"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            torchaudio.save(f'{save_path }/{order}.mp3', torch.from_numpy(wavs[0]), 24000)
            break
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                asyncio.sleep(retry_delay)
            else:
                print(f"Failed to save speech after {max_retries} attempts.")


# text ='男人一步步走近，叶婉晴的身体绷得越来越紧，直到男人硬实的胸膛贴上她的背，忐忑慌乱的心忽的平静下来'
# wavs = generate_audio(text=text,oral=2, laugh=9, bk=3, language='cn', txt_name='test', order=1)
# # torchaudio.save("../output/output_e2.mp3", torch.from_numpy(wavs[0]), 24000)
