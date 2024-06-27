import os
import asyncio
from utils import text_utils
from tqdm import tqdm
import utils.llm as llm
import utils.tts_pro as tts
import utils.sd as sd
import utils.video_util as video_util

def generate_videos(start_chapter, end_chapter, book_dir, book_name):
    # 遍历这本书的目录，获取到每一章的文件名，并按编号从小到大排序，结果存储在chapter_files列表中
    chapter_files = sorted([f for f in os.listdir(book_dir) if f.startswith('chapters_') and f.endswith('.txt')],
                           key=lambda x: int(x.split('_')[1].split('.')[0]))

    # 提取出我们需要生成视频的章节
    chapter_files = [f for f in chapter_files if start_chapter <= int(f.split('_')[1].split('.')[0]) <= end_chapter]

    # 遍历这本书的每一章的txt文件
    for chapter_order, txt_file in enumerate(chapter_files, start=start_chapter):
        txt_name = book_name + '_' + txt_file.split('.')[0]
        try:
            os.makedirs(f'./output/audios/{txt_name}/en')
            os.makedirs(f'./output/audios/{txt_name}/cn')
            os.makedirs(f'./output/images/{txt_name}', exist_ok=True)
            os.makedirs(f'./output/video/en', exist_ok=True)
            os.makedirs(f'./output/video/cn', exist_ok=True)
            os.makedirs(f'./output/subtitles/{txt_name}', exist_ok=True)
            print(f"Folder '{txt_name}' created successfully.")
        except FileExistsError:
            print(f"Folder '{txt_name}' already exists.")

        # 对应章节txt文件的存放路径
        txt_path = os.path.join(book_dir, txt_file)

        # 把对应章节的内容读出来，并把每一句话存放进列表中
        txt = text_utils.read_txt(txt_path)

        # 创建一个列表保存每句话的英文字幕
        subtitles = []

        for index, text in enumerate(tqdm(txt, total=len(txt))):
            # 调用gpt3.5生成json格式的内容，注意，这里out是json格式的
            out = llm.text_to_prompt(text)

            # 记录英文字幕
            subtitles.append(out['txt'])

            # # 生成英文语音
            # # await tts.generate_speech(out['txt'], 'en', txt_name, index + 1)
            # tts.generate_audio(text=out['txt'], language='en', txt_name=txt_name, order=index+1)

            # 生成中文语音
            # await tts.generate_speech(text, 'cn', txt_name, index + 1, 'zh-CN-YunxiNeural')
            tts.generate_audio(text=text, language='cn', txt_name=txt_name, order=index + 1)

            # 只有当句子长度大于5，我们才去生成图像
            sd.generate_image(prompt=out['prompt'], seed=114514, width=405, height=720, txt_name=txt_name, order=index+1)

        # 将字幕写入txt文件
        try:
            with open(f'./output/subtitles/{txt_name}/subtitle_{chapter_order}.txt', 'w') as f:
                f.write('\n'.join(subtitles))
        except Exception as e:
            print(e)

        video_util.create_video_with_audio_images(len(txt), txt_name, chapter_order, 'cn')
        # video_util.create_video_with_audio_images(len(txt), txt_name, chapter_order, 'en')


def main():
    # 修改这里的章节数
    generate_videos(1, 1, '素材/小说原文/霸道总裁爱上我', '霸道总裁爱上我')


if __name__ == "__main__":
    main()