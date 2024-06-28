import utils.tts_pro as tts

text = "叶婉晴从不知道一天一夜有那么漫长，漫长到可以让一个人从希望到绝望，从鲜活到行尸走肉，连心脏都被冻结。"
tts.generate_audio(text=text, language='cn', txt_name="test", order=1)
print(f"文件保存在./test/output/audio/test/cn/1.mp3")
