import utils.sd as sd

sd.generate_image("a girl, white dress", seed=114514, width=405, height=720, txt_name='test', order=1)
print("文件保存在./test/output/images/test/1.png")
