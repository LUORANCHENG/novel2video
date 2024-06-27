import requests
import parsel
import os
import re

# 用于字体解密的码字字典
dit_data = {
    '58670': '0',
    '58413': '1',
    '58678': '2',
    '58371': '3',
    '58353': '4',
    '58480': '5',
    '58359': '6',
    '58449': '7',
    '58540': '8',
    '58692': '9',
    '58712': 'a',
    '58542': 'b',
    '58575': 'c',
    '58626': 'd',
    '58691': 'e',
    '58561': 'f',
    '58362': 'g',
    '58619': 'h',
    '58430': 'i',
    '58531': 'j',
    '58588': 'k',
    '58440': 'l',
    '58681': 'm',
    '58631': 'n',
    '58376': 'o',
    '58429': 'p',
    '58555': 'q',
    '58498': 'r',
    '58518': 's',
    '58453': 't',
    '58397': 'u',
    '58356': 'v',
    '58435': 'w',
    '58514': 'x',
    '58482': 'y',
    '58529': 'z',
    '58515': 'A',
    '58688': 'B',
    '58709': 'C',
    '58344': 'D',
    '58656': 'E',
    '58381': 'F',
    '58576': 'G',
    '58516': 'H',
    '58463': 'I',
    '58649': 'J',
    '58571': 'K',
    '58558': 'L',
    '58433': 'M',
    '58517': 'N',
    '58387': 'O',
    '58687': 'P',
    '58537': 'Q',
    '58541': 'R',
    '58458': 'S',
    '58390': 'T',
    '58466': 'U',
    '58386': 'V',
    '58697': 'W',
    '58519': 'X',
    '58511': 'Y',
    '58634': 'Z',
    '58611': '的',
    '58590': '一',
    '58398': '是',
    '58422': '了',
    '58657': '我',
    '58666': '不',
    '58562': '人',
    '58345': '在',
    '58510': '他',
    '58496': '有',
    '58654': '这',
    '58441': '个',
    '58493': '上',
    '58714': '们',
    '58618': '来',
    '58528': '到',
    '58403': '大',
    '58461': '地',
    '58481': '为',
    '58700': '子',
    '58708': '中',
    '58503': '你',
    '58442': '说',
    '58639': '生',
    '58506': '国',
    '58663': '年',
    '58436': '着',
    '58563': '就',
    '58391': '那',
    '58357': '和',
    '58354': '要',
    '58695': '她',
    '58372': '出',
    '58696': '也',
    '58551': '得',
    '58445': '里',
    '58408': '后',
    '58599': '自',
    '58424': '以',
    '58394': '会',
    '58348': '家',
    '58426': '可',
    '58673': '下',
    '58417': '而',
    '58556': '过',
    '58603': '天',
    '58565': '去',
    '58604': '能',
    '58522': '对',
    '58632': '小',
    '58622': '多',
    '58350': '然',
    '58605': '于',
    '58617': '心',
    '58401': '学',
    '58637': '么',
    '58684': '之',
    '58382': '都',
    '58464': '好',
    '58487': '看',
    '58693': '起',
    '58608': '发',
    '58392': '当',
    '58474': '没',
    '58601': '成',
    '58355': '只',
    '58573': '如',
    '58499': '事',
    '58469': '把',
    '58361': '还',
    '58698': '用',
    '58489': '第',
    '58711': '样',
    '58457': '道',
    '58635': '想',
    '58492': '作',
    '58647': '种',
    '58623': '开',
    '58521': '美',
    '58609': '总',
    '58530': '从',
    '58665': '无',
    '58652': '情',
    '58676': '己',
    '58456': '面',
    '58581': '最',
    '58509': '女',
    '58488': '但',
    '58363': '现',
    '58685': '前',
    '58396': '些',
    '58523': '所',
    '58471': '同',
    '58485': '日',
    '58613': '手',
    '58533': '又',
    '58589': '行',
    '58527': '意',
    '58593': '动',
    '58699': '方',
    '58707': '期',
    '58414': '它',
    '58596': '头',
    '58570': '经',
    '58660': '长',
    '58364': '儿',
    '58526': '回',
    '58501': '位',
    '58638': '分',
    '58404': '爱',
    '58677': '老',
    '58535': '因',
    '58629': '很',
    '58577': '绘',
    '58606': '多',
    '58497': '法',
    '58662': '间',
    '58479': '斯',
    '58532': '知',
    '58380': '世',
    '58385': '什',
    '58405': '两',
    '58644': '次',
    '58578': '使',
    '58505': '身',
    '58564': '者',
    '58412': '被',
    '58686': '高',
    '58624': '已',
    '58667': '亲',
    '58607': '其',
    '58616': '进',
    '58368': '此',
    '58427': '话',
    '58423': '常',
    '58633': '与',
    '58525': '活',
    '58543': '正',
    '58418': '感',
    '58597': '见',
    '58683': '明',
    '58507': '问',
    '58621': '力',
    '58703': '理',
    '58438': '尔',
    '58536': '占',
    '58384': '文',
    '58484': '几',
    '58539': '定',
    '58554': '木',
    '58421': '公',
    '58347': '特',
    '58569': '做',
    '58710': '外',
    '58574': '孩',
    '58375': '相',
    '58645': '西',
    '58592': '果',
    '58572': '走',
    '58388': '将',
    '58370': '月',
    '58399': '十',
    '58651': '实',
    '58546': '向',
    '58504': '声',
    '58419': '车',
    '58407': '全',
    '58672': '信',
    '58675': '重',
    '58538': '三',
    '58465': '机',
    '58374': '工',
    '58579': '物',
    '58402': '气',
    '58702': '每',
    '58553': '并',
    '58360': '别',
    '58389': '真',
    '58560': '打',
    '58690': '太',
    '58473': '新',
    '58512': '比',
    '58653': '才',
    '58704': '便',
    '58545': '夫',
    '58641': '再',
    '58475': '书',
    '58583': '部',
    '58472': '水',
    '58478': '像',
    '58664': '眼',
    '58586': '等',
    '58568': '体',
    '58674': '却',
    '58490': '加',
    '58476': '电',
    '58346': '主',
    '58630': '界',
    '58595': '门',
    '58502': '利',
    '58713': '海',
    '58587': '受',
    '58548': '听',
    '58351': '表',
    '58547': '德',
    '58443': '少',
    '58460': '克',
    '58636': '代',
    '58585': '员',
    '58625': '许',
    '58694': '稜',
    '58428': '先',
    '58640': '口',
    '58628': '由',
    '58612': '死',
    '58446': '安',
    '58468': '写',
    '58410': '性',
    '58508': '马',
    '58594': '光',
    '58483': '白',
    '58544': '或',
    '58495': '住',
    '58450': '难',
    '58643': '望',
    '58486': '教',
    '58406': '命',
    '58447': '花',
    '58669': '结',
    '58415': '乐',
    '58444': '色',
    '58549': '更',
    '58494': '拉',
    '58409': '东',
    '58658': '神',
    '58557': '记',
    '58602': '处',
    '58559': '让',
    '58610': '母',
    '58513': '父',
    '58500': '应',
    '58378': '直',
    '58680': '字',
    '58352': '场',
    '58383': '平',
    '58454': '报',
    '58671': '友',
    '58668': '关',
    '58452': '放',
    '58627': '至',
    '58400': '张',
    '58455': '认',
    '58416': '接',
    '58552': '告',
    '58614': '入',
    '58582': '笑',
    '58534': '内',
    '58701': '英',
    '58349': '军',
    '58491': '候',
    '58467': '民',
    '58365': '岁',
    '58598': '往',
    '58425': '何',
    '58462': '度',
    '58420': '山',
    '58661': '觉',
    '58615': '路',
    '58648': '带',
    '58470': '万',
    '58377': '男',
    '58520': '边',
    '58646': '风',
    '58600': '解',
    '58431': '叫',
    '58715': '任',
    '58524': '金',
    '58439': '快',
    '58566': '原',
    '58477': '吃',
    '58642': '妈',
    '58437': '变',
    '58411': '通',
    '58451': '师',
    '58395': '立',
    '58369': '象',
    '58706': '数',
    '58705': '四',
    '58379': '失',
    '58567': '满',
    '58373': '战',
    '58448': '远',
    '58659': '格',
    '58434': '士',
    '58679': '音',
    '58432': '轻',
    '58689': '目',
    '58591': '条',
    '58682': '呢',
}

def remove_unwanted_text(text):
    """移除章节标题、空行和空格"""
    # 移除章节标题
    text = re.sub(r'第\d+章.*?[\r\n]+', '', text, flags=re.DOTALL)
    # 移除所有空行
    text = re.sub(r'\n\s*\n', '\n', text)
    # 移除所有行首和行尾的空格（包括文本中间的空行）
    text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
    text = text.replace("'", "").replace('"', "").replace("”", "").replace('“', '')
    text = text.replace("?", ",").replace("？", ",")
    text = text.replace("……", ",")
    text = text+'。'
    return text

# 发送请求：模拟浏览器对于url地址发送请求
headers = {
    'Cookie':'s_v_web_id=verify_lxv92wzy_ApG24Fd0_gjyL_466A_ARnL_1736W4xZoOK2; csrf_session_id=7a500758378d73e2c4df00888c1d4244; novel_web_id=7101332169921454477; serial_uuid=7101332169921454477; serial_webid=7101332169921454477; passport_csrf_token=5ef9f11db52d7d9b0d6f482d56a5a0a3; passport_csrf_token_default=5ef9f11db52d7d9b0d6f482d56a5a0a3; d_ticket=78528e13fc813b222aab71a3e22d70f93a535; odin_tt=e20947166b4d961385f6a9d3c0aab251cc5f4fd2d175f06f4027360f99edbe36b15cbbfff394c1d187b11573f4995194f698c4204d89f8571b46c7bd1dc9b9ac; n_mh=K-QT9aYc6S7R1RrONXgs75OxUE2VqileLmLOSH2sdK8; passport_auth_status=2ba4a6b445477953f55e90037b134952%2C; passport_auth_status_ss=2ba4a6b445477953f55e90037b134952%2C; sid_guard=f59404f9a28b9f777a812dc299792541%7C1719371007%7C5184000%7CSun%2C+25-Aug-2024+03%3A03%3A27+GMT; uid_tt=aa0fbbaaa39766d6315854b743b9104c; uid_tt_ss=aa0fbbaaa39766d6315854b743b9104c; sid_tt=f59404f9a28b9f777a812dc299792541; sessionid=f59404f9a28b9f777a812dc299792541; sessionid_ss=f59404f9a28b9f777a812dc299792541; sid_ucp_v1=1.0.0-KGY1MDc2MTM3ZTJiMTJkZDZiNjMzOTBkOTZjOTE1ZmVhMjAyYzg3NGIKHwjjnYDC-8ytBhD_ie6zBhjHEyAMMP-J7rMGOAJA7AcaAmhsIiBmNTk0MDRmOWEyOGI5Zjc3N2E4MTJkYzI5OTc5MjU0MQ; ssid_ucp_v1=1.0.0-KGY1MDc2MTM3ZTJiMTJkZDZiNjMzOTBkOTZjOTE1ZmVhMjAyYzg3NGIKHwjjnYDC-8ytBhD_ie6zBhjHEyAMMP-J7rMGOAJA7AcaAmhsIiBmNTk0MDRmOWEyOGI5Zjc3N2E4MTJkYzI5OTc5MjU0MQ; store-region=cn-gd; store-region-src=uid; Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1719394820; Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1719395683; ttwid=1%7CviOF-tP8KM0M---fsVfuLmfV16uPiJ9I9wXSnvLarLY%7C1719395683%7C613d645eba582507b395707e1076ada9ec69b3673ab55d856955ab0c8a95c688; msToken=hMxzhL6IvoFL44-m6O_2YZWzjazrdG6YCVrW_HLhmLH8RVI5HMR8EXW904XecjdRTOV_bnUfPBb2ndgirgEePuR80qDhOEq7TlFFRlUy4W7JIc7yJDH2',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

book_id = input("请输入要爬取书目的ID：")
start_chapters_num = int(input("请输入起始章节数字："))
end_chapters_num = int(input("请输入结束章节数字："))

# url地址
url = f'https://fanqienovel.com/page/{book_id}?enter_from=search'

# 发送请求
response = requests.get(url=url, headers=headers)

# 获取数据
html = response.text
# print(html)

# 解析数据
# 把数据转换成可解析的对象
selector = parsel.Selector(html)

# 提取书名
book_name = selector.css('.page-header-info .info-name h1::text').get()

# 创建保存小说内容的文件夹
book_directory = f"../素材/小说原文/{book_name}"
if not os.path.exists(book_directory):
    os.makedirs(book_directory)


# 提取章节ID和章节名字
title_name_list = selector.css('.chapter .chapter-item-title::text').getall()
title_ID_list = selector.css('.chapter .chapter-item-title::attr(href)').getall()

# 创建一个计数器来记录爬取的章节数
flag = 1
for title, link in zip(title_name_list, title_ID_list):
    if (flag<start_chapters_num) or (flag>end_chapters_num):
        break
    # 完整的小说章节链接
    link_url = 'https://fanqienovel.com' + link
    print(title, link_url)
    # 发送请求，获取数据内容
    link_data = requests.get(url=link_url, headers=headers).text
    # 解析数据，提取小说内容
    link_setector = parsel.Selector(link_data)
    content_list = link_setector.css('.muye-reader-content-16 p::text').getall()
    # 把列表合并成字符串
    content = ''.join(content_list)
    # 解密字体
    novel_content = ""
    for index in content:
        try:
            word = dit_data[str(ord(index))]
        except:
            word = index
        novel_content += word
    # 将整篇文章按句号划分成一个个句子，存放在列表中
    novel_content_list = novel_content.split('。')
    # 小说每章内容的保存路径
    content_path = book_directory + f'/chapters_{flag}.txt'
    with open(content_path, mode='w', encoding='utf-8') as f:
        for sentence in novel_content_list:
            text = remove_unwanted_text(sentence)
            text.replace(r'\ue4fc', '时')
            f.write(text)
            f.write('\n')
    flag+=1











#     # 发送请求，获取数据内容
#     link_data = requests.get(url=link_url, headers=headers).text
#     # 解析数据，提取小说内容
#     link_setector = parsel.Selector(link_data)
#     content_list = link_setector.css('.muye-reader-content-16 p::text').getall()
#     # 把列表合并成字符串
#     content = '\n\n'.join(content_list)
#     novel_content = ""
#     # 解密字体
#     for index in content:
#         try:
#             word = dit_data[str(ord(index))]
#
#         except:
#             word = index
#         novel_content += word
#     with open(name+'.txt', mode='a', encoding='utf-8') as f:
#         f.write(title)
#         f.write('\n\n')
#         f.write(novel_content)
#         f.write('\n\n')