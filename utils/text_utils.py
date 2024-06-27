def read_txt(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用列表推导式读取非空行，并删除所有\xa0字符
        content = [line.replace('\xa0', '') for line in file.read().split('\n') if line.strip()]
    return content