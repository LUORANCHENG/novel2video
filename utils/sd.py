import requests
import base64
import os
def generate_image(prompt: str, seed: int, width: int, height: int, txt_name, order):
    url = "http://0.0.0.0:7860"
    # print(prompt)
    payload = {
        "prompt": prompt,
        "negative_prompt": "booty, boob, (nsfw), (painting by bad-artist-anime:0.9), (painting by bad-artist:0.9), watermark, text, error, blurry, jpeg artifacts, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, artist name, (worst quality, low quality:1.4), bad anatomy",
        "cfg_scale": 7,
        "steps": 20,
        "seed": seed,
        "width": width,
        "height": height,
        "override_settings": {
            "sd_model_checkpoint": "niji-动漫二次元加强版_2.0"
            # "CLIP_stop_at_last_layers": 2,
        }
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    output_dir = f"./output/images/{txt_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filename = f"{output_dir}/{order}.png"
    with open(output_filename, 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))


# generate_image("inside a bus interior, there are three women and four men standing or sitting, each with distinct features and clothing, showcasing diversity and individuality, various expressions like happy, surprised, and curious, details of bus surroundings like seats, windows, and handles, vivid colors and dynamic poses, anime style, ((masterpiece))", 114514191981, 540, 960, 'test1', 1)
