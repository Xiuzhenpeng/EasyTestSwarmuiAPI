import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import json
import random
import urllib.request
import urllib.parse
import base64
from PIL import Image
from io import BytesIO
import requests

def get_new_session(url):
    data = json.dumps({}).encode('utf-8')
    req = urllib.request.Request(f"http://{url}/API/GetNewSession", data=data)
    req.add_header("Content-Type", "application/json")
    response = urllib.request.urlopen(req).read()
    return json.loads(response)

url = "localhost:23091"
ws = websocket.WebSocket()
# seed = random.randint(1, 2**32)
seed = 1073741824

image_path = r"C:\Users\xiuzhenpeng\Desktop\fluxUnionControlnet_v10\ComfyUI_00040_.png"
with open(image_path, "rb") as image_file:
    base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    print(type(base64_string))

base_prompt = "best quality, masterpiece, high-res, iatsh, tinted windows, car design, clean surface, glossy finish, Glossy paint, pearlescent, water-like, clean background, studio lighting"

prompt_data = {
    "session_id": "//session_id",
    "images": 1,
    "seed":seed,
    "model": "chilloutmix_NiPrunedFp16Fix",
    "initimage":f"{base64_string}",
    "comfyuicustomworkflow": "光影优化（SD15）",
    "comfyrawworkflowinputtextpositivepromptnodetextbe":base_prompt,
    "comfyrawworkflowinputdropdownefficientloadernodeloranamep":"EXT/02.机甲凶猛.safetensors",
    "comfyrawworkflowinputdecimalefficientloadernodeloraclipstrengthp":"0.8",
    "comfyrawworkflowinputdecimalefficientloadernodeloramodelstrengthp":"0.8",
    "comfyrawworkflowinputseedseedeverywherenodeseede":seed,
    "comfyrawworkflowinputdecimalksamplerefficientnodedenoises":0.5,
}

session_id = get_new_session(url)["session_id"]
print(type(session_id))

ws.connect(f"ws://{url}/API/GenerateText2ImageWS")

# 添加 session_id 到 prompt_data
prompt_data["session_id"] = session_id

ws.send(json.dumps(prompt_data))

# 初始化图像计数器
image_counter = 0

# 创建/清空文件
with open("output.txt", "w") as file:
    pass

# 接收数据
while True:
    try:
        out = ws.recv()
        
        # 将数据追加写入 output.txt 文件
        with open("output.txt", "a") as file:
            file.write(out + "\n")  # 每次接收到的数据换行写入

        if isinstance(out, str):
            try:
                message = json.loads(out)
                if 'gen_progress' in message:
                    data = message["gen_progress"]
                    if 'preview' in data:
                        image_base64 = data["preview"].split(",")[-1]
                        # 这里可以选择解码并显示图像
                        # image_data = base64.b64decode(image_base64)
                        # image = Image.open(BytesIO(image_data))
                        # image.show()
                if "image" in message:
                    image_name = message["image"]
                    image_url = f"http://{url}/{image_name}"
                    print(image_url)
                    # 这里可以选择下载并显示图像
                    # response = requests.get(image_url)
                    # image = Image.open(BytesIO(response.content))
                    # image.show()
                    ws.close()
            except json.JSONDecodeError:
                ws.close()
    except websocket.WebSocketConnectionClosedException:
        break
          