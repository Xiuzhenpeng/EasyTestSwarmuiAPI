import gradio as gr
import requests

css = """
#stateemjio {
    width: 30px !important;
    display: inline-block;
    text-align: center;
    overflow: hidden;
}
"""

def testurlstate(url):
    if url == "":
        return gr.update(value="未测地址"), gr.Warning("请填入地址")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return gr.update(value="地址可用✔️"), None
        else:
            return gr.update(value=f"未通过测试，状态码{response.status_code}")
    except requests.RequestException as e:
        return gr.update(value=f"未通过测试，错误：{e}"), None

with gr.Blocks(css=css) as demo:
    gr.Markdown("## 这是为了方便测试Swarmui的api而创建的测试项目")
    with gr.Row():
        swarmuiurl = gr.Textbox(placeholder="填入swarmui的地址", container=False)
        texturl = gr.Button(value="测试地址")
        swarmuiurlstate = gr.Textbox("未测地址",elem_id="stateemjio", container=False, max_lines=1)
        test = gr.Textbox(visible=False)
        texturl.click(testurlstate, swarmuiurl, outputs=[swarmuiurlstate, test])

demo.launch()