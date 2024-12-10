import gradio as gr
import json
import urllib.request

url = "60.205.191.88:2301"

def testurlstate(url):
    data = json.dumps({}).encode('utf-8')
    req = urllib.request.Request(f"http://{url}/API/GetNewSession", data=data)
    req.add_header("Content-Type", "application/json")
    response = urllib.request.urlopen(req).read()
    return json.loads(response)

resqonse = testurlstate(url)
print(resqonse)