#!/usr/bin/env python
# coding=utf-8
'''
@描述: 
@版本: V1_0
@作者: LiWanglin
@创建时间: Do not edit
@最后编辑人: LiWanglin
@最后编辑时间: Do not Edit
'''
import base64
import io
import os
import json
import requests
from PIL import Image
import datetime

predict_instance_json_file_name = "inputs.json"

def convert_images(img_list, output_dir):
      with open(os.path.join(output_dir, predict_instance_json_file_name), "wb") as fp:
        fp.write("{\"instances\": [".encode('utf-8'))
        json_body = []
        for image in img_list:
          img = Image.open(image)
          output_str = io.BytesIO()
          img.save(output_str, "JPEG")
          base64_bytes = base64.b64encode(output_str.getvalue())
          base64_string = base64_bytes.decode('utf-8')
          json_data = json.dumps({"b64": base64_string})
          json_body.append(json_data)
          output_str.close()
        fp.write((",".join(json_body)).encode('utf-8'))
        fp.write("]}".encode('utf-8'))
        print(os.path.join(output_dir, predict_instance_json_file_name))

def run_test():
    headers = {'Content-Type': 'application/json'}
    with open('/tmp/inputs.json') as image_json_file:
        image_json = json.load(image_json_file)
    image_string = json.dumps(image_json)

    r = requests.post("http://localhost:8889/tree/http_request/tmp",
                        data=image_string, headers=headers)
    time_end = datetime.datetime.now()
    print(time_end - time_begin)
    print(r.content)

time_begin = datetime.datetime.now()
convert_images(["tmp/image0.bmp", "tmp/image0.bmp"], "tmp")
run_test()