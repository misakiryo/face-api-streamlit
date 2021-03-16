import streamlit as st
from PIL import Image
import requests
import json
from PIL import ImageDraw
from PIL import ImageFont
import io

st.title("顔認識アプリ")

subscription_key = 'subscription_keyを入れるところ'
assert subscription_key

face_api_url = 'face_api_urlを入れるところ'



uploaded_file = st.file_uploader('Choose an image...', type ='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得
    headers = {
    'Content-Type': 'application/octet-stream', 
    'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = {
    'returnFaceId': 'true', 
    'returnFaceAttributes': 'age, gender, headpose, smile, facialhair, glasses, emotion, hair, makeup, occlusion, blur, exposure, noise, accessories' 
    }

    res = requests.post(face_api_url, params=params, headers = headers, data = binary_img)

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        gender = result['faceAttributes']['gender']
        age = round(result['faceAttributes']['age'])

        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill =None, outline='green', width =5)
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf', 25)
        draw.text((rect['left'], rect['top']-50), gender+str(age), fill ='yellow',font =font,  spacing=20, align ='right')

    st.image(img, caption='Uploaded Image.',  use_column_width=True)


