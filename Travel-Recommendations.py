import streamlit as st
import sys
import warnings
import yaml
import os
import subprocess
import openai
import base64
from PIL import Image
import markdown
from markupsafe import Markup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from project_aiver2.crew import ProjectAiver2

from crewai.project import crew
from dotenv import load_dotenv
load_dotenv()
#!/usr/bin/env python
openai_api_key = os.getenv("GEMINI_API_KEY")


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
st.set_page_config(page_title="AI แนะนำสถานที่ท่องเที่ยวภาคตะวันตก", layout="wide")  # ตั้งค่าเป็น Wide Mode
def get_provinces(provinces):
    n_provinces = ""
    for i in range(len(provinces)):
        n_provinces = n_provinces +" "+ provinces[i]
    return n_provinces

def get_travel_styles(travel_styles):
    n_travel_styles = ""
    for i in range(len(travel_styles)):
        n_travel_styles = n_travel_styles + " "+ travel_styles[i]
    return n_travel_styles

# ใส่ Banner โดยใช้ st.image()
image_path = os.path.join("images", "หน้าปก.png")

# แสดง Banner
st.markdown(
    f"""
    <style>
    .banner-img {{
        display: block;
        margin: auto;
        width: 100%; 
        height: 400px;  
        object-fit: cover;
    }}
    </style>
    <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" class="banner-img">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;700&display=swap');

    html, body, [class*="st-"] {{
        font-family: 'Prompt', sans-serif;
    }}
    .hover-img {
        transition: transform 0.3s ease-in-out;
        margin: 5px;
        width:100%;
    }
    .hover-img:hover {
        transform: scale(1.1); /* ขยาย 1.1 เท่า */
    }
    h1,h2,h3,h4{{
        font-family: 'Prompt', sans-serif;
    }}
    </style>
    """,unsafe_allow_html=True)
st.write(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;700&display=swap');

            html, body, [class*="st-"] {{
                font-family: 'Prompt', sans-serif;
            }}
            .header{{
                font-size : 24px;
                font-style : Bold;
            }}
              
        </style>
        
        """, unsafe_allow_html=True)
# เลือกจังหวัด
st.markdown("""<h2 style="text-align: center; font-family : 'Prompt', sans-serif;">อยากไปที่ไหน</h2>""", unsafe_allow_html=True)

# พาธของโฟลเดอร์รูปภาพ
image_folder = "images"

# รายชื่อจังหวัดและพาธรูปภาพ
provinces = {
    "กาญจนบุรี": os.path.join(image_folder, "กาญ.jpg"),
    "ประจวบคีรีขันธ์": os.path.join(image_folder, "ประจวบ.jpg"),
    "ตาก": os.path.join(image_folder, "ตาก.jpg"),
    "เพชรบุรี": os.path.join(image_folder, "เพชรบุรี.jpg"),
    "ราชบุรี": os.path.join(image_folder, "ราชบุรี.jpg"),
}

# ตัวเลือกจังหวัด (ใช้ checkbox สำหรับเลือกหลายรายการ)
selected_provinces = []

# แสดงตัวเลือกในรูปแบบรูปภาพ
st.markdown("""<h4 style="font-family : 'Prompt', sans-serif;">คลิกเลือกจังหวัดที่ต้องการ</h4>""", unsafe_allow_html=True)
cols_per_row = 5  # จำนวนรูปภาพต่อแถว
cols = st.columns(cols_per_row)  # สร้างคอลัมน์ตามจำนวนที่กำหนด

# เพิ่ม CSS สำหรับการขยายรูปเมื่อเอาเมาส์ไปวาง

# ฟังก์ชั่นสำหรับแปลงรูปเป็น base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# แสดงภาพและให้ผู้ใช้เลือก checkbox
for i, (province, image_path) in enumerate(provinces.items()):
    with cols[i % cols_per_row]:  # วนซ้ำในแต่ละคอลัมน์
        # แปลงภาพเป็น base64
        encoded_image = image_to_base64(image_path)
        # แสดงภาพพร้อมกับ class สำหรับ hover effect
        st.markdown(
            f'<img src="data:image/jpg;base64,{encoded_image}" class="hover-img" width="150">',
            unsafe_allow_html=True
        )
        if st.checkbox(f"{province}", key=f"checkbox_{i}"):
            selected_provinces.append(province)

# แสดงผลจังหวัดที่เลือก
if selected_provinces:
    
    #สร้างเส้นขั้น
    st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)
    st.markdown("""<h6 style="font-family : 'Prompt', sans-serif;">จังหวัดที่คุณเลือก</h6>""", unsafe_allow_html=True)
    st.write(", ".join(selected_provinces))
else:
    st.markdown("""<h6 style="font-family : 'Prompt', sans-serif;">ยังไม่ได้เลือกจังหวัด</h6>""", unsafe_allow_html=True)

# สร้างเส้นขั้น
st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)

# ระบุจำนวนวันและคืน
st.markdown("""<h4 style="font-family : 'Prompt', sans-serif;">จำนวนวันที่ต้องการไป</h4>""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    days = st.number_input("จำนวนวัน:", min_value=1, step=1, value=1)
with col2:
    # จำนวนคืนต้องสัมพันธ์กับจำนวนวัน
    nights = st.number_input("จำนวนคืน:", min_value=days-1, max_value=days, step=1, value=days-1)

import streamlit as st

#สร้างเส้นขั้น
st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)

# เลือกรูปแบบการท่องเที่ยว
st.markdown("""<h4 style="font-family : 'Prompt', sans-serif;">เลือกรูปแบบการท่องเที่ยว</h4>""", unsafe_allow_html=True)
travel_styles = st.multiselect(
    "เลือกประเภทการท่องเที่ยวที่ต้องการ:",
    options=["🌿 ธรรมชาติ",
    "☕ คาเฟ่",
    "⛩️ วัด",
    "🏰 ประวัติศาสตร์",
    "🌊 ทะเล",
    "⛰️ ภูเขา",
    "🛍️ ช้อปปิ้ง"],
    default=None,
)

#สร้างเส้นขั้น
st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)

# งบประมาณ
st.markdown("""<h4 style="font-family : 'Prompt', sans-serif;">งบประมาณ</h4>""", unsafe_allow_html=True)
budget = st.number_input("ระบุงบประมาณ (บาท):", min_value=0, step=100, value=0)

#สร้างเส้นขั้น
st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)

# แสดงข้อมูลที่กรอก
selected_provinces = get_provinces(selected_provinces)
travel_styles = get_travel_styles(travel_styles)
if st.button("ยืนยันข้อมูล"):
    st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)
    if not selected_provinces:
        st.warning("กรุณาเลือกจังหวัดอย่างน้อย 1 จังหวัด")
    elif not travel_styles:
        st.warning("กรุณาเลือกรูปแบบการท่องเที่ยวอย่างน้อย 1 ประเภท")
    else:
        st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;700&display=swap');

            html, body, [class*="st-"] {{
                font-family: 'Prompt', sans-serif;
            }}
            .box-1 {{
                border: 3px solid black; /* กรอบสีดำ */
                padding: 15px;
                border-radius: 10px;
                background-color:rgba(240, 240, 240, 0.89);
                width: 80%;
                text-align: left;
                color : black ;
                margin : auto auto;
            }}
            .box-2 {{
                font-family: 'Prompt', sans-serif;
                border: 3px solid black; /* กรอบสีดำ */
                padding: 15px;
                border-radius: 10px;
                background-color:rgba(240, 240, 240, 0.89);
                width: 90%;
                margin: auto auto; 
                text-align: left;
                color : black;
            }}
            .button {{
                background-color:rgb(228, 237, 224);
                padding: 10px;
                display: inline-block;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 10px;
            }}
            .success {{
                background-color: #DFF0D8;
                padding: 10px;
                border-radius: 5px;
            }}
            .custom-heading {{
                font-family : 'Prompt', sans-serif;
                font-size : 24px;
                font-weight : bold;
                text-align : center;
            }}
            h2 {{
                font-family: 'Prompt', sans-serif;
            }}
        </style>
        
        <div class="box-1">
            <h3 style="font-family : 'Prompt', sans-serif;">ข้อมูลที่คุณเลือก</h3>
            <div class="success">✅ ข้อมูลของคุณถูกบันทึกเรียบร้อยแล้ว!</div>
            <p><b>จังหวัดที่เลือก:</b> {selected_provinces}</p>
            <p><b>จำนวนวัน/คืน:</b> {days} วัน {nights} คืน</p>
            <p><b>รูปแบบการท่องเที่ยว:</b> {travel_styles}</p>
            <p><b>งบประมาณ:</b> {budget:,} บาท</p>
        </div>
        
        """, unsafe_allow_html=True)
        
        #สร้างเส้นขั้น
        st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)
        
        # แสดงข้อความแนะนำ
        st.markdown("""<h3 style="font-family : 'Prompt', sans-serif;">สถานที่ท่องเที่ยวแนะนำคือ</h3>""", unsafe_allow_html=True)
        
        with st.spinner("Running the crew..."):
            inputs = {"topic": "แนะนำสถานที่ท่องเที่ยว",
                        "provinces" : selected_provinces,
                        "days" : days,
                        "nights" : nights,
                        "travel_styles": travel_styles,
                        "budget":budget
                        }
            crew = ProjectAiver2().crew()
            crew.kickoff(inputs=inputs)
        filepath = "output/report.md"
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        import re
        content_html = markdown.markdown(content)
        st.markdown(
            f' <div class="box-2">{content_html}</div> ',
            unsafe_allow_html=True
        )
