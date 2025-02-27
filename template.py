import streamlit as st
import sys
import warnings
import yaml
import os
import subprocess
import openai
from project_aiver2.crew import ProjectAiver2
from crewai.project import crew
from dotenv import load_dotenv
load_dotenv()
#!/usr/bin/env python
import os
import requests

api_key = os.getenv("GEMINI_API_KEY")

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
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

# รับค่าจากผู้ใช้
def getDescription(provinces , days , nights , travel_styles , budget):
    # รับค่าจากผู้ใช้
    file_path = os.path.join(os.path.dirname(__file__), 'src/project_aiver2/config/tasks.yaml')
    new_description = f"ท่องเที่ยวจังหวัด{provinces} เที่ยว{days}วัน {nights}คืน และมีงบอยู่ที่ {budget} บาท โดยเน้นไปที่{travel_styles}"
    print(new_description)


st.title("ระบบวางแผนการท่องเที่ยว")


# เลือกจังหวัด (สามารถเลือกได้หลายจังหวัด)
st.header("เลือกจังหวัดที่จะไป")
provinces = st.multiselect(
    "กรุณาเลือกจังหวัดที่ต้องการไป:",
    options=["กาญจนบุรี", "ประจวบคีรีขันธ์", "ตาก", "เพชรบุรี", "ราชบุรี"],
    default=None,
)

# ระบุจำนวนวันและคืน
st.header("จำนวนวันที่ต้องการไป")
days = st.number_input("จำนวนวัน:", min_value=1, step=1, value=1)
nights = st.number_input("จำนวนคืน:", min_value = days-1 ,max_value = days, step=1, value=days-1)

# เลือกรูปแบบการท่องเที่ยว
st.header("เลือกรูปแบบการท่องเที่ยว")
travel_styles = st.multiselect(
    "เลือกประเภทการท่องเที่ยวที่ต้องการ:",
    options=["ธรรมชาติ", "คาเฟ่", "วัด", "ประวัติศาสตร์", "ทะเล", "ภูเขา", "ช้อปปิ้ง"],
    default=None,
)

# งบประมาณ
st.header("งบประมาณ")
budget = st.number_input("ระบุงบประมาณ (บาท):", min_value=0, step=100, value=0)

# แสดงข้อมูลที่กรอก
st.header("ข้อมูลที่คุณเลือก")
if st.button("ยืนยันข้อมูล"):
    if not provinces:
        st.warning("กรุณาเลือกจังหวัดอย่างน้อย 1 จังหวัด")
    elif not travel_styles:
        st.warning("กรุณาเลือกรูปแบบการท่องเที่ยวอย่างน้อย 1 ประเภท")
    else:
        st.success("ข้อมูลของคุณถูกบันทึกเรียบร้อยแล้ว!")
        st.write("**จังหวัดที่เลือก:**", ", ".join(provinces))
        st.write("**จำนวนวัน/คืน:**", f"{days} วัน {nights} คืน")
        st.write("**รูปแบบการท่องเที่ยว:**", ", ".join(travel_styles))
        st.write("**งบประมาณ:**", f"{budget:,} บาท")
        provinces = get_provinces(provinces)
        travel_styles = get_travel_styles(travel_styles)
        print(provinces , days , nights ,travel_styles,budget )
        with st.spinner("Running the crew..."):
            inputs = {"topic": "แนะนำสถานที่ท่องเที่ยว",
                      "provinces" : provinces,
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
        st.write(content)
        

