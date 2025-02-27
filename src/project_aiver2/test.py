#!/usr/bin/env python
import streamlit as st
import sys
import warnings
import yaml
import os

from project_aiver2.crew import ProjectAiver2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
def get_Value(provinces , days , nights , travel_styles , budget):
    provinces = " ".join(provinces)
    travel_styles = " ".join(travel_styles)
    return provinces , days , nights , travel_styles , budget
def update_description(file_path, new_description):
    # โหลดไฟล์ YAML
    with open(file_path ,encoding='utf-8') as file:
        data = yaml.safe_load(file)
        data['research_task']['description'] = new_description + "{topic}"

    # เขียนข้อมูลกลับไปที่ไฟล์ YAML
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, sort_keys=False)
        print("ไฟล์ YAML ถูกอัปเดตเรียบร้อยแล้ว!")

# รับค่าจากผู้ใช้
def getDescription():
    # รับค่าจากผู้ใช้
    file_path = os.path.join(os.path.dirname(__file__), 'config/tasks.yaml')
    new_description = f"ท่องเที่ยวจังหวัด{provinces} เที่ยว{days}วัน {nights}คืน และมีงบอยู่ที่ {budget} บาท โดยเน้นไปที่{travel_styles}"
    print(new_description)
    # เรียกฟังก์ชันเพื่ออัปเดต
    update_description(file_path, new_description)

def run():
    """
    Run the crew.
    """
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
        get_Value(provinces , days , nights , travel_styles , budget)
        getDescription()
        st.success("ข้อมูลของคุณถูกบันทึกเรียบร้อยแล้ว!")
        st.write("**จังหวัดที่เลือก:**", ", ".join(provinces))
        st.write("**จำนวนวัน/คืน:**", f"{days} วัน {nights} คืน")
        st.write("**รูปแบบการท่องเที่ยว:**", ", ".join(travel_styles))
        st.write("**งบประมาณ:**", f"{budget:,} บาท")
    
        with open("../../output/report.md" , 'r' , encoding = 'utf-8') as file:
            content = file.read()
        st.write(content)
    inputs = {
        'topic': 'AI Agent สำหรับแนะนำสถานที่ท่องเที่ยว'
    }
    ProjectAiver2().crew().kickoff(inputs=inputs)