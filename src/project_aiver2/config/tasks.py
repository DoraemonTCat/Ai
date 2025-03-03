tasks_config = {
    "research_task": {
        "description": "ท่องเที่ยวจังหวัด{provinces} เที่ยว{days}วัน {nights}คืน และมีงบอยู่ที่ {budget} บาท โดยเน้นไปที่{travel_styles}",
        "expected_output": "รายการข้อมูลสำคัญ {topic}",
        "agent": "researcher"
    },
    "Writing_task": {
        "description": "สร้างสถานที่แนะนำ 1.สถานที่ท่องเที่ยว 2.ร้านอาหารแนะนำ 3.สถานที่พักแนะนำ 4.รายการค่าใช้จ่ายแบบเป็นตัวเลข",
        "expected_output": "แนะนำสถานที่ท่องเที่ยวแล้วก็พวกจัดแพ็คเกจไปที่ไหนพักที่ไหนกินที่ไหน",
        "agent": "Writer",
        "output_file": "content.md",
        "context": ["research_task"]
    }
}
