<?php
require 'vendor/autoload.php';

use Symfony\Component\Yaml\Yaml;

// โหลดไฟล์ YAML
$filePath = 'tasks.yaml';
$data = Yaml::parseFile($filePath);

// แก้ไขข้อความใน description
$data['research_task']['description'] = 'สถานที่ท่องเที่ยว 5 จังหวัด {topic} - Updated version';
$data['Writing_task']['description'] = 'เพิ่มคำแนะนำเกี่ยวกับสถานที่เพิ่มเติม';

// เพิ่มข้อมูลใหม่
$data['research_task']['additional_info'] = 'This is a new field added to research_task';

// เขียนข้อมูลกลับไปที่ไฟล์ YAML
file_put_contents($filePath, Yaml::dump($data, 4, 2));

echo "แก้ไขและเพิ่มข้อมูลในไฟล์ YAML เรียบร้อยแล้ว!";
?>
