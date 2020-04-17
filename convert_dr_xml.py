import sys
import os
import glob
import shutil
import xml.etree.ElementTree as ET

if not os.path.exists("../results/"):
  os.makedirs("../results/")
if os.path.exists("../results/detection/"):
  shutil.rmtree("../results/detection/")
os.makedirs("../results/detection/")

# create VOC format files
xml_list = [f for f in os.listdir('../predictions') if f.endswith('xml')]
if len(xml_list) == 0:
  print("Error: no .xml files found in predictions")
  sys.exit()
for tmp_file in xml_list:
  print(tmp_file)
  with open(os.path.join('../results/detection', tmp_file.replace(".xml", ".txt")), "a") as new_f:
    root = ET.parse(os.path.join('../predictions', tmp_file)).getroot()
    for obj in root.findall('object'):
      obj_name = obj.find('name').text.replace(' ', '_').rstrip().lower()
      bndbox = obj.find('bndbox')
      left = bndbox.find('xmin').text
      top = bndbox.find('ymin').text
      right = bndbox.find('xmax').text
      bottom = bndbox.find('ymax').text
      conf = obj.find('difficult').text
      new_f.write("%s %s %s %s %s %s\n" % (obj_name, conf, left, top, right, bottom))
print("Conversion completed!")
