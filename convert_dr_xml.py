import sys
import os
import glob
import shutil
import xml.etree.ElementTree as ET
from pdb import set_trace as bp

# create VOC format files
xml_list = [f for f in os.listdir('./res') if f.endswith('xml') or f.endswith('csv')]
if len(xml_list) == 0:
    print("Error: no .xml or .csv files found in predictions")
    sys.exit()
for tmp_file in xml_list:
    # print(tmp_file)
    if tmp_file.endswith('xml'):
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
    elif tmp_file.endswith('csv'):
        shutil.copy("../predictions/%s"%tmp_file, "../results/detection/%s"%tmp_file.replace(".csv", ".txt"))
        # os.system("cp ../predictions/%s ../results/detection/%s"%(tmp_file, tmp_file.replace(".csv", ".txt")))
print("Conversion completed!")
