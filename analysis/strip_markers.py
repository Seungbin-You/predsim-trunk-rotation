"""Make a copy of the .osim without markers (for the Fig 1a snapshot only).
Run from project root:  python analysis\\strip_markers.py
-> ..._nomarkers.osim next to the original; open it in the GUI and load motion.mot again."""
import xml.etree.ElementTree as ET
src = r'OpenSimModel\Hamner_modified\Model\Hamner_modified_scaled.osim'
dst = src.replace('.osim', '_nomarkers.osim')
tree = ET.parse(src); n = 0
for ms in tree.getroot().iter('MarkerSet'):
    objs = ms.find('objects')
    if objs is not None:
        n += len(list(objs)); objs.clear()
tree.write(dst, encoding='UTF-8', xml_declaration=True)
print(f'removed {n} markers -> {dst}')
