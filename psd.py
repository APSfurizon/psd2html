# -*- coding: utf-8 -*-
from psd_tools import PSDImage
from psd_tools.constants import Resource
from psd_tools.psd.image_resources import ResoulutionInfo
import re, argparse
import codecs

parser = argparse.ArgumentParser(description="A script that converts a Photoshop file into HTML/CSS Edit")
parser.add_argument("-f", "--file", required=True)
parser.add_argument("-m", "--mm", action=argparse.BooleanOptionalAction)
args, leftovers = parser.parse_known_args()

psd: PSDImage = PSDImage.open(args.file)

widthPx = psd.width
heightPx = psd.height
widthCm = heightCm = 0
if (args.mm):
	# Get size in mm. Reference:
	# - https://github.com/GNOME/gimp/blob/e139e016a58da2545119a51fbf49745535ea22e4/plug-ins/file-psd/psd-image-res-load.c#L567
	# - https://github.com/GNOME/gimp/blob/e139e016a58da2545119a51fbf49745535ea22e4/plug-ins/file-psd/psd.h#L281
	resInfo: ResoulutionInfo = psd.image_resources.get_data(Resource.RESOLUTION_INFO)
	ppcVertical = resInfo.vertical / 65536.0
	if resInfo.vertical_unit != 2:
		ppcVertical /= 2.54
	heightCm = heightPx / ppcVertical
	ppcHorizontal = resInfo.horizontal / 65536.0
	if resInfo.horizontal_unit != 2:
		ppcHorizontal /= 2.54
	widthCm = widthPx / ppcHorizontal

# if layer name is already used for an id append _n, where n is smallest available number
def namelayer(checkname: str, i: int):
	if(checkname in elements):
		i += 1
		# remove _n if i higher than 1
		if(i > 1):
			splitstring = checkname.split('_')
			splitstring.pop()
			checkname = ''.join(splitstring)
		return namelayer(f"{checkname}_{i}", i)
	else:
		return checkname
	
def apporximateStr(i: int):
	return "%.2f" % i
def getCorrectDimStr(dim, sizePx, sizeCm):
	#dimPx : maxPx = ? : maxCm
	return f"{apporximateStr(((dim * sizeCm) / sizePx) * 10)}mm" if args.mm else f"{dim}px"

zIndex = 289
elements = []
def layerstoimage(layers: PSDImage):
	global zIndex
	global elements
	html, css = '', ''
	for layer in reversed(layers):
		if layer.is_group():
			site = layerstoimage(layer.layers)
			html += site[0]
			css += site[1]
		else:
			# process name to make unique and strip special characters
			name = namelayer(layer.name, 0)
			elements.append(name)
			name = re.sub(',','', name)
			name = re.sub('\\.','', name)
			name = re.sub('\\s', '-', name)
			name = re.sub('\\*', '-', name)
			name = re.sub('#', '-', name)
			name = re.sub('©', '', name)
			print(f"Processing Layer: {name}")
			
			print(psd.size, layer.bbox)
			

			# create css
			css += f'''
#{name}{{
  left: {getCorrectDimStr(layer.bbox[0], widthPx, widthCm)};
  top: {getCorrectDimStr(layer.bbox[1], heightPx, heightCm)};
  position: absolute;
  width: {getCorrectDimStr(layer.bbox[2] - layer.bbox[0], widthPx, widthCm)};
  height: {getCorrectDimStr(layer.bbox[3] - layer.bbox[1], heightPx, heightCm)};
  background-repeat: no-repeat;
  background-size: contain;
  background-image: url("images/{name}.png");
  z-index: {zIndex}
}}
'''
			zIndex -= 1

			# create html
			html += f'  <div id="{name}"></div>\n'

			# save images as images
			layer_image = layer.topil()
			layer_image.save(f"bin/images/{name}.png")

	return html, css

html = '''
<html>
<head>
<link rel="stylesheet" href="index.css">
</head>
<body>
  <div class="page">
'''
cssWidthStr = f"{apporximateStr(widthCm * 10)}mm" if args.mm else f"{psd.width}px"
cssHeightStr = f"{apporximateStr(heightCm * 10)}mm" if args.mm else f"{psd.height}px"
css = f'''
body {{
	width: 100%;
	height: 100%;
	position: absolute;
	margin: 0;
	padding: 0;
}}
* {{
	box-sizing: border-box;
	-moz-box-sizing: border-box;
}}
.page {{
	position: relative;
	width: {cssWidthStr};
	min-height: {cssHeightStr};
}}
@page {{
	size: {cssWidthStr} {cssHeightStr};
	margin: 0;
}}
@media print {{
	html, body {{
		width: {cssWidthStr};
		height: {cssHeightStr};        
	}}
	.page {{
		margin: 0;
		border: initial;
		border-radius: initial;
		width: initial;
		min-height: initial;
		box-shadow: initial;
		background: initial;
		page-break-after: always;
	}}
}}
'''

site = layerstoimage(psd)
html += site[0]
html += '  </div>\n</body>\n</html>'
css += site[1]

f = codecs.open('bin/index.html','w', "utf-8")
f.write(html)
f.close()

f = codecs.open('bin/index.css','w', "utf-8")
f.write(css)
f.close()
