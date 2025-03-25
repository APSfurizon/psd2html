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

# Debug testing:
# class ArgsObj:
# 	def __init__(self, d=None):
# 		if d is not None:
# 			for key, value in d.items():
# 				setattr(self, key, value)
# args = ArgsObj({
# 	"file": "../Furizon/badges/BadgesZenithMerged.psd",
# 	"mm": True
# })

'''
a = {
    "KinsokuSet": [
        {
            "Name": "PhotoshopKinsokuHard",
            "NoStart": "、。，．・：；？！ー―’”）〕］｝〉》」』】ヽヾゝゞ々ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶ゛゜?!)]},.:;℃℉¢％‰",
            "NoEnd": "‘“（〔［｛〈《「『【([{￥＄£＠§〒＃",
            "Keep": "―‥",
            "Hanging": "、。.,",
        },
        {
            "Name": "PhotoshopKinsokuSoft",
            "NoStart": "、。，．・：；？！’”）〕］｝〉》」』】ヽヾゝゞ々",
            "NoEnd": "‘“（〔［｛〈《「『【",
            "Keep": "―‥",
            "Hanging": " 、。.,",
        },
    ],
    "MojiKumiSet": [
        {"InternalName": "Photoshop6MojiKumiSet1"},
        {"InternalName": "Photoshop6MojiKumiSet2"},
        {"InternalName": "Photoshop6MojiKumiSet3"},
        {"InternalName": "Photoshop6MojiKumiSet4"},
    ],
    "TheNormalStyleSheet": 0,
    "TheNormalParagraphSheet": 0,
    "ParagraphSheetSet": [
        {
            "Name": "Normal RGB",
            "DefaultStyleSheet": 0,
            "Properties": {
                "Justification": 0,
                "FirstLineIndent": 0.0,
                "StartIndent": 0.0,
                "EndIndent": 0.0,
                "SpaceBefore": 0.0,
                "SpaceAfter": 0.0,
                "AutoHyphenate": True,
                "HyphenatedWordSize": 6,
                "PreHyphen": 2,
                "PostHyphen": 2,
                "ConsecutiveHyphens": 8,
                "Zone": 36.0,
                "WordSpacing": [0.8, 1.0, 1.33],
                "LetterSpacing": [0.0, 0.0, 0.0],
                "GlyphSpacing": [1.0, 1.0, 1.0],
                "AutoLeading": 1.2,
                "LeadingType": 0,
                "Hanging": False,
                "Burasagari": False,
                "KinsokuOrder": 0,
                "EveryLineComposer": False,
            },
        }
    ],
    "StyleSheetSet": [
        {
            "Name": "Normal RGB",
            "StyleSheetData": {
                "Font": 2,
                "FontSize": 12.0,
                "FauxBold": False,
                "FauxItalic": False,
                "AutoLeading": True,
                "Leading": 0.0,
                "HorizontalScale": 1.0,
                "VerticalScale": 1.0,
                "Tracking": 0,
                "AutoKerning": True,
                "Kerning": 0,
                "BaselineShift": 0.0,
                "FontCaps": 0,
                "FontBaseline": 0,
                "Underline": False,
                "Strikethrough": False,
                "Ligatures": True,
                "DLigatures": False,
                "BaselineDirection": 2,
                "Tsume": 0.0,
                "StyleRunAlignment": 2,
                "Language": 0,
                "NoBreak": False,
                "FillColor": {"Type": 1, "Values": [1.0, 0.0, 0.0, 0.0]},
                "StrokeColor": {"Type": 1, "Values": [1.0, 0.0, 0.0, 0.0]},
                "FillFlag": True,
                "StrokeFlag": False,
                "FillFirst": True,
                "YUnderline": 1,
                "OutlineWidth": 1.0,
                "CharacterDirection": 0,
                "HindiNumbers": False,
                "Kashida": 1,
                "DiacriticPos": 2,
            },
        }
    ],
    "FontSet": [
        {"Name": "RoundedElegance-Regular", "Script": 0, "FontType": 1, "Synthetic": 0},
        {"Name": "AdobeInvisFont", "Script": 0, "FontType": 0, "Synthetic": 0},
        {"Name": "MyriadPro-Regular", "Script": 0, "FontType": 0, "Synthetic": 0},
    ],
    "SuperscriptSize": 0.583,
    "SuperscriptPosition": 0.333,
    "SubscriptSize": 0.583,
    "SubscriptPosition": 0.333,
    "SmallCapSize": 0.7,
}


b = {
    "Editor": {"Text": "11223344\r"},
    "ParagraphRun": {
        "DefaultRunData": {
            "ParagraphSheet": {"DefaultStyleSheet": 0, "Properties": {}},
            "Adjustments": {"Axis": [1.0, 0.0, 1.0], "XY": [0.0, 0.0]},
        },
        "RunArray": [
            {
                "ParagraphSheet": {
                    "DefaultStyleSheet": 0,
                    "Properties": {
                        "Justification": 2, # https://github.com/felixSchl/photoshop.d.ts/blob/master/dist/cc/ps.constants.d.ts
                        "FirstLineIndent": 0.0,
                        "StartIndent": 0.0,
                        "EndIndent": 0.0,
                        "SpaceBefore": 0.0,
                        "SpaceAfter": 0.0,
                        "AutoHyphenate": True,
                        "HyphenatedWordSize": 6,
                        "PreHyphen": 2,
                        "PostHyphen": 2,
                        "ConsecutiveHyphens": 8,
                        "Zone": 36.0,
                        "WordSpacing": [0.8, 1.0, 1.33],
                        "LetterSpacing": [0.0, 0.0, 0.0],
                        "GlyphSpacing": [1.0, 1.0, 1.0],
                        "AutoLeading": 1.2,
                        "LeadingType": 0,
                        "Hanging": False,
                        "Burasagari": False,
                        "KinsokuOrder": 0,
                        "EveryLineComposer": False,
                    },
                },
                "Adjustments": {"Axis": [1.0, 0.0, 1.0], "XY": [0.0, 0.0]},
            }
        ],
        "RunLengthArray": [9],
        "IsJoinable": 1,
    },
    "StyleRun": {
        "DefaultRunData": {"StyleSheet": {"StyleSheetData": {}}},
        "RunArray": [
            {
                "StyleSheet": {
                    "StyleSheetData": {
                        "Font": 0,
                        "FontSize": 58.38475,
                        "FauxBold": False,
                        "FauxItalic": False,
                        "AutoLeading": True,
                        "Leading": 70.06171,
                        "HorizontalScale": 1.0,
                        "VerticalScale": 1.0,
                        "Tracking": 0,
                        "AutoKerning": True,
                        "Kerning": 0,
                        "BaselineShift": 0.0,
                        "FontCaps": 0,
                        "FontBaseline": 0,
                        "Underline": False,
                        "Strikethrough": False,
                        "Ligatures": True,
                        "DLigatures": False,
                        "BaselineDirection": 1,
                        "Tsume": 0.0,
                        "StyleRunAlignment": 2, # https://documentation.help/Illustrator-CS6/pe_StyleRunAlignmentType.html
                        "Language": 7,
                        "NoBreak": False,
                        "FillColor": {"Type": 1, "Values": [1.0, 0.0, 0.0, 0.0]},
                        "StrokeColor": {
                            "Type": 1,
                            "Values": [1.0, 0.98038, 0.62744, 0.76471],
                        },
                        "YUnderline": 1,
                        "HindiNumbers": False,
                        "Kashida": 1,
                    }
                }
            }
        ],
        "RunLengthArray": [9],
        "IsJoinable": 2,
    },
    "GridInfo": {
        "GridIsOn": False,
        "ShowGrid": False,
        "GridSize": 18.0,
        "GridLeading": 22.0,
        "GridColor": {"Type": 1, "Values": [0.0, 0.0, 0.0, 1.0]},
        "GridLeadingFillColor": {"Type": 1, "Values": [0.0, 0.0, 0.0, 1.0]},
        "AlignLineHeightToGridFlags": False,
    },
    "AntiAlias": 4,
    "UseFractionalGlyphWidths": True,
    "Rendered": {
        "Version": 1,
        "Shapes": {
            "WritingDirection": 0,
            "Children": [
                {
                    "ShapeType": 0,
                    "Procession": 0,
                    "Lines": {"WritingDirection": 0, "Children": []},
                    "Cookie": {
                        "Photoshop": {
                            "ShapeType": 0,
                            "PointBase": [0.0, 0.0],
                            "Base": {
                                "ShapeType": 0,
                                "TransformPoint0": [1.0, 0.0],
                                "TransformPoint1": [0.0, 1.0],
                                "TransformPoint2": [0.0, 0.0],
                            },
                        }
                    },
                }
            ],
        },
    },
}

'''

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
		checkname = re.sub(',','', checkname)
		checkname = re.sub('\\.','', checkname)
		checkname = re.sub('\\s', '-', checkname)
		checkname = re.sub('\\*', '-', checkname)
		checkname = re.sub('#', '-', checkname)
		checkname = re.sub('©', '', checkname)
		return checkname

def psdColorArrToHexStr(arr) -> str:
    def x(c: int) -> str:
        return "%02x" % int(255 * c)
    return f"#{x(arr[1])}{x(arr[2])}{x(arr[3])}{x(arr[0])}"

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
	html = ''
	for layer in reversed(layers):
		if layer.is_group():
			print(layer)
			site = layerstoimage(layer)
			html += site
		else:
			# process name to make unique and strip special characters
			name = namelayer(layer.name, 0)
			elements.append(name)
			print(f"Processing Layer: {name}")

			# create css
			style = ""
			style += f'left: {getCorrectDimStr(layer.bbox[0], widthPx, widthCm)}; '
			style += f'top: {getCorrectDimStr(layer.bbox[1], heightPx, heightCm)}; '
			style += f'position: absolute; '
			style += f'width: {getCorrectDimStr(layer.bbox[2] - layer.bbox[0], widthPx, widthCm)}; '
			style += f'height: {getCorrectDimStr(layer.bbox[3] - layer.bbox[1], heightPx, heightCm)}; '
			style += f'z-index: {zIndex}; '

			zIndex -= 1

			if layer.kind == 'type':
				texts = ""
				# Extract font for each substring in the text.
				text = layer.engine_dict['Editor']['Text'].value
				fontset = layer.resource_dict['FontSet']
				runlength = layer.engine_dict['StyleRun']['RunLengthArray']
				rundata = layer.engine_dict['StyleRun']['RunArray']
				index = 0
				for length, rd in zip(runlength, rundata):
					substring: str = text[index:index + length]
					substring = substring.replace("\n", "").replace("\r", "")
					stylesheet = rd['StyleSheet']['StyleSheetData']
					font = fontset[stylesheet['Font']]
					index += length
					# What we don't support: markdown (EG, bold, italics, etc) + alignment/justification
					textStyle = ""
					textStyle += f'font-family: {font["Name"]}; '
					textStyle += f'font-size: {getCorrectDimStr(stylesheet["FontSize"], widthPx, widthCm)}; '
					textStyle += f'color: {psdColorArrToHexStr(stylesheet["FillColor"]["Values"])}; '
					texts += f'    <span style="{textStyle}">{substring}</span>\n'
				html += f'  <p id="{name}" style="{style}">\n{texts}  </p>\n'
	 
			else:
				style += f'background-repeat: no-repeat; '
				style += f'background-size: contain; '
				style += f'background-image: url(\'images/{name}.png\'); '
				# create html
				html += f'  <div id="{name}" style="{style}"></div>\n'
				# save images as images
				layer_image = layer.topil()
				layer_image.save(f"images/{name}.png")

	return html

cssWidthStr = f"{apporximateStr(widthCm * 10)}mm" if args.mm else f"{psd.width}px"
cssHeightStr = f"{apporximateStr(heightCm * 10)}mm" if args.mm else f"{psd.height}px"

html = f'''
<html>
<head>
<script>window.print();</script>
<style>
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
</style>
</head>
<body>
  <div class="page">
{layerstoimage(psd)}
  </div>
</body>
</html>
'''

f = codecs.open('index.html','w', "utf-8")
f.write(html)
f.close()
