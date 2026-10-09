"""Render storefront social cards using the site's native color and type system."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
S=2
COLORS={'paper':'#f7f6f2','ink':'#172439','muted':'#586575','blue':'#365bce','yellow':'#f7c948','lavender':'#e5eafd'}
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size*S)
def box(d,xy,fill,radius=18,outline=None,width=1):
 d.rounded_rectangle(tuple(int(v*S) for v in xy),radius=radius*S,fill=fill,outline=outline,width=width*S)
def text(d,xy,value,size,color,bold=False):d.text((xy[0]*S,xy[1]*S),value,font=font(size,bold),fill=color)
def line(d,points,color,width=3):d.line([(x*S,y*S) for x,y in points],fill=color,width=width*S,joint='curve')
def ellipse(d,xy,fill,outline=None,width=1):d.ellipse(tuple(v*S for v in xy),fill=fill,outline=outline,width=width*S)

def controller(d):
 # An original controller illustration, drawn as a native vector-style asset.
 box(d,(805,195,1078,384),'#fff',48)
 d.polygon([(809*S,264*S),(776*S,405*S),(794*S,430*S),(843*S,418*S),(892*S,345*S)],fill='#fff')
 d.polygon([(1070*S,264*S),(1100*S,405*S),(1082*S,430*S),(1033*S,418*S),(984*S,345*S)],fill='#fff')
 box(d,(806,216,858,233),COLORS['blue'],7)
 box(d,(1024,216,1076,233),COLORS['blue'],7)
 box(d,(916,230,967,270),COLORS['lavender'],8)
 box(d,(837,269,857,329),COLORS['ink'],5)
 box(d,(817,289,877,309),COLORS['ink'],5)
 for x,y,c in [(1033,277,COLORS['blue']),(1009,301,COLORS['yellow']),(1057,301,COLORS['ink']),(1033,325,'#b4bdeb')]:ellipse(d,(x-9,y-9,x+9,y+9),c)
 ellipse(d,(892,313,927,348),COLORS['lavender'])
 ellipse(d,(957,313,992,348),COLORS['lavender'])
 ellipse(d,(900,321,919,340),COLORS['ink'])
 ellipse(d,(965,321,984,340),COLORS['ink'])
 # Floating accents echo the category icon tiles on the storefront.
 box(d,(1025,128,1090,193),COLORS['yellow'],18)
 line(d,[(1048,160),(1057,170),(1071,151)],COLORS['ink'],4)
 ellipse(d,(781,167,796,182),COLORS['blue'])
 ellipse(d,(1069,466,1085,482),COLORS['blue'])

def general_art(d):
 box(d,(790,163,955,369),'#fff',22)
 box(d,(973,224,1134,430),'#fff',22)
 box(d,(837,221,907,296),COLORS['blue'],13)
 line(d,[(850,240),(891,240),(891,275),(850,275),(850,240)],'#fff',3)
 line(d,[(842,286),(901,286)],'#fff',3)
 box(d,(807,321,902,332),COLORS['lavender'],5)
 box(d,(807,339,933,348),'#edf0f7',4)
 d.polygon([(1010*S,307*S),(1053*S,269*S),(1097*S,307*S)],fill=COLORS['yellow'])
 box(d,(1020,307,1088,365),COLORS['yellow'],5)
 box(d,(1045,331,1062,365),COLORS['ink'],3)
 box(d,(991,385,1086,396),COLORS['lavender'],5)
 box(d,(991,404,1111,413),'#edf0f7',4)
 ellipse(d,(1025,135,1043,153),COLORS['blue'])
 ellipse(d,(804,438,820,454),COLORS['yellow'])

def build(gaming):
 im=Image.new('RGB',(1200*S,630*S),COLORS['paper']);d=ImageDraw.Draw(im)
 box(d,(64,54,111,101),COLORS['yellow'],13)
 text(d,(76,55),'G',30,COLORS['ink'],True)
 text(d,(125,57),'Gardezi',31,COLORS['ink'],True)
 text(d,(275,57),'Finds.',31,COLORS['blue'],True)
 text(d,(64,162),'THE GAMING GIFT GUIDE' if gaming else 'EVERYDAY DISCOVERIES',14,COLORS['blue'],True)
 text(d,(60,205),'Great gaming gifts.' if gaming else 'Little finds.',52 if gaming else 63,COLORS['ink'],True)
 text(d,(60,277),'Start here.' if gaming else 'Everyday upgrades.',63 if gaming else 51,COLORS['blue'],True)
 text(d,(64,376),'Check the platform. Choose the right edition.' if gaming else 'Useful Amazon finds. Thoughtfully organized.',21,COLORS['muted'])
 text(d,(64,412),'A simple guide to a better gaming gift.' if gaming else 'For your home, your routine and your next hobby.',21,COLORS['muted'])
 chips=['Nintendo','PlayStation','Xbox','PC'] if gaming else ['Tech','Home','Beauty','Gaming']
 x=64
 for label in chips:
  w=d.textbbox((0,0),label,font=font(14))[2]/S+30
  box(d,(x,470,x+w,510),'#fff',20,outline='#e2e5e8')
  text(d,(x+15,480),label,14,COLORS['ink']);x+=w+10
 box(d,(741,137,1136,520),COLORS['lavender'],36)
 if gaming:controller(d)
 else:general_art(d)
 line(d,[(64,558),(1136,558)],'#e2e5e8',1)
 text(d,(64,578),'Independent product discovery · Amazon.com finds',13,COLORS['muted'])
 text(d,(972,578),'GARDEZI FINDS',13,COLORS['blue'],True)
 im.resize((1200,630),Image.Resampling.LANCZOS).save(ROOT/'assets'/('gaming-guide-preview-v2.png' if gaming else 'gardezi-finds-social.png'),optimize=True)

if __name__=='__main__':build(False);build(True)
