from PIL import Image
import base64, io, json
src = Image.open('hairstyle-analysis.jpeg')
OPTIONS = [
    ((460,158,687,432), "Textured Messy Fringe", 1),
    ((689,158,914,432), "Curtain Style Middle Part", 1),
    ((917,158,1146,432), "Natural Waves + Volume", 1),
    ((16,570,233,806),  "Short Textured Crop", 0),
    ((240,570,461,806), "Layered Shaggy Cut", 0),
    ((468,570,689,806), "Side Part + Waves", 0),
    ((696,570,917,806), "Quiff + Taper", 0),
    ((924,570,1146,806),"Brush Up + Texture", 0),
]
def fit(box, tw, th):
    im = src.crop(box); sw,sh = im.size
    s = max(tw/sw, th/sh)
    im = im.resize((max(tw,int(sw*s)), max(th,int(sh*s))), Image.LANCZOS)
    w,h = im.size
    return im.crop(((w-tw)//2,0,(w-tw)//2+tw,th))
out=[]
for box,name,top in OPTIONS:
    im = fit(box, 440, 460)
    buf = io.BytesIO(); im.save(buf,'JPEG',quality=80,optimize=True)
    out.append({"name":name,"top":bool(top),"img":"data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()})
json.dump(out, open('options.json','w'))
print(sum(len(o['img']) for o in out)/1024, "KB total")
