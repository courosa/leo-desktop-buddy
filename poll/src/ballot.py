from PIL import Image, ImageDraw, ImageFont

SRC = 'hairstyle-analysis.jpeg'
src = Image.open(SRC)

OPTIONS = [
    ((460,158,687,432), "TEXTURED MESSY FRINGE", True),
    ((689,158,914,432), "CURTAIN STYLE MIDDLE PART", True),
    ((917,158,1146,432), "NATURAL WAVES + VOLUME", True),
    ((16,570,233,806),  "SHORT TEXTURED CROP", False),
    ((240,570,461,806), "LAYERED SHAGGY CUT", False),
    ((468,570,689,806), "SIDE PART + WAVES", False),
    ((696,570,917,806), "QUIFF + TAPER", False),
    ((924,570,1146,806),"BRUSH UP + TEXTURE", False),
]

CREAM = (245,241,232); GREEN = (44,74,50); GOLD = (166,124,82); INK = (26,32,28)
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
f_title = ImageFont.truetype(B, 78)
f_sub   = ImageFont.truetype(R, 38)
f_name  = ImageFont.truetype(B, 30)
f_num   = ImageFont.truetype(B, 52)
f_tag   = ImageFont.truetype(B, 22)
f_foot  = ImageFont.truetype(B, 34)

W = 1200; M = 40; GAP = 28
CW = (W - 2*M - GAP)//2          # 552
PH = 520                          # photo height
LH = 84                           # label bar
RH = PH + LH + GAP
HEAD = 250; FOOT = 150
H = HEAD + 4*RH + FOOT

canvas = Image.new('RGB',(W,H),CREAM)
d = ImageDraw.Draw(canvas)

def center(text, font, y, fill, cx=W//2):
    w = d.textlength(text, font=font)
    d.text((cx-w/2, y), text, font=font, fill=fill)

# header
d.rectangle([0,0,W,HEAD-30], fill=GREEN)
center("LEO'S HAIR: THE VOTE", f_title, 42, CREAM)
center("Text back a number  •  1 vote each  •  no takebacks", f_sub, 138, (214,224,212))

def fit(box, tw, th):
    im = src.crop(box)
    sw, sh = im.size
    s = max(tw/sw, th/sh)
    im = im.resize((max(tw,int(sw*s)), max(th,int(sh*s))), Image.LANCZOS)
    w,h = im.size
    return im.crop(((w-tw)//2, 0, (w-tw)//2+tw, th))

for i,(box,name,top) in enumerate(OPTIONS):
    col, row = i%2, i//2
    x = M + col*(CW+GAP)
    y = HEAD + row*RH
    # card
    d.rectangle([x-4,y-4,x+CW+4,y+PH+LH+4], fill=(255,255,255))
    canvas.paste(fit(box, CW, PH), (x,y))
    # label bar
    d.rectangle([x, y+PH, x+CW, y+PH+LH], fill=GREEN)
    words = name.split()
    lines = [name]
    if d.textlength(name, font=f_name) > CW-110:
        best = None
        for k in range(1,len(words)):
            a,b_ = " ".join(words[:k]), " ".join(words[k:])
            m = max(d.textlength(a,font=f_name), d.textlength(b_,font=f_name))
            if best is None or m < best[0]: best = (m,[a,b_])
        lines = best[1]
    ty = y+PH + (LH - len(lines)*34)//2
    for ln in lines:
        d.text((x+24, ty), ln, font=f_name, fill=CREAM); ty += 34
    # number badge
    d.ellipse([x+18, y+18, x+18+76, y+18+76], fill=CREAM, outline=GREEN, width=4)
    n = str(i+1); nw = d.textlength(n, font=f_num)
    d.text((x+18+38-nw/2, y+18+9), n, font=f_num, fill=GREEN)
    if top:
        tw_ = d.textlength("TOP PICK", font=f_tag)
        d.rounded_rectangle([x+CW-tw_-46, y+22, x+CW-18, y+22+38], radius=19, fill=GOLD)
        d.text((x+CW-tw_-32, y+30), "TOP PICK", font=f_tag, fill=(255,252,246))

fy = HEAD + 4*RH + 6
d.rectangle([0, fy, W, H], fill=GREEN)
center("Reply with your number  →  1  2  3  4  5  6  7  8", f_foot, fy+34, CREAM)
center("Leo gets one veto. Voting closes when Dad says so.", ImageFont.truetype(R,28), fy+82, (200,214,199))

canvas.save('leo-hair-ballot.jpg', quality=92)
print(canvas.size)
