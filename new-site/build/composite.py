"""Compose assets/hero/belt-wallet-sherpa.jpg.

Starts from the Regal wallet frame (source-images/Kignsman/Regal/KRW_1438.JPG), removes the
second (black) wallet by rebuilding the backdrop behind it, softens the frame slightly so the wallet
sits back, then places two belt cutouts in front: the Outlaw coil behind and the Monarch coil in
front with the Stagr mark debossed on its face. Run from new-site/:

    python3 build/composite.py            # writes the asset + 2000/1200/800 sizes
    python3 build/composite.py --debug    # also writes build/_composite-debug/*.jpg and stops
"""
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageEnhance
import numpy as np, scipy.ndimage as ndi, scipy.sparse as sp, scipy.sparse.linalg as spl, sys
import os
S='build/_composite-debug/'
os.makedirs(S,exist_ok=True)
DEBUG='--debug' in sys.argv

def deboss(belt, mark, cx, cy, frac, rot, strength=.5):
    bw,bh=belt.size; mw=int(bw*frac); m=mark.resize((mw,int(mark.height*mw/mark.width)),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    ma=np.array(m)[...,3].astype(float)/255; layer=np.zeros((bh,bw),float); x,y=int(cx*bw)-m.width//2,int(cy*bh)-m.height//2
    layer[y:y+m.height,x:x+m.width]=ma; rim=np.clip(np.roll(np.roll(layer,-2,0),-2,1)-layer,0,1)
    arr=np.array(belt).astype(float)
    for c in range(3): arr[...,c]=np.clip(arr[...,c]*(1-strength*layer)+40*rim,0,255)
    return Image.fromarray(arr.astype(np.uint8))
def grade(belt, tint, fall):
    r,g,b,a=belt.split(); arr=np.asarray(Image.merge('RGB',(r,g,b))).astype(float)*np.array(tint)
    arr=arr*np.linspace(1.0,fall,arr.shape[0])[:,None,None]; rgb=ImageEnhance.Contrast(Image.fromarray(np.clip(arr,0,255).astype(np.uint8))).enhance(1.06)
    return Image.merge('RGBA',(*rgb.split(),a))
def shadow(bg, belt, x0, y0, strength=200, squash=.3):
    al=np.array(belt)[...,3]; ys,xs=np.where(al>40); bx0,by0,bx1,by1=x0+xs.min(),y0+ys.min(),x0+xs.max(),y0+ys.max()
    sh=Image.new('RGBA',bg.size,(0,0,0,0)); d=ImageDraw.Draw(sh); h=int((by1-by0)*squash); sy=by1-h*.35
    d.ellipse([bx0+(bx1-bx0)*.02, sy-h/2, bx1-(bx1-bx0)*.02, sy+h/2], fill=(30,12,4,strength)); bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(int(bg.width*.018)))); return (bx0,by0,bx1,by1)

# ---------- source + removal of the second (black) wallet ----------
mark=Image.open('../stagr-lockup-dark.png').convert('RGBA')
src=ImageOps.exif_transpose(Image.open('../source-images/Kignsman/Regal/KRW_1438.JPG')).convert('RGB')
W,H=src.size; c=src.crop((int(W*.08),0,W,H)); W,H=c.size
X=lambda f:int(W*f); Y=lambda f:int(H*f)
A=np.asarray(c).astype(np.float32)
R,G,B=A[...,0],A[...,1],A[...,2]; mx=A.max(2)
# black wallet: dark + neutral, inside its bounding box
black=(mx<110)&((R-B)<8)
bbox=np.zeros((H,W),bool); bbox[Y(.16):Y(.68),X(.17):X(.62)]=True
black&=bbox
black=ndi.binary_closing(black,iterations=12)
black=ndi.binary_fill_holes(black)
black=ndi.binary_opening(black,iterations=6)          # drop specks
lab,n=ndi.label(black); sizes=ndi.sum(black,lab,range(1,n+1)); black=lab==(1+int(np.argmax(sizes)))
hole=ndi.binary_dilation(black,iterations=52)          # ~22px margin over the stitching/edge
band=ndi.binary_dilation(hole,iterations=30)&~hole      # ring where the donor must agree with the photo

# donor: fine texture only, borrowed from clean textile at the same rows (rows above the brown wallet
# come from the far right, the column beside it from just right of the wallet); the base tone is then
# interpolated smoothly from the surrounding backdrop so no donor patch can show through.
def shift(a,dx):
    o=np.empty_like(a); o[:, :W-dx]=a[:, dx:]; o[:, W-dx:]=a[:, W-1:W]; return o
D1=shift(A,X(.40)); D2=shift(A,X(.22))
t=np.clip((np.arange(H)-Y(.272))/(Y(.292)-Y(.272)),0,1)[:,None,None]; t=t*t*(3-2*t)
D=D1*(1-t)+D2*t
sc=8; h,w=H//sc,W//sc
def down(a): return np.asarray(Image.fromarray(np.clip(a,0,255).astype(np.uint8)).resize((w,h),Image.BOX)).astype(np.float32)
def up(a): return np.asarray(Image.fromarray(np.clip(a+128,0,255).astype(np.uint8)).resize((W,H),Image.BICUBIC)).astype(np.float32)-128
def mblur(img,valid,sig=5):
    v=valid.astype(np.float32)[...,None]; num=ndi.gaussian_filter(img*v,(sig,sig,0)); den=ndi.gaussian_filter(v,(sig,sig,0))
    return num/np.maximum(den,1e-3)
validA=~ndi.binary_dilation(black,iterations=62)
validA[Y(.21):Y(.67), X(.05):X(.505)]=False; validA[Y(.40):Y(.53), X(.50):X(.63)]=False
vD1=shift(validA.astype(np.float32)[...,None],X(.40))[...,0]; vD2=shift(validA.astype(np.float32)[...,None],X(.22))[...,0]
validD=(vD1*(1-t[...,0])+vD2*t[...,0])>.5
dm=lambda b: np.asarray(Image.fromarray(b.astype(np.uint8)*255).resize((w,h),Image.BOX))>127
Alow=mblur(down(A),dm(validA)); Dlow=mblur(down(D),dm(validD))
maskL=lambda b,th: np.asarray(Image.fromarray(b.astype(np.uint8)*255).resize((w,h),Image.BOX))>th
bandL=maskL(band,100); holeL=maskL(hole,60)
rects=np.zeros((h,w),bool)
rects[int(h*.21):int(h*.67), int(w*.05):int(w*.505)]=True   # brown wallet
rects[int(h*.40):int(h*.53), int(w*.50):int(w*.63)]=True    # tool tip
valid=bandL&~rects
roi=ndi.binary_dilation(holeL|rects,iterations=6)
unk=roi&~valid
idx=-np.ones((h,w),int); ids=np.where(unk.ravel())[0]; idx.ravel()[ids]=np.arange(len(ids)); N=len(ids)
rows,cols,vals=[],[],[]; rhs=np.zeros((N,3),np.float32)
ui,uj=np.where(unk)
for k,(i,j) in enumerate(zip(ui,uj)):
    rows.append(k); cols.append(k); vals.append(4.0)
    for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
        ii,jj=i+di,j+dj
        if ii<0 or jj<0 or ii>=h or jj>=w: vals[-1]-=1; continue
        if unk[ii,jj]: rows.append(k); cols.append(idx[ii,jj]); vals.append(-1.0)
        else: rhs[k]+=Alow[ii,jj]
M=sp.csr_matrix((vals,(rows,cols)),shape=(N,N))
sol=np.stack([spl.spsolve(M,rhs[:,ch]) for ch in range(3)],1)
L=Alow.copy(); L[unk]=sol
fill=np.clip(D-up(Dlow-128)+up(L-128),0,255)
m=ndi.gaussian_filter(hole.astype(np.float32),16)[...,None]
base=Image.fromarray(np.clip(A*(1-m)+fill*m,0,255).astype(np.uint8))
p=base.copy(); p.thumbnail((1400,1400)); p.save(S+'base.jpg',quality=85)
if DEBUG:
    p=base.copy(); p.thumbnail((1400,1400)); p.save(S+'base.jpg',quality=85)
    ov=A.copy(); ov[hole]=ov[hole]*.4+np.array([0,255,0])*.6; pp=Image.fromarray(ov.astype(np.uint8)); pp.thumbnail((1400,1400)); pp.save(S+'mask.jpg',quality=80); print('debug saved'); sys.exit()

# ---------- composite ----------
bg=base.filter(ImageFilter.GaussianBlur(2.6)).convert('RGBA')
bB=grade(Image.open('assets/cutouts/outlaw-1.webp').convert('RGBA'),[1.03,.94,.84],.8)
w_=X(.34); bB=bB.resize((w_,int(bB.height*w_/bB.width)),Image.LANCZOS); xB,yB=X(.66)-bB.width//2,Y(.57)-bB.height//2
shadow(bg,bB,xB,yB,170); bg.alpha_composite(bB,(xB,yB))
bA=Image.open('assets/cutouts/monarch-1.webp').convert('RGBA'); bA=deboss(bA,mark,.70,.72,.10,-4,.48); bA=grade(bA,[1.04,.93,.80],.8)
w_=X(.40); bA=bA.resize((w_,int(bA.height*w_/bA.width)),Image.LANCZOS); xA,yA=X(.52)-bA.width//2,Y(.76)-bA.height//2
box=shadow(bg,bA,xA,yA,210); bg.alpha_composite(bA,(xA,yA))
fur=base.convert('RGBA'); mk=Image.new('L',bg.size,0); md=ImageDraw.Draw(mk)
md.rectangle([box[0],box[3]-int((box[3]-box[1])*.07),box[2],box[3]],fill=120); mk=mk.filter(ImageFilter.GaussianBlur(14)); bg=Image.composite(fur,bg,mk)
out=bg.convert('RGB'); out.save('assets/hero/belt-wallet-sherpa.jpg',quality=86,optimize=True,progressive=True)
for s in (2000,1200,800):
    o=out.copy(); o.thumbnail((s,s),Image.LANCZOS); o.save(f'assets/hero/belt-wallet-sherpa-{s}.jpg',quality=84,optimize=True,progressive=True)
p=out.copy(); p.thumbnail((1400,1400)); p.save(S+'preview.jpg',quality=85); print('ok')
