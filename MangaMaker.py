from reportlab.pdfgen import canvas
from PIL import Image,ImageEnhance  
import os


def ifCut():
    ans = raw_input("Do you want to cut images?[Y/N]")
    if ans in {"Y","y"}:
        return True
    elif ans in {"N","n"}:
        return False
    else:
        return ifCut()

def cutPage(filename,func=None):
    a = Image.open(filename)
    if func:
        a = func(a)
    if a.width >= a.height:
        return [a.crop((a.width/2 - 10,0,a.width,a.height)),a.crop((0,0,a.width/2 + 10,a.height))]
    else:
        return [a]

def getPath(RE = None,before="C:\\"):
    print "We are in [%s]."%before
    dirs = [i for i in os.listdir(before) if os.path.isdir(before + i)]
    for num,i in enumerate(dirs):
        print "[%i]%s"%(num,i)
    print "="*18
    print '[Choose - Num]   [Go Back - B]    [Stop - Enter]'
    while 1:
        inp = raw_input("$ ")
        if inp == "B" or inp == 'b':
            return
        elif inp == "":
            return before
        else:
            try:
                inp = int(inp)
                if inp>len(dirs)-1 or inp<0:
                    continue
            except ValueError,e:
                continue
            ans = getPath(before=before+dirs[inp]+'\\')
            if ans:
                return ans
            for num,i in enumerate(dirs):
                print "[%i]%s"%(num,i)
            print "="*18
            print '[Choose - Num]   [Go Back - B]    [Stop - Enter]'
            continue
                
def chooseType(tp="kindle"):
    if tp == "kindle":
        return 114.0 * 3,166.0 * 3

def cutMovement(path,pdfname,pagesize=(114.0 * 3,166.0 * 3),cut=True,func=None):
    """
    Read Images at Path, then save them as a PDF file.
    """
    flist = os.listdir(path)
    flist = [path+item for item in flist if item[-3:] in {"jpg","png"}]

    c = canvas.Canvas(filename+".pdf",pagesize=pagesize)
    if not cut:
        for num,i in enumerate(flist):
            c.drawImage(i,0,0,W,H)
            c.showPage()
            print "Page %i Finished."%(num+1)
    else:
        num = 0
        for i in flist:
            for ir in [canvas.ImageReader(im) for im in cutPage(i,func=func)]:
                c.drawImage(ir,0,0,W,H)
                c.showPage()
                num += 1
                print "Page %i Finished."%num
    c.save()

if __name__=="__main__":
    while 1:
        W,H = chooseType()
        path = getPath()
        filename = raw_input("Input Filename Here: (Default HelloWorld.pdf)")
        if not len(filename):
            filename = "HelloWorld"
        cut = ifCut()

        def func(im):
            p = 0.8
            ans = im.draft(mode="L",size=(int(im.width * p),int(im.height * p)))
            if ans: 
                im = ImageEnhance.Sharpness(ans).enhance(1.6)
            else:
                im = im.resize((int(im.width * p),int(im.height * p)),resample=0)
            return im

        cutMovement(path,filename,pagesize=(W,H),cut=cut,func=func)
        raw_input("Any Key to Continue. Ctrl+C to Quit.")
