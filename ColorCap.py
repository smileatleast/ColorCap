'''
Color Cap v.1.0
@smileatleast 11.4.2015
please install python 2.X and PIL before using.
not tested for python 3.X

Instructions:
1. clearPickle() to clear out old data
2. startCap(n, box) to start capture every n seconds & send to pkl file;
    suggested minimum of 2. Use optional arg "box" (x, y, width, height)
    to define height 
3. Ctrl+C to stop capture
4. If necessary, remove caps from pkl dict using timestamp keys, then savePickle()
5. processAvg(file_path) or processFreq(file_path) to create image using the 
    average or most frequent color in each cap.
'''

import pickle, datetime, os, time
from PIL import Image, ImageGrab
from numpy import mean
from collections import Counter
from random import shuffle

        
# --- Cap Functions --
def screenCap(box, i):
    print("capturing...")
    cap = ImageGrab.grab(box)
    now = datetime.datetime.now()
    pkl.append(cap)
    savePickle()
    print("cap #" + str(i) + " @" + now.strftime("%b %d %H:%M:%S") )
    
def schedCap(n, box=None):
    i = 0
    while True:
        time.sleep(n)
        screenCap(box, i)
        i += 1

# --- SubProcessing ---

# -functions- 
def rgbToHex(rgb_tup):
    return '#%02x%02x%02x' % rgb_tup

def preProcess():
    #pkl = loadPickle() #just in case
    avgs = []
    timestamps = pkl.keys()
    timestamps.sort()
    return timestamps
    
def processAvg(file_path):
    #if os.path.splitext(file_path)[1] not in [".jpg", ".jpeg"]:
    #    print(".JPG paths only please")
    avgs = []
    for t in preProcess():
        c = ColorCapObj(pkl[t])
        avgs.append(c.avgColor())
    convertToPic(file_path, avgs)
    
def processFreq(file_path):
    freqs = []
    for t in preProcess():
        c = ColorCapObj(pkl[t])
        freqs.append(c.mostFreqColor())
    convertToPic(file_path, freqs)

def convertToPic(file_path, colors):
    img = Image.new("RGB", (len(colors), 200))
    pix = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pix[x,y] = colors[x]
    img.save(file_path)
    

# -class-
class ColorCapObj:
    def __init__(self,img):
        self.img = img
        self.pix = self.img.load()
        self.r = []
        self.g = []
        self.b = []
        self.rgb = []
        
        for x in range(self.img.size[0]):
            for y in range(self.img.size[1]):
                i = self.pix[x,y]
                self.r.append(i[0])
                self.g.append(i[1])
                self.b.append(i[2])
                self.rgb.append(i)
                
    def avgColor(self):
        r = int(round(mean(self.r)))
        g = int(round(mean(self.g)))
        b = int(round(mean(self.b)))
        return (r, g, b)
        
    def mostFreqColor(self):
        a = Counter(self.rgb).most_common()
        b = max([i[1] for i in a])
        c = [i[0] for i in a if i[1] == b]
        if len(c) > 1:                              #if there's a tie
            shuffle(c)
        return c[0]

        
# --- Run ---
print ("Loading...")
loadPickle()
print ("'''")
print ("Color Cap v.1.0")
print ("@smileatleast 11.4.2015")
print ("please install python 2.X and PIL before using.")
print ("not tested for python 3.X")
print ("Instructions:")
print ("1. clearPickle() to clear out old data")
print ("2. startCap(n, box) to start capture every n seconds & send to pkl file;")
print ("    suggested minimum of 2. Use optional arg 'box' (x, y, width, height)")
print ("    to define height")
print ("3. Ctrl+C to stop capture")
print ("4. postProcessAvg() or postProcessFreq() to create image using the")
print ("    average or most frequent color in each cap.")
print ("'''")