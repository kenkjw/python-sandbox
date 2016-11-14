from subprocess import call,Popen,PIPE
from PIL import Image
from StringIO import StringIO

ADB = ""

path = r"D:\Android\android-sdk\platform-tools\adb.exe -s 127.0.0.1:62001"
def init():
    global ADB
    call("{} connect 127.0.0.1:62001".format(path).split())  
    ADB = Popen('{} shell'.format(path).split(),stdin=PIPE,stdout=PIPE,stderr=PIPE)
    ADB.stdin.write('PS1=#####$\n')
    _ = ADB.stdout.readline()
    _ = ADB.stdout.readline()

def raw(s):
    ADB.stdin.write("{}\n".format(s))

def clearline():
    _ = ADB.stdout.readline()


def tap(x,y):
    ADB.stdin.write("input tap {} {}\n".format(x,y))
    _ = ADB.stdout.readline()
def swipe(x1,y1,x2,y2,t):
    ADB.stdin.write("input swipe {} {} {} {} {}\n".format(x1,y1,x2,y2,t))
    _ = ADB.stdout.readline()

def screencap():
    ADB.stdin.write("screencap -p\n\n")
    lines = []
    line = ADB.stdout.readline()
    while len(line) < 10 or line[-6:] != "#$\r\r\r\n":
      lines.append(line)
      line = ADB.stdout.readline()
    lines.append(line)
    raw = ''.join(lines).replace('#####$screencap -p\r\r\r\n','').replace('#####$\r\r\r\n','').replace('\r\r\n','\n')
    buff = StringIO(raw)
    return Image.open(buff)

