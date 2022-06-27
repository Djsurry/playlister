import os, requests, random, re, os, string
from flask import Flask, render_template, request
from subprocess import check_output, Popen, call
from base64 import b64encode

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# init Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/getsong')
def getSong():
    if "url" not in request.args:
        return 'fuck u'
    playlist = request.args["url"]

    print(playlist)
    if re.match(regex, playlist) is None:
        return 'ur a good person dw'
    # yt-dlp --flat-playlist   https://www.youtube.com/playlist?list=PLBRIO7dbinFq7Xf_O9rjjUA5HE8fxE6c4

    resp = check_output(["yt-dlp", "--flat-playlist", playlist]).decode()
    print(resp)
    if "[download] Finished downloading playlist:" not in resp.split('\n')[-2]:
        return 'fuck u x2'
    n = resp.split('\n')[-3].split(' ')[-1]
    letters = string.ascii_uppercase + string.ascii_lowercase
    name= ''.join(random.choice(letters) for i in range(12)) 
    while 1:
        vidToDownload = random.randint(1, int(n))
        print(f"-*-*-*-*-*-*-*- GOT NUMBER OF VIDS {n} AND WHICH TO DL {vidToDownload}")
        call(["yt-dlp", "--playlist-items", str(vidToDownload), "-o", name, playlist])
        print(f"*-*-*-*-*-*-*- FINISHED yt-dlp -*-*-*-*-*-*-*-")
        call(["ffmpeg", "-i", f"{name}.webm", f"{name}.wav"])
        print(f"*-*-*-*-*-*-*- FINISHED ffmpeg -*-*-*-*-*-*-*-")
        if os.path.isfile(f"{name}.wav"):
            break
    f=open(f"{name}.wav", "rb")
    enc=b64encode(f.read())
    f.close()
    print(f"*-*-*-*-*-*-*- FINISHED converting -*-*-*-*-*-*-*-")
    call(f"find -type f -name '*{name}*' -delete".split())
    return enc

app.run(port=8080, debug=True)
