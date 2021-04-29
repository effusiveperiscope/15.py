import frequest as frq
from io import BytesIO
from getch import getch 
import subprocess

opts = {
    "character": frq.DEFAULT_CHARACTER,
    "emotion": frq.DEFAULT_EMOTION,
    "text": ""
}
result = {}
wav_result = {}
MEDIA_PROGRAM = "mpv"

def select_result():
    print("Type in the number of the result you wish to select (1-3).")
    num = ord(getch()) - ord("1")
    assert(result),"No result"
    if (num < 0) or (num > len(result["wavNames"])):
        print("Could not select result "+str(num+1))
        return None
    print("Selected result "+str(num+1))
    return num

def play_result(buf):
    if len(MEDIA_PROGRAM) == 0:
        print("Error: Set MEDIA_PROGRAM in frepl.py before previewing audio.")
        pass
    try:
        p = subprocess.Popen([MEDIA_PROGRAM, "-"], stdin=subprocess.PIPE)
        p.communicate(buf)
    except Exception as e:
        print(e)

def save_result(buf):
    open(frq.generate_file_name(result["opts"]["character"],
        result["opts"]["text"]), "wb").write(buf)

def print_result_urls():
    assert(result),"No result"
    for i,w in enumerate(result["wavNames"]):
        print("File "+str(i+1)+": "+w)

def run():
    global opts
    print("Welcome to 15.py. Press (Shift+Q) to quit.")
    try: # "Goto considered harmful"
        while 1:
            key = chr(ord(getch()))
            if key == "Q":
                break
            elif key == "C":
                txt = input("Please enter a character name"
                    "or acronym: ")
                if not txt:
                    print("Character name unchanged: "+opts["character"])
                else:
                    opts["character"] = txt;
                print("Character set: "+opts["character"])
                continue
            elif key == "c":
                print("Character name is: "+opts["character"])
                continue
            elif key == "T":
                txt = input("Please enter desired text: ")
                if not txt:
                    print("Text unchanged.")
                else:
                    opts["text"] = txt;
                    print("Text set: "+opts["text"])
                continue
            elif key == "t":
                print("Text is: "+opts["text"])
                continue
            elif key == "R":
                print("==REQUEST==")
                global result
                global wav_result
                print("Character: "+opts["character"])
                print("Text: "+opts["text"])
                print("Requesting from: "+frq.DEFAULT_API_URL+"...")
                result = frq.get_raw(opts["character"],
                    opts["emotion"], opts["text"])
                if not result:
                    print("Error encountered.")
                    continue
                else:
                    print("Got result. Prefetching sounds...")
                    wav_result = frq.prefetch(result)
                    if not wav_result:
                        print("Error encountered.")
                        continue
                    print("Prefetched sounds.")
                    print_result_urls()
                    result["opts"] = opts
                continue
            elif key == "p":
                if not (result and wav_result):
                    print("No result to preview.")
                    continue
                res = select_result()
                if res == None:
                    continue
                print("Previewing file "+str(res+1)+".")
                play_result(wav_result[res])
                continue
            elif key == "S":
                if not (result and wav_result):
                    print("No result to save.")
                    continue
                print("Saving file "+str(res+1)+".")
                res = select_result()
                if res == None:
                    continue
                save_result(wav_result[res])
                continue
    except Exception as e:
        pass
