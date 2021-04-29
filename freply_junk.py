# REPL mode
import curses
from curses.textpad import Textbox
import frequest as frq

opts = {
    "character": frq.DEFAULT_CHARACTER,
    "emotion": frq.DEFAULT_EMOTION,
    "text": ""
}
last_opts = {
    "character": "N/A",
    "emotion": "N/A",
    "text": "N/A"
}
result = {}

def run():
    global result
    global opts
    global last_opts
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.addstr("Welcome to 15.py. Press Q (Shift+q) to quit.\n")

    try:
        while 1:
            key = screen.getkey()
            if key == "Q": # quit
                break
            elif key == "C": # change character
                screen.addstr("Please enter a character name"
                    " or acronym:\n")
                sub = screen.subwin(1,80,screen.getyx()[0],0)
                tb = Textbox(sub)
                screen.refresh()
                opts["character"] = tb.edit()
                screen.addstr("Character name set to "+
                    opts["character"]+"\n")
                continue
            elif key == "c": # display character name
                screen.addstr("Character name is: "+opts["character"]+"\n")
                continue
            elif key == "T": # change text
                screen.addstr("Please enter text; press Ctrl+G to submit:\n")
                sub = screen.subwin(2,80,2,0)
                tb = Textbox(sub)
                screen.refresh()
                opts["text"] = tb.edit()
                screen.addstr("Text set to "+opts["text"]+"\n")
                continue
            elif key == "t": # display text
                screen.addstr("Text is: "+opts["text"]+"\n")
                continue
            elif key == "R": # request files

                screen.addstr("Sending request to "+
                    frq.DEFAULT_API_URL+"\n")
                screen.addstr("Character:"+opts["character"]+"\n")
                screen.addstr("Text:"+opts["text"]+"\n")

                result = frq.get_raw(opts["character"],
                    opts["emotion"], opts["text"])
                if not result:
                    screen.addstr("Error encountered.\n")
                else:
                    screen.addstr("Got result!\n")
                    last_opts = opts
                continue
            elif key == "l": # last opts
                screen.addstr("Last options:\n")
                screen.addstr("Character:"+last_opts["character"]+"\n")
                screen.addstr("Text:"+last_opts["text"]+"\n")
                continue
            elif key == "p": # play wav files if available
                if len(result) == 0:
                    screen.addstr("No wav files!\n")
                    continue
                key = screen.getkey()
    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
