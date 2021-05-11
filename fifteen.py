#!/usr/bin/python
# Python's where it's at. You can do almost anything with it. Did you know tha
# python -m pip install requests
import argparse
import frequest as frq
import frepl

# CLI 
parser = argparse.ArgumentParser(
        description="Request and download all three files outputted.")
parser.add_argument("-u","--url",
        help="audio file request url",default=frq.DEFAULT_API_URL)
parser.add_argument("-c","--character",
        help="character name",default=frq.DEFAULT_CHARACTER)
parser.add_argument("-e","--emotion",
        help="emotion",default=frq.DEFAULT_EMOTION)
parser.add_argument("text",help="text to generate")
args = parser.parse_args()

frepl.run()

#TODO input sanitizing (nonzero input length, ARPAbet)
#TODO add TUI mode
#TODO proper packaging (requests, getch)