# Python's where it's at. You can do almost anything with it. Did you know tha
# python -m pip install requests
import argparse
import logging
import json

import requests
from requests.exceptions import ConnectionError

# Constants
DEFAULT_API_URL = "http://api.15.ai/app/getAudioFile4"
DEFAULT_AI_URL = "http://test16.15.ai"
DEFAULT_CDN_URL = "http://cdn.15.ai/audio/"
MAX_TEXT_LEN = 200
FILENAME_TRUNC_LEN = 32
REQ_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "access-control-allow-origin": "*",
    "content-type": "application/json;charset=UTF-8",
    # "origin": DEFAULT_AI_URL,
    # "referer": DEFAULT_AI_URL+"/app",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}
DEFAULT_CHARACTER = "Twilight Sparkle"
DEFAULT_EMOTION = "Contextual"
DEFAULT_FILENAME_PREFIX = "fifteen_ai_"

# CLI 
parser = argparse.ArgumentParser(
        description="Request and download all three files outputted.")
parser.add_argument("-u","--url",
        help="audio file request url",default=DEFAULT_API_URL)
parser.add_argument("-c","--character",
        help="character name",default=DEFAULT_CHARACTER)
parser.add_argument("-e","--emotion",
        help="emotion",default=DEFAULT_EMOTION)
parser.add_argument("text",help="text to generate")
args = parser.parse_args()

# Request
def get_raw(character = args.character,
    emotion = args.emotion,
    text = args.text):

    data = json.dumps({"text":text,"character":character,
        "emotion":emotion,"use_diagonal":True})

    if len(text) > MAX_TEXT_LEN:
        logging.warning("Warning - text too long. Trimming.")
        text = text[:MAX_TEXT_LEN - 1]
    if not (text.endswith(".") or text.endswith("?") or text.endswith("!")):
        logging.warning(
            "Warning - text not terminated with punctuation. Adding .")
        if text.len != MAX_TEXT_LEN:
            text += "."
        else:
            text = text[:-1] + "."
    logging.info("Requesting...")

    try:
        response = requests.post(args.url, data=data, headers=REQ_HEADERS)
    except requests.exceptions.ConnectionError as e:
        logging.error(f"ConnectionError ({e})")
        return None

    if response.status_code == 200:
        logging.info("API response success")
        return response.content
    else:
        logging.error(f"API returned error code ({response.status_code})")
        return None

def get_all(response):
    if not response:
        return 
    obj = json.loads(response)
    for i,w in enumerate(obj["wavNames"]):
        r = requests.get(DEFAULT_CDN_URL + w)
        filename = (clean_filename(
            args.character[:FILENAME_TRUNC_LEN]+"_"+
            args.text[:FILENAME_TRUNC_LEN])+str(i)+".wav").lower()
        open(filename, 'wb').write(r.content)

# Filename sanitization (courtesy of github.com/wassname)
import unicodedata
import string

VALID_FILENAME_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
CHAR_LIMIT = 255

def clean_filename(filename, whitelist=VALID_FILENAME_CHARS, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode(
        'ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>CHAR_LIMIT:
        logging.warning("Warning, filename truncated because it was over {}."
        "Filenames may no longer be unique".format(CHAR_LIMIT))
    return cleaned_filename[:CHAR_LIMIT]    

get_all(get_raw())

#TODO input sanitizing
#TODO add TUI mode
#TODO add character shorthands