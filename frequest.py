import requests
import logging
import json
from fchars import match_character
from requests.exceptions import ConnectionError

# Constants
DEFAULT_API_URL = "http://api.15.ai/app/getAudioFile4"
DEFAULT_AI_URL = "http://test000.15.ai"
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

# Request
def get_raw(character, emotion, text, url = DEFAULT_API_URL):

    data = json.dumps({"text":text,"character":character,
        "emotion":emotion,"use_diagonal":True})

    character = match_character(character)
    if character == None:
        raise Exception("Character does not match a known character")

    if len(text) > MAX_TEXT_LEN:
        logging.warning("Warning - text too long. Trimming.")
        text = text[:MAX_TEXT_LEN - 1]
    if not (text.endswith(".") or text.endswith("?") or text.endswith("!")):
        logging.warning(
            "Warning - text not terminated with punctuation. Adding .")
        if len(text) != MAX_TEXT_LEN:
            text += "."
        else:
            text = text[:-1] + "."
    logging.info("Requesting...")

    try:
        response = requests.post(url, data=data, headers=REQ_HEADERS)
    except requests.exceptions.ConnectionError as e:
        logging.error(f"ConnectionError ({e})")
        raise 

    if response.status_code == 200:
        logging.info("API response success")
        try:
            return json.loads(response.content)
        except Exception as e:
            logging.error(f"JSON loading error ({e})")
    else:
        logging.error(f"API returned error code ({response.status_code})")
        raise

def prefetch(response):
    ret = []
    for i,w in enumerate(response["wavNames"]):
        try:
            r = requests.get(DEFAULT_CDN_URL + w)
        except requests.exceptions.ConnectionError as e:
            logging.error(f"ConnectionError ({e})")
            raise
        # Why doesn't ret[i] = r.content work?
        ret.append(r.content)
    return ret

def generate_file_name(character, text):
    return (clean_filename(character[:FILENAME_TRUNC_LEN]+"_"+
        text[:FILENAME_TRUNC_LEN])+".wav").lower()

def get_all(response, character, text):
    if not response:
        return 
    obj = response
    for i,w in enumerate(obj["wavNames"]):
        r = requests.get(DEFAULT_CDN_URL + w)
        filename = generate_file_name(character, text)
        open(filename, "wb").write(r.content)

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

# Default behavior
