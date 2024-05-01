from pypdf import PdfReader

#####FILE
reader = PdfReader('YOU_FILE.pdf')

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys


session = Session(aws_secret_access_key='YOUR_ACCES_KEY', aws_access_key_id='YOUR_KEY_ID', region_name='us-east-1')
polly = session.client("polly")

def audio(text, page, part):
    try:
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                            VoiceId="Vicki")######VICKI - GERMAN, JOANNA - ENGLISH
    except (BotoCoreError, ClientError) as error:

        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(f'speech{page}_{part}.mp3')

                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)

    else:
        print("Could not stream audio")
        sys.exit(-1)

    if page == 1 and part == 1:
        os.startfile(output)


page_num = 1
###if too much text in pdf
for page in reader.pages:
    text = page.extract_text()
    if len(text) > 3000:
        x = len(text)//2
        print(x)
        while text[x] not in [' ',',','.','\n']:
            x += 1
        audio(text=text[:x], page=page_num, part=1)
        audio(text=text[x:], page=page_num, part=2)
    else:
        audio(text=text, page=page_num, part=1)

