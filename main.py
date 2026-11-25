import os, random, textwrap
from gtts import gTTS
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

quotes = [
"Zindagi me haar tab hoti hai jab tum maan lete ho, warna jeet pakki hai.",
"Mehnat itni khamoshi se karo ki safalta shor macha de.",
"Kal se behtar bano, kal ka tum aaj se aage hona chahiye.",
"Aaj ka dard kal ki taqat banega, rukna mat.",
"Sapne wo nahi jo neend me aaye, sapne wo hai jo neend na aane de."
]
quote = random.choice(quotes)
tts = gTTS(text=quote, lang='hi', slow=False)
tts.save("voice.mp3")
img = Image.new('RGB', (1080, 1920), color=(10,10,20))
draw = ImageDraw.Draw(img)
wrapped = "\n".join(textwrap.wrap(quote, width=22))
draw.text((100, 800), wrapped, fill=(255, 215, 0))
img.save("bg.jpg")
audio = AudioFileClip("voice.mp3")
video = ImageClip("bg.jpg").set_duration(30).set_audio(audio)
video.write_videofile("short.mp4", fps=24, codec="libx264", audio_codec="aac")
creds = Credentials(None, refresh_token=os.environ['YT_REFRESH_TOKEN'], client_id=os.environ['YT_CLIENT_ID'], client_secret=os.environ['YT_CLIENT_SECRET'], token_uri="https://oauth2.googleapis.com/token")
youtube = build("youtube", "v3", credentials=creds)
youtube.videos().insert(part="snippet,status", body={"snippet": {"title": quote[:90] + " #shorts #motivation", "description": quote + "\n\n#motivation #shorts #viral", "categoryId": "22"}, "status": {"privacyStatus": "public", "madeForKids": False}}, media_body=MediaFileUpload("short.mp4")).execute()
print("Upload Ho Gaya!")
