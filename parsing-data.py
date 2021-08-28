from telethon import TelegramClient, events
import os
from config import cfg
import sys

# Remember to use your own values from my.telegram.org!
api_id = cfg["api_id"]
api_hash = cfg["api_hash"]
client = TelegramClient('user', api_id, api_hash)

def callback(current, total):
    print('Uploaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))

def idget(data):
	if "/" in data:
		id = int((data.split("/"))[-1])
	else:
		id = int(data)
	return id

def makedir(idc, exten):
    refer_name = os.getcwd() + "/downloads/" + idc + "/" + exten
    os.makedirs(refer_name, mode=0o777, exist_ok=True)

def rename_valid(name):
    name1 = name.replace("<", "").replace(">", "").replace("«", "").replace("»", "").replace("|", "")
    return name1.replace("\\", "").replace("/", "").replace("?", "").replace("!", "").replace("*", "").replace('"', "")

def callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))

async def down(num1, num2, message, file_name):
    extensions = (str(message.file.mime_type)).replace("/", "-")
    makedir(file_name, extensions)
    path = await message.download_media(os.getcwd() + "/downloads/"+file_name+"/"+extensions, progress_callback=callback)
    print("["+str(num1)+"/"+str(num2)+"]> Saved to", path)

async def main():
    id_from = int(input("Chat ID> "))
    url_start = input("URL or ID Start> ")
    url_stop = input("URL or ID Stop> ")
    type_media = input("img/vid/aud/gif> ")
    os.system('cls' if os.name == 'nt' else 'clear')
    list = []
    id1 = idget(url_stop)
    id2 = idget(url_start)
    if id1 > id2:
    	count = id2
    	stoping = id1
    else:
    	count = id1
    	stoping = id2
    while True==True:
        list.append(count)
        count += 1
        if stoping  < count:
        	break
    num1 = 0
    num2 = len(list)
    async for message in client.iter_messages(id_from):
        if message.id < list[0]:
            print("[END]")
            sys.exit()
        if message.id not in list:
            continue
        num1 += 1
        file_name = rename_valid(str(message.chat.title))
        if type_media == "img" and message.photo:
            await down(num1, num2, message, file_name)
        elif type_media == "vid" and message.video:
            await down(num1, num2, message, file_name)
        elif type_media == "aud" and message.audio:
            await down(num1, num2, message, file_name)
        elif type_media == "gif" and message.gif:
            await down(num1, num2, message, file_name)
        elif type_media not in ["img", "vid", "aud", "gif"]:
            try:
                await down(num1, num2, message, file_name)
            except:
                pass
        else:
            pass


with client:
    client.loop.run_until_complete(main())

#await client.send_message("gfreeman_bot", 'Hello, group!', file="https://video-hw.xvideos-cdn.com/videos/mp4/c/9/3/xvideos.com_c9353fd3cd8b6603a3d09f53e3910e82.mp4?e=1604790553&h=8e96d286184d3d284be558010a43217f&download=1")
#await client.send_message(-1001242752198, 'Hello, group!', file="https://data.necrosis.ml/n2HqZkTDYmU5hEE7fx7L6x4ky3CBvbUVFctbKcFh/YYk4xTvFVWXrOA.mp4")
#await client.send_file(-1001374055263, 'cd_001.mp4', supports_streaming=True, progress_callback=callback)
#await client.send_file(-1001374055263, "https://vkvd170.mycdn.me/?sig=Mx8GZhlS62s&ct=0&srcIp=94.25.181.62&urls=185.226.53.165&expires=1605520980224&clientType=13&srcAg=UNKNOWN&fromCache=1&ms=45.136.21.172&appId=512000384397&id=695977446139&type=4", filename="d2854cf7gj.mp4", supports_streaming=True, progress_callback=callback)