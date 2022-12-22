import os
import time
import json
from discord_webhook import DiscordWebhook

with open("config.json", "r") as cfg:
    data = json.load(cfg)
    cfg.close()

webhook_url = data["webhook_url"]

webhook = DiscordWebhook(url=webhook_url, username="Dumpster Bot")

directory = os.path.join(os.getcwd(), "images")

images = []
fname = []

for file_name in os.listdir(directory):
    f = os.path.join(directory, file_name)

    if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
        images.append(f)
        fname.append(file_name)

# split into chunks of size n
def chunks(l, n):
    for i in range(0, len(l), n):
        yield images[i : i + n]


image_list = list(chunks(images, 10))

chunk_count = 0
fname_count = 0

for index in image_list:
    for image in index:
        with open(image, "rb") as fr:
            name = fname[fname_count]
            webhook.add_file(file=fr.read(), filename=name)

            fname_count += 1

    response = webhook.execute()
    webhook.remove_files()

    time.sleep(10)
