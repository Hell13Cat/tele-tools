from telethon import TelegramClient, events
from config import cfg
import xlwt

api_id = cfg["api_id"]
api_hash = cfg["api_hash"]
client = TelegramClient('anon', api_id, api_hash)
book = xlwt.Workbook()
sheet1 = book.add_sheet("List full")
sheet1.write(0, 0, "№")
sheet1.write(0, 1, "ID")
sheet1.write(0, 2, "NAME")
sheet1.write(0, 3, "TYPE")
sheet1.write(0, 4, "COUNT USERS")
sheet1.write(0, 5, "DATE CREATED")
sheet1.write(0, 6, "LAST DATE")

async def main():
    dialogs = await client.get_dialogs()
    count = 0
    for one_d in dialogs:
        count += 1
        sheet1.write(count, 0, str(count))
        sheet1.write(count, 1, str(one_d.id))
        sheet1.write(count, 2, str(one_d.title))
        if one_d.is_user:
            sheet1.write(count, 3, "USER")
            sheet1.write(count, 4, "-")
            sheet1.write(count, 5, "-")
        else:
            if one_d.is_group:
                sheet1.write(count, 3, "GROUP")
                sheet1.write(count, 4, one_d.entity.participants_count)
                sheet1.write(count, 5, str(one_d.entity.date.strftime("%Y.%m.%d-%H:%M:%S")))
            else:
                if one_d.is_channel:
                    sheet1.write(count, 3, "CHANNEL")
                    sheet1.write(count, 4, one_d.entity.participants_count)
                    sheet1.write(count, 5, str(one_d.entity.date.strftime("%Y.%m.%d-%H:%M:%S")))
        try:
            sheet1.write(count, 6, str(one_d.message.date.strftime("%Y.%m.%d-%H:%M:%S")))
        except:
            sheet1.write(count, 6, "ERROR")
    book.save("chats.xls")

with client:
    client.loop.run_until_complete(main())