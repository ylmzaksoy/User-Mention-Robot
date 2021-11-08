import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID", "3614731"))
api_hash = os.environ.get("API_HASH", "706629c106cdb9347e61ae877edf63dc")
bot_token = os.environ.get("TOKEN", "2111210757:AAF9le9USnEjUMkeI6IvU6AHL8t7QYayprk")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("Merhaba! Grubunuzdaki Kullanıcıları Etiketlemek İçin Yaratıldım. Beni Grubunuza Ekleyin Ve Gerisini Bana Bırakın. \nDaha Fazla Bilgi İçin /help'i Kullanınız.",
                    buttons=(
                      [Button.url('➕ Beni Bir Gruba Ekle ➕', 'https://t.me/usertaggerrobot?startgroup=a'),
                      Button.url('👤 Geliştirici', 'https://t.me/thewanderfull')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "@UserTaggerRobot Yardım Menüsü \n\nKomut: /utag \n Bu Komutu, Başkalarına Bahsetmek İstediğiniz Metinle Birlikte Kullanabilirsiniz. \n\n`Örnek: /utag Günaydın!`  \n\nBu Komutu Yanıt Olarak Kullanabilirsiniz. Herhangi Bir Mesaj Yanıtlandığında, Yanıtlanan Mesaj İle Kullanıcıları Etiketleyecektir."
  await event.reply(helptext,
                    buttons=(
                      [Button.url('➕ Beni Bir Gruba Ekle ➕', 'https://t.me/UserTaggerRobot?startgroup=a'),
                      Button.url('👤 Geliştirici', 'https://t.me/thewanderfull')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/utag ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu Komut Gruplarda Veya Kanallarda Kullanılabilir.!__")
   
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"[{get_display_name(u)}](tg://user?id={u.id})**__Yalnızca Yöneticiler Hepsinden Bahsedebilir Warn Text Bold__**")
 
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**__Bana Bir Mesaj Ver!__**")
  else:
    return await event.respond("**__Bir Mesajı Yanıtlayın Veya Başkalarından Bahsetmem İçin Bana Bir Metin Verin!__**")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) , "
      if event.chat_id not in anlik_calisan:
        await event.respond("İşlem Başarılı Bir Şekilde Durduruldu ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg} \n\n {usrtxt}")
        await asyncio.sleep(5.0)
        usrnum = 0
        usrtxt = ""

print(">> Bot çalıyor merak etme 🚀 @TheWanderfull bilgi alabilirsin <<")
client.run_until_disconnected()
 
