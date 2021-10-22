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
bot_token = os.environ.get("TOKEN", "2051706992:AAGbc_P2DzgLKZ80kMbeI6LBqql777zpAsQ")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**@UserMentionRobot**, Grup Veya Kanaldaki Neredeyse Tüm Üyelerden Bahsedebilirim ★\nDaha Fazla Bilgi İçin **/help**'i Tıklayın.",
                    buttons=(
                      [Button.url('➕ Beni Bir Gruba Ekle ➕', 'https://t.me/UserMentionRobot?startgroup=a'),
                      Button.url('👤 Geliştirici', 'https://t.me/theezelboss')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**@UserMentionRobot Yardım Menüsü**\n\nKomut: /all \n  Bu Komutu, Başkalarına Bahsetmek İstediğiniz Metinle Birlikte Kullanabilirsiniz. \n\n`Örnek: /all Günaydın!`  \n\nBu komutu yanıt olarak kullanabilirsiniz. Herhangi bir mesaj yanıtlandığında, yanıtlanan mesaj ile kullanıcıları etiketleyecebilir."
  await event.reply(helptext,
                    buttons=(
                      [Button.url('➕ Beni Bir Gruba Ekle ➕', 'https://t.me/UserMentionRobot?startgroup=a'),
                      Button.url('👤 Geliştirici', 'https://t.me/theezelboss')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu komut gruplarda ve kanallarda kullanılabilir.!__")
   
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"[{get_display_name(u)}](tg://user?id={u.id})**__Yalnızca Yöneticiler Hepsinden Bahsedebilir Warn Text Bold__**")
 
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**__Bana bir mesaj ver!__**")
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
        await asyncio.sleep(1.5)
        usrnum = 0
        usrtxt = ""

print(">> Bot çalıyor merak etme 🚀 @TheEzelBoss bilgi alabilirsin <<")
client.run_until_disconnected()
 
