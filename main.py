import discord
import re

from apscheduler.schedulers.asyncio import AsyncIOScheduler

with open('replace', 'r') as f:
    REPLACE = eval(f.read())


class Schedule:
    month_conv = {'janvier': '2022-01', 'février': '2022-02', 'mars': '2022-03', 'avril': '2022-04', 'mai': '2022-05',
                  'juin': '2022-06', 'juillet': '2022-07', 'aout': '2022-08', 'septembre': '2022-09',
                  'octobre': '2021-10', 'novembre': '2021-11', 'décembre': '2021-12'}

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        with open('birthdays', 'r') as f:
            self.birthdays = dict()
            for line in f:
                name, date = line.split(' - ')
                self.birthdays.update({self.convert_date(date.lower()): name})
        self.scheduler.start()
        self.init_dates()
        self.scheduler.add_job(treize_douze, 'cron', hour=13, minute=12)

    def convert_date(self, date):
        day, month = date.split(' ')
        return f'{self.month_conv[month]}-{day.zfill(2)}'

    def init_dates(self):
        for date, name in self.birthdays:
            self.scheduler.add_job(lambda: happy_birthday(name), 'date', run_date=date)

    def add_date(self, string):
        date, name = string.split(' - ')
        date = self.convert_date(date)
        self.scheduler.add_job(lambda: happy_birthday(name), 'date', run_date=date)


bot = discord.Client()
schedule = Schedule()


def replace(text, old, new):
    send = str()
    prev = -len(old)
    for i, c in enumerate(text):
        if text[i:].lower().startswith(old):
            send += new
            prev = i
        elif prev + len(old) - 1 < i:
            send += c
    return send


async def happy_birthday(name):
    await bot.get_channel(889469447050510349).send(f"C'est l'anniversaire de {name} aujourd'hui !")


async def treize_douze():
    await bot.get_channel(889469447050510349).send('13h12')


@bot.event
async def on_message(msg):
    if msg.author != bot.user:
        test_koi = ''.join([c for c in msg.content.lower() if c.isalpha()])
        dit = re.search(r'(?<=[Dd][IYiy]).*$', msg.content)
        cri = re.search(r'(?<=[cC][rR][iIyY]).*$', msg.content)
        if msg.content.startswith("!replace"):
            old, new = msg.content[9:].split('/')
            REPLACE.update({old: new})
            with open('replace', 'w') as f:
                f.write(str(REPLACE))
        elif msg.content.startswith('!birthday'):
            with open('birthdays', 'a') as f:
                f.write(msg.content[10:])
            schedule.add_date(msg.content[10:])
        elif dit is not None:
            await msg.channel.send(dit.group())
        elif cri is not None:
            await msg.channel.send(cri.group().upper())
        elif "du coup" in msg.content.lower():
            await msg.channel.send('Non, pas du coup, non')
        elif re.search(r'((qu)|k)oi[tepsdh]$', test_koi) is not None:
            await msg.channel.send("FEUR")
        elif re.search(r'(^| )gens($| )', msg.content.lower()) is not None:
            await msg.channel.send("C'est <@276419613703798784> Jean")
        else:
            for key in REPLACE.keys():
                if key in msg.content.lower():
                    await msg.channel.send("*" + replace(msg.content, key, REPLACE[key]))


bot.run(input('Token: '))
