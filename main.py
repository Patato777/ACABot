import discord
import re

with open('replace', 'r') as f:
    REPLACE = eval(f.read())

bot = discord.Client()


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


@bot.event
async def on_message(msg):
    if msg.author != bot.user:
        test_koi = ''.join([c for c in msg.content.lower() if c.isalpha()])
        dit = re.match(r'(?<=[Dd][IYiy]).*$', msg.content)
        cri = re.match(r'(?<=[cC][rR][iIyY]).*$', msg.content)
        if msg.content.startswith("!replace"):
            old, new = msg.content[9:].split('/')
            REPLACE.update({old: new})
            with open('replace', 'w') as f:
                f.write(str(REPLACE))
        elif dit is not None:
            await msg.channel.send(dit.group())
        elif cri is not None:
            await msg.channel.send(cri.group().upper())
        elif "du coup" in msg.content.lower():
            await msg.channel.send('Non, pas du coup, non')
        elif re.search(r'((qu)|k)oi[tepsdh]$', test_koi, re.MULTILINE) is not None:
            await msg.channel.send("FEUR")
        elif re.search(r'(^| )gens($| )', msg.content.lower()) is not None:
            await msg.channel.send("C'est <@276419613703798784> Jean")
        else:
            for key in REPLACE.keys():
                if key in msg.content.lower():
                    await msg.channel.send("*" + replace(msg.content, key, REPLACE[key]))


bot.run(input('Token: '))

# TODO: Réveil à 13:12
