import discord

REPLACE = {"putain": "ofan de chichoune", "fils de pute": "fils de flic"}

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
        if "di" in msg.content.lower():
            await msg.channel.send(msg.content.lower().split("di")[-1])
        elif "dy" in msg.content.lower():
            await msg.channel.send(msg.content.lower().split("dy")[-1])
        elif "du coup" in msg.content.lower():
            await msg.channel.send('Non, pas du coup, non')
        else:
            for key in REPLACE.keys():
                if key in msg.content.lower():
                    await msg.channel.send("*" + replace(msg.content, key, REPLACE[key]))
        test_koi = ''.join([c for c in msg.content.lower() if c.isalpha()])
        if test_koi.endswith("quoi") or test_koi.endswith("koi") or (
                test_koi[-1] in ['t', 'e', 'p', 's', 'd', 'h'] and (
                test_koi[:-1].endswith("quoi") or test_koi[:-1].endswith("koi"))):
            await msg.channel.send("FEUR")


bot.run(input('Token: '))

# TODO: Réveil à 13:12
