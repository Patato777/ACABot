import discord

bot = discord.Client()


@bot.event
async def on_message(msg):
    if msg.author != bot.user:
        if "di" in msg.content.lower():
            await msg.channel.send(msg.content.lower().split("di")[-1])
        elif "dy" in msg.content.lower():
            await msg.channel.send(msg.content.lower().split("dy")[-1])
        elif "du coup" in msg.content.lower():
            await msg.channel.send('Non, pas du coup, non')
        elif "putain" in msg.content.lower():
            send = str()
            prev = -6
            for i, c in enumerate(msg.content):
                if msg.content[i:].lower().startswith('putain'):
                    send += "ofan de chichoune"
                    prev = i
                elif prev + 5 < i:
                    send += c
            await msg.channel.send("*" + send)
        test_koi = ''.join([c for c in msg.content.lower() if c.isalpha()])
        if test_koi.endswith("quoi") or test_koi.endswith("koi") or (
                test_koi[-1] in ['t', 'e', 'p', 's', 'd', 'h'] and (
                test_koi[:-1].endswith("quoi") or test_koi[:-1].endswith("koi"))):
            await msg.channel.send("FEUR")


bot.run("ODkzMjM5MTg0MTQ2NDM2MTg3.YVYj0Q.w70GM-fYKfhJNuTI_IyNG5Nskrs")

# TODO: Réveil à 13:12
