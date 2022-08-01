import discord, random, datetime, requests, math
from discord.ext import commands, tasks

TOKEN = open('token.txt', 'r').readlines()[0].strip()
TOOLS = open('tools.txt', 'r', encoding='utf-8').readlines()
VOWELS = open('name_vowels.txt', 'r').readlines()
NON_VOWELS = open('name_non_vowels.txt', 'r').readlines()
intents = discord.Intents().all()
prefixes = 'h.', 'H.'
client = commands.Bot(command_prefix=prefixes, intents=intents)
client.remove_command('help')
base_url = "http://api.openweathermap.org/data/2.5/weather?"
api_key = open('weatherapikey.txt').readlines()[0].strip()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with forces to powerful for my own good'))
    print('BOT ONLINE')

@client.command()
async def ping(ctx):
    print('PONG')
    await ctx.send(f'PONG! {round(client.latency * 1000)}ms')

@client.command()
async def hhh(ctx):
    exhale = 'h' * random.randint(3,30)
    print(exhale)
    await ctx.send(exhale)

@client.command()
async def help(ctx):
    await ctx.send('ping, hhh, game, bonk, bagel, shake/handshake/respectfulhandshake, five/highfive, bite, deny, salami, holler, hug')  

@client.command()
async def nothing(ctx):
    await ctx.send('​')

@client.command() #action command that pastes the image of del having a bagel crisis
async def bagelcrisis(ctx):
    with open('bagel.jpg', 'rb') as fp:
        await ctx.send(file=discord.File(fp, 'bagel.jpg'))

@client.command()
async def zalgo(ctx, *args):
    rounds = 10
    text = args
    if args[0].isdigit():
        if 0 < int(args[0]) < 10:
            rounds = int(args[0])
        else:
            await ctx.send('Supply valid input between 1-10. Using default value of 10 instead')
        text = args[1:]

    rounds *= 10

    output_sentence = []
    for word in text:
        output_word = ''
        for ch in word:
            for _ in range(rounds):
                ch += random.randint(0x300,0x36f).to_bytes(2, 'big').decode('utf-16be')
            output_word += ch 
        output_sentence.append(output_word)
    await ctx.send(' '.join(output_sentence))

@client.command()
async def salami(ctx):
    source = requests.get('https://salamitimer.neocities.org').text
    source = source.split('$$$$$')[1].split()
    salami_time = datetime.datetime(*map(int, source))
    today = datetime.datetime.now()

    distance = today - salami_time
    distance = distance.total_seconds()

    years = math.floor(distance / (60 * 60 * 24 * 365))
    days = math.floor(distance / (60 * 60 * 24))
    hours = math.floor((distance % (60 * 60 * 24)) / (60 * 60))
    minutes = math.floor((distance % (60 * 60)) / 60)
    seconds = math.floor(distance % 60)

    await ctx.send(f'I (Hesse) have not eaten salami in {years}y {days}d {hours}h {minutes}m {seconds}s')

@client.command()
async def me(ctx):
    await ctx.send(random.choice(TOOLS))
@client.command()
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}",
                color=ctx.guild.me.top_role.color,
                timestamp=ctx.message.created_at,)
            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send("City not found.")

@client.command()
async def avatar(ctx):
    sender = ctx.message.author
    receiver = ctx.message.mentions
    if receiver:
        await ctx.send(receiver[0].avatar_url)
    else:
        await ctx.send(sender.avatar_url)

def generate_name():
    name = ''
    for i in range(random.randint(2,4)):
        if i % 2:
            name += random.choice(VOWELS).strip()
        else:
            name += random.choice(NON_VOWELS).strip()

    return name.title()

@client.command()
async def cryptid(ctx):
    embed = discord.Embed(
        title=generate_name(),
        colour=discord.Colour.blue()
    )
    embed.add_field(name='Test Embed', value='Test Embed',
                    inline=False)
    await ctx.send(embed=embed)

######################################
#                                    #
#    [sender] [action] [receiver]    #
#                                    #
######################################

sender = None
receiver = None
delaccepthug = False

@client.command()
async def game(ctx):
    global sender
    global receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'**{sender}** just made **{receiver}** lose the game!!!',
            f'**{sender}** pulled a sneaky and made **{receiver}** lose the game! What a trickster. What a jester.',
            f'**{sender}** made **{receiver}** lose the game. haha get fucked **{receiver}**. bozo']
    
    await ctx.send(random.choice(options))

@client.command()
async def bonk(ctx):
    global sender
    global receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'BONK!!!! **{sender}** bonks the everloving shit out of **{receiver}**',
            f'**{sender}** RIPS a traffic sign out of the ground and bonks **{receiver}** on the noggin. Estimated recovery time: {random.randint(1,24)} months',
            f'**{sender}** bonks **{receiver}** on the head, making a loud and obnoxious cartoon sound effect. \"And I live to bonk again...\" says **{sender}**. they stare off into the sunset.',
            f'**{sender}** bonks **{receiver}** with a baseball bat, killing them instantly']
    
    await ctx.send(random.choice(options))

@client.command() #A Del-specific command that allows him to accept hugs 
async def delhug(ctx):
    global sender
    global receiver
    global delaccepthug
    global del_receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name

    if sender == 'WolfDeluxe':#checks if Del sent the command
        if delaccepthug is True:#Switches if Del is accepting hugs or not
            delaccepthug = False
            await ctx.send(f'**{sender}** is no longer accepting a hug.')
        else:
            delaccepthug = True
            del_receiver = ctx.message.mentions[0].name
            await ctx.send(f'**{sender}** is now accepting a (single) hug from **{receiver}**.')  
    else:
        await ctx.send('You are not Del.')

@client.command()
async def hug(ctx):
    global sender
    global receiver
    global delaccepthug
    global del_receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'**{sender}** hugs **{receiver}**']#WE NEED MORE MESSAGES HERE
    
    if receiver == 'WolfDeluxe':#Del-specific hug command
        if delaccepthug == True and del_receiver == sender:#runs if Del wants hugs, and the sender is a specific person mentioned
            del_options_positive = [f'**{sender}** enters **{receiver}**\'s warm embrace. Watch out for the spikes!', 
             f'**{receiver}** opens his arms wide, and **{sender}** is squeezed tightly.',
             f'**{receiver}** gets a facefull of {receiver}\'s mane as they are swallowed up in a big hug.',
             f'**{sender}** hugs **{receiver}**, who quickly picks **{sender}** up and spins them around in a large circle!!!']
            await ctx.send(random.choice(del_options_positive))  
            delaccepthug = False     
        else:#if del cannot be hugged right now
            del_options_negative = [f'**{sender}** can go fuck themselves <3', 
            f'**{receiver}** easily dodges **{sender}**\'s attempt at a hug. Go away.',
            f'**{receiver}** questions why **{sender}** thought this was a good idea.',
            f'**{sender}** is either doing this for attention, or forgot to get **{receiver}**\'s consent or some shit like that.']
            await ctx.send(random.choice(del_options_negative))
    else:
        await ctx.send(random.choice(options))

@client.command()
async def hollar(ctx):
    global sender
    global receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'**{sender}** shouts from the streets at **{receiver}** to GET OVER HERE!!!!',
            f'**{sender}** takes in several breaths and YELLS AT THE TOP OF THEIR LUNGS TO GET **{receiver}** TO C\'MERE ALREADY!!!',
            f'**{sender}** yells. A lot. Like wow **{receiver}** should probably figure out why or something.']
    
    await ctx.send(random.choice(options))

@client.command()
async def bagel(ctx):
    global sender
    global receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'**{sender}** gives a bagel to **{receiver}**. \"It\'s pronounced *b-ay-gel*\", they say. **{receiver}** keels over and dies. \"Impossible...\"',
            f'**{sender}** gives a bagel to **{receiver}**. \"It\'s pronounced *b-ah-gel*\", they say. **{receiver}** keels over and dies. \"Impossible...\"',
            f'**{sender}** gives a bagel to **{receiver}**. \"It\'s pronounced *b-ä-gel*\", they say. **{receiver}** keels over and dies. \"Impossible...\"',
            f'**{sender}** gives a bagel to **{receiver}**. \"It\'s pronounced *b-æ̃-gel*\", they say. **{receiver}** keels over and dies. \"Impossible...\"']
    
    await ctx.send(random.choice(options))

@client.command(aliases=['respectfulhandshake', 'handshake'])
async def shake(ctx):
    global sender
    global receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'**{sender}** gives **{receiver}** a firm yet kind handshake. \"You\'re a real one, homeslice\"',
            f'**{sender}** gives **{receiver}** a respectable handshake. \"Godspeed, my eternal compadre\"',
            f'**{sender}** gives **{receiver}** a classic **{sender}** handshake. \"Keep on rocking, skater-bitch (positive)\"']
    
    await ctx.send(random.choice(options))

@client.command(aliases=['five'])
async def highfive(ctx):
    global sender
    global receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'**{sender}** does the WORLD\'S SWAGGIEST HIGH FIVE with **{receiver}**. The resulting shockwave kills {random.randint(3000,10000)} and injures millions more',
            f'**{sender}** high-fives **{receiver}**. holy shit they are so cool. holy fuck',
            f'**{sender}** gives **{receiver}** a high five. In the distance, a jazz solo plays. **{sender}** puts on a pair of sunglasses over the pair of sunglasses they are already wearing. Obama is there']
    
    await ctx.send(random.choice(options))

@client.command()
async def bite(ctx):
    global sender
    global receiver
    sender = ctx.message.author.name
    receiver = ctx.message.mentions[0].name
    options = [f'**{sender}** bites down hard on **{receiver}**\'s arm. ${random.randint(10000,50000)} hospital fee. (America)',
            f'**{sender}** bites on **{receiver}**\'s ear, creating several ear piercings for free! What a bargain',
            f'**{sender}** bites **{receiver}**\'s entire hand off. There is no joke here. **{receiver}** is in extreme pain']
    
    await ctx.send(random.choice(options))

@client.command()
async def deny(ctx):
    global sender
    global receiver
    new_sender = ctx.message.author.name
    new_receiver = ctx.message.mentions[0].name
    
    if receiver == new_sender and sender == new_receiver:
    
        sender = new_sender
        receiver = new_receiver

        options = [f'DENIED!!!!! **{sender}** dodges and lands a critical blow to **{receiver}**\'s jugalar',
                f'DENIED!!!!! **{sender}** does a cool backflip and boards the nearest flight to Bolivia, never to be seen again. The Boeing 787 Dreamliner {sender} is on sucks up **{receiver}** into its engine. rip bozo',
                f'DENIED!!!!! **{sender}** pulls an entire katana out of their ass (ancient samurai technique). **{receiver}** is sliced into fun celebratory confetti. YIPEEE',
                f'DENIED!!!!! **{sender}** activates their Special Move and pushes **{receiver}** down the stairs and then drags them up the stairs and then pushes them down the stairs and then',
                f'DENIED!!!!! **{sender}** does an Evasive Cartwheel and Exits the Situation. \"You Have No Bitches! Bitchless!!!\" **{sender}** shouts as they leave. **{receiver}**\'s body collapses out of pure shame',
                f'DENIED!!!!! **{sender}** does a silly dance, destroying **{receiver}**\'s body beyond recognition',
                f'DENIED!!!!! **{sender}** enters Angry Mode. \"Now Prepare You\'r\'m\'self For Utter Destrctuiioun!!\". {random.randint(3,10)} dead, {random.randint(10,20)} injured. **{receiver}**\'s corpse was never recovered']

        await ctx.send(random.choice(options))
    else:
        await ctx.send('There is no action to deny')
         
client.run(TOKEN)

@client.command()
async def jj(ctx):
    print('Jedes Jahr an deinem Geburtstag gehen deine Eltern in den Zoo und bewerfen den Storch mit Steinen') 
    await ctx.send('Jedes Jahr an deinem Geburtstag gehen deine Eltern in den Zoo und bewerfen den Storch mit Steinen')

@client.command()
async def DEsentence(ctx):
    print('Ich lebe in deinen Mauern von Son nenuntergang bis zur Dämmerung, aber tagsüber bin ich in deinem Schornstein')
    await ctx.send('Ich lebe in deinen Mauern von Son nenuntergang bis zur Dämmerung, aber tagsüber bin ich in deinem Schornstein')

@client.command()
async def RUsentence(ctx):
    print('Я не терплю, когда мои друзья мочатся в моем супе')
    await ctx.send('Я не терплю, когда мои друзья мочатся в моем супе')

@client.command()
async def JPtest(ctx):
    print('ハンバーガーチーズバーガーホットドッグハンバーガーチーズバーガーホットドッグ')
    await ctx.send ('ハンバーガーチーズバーガーホットドッグハンバーガーチーズバーガーホットドッグ')

@client.command()
async def LEAN(ctx):
    print('Its literally just cola you piece of shit. Theres no cough syrup or anything. What the fuck is wrong with you. How fucking desperate are you to seem cool that you decide you want to force a "joke" about a child consuming drugs. Which would be funny except nothing in this scene implies that theyre doing drugs or a drug stand-in. You just saw a can of soda and the two neurons in your head fired for the first time in a week, and you jumped into the comments to screech lEAn and spam purple emojis like a clown bastard. You people are the reason art is dying. Fuck you')
    await ctx.send('Its literally just cola you piece of shit. Theres no cough syrup or anything. What the fuck is wrong with you. How fucking desperate are you to seem cool that you decide you want to force a "joke" about a child consuming drugs. Which would be funny except nothing in this scene implies that theyre doing drugs or a drug stand-in. You just saw a can of soda and the two neurons in your head fired for the first time in a week, and you jumped into the comments to screech lEAn and spam purple emojis like a clown bastard. You people are the reason art is dying. Fuck you')

@client.command()
async def NFT(ctx):
    print('Dude I own this NFT. Do you really think that you can get away with theft when youre showing what you stole from me directly to my face? My lawyer will make an easy job of this case. Prepare to say goodbye to your luscious life and start preparing for the streets. I will ruin you.')
    await ctx.send('Dude I own this NFT. Do you really think that you can get away with theft when youre showing what you stole from me directly to my face? My lawyer will make an easy job of this case. Prepare to say goodbye to your luscious life and start preparing for the streets. I will ruin you.')

@client.command()
async def amogus(ctx):
    print('AMONG US Funny Moments! How to Free Robux and VBUCKS in SQUID GAME FORTNITE UPDATE! (NOT CLICKBAIT) MUKBANG ROBLOX GAMEPLAY TUTORIAL (GONE WRONG) Finger Family Learn Your ABCs at 3AM! Fortnite Impostor Potion! MrBeast free toys halal gameplay nae nae download حدث خطأ في الساعة 3 صباحًاحدث خطأ في الساعة 3 صباحًاحدث خطأ في الساعة 3 صباحًا Super Idol的笑容都没你的甜八月正午的阳光都没你耀眼热爱 105 °C的你滴滴清纯的蒸馏水 amongla download Meme Compilation (POLICE CALLED) (GONE WRONG) (GONE SEXUAL) (NOT CLICKBAIT) Minecraft Series Lets Play Videos Number 481 - Poop Funny Hilarious Minecraft Roblox Fails for Fortnite - How to install halal minecraft cheats hacks 2021 still works (STILL WORKS 2018) Impostor Gameplay (Among Us) Zamn')
    await ctx.send('AMONG US Funny Moments! How to Free Robux and VBUCKS in SQUID GAME FORTNITE UPDATE! (NOT CLICKBAIT) MUKBANG ROBLOX GAMEPLAY TUTORIAL (GONE WRONG) Finger Family Learn Your ABCs at 3AM! Fortnite Impostor Potion! MrBeast free toys halal gameplay nae nae download حدث خطأ في الساعة 3 صباحًاحدث خطأ في الساعة 3 صباحًاحدث خطأ في الساعة 3 صباحًا Super Idol的笑容都没你的甜八月正午的阳光都没你耀眼热爱 105 °C的你滴滴清纯的蒸馏水 amongla download Meme Compilation (POLICE CALLED) (GONE WRONG) (GONE SEXUAL) (NOT CLICKBAIT) Minecraft Series Lets Play Videos Number 481 - Poop Funny Hilarious Minecraft Roblox Fails for Fortnite - How to install halal minecraft cheats hacks 2021 still works (STILL WORKS 2018) Impostor Gameplay (Among Us) Zamn')

@client.command()
async def literally(ctx):
    print('"LiTeRaLlY nInEtEeN eIgHtY-fOuR" -George Orwell, 1948')
    await ctx.send('"LiTeRaLlY nInEtEeN eIgHtY-fOuR" -George Orwell, 1948')

@client.command()
async def fortnite(ctx):
    print('Hello, concerned father here. My son has recently got into the game called Fortnite? Ive spent well over $500 on this game and its becoming a problem. Apparently the game is down right now and its causing a lot distress for my child. He keeps taking my newspaper and tries to "full piece" me. I dont know what this means but Im starting to think its something associated with the devil. He wont come with us anywhere unless we take a "launch pad" to get there. Its starting to get worse by the hour and I dont know how much longer I can take this. His legs, arms, and hands are shaking violently yet he refuses to take any type of medicine unless its a "big pot" or "chuggies." Someone please help me.')
    await ctx.send('Hello, concerned father here. My son has recently got into the game called Fortnite? Ive spent well over $500 on this game and its becoming a problem. Apparently the game is down right now and its causing a lot distress for my child. He keeps taking my newspaper and tries to "full piece" me. I dont know what this means but Im starting to think its something associated with the devil. He wont come with us anywhere unless we take a "launch pad" to get there. Its starting to get worse by the hour and I dont know how much longer I can take this. His legs, arms, and hands are shaking violently yet he refuses to take any type of medicine unless its a "big pot" or "chuggies." Someone please help me.')

@client.command()
async def walter(ctx):
    print('My name is Walter Hartwell White. I live at 308 Negra Arroyo Lane, Albuquerque, New Mexico, 87104. This is my confession. If youre watching this tape, Im probably dead– murdered by my brother-in-law, Hank Schrader. Hank has been building a meth empire for over a year now, and using me as his chemist. Shortly after my 50th birthday, he asked that I use my chemistry knowledge to cook methamphetamine, which he would then sell using connections that he made through his career with the DEA. I was... astounded. I... I always thought Hank was a very moral man, and I was particularly vulnerable at the time – something he knew and took advantage of. I was reeling from a cancer diagnosis that was poised to bankrupt my family. Hank took me in on a ride-along and showed me just how much money even a small meth operation could make. And I was weak. I didnt want my family to go into financial ruin, so I agreed. Hank had a partner, a businessman named Gustavo Fring. Hank sold me into servitude to this man. And when I tried to quit, Fring threatened my family. I didnt know where to turn. Eventually, Hank and Fring had a falling-out. Things escalated. Fring was able to arrange – uh, I guess... I guess you call it a "hit" – on Hank, and failed, but Hank was seriously injured. And I wound up paying his medical bills, which amounted to a little over $177,000. Upon recovery, Hank was bent on revenge. Working with a man named Hector Salamanca, he plotted to kill Fring. The bomb that he used was built by me, and he gave me no option in it. I have often contemplated suicide, but Im a coward. I wanted to go to the police, but I was frightened. Hank had risen to become the head of the Albuquerque DEA. To keep me in line, he took my children. For three months, he kept them. My wife had no idea of my criminal activities, and was horrified to learn what I had done. I was in hell. I hated myself for what I had brought upon my family. Recently, I tried once again to quit, and in response, he gave me this.')
    await ctx.send('My name is Walter Hartwell White. I live at 308 Negra Arroyo Lane, Albuquerque, New Mexico, 87104. This is my confession. If youre watching this tape, Im probably dead– murdered by my brother-in-law, Hank Schrader. Hank has been building a meth empire for over a year now, and using me as his chemist. Shortly after my 50th birthday, he asked that I use my chemistry knowledge to cook methamphetamine, which he would then sell using connections that he made through his career with the DEA. I was... astounded. I... I always thought Hank was a very moral man, and I was particularly vulnerable at the time – something he knew and took advantage of. I was reeling from a cancer diagnosis that was poised to bankrupt my family. Hank took me in on a ride-along and showed me just how much money even a small meth operation could make. And I was weak. I didnt want my family to go into financial ruin, so I agreed. Hank had a partner, a businessman named Gustavo Fring. Hank sold me into servitude to this man. And when I tried to quit, Fring threatened my family. I didnt know where to turn. Eventually, Hank and Fring had a falling-out. Things escalated. Fring was able to arrange – uh, I guess... I guess you call it a "hit" – on Hank, and failed, but Hank was seriously injured. And I wound up paying his medical bills, which amounted to a little over $177,000. Upon recovery, Hank was bent on revenge. Working with a man named Hector Salamanca, he plotted to kill Fring. The bomb that he used was built by me, and he gave me no option in it. I have often contemplated suicide, but Im a coward. I wanted to go to the police, but I was frightened. Hank had risen to become the head of the Albuquerque DEA. To keep me in line, he took my children. For three months, he kept them. My wife had no idea of my criminal activities, and was horrified to learn what I had done. I was in hell. I hated myself for what I had brought upon my family. Recently, I tried once again to quit, and in response, he gave me this.')

@client.command()
async def i(ctx):
    print('"Now I am become death, destroyer of worlds" -J. Robert Oppenheimer, father of the atomic bomb, after witnessing the first test"')
    await ctx.send('"Now I am become death, destroyer of worlds" -J. Robert Oppenheimer, father of the atomic bomb, after witnessing the first test"')
