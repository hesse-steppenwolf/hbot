import discord, random, datetime, requests, math
from discord.ext import commands, tasks

TOKEN = open('token.txt', 'r').readlines()[0].strip()
TOOLS = open('tools.txt', 'r').readlines()
VOWELS = open('name_vowels.txt', 'r').readlines()
NON_VOWELS = open('name_non_vowels.txt', 'r').readlines()
intents = discord.Intents().all()
prefixes = 'h.', 'H.', 'f.'
client = commands.Bot(command_prefix=prefixes, intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('oh no'))
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
    await ctx.send('ping, hhh, game, bonk, bagel, shake/handshake/respectfulhandshake, five/highfive, bite, deny, salami')  

@client.command()
async def nothing(ctx):
    await ctx.send('​')

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
