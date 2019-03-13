from wxpy import *
bot=Bot(cache_path=True)
friend=bot.friends().search(name='张工')[0]
friend.send('hello')
embed()