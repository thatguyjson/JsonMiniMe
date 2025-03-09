'''
Grim commands cog. This is gonna be used so Grim 
can maybe make a command or two at some point.
'''
class GrimCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(GrimCog(bot))
