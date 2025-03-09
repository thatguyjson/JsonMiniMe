'''
General commands cog
'''
class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(GeneralCog(bot))
