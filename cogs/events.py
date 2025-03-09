'''
Events cog
'''
class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(EventsCog(bot))
