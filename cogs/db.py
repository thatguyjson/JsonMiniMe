'''
Database commands cog
'''
class DBCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(DBCog(bot))
