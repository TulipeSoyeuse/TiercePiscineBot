from discord.ext import commands


def in_channel(channel_id):
    def predicate(ctx):
        return ctx.message.channel.id == channel_id

    return commands.check(predicate)
    return commands.check(predicate)
