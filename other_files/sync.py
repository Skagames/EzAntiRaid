import time
from tinydb import TinyDB, Query

async def sync1(ctx):
    """
    
    """
    res = await ctx.respond("Syncing...",ephemeral=True)
    t1 = time.time()
    db = TinyDB('ezantiraid.json')
    table = db.table('joinlog')
    query = Query()
    for member in ctx.guild.members:
        if member.joined_at is not None:
            table.upsert({'id': member.id, 'joined_at': member.joined_at.timestamp()}, query.id == member.id)
    
    t2 = time.time()
    await res.edit_original_message(content=f"Syncing done! synced {len(ctx.guild.members)}. excecution took {round(t2-t1,5)} seconds")

async def sync(ctx):
    """

    """
    res = await ctx.respond("Syncing...",ephemeral=True)
    t1 = time.time()
    db = TinyDB('ezantiraid.json')
    table = db.table('joinlog')
    query = Query()
    mem_list = {}
    for member in ctx.guild.members:
        mem_list[member.id] = {'name': f"{member.name}#{member.discriminator}", 'joined_at': member.joined_at.timestamp()}
    total = {ctx.guild.id: mem_list}
    table.insert(total)

    t2 = time.time()
    await res.edit_original_message(content=f"Syncing done! synced {len(ctx.guild.members)}. excecution took {round(t2-t1,5)} seconds")