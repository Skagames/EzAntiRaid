import time
from tinydb import TinyDB, Query


async def sync2(ctx):
    """
    0.024s for 4384 members
    """
    res = await ctx.respond("Syncing...",ephemeral=True)
    t1 = time.time()
    db = TinyDB('ezantiraid.json')
    table = db.table('joinlog')
    mem_list = {}
    for member in ctx.guild.members:
        mem_list[member.id] = {'name': f"{member.name}#{member.discriminator}", 'joined_at': member.joined_at.timestamp()}
    total = {ctx.guild.id: mem_list}
    table.insert(total)

    t2 = time.time()
    await res.edit_original_message(content=f"Syncing done! synced {len(ctx.guild.members)}. excecution took {round(t2-t1,5)} seconds")



async def sync4(ctx):
    """
    0.023s for 4384 members
    """
    res = await ctx.respond("Syncing...",ephemeral=True)
    t1 = time.time()
    db = TinyDB('ezantiraid.json')
    table = db.table('joinlog')
    q = Query()
    total = {'server_id': ctx.guild.id, 'members': {}}
    mem_list = {}
    for member in ctx.guild.members:
        mem_list[member.id] = {'name': f"{member.name}#{member.discriminator}", 'joined_at': member.joined_at.timestamp()}
    total['members'] = mem_list

    table.upsert(total, q.server_id == ctx.guild.id)

    t2 = time.time()
    await res.edit_original_message(content=f"Syncing done! synced {len(ctx.guild.members)}. excecution took {round(t2-t1,5)} seconds")


async def sync5(ctx):
    """
    0.023s for 4384 members
    """
    res = await ctx.respond("Syncing...",ephemeral=True)
    t1 = time.time()
    db = TinyDB('ezantiraid.json')
    table = db.table('joinlog')
    q = Query()
    total = {'server_id': ctx.guild.id, 'members': {}}

    total['members'] = {member.id: {'name': f"{member.name}#{member.discriminator}", 'joined_at': member.joined_at.timestamp()} for member in ctx.guild.members}

    table.upsert(total, q.server_id == ctx.guild.id)

    t2 = time.time()
    await res.edit_original_message(content=f"Syncing done! synced {len(ctx.guild.members)}. excecution took {round(t2-t1,5)} seconds")