# for pagination
async def addPages(client,ctx,message,pages):
    await message.add_reaction(client.emojis_list["leftArrow"])
    await message.add_reaction(client.emojis_list["left"])
    await message.add_reaction(client.emojis_list["stop"])
    await message.add_reaction(client.emojis_list["right"])
    await message.add_reaction(client.emojis_list["rightArrow"])

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if  str(reaction) == client.emojis_list["leftArrow"]:
            await message.edit(embed = pages[0])
            i = 0
        elif str(reaction) == client.emojis_list["left"]:
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == client.emojis_list["right"]:
            if i < len(pages):
                i += 1
                await message.edit(embed = pages[i])
        elif  str(reaction) == client.emojis_list["rightArrow"]:
            await message.edit(embed = pages[len(pages)-1])
            i = len(pages)-1
        elif  str(reaction) == client.emojis_list["stop"]:
            await message.clear_reactions()
            return
            
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()