import time
import discord
from TagScriptEngine import Interpreter, adapter, block
from discord.ext.buttons import Paginator
from discord.ext import commands,tasks

blocks = [
    block.MathBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
]
engine = Interpreter(blocks)

async def donor_roles(client,query,user):
    role_dict = client.role_dict    
    roles_added = []
    for roles in role_dict.keys():
        actual_value = int(roles) * 1000000
        if float(actual_value)<=float(query):
            if role_dict[roles] not in user.roles:
                await user.add_roles(role_dict[roles])
                roles_added.append(role_dict[roles])
        else:
            break
    return roles_added

async def event_roles(client,query,user,event_name):
    guild = user.guild
    celeb_role = guild.get_role(943535266143039500)
    role_dict = client.event_8k
    if event_name == "8k":     
        roles_added = []
        for roles in role_dict.keys():
            actual_value = int(roles) * 1000000
            if float(actual_value)<=float(query):
                if role_dict[roles] not in user.roles:
                    roles_added.append(role_dict[roles])
            else:
                break
        if celeb_role not in user.roles:
            # await user.add_roles(celeb_role)
            roles_added.append(celeb_role)
        return roles_added
    else:
        return []
        
async def convert_to_time(query):
    query = query.lower()
    query = query.replace("d", "*86400+",1)
    query = query.replace("h", "*3600+",1)
    query = query.replace("m", "*60+",1)       
    query = query.replace("s", "*1+",1)  
    query = f"{query}0"
    return query
    
async def convert_to_numeral(query):
    query = query.lower()
    query = query.replace("k", "e3",100)
    query = query.replace("m", "e6",100)       
    query = query.replace("b", "e9",100)  
    return query

async def calculate(query):
    query = query.replace(",", "")
    engine_input = "{m:" + query + "}"
    start = time.time()
    output = engine.process(engine_input)
    end = time.time()

    output_string = output.body.replace("{m:", "").replace("}", "")
    return int(float(output_string))

async def clean_colour_roles(client,user):
    colour_pack = client.all_colour_pack
    user_roles = user.roles
    for i in colour_pack:
        if i in user_roles:
            await user.remove_roles(i)

async def convert_to_human_time(seconds):
    
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder , 3600)
    minutes, seconds = divmod(remainder, 60)
        
    human_timer = []
    if int(days)>0:
        if int(days)==1:
            human_timer.append(f"{int(days)} day")
        else:
            human_timer.append(f"{int(days)} days")
    if int(hours)>0:
        if int(hours) == 1:
            human_timer.append(f'{int(hours)} hour')
        else:
            human_timer.append(f'{int(hours)} hours')
    if int(minutes)>0:
        if int(minutes) == 1:
            human_timer.append(f'{int(minutes)} minute')
        else:
            human_timer.append(f'{int(minutes)} minutes')
    if int(seconds)>0:
        if int(seconds) == 1:
            human_timer.append(f'{int(seconds)} second')
        else:
            human_timer.append(f'{int(seconds)} seconds')
    
    if len(human_timer)>1:
        timer = f'{", ".join(i for i in human_timer[:-1])} and {human_timer[-1]}'
    else:
        timer = human_timer[-1]

    return timer.strip()


