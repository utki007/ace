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
    role_dict = client.event_diwali
    if event_name == "diwali":     
        roles_added = []
        for roles in role_dict.keys():
            actual_value = int(roles) * 1000000
            if float(actual_value)<=float(query):
                if role_dict[roles] not in user.roles:
                    # await user.add_roles(role_dict[roles])
                    roles_added.append(role_dict[roles])
            else:
                break
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




