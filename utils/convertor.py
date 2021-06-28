import time
from TagScriptEngine import Interpreter, adapter, block
from discord.ext.buttons import Paginator

blocks = [
    block.MathBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
]
engine = Interpreter(blocks)

async def convert_to_time(query):
    query = query.lower()
    query = query.replace("h", "*3600+",1)
    query = query.replace("m", "*60+",1)       
    query = query.replace("s", "*1+",1)  
    query = f"{query}0"
    return query
    
async def convert_to_numeral(self, query):
    query = query.lower()
    query = query.replace("k", "e3",100)
    query = query.replace("m", "e6",100)       
    query = query.replace("b", "e12",100)  
    return query

async def calculate(query):
    query = query.replace(",", "")
    engine_input = "{m:" + query + "}"
    start = time.time()
    output = engine.process(engine_input)
    end = time.time()

    output_string = output.body.replace("{m:", "").replace("}", "")
    return int(float(output_string))