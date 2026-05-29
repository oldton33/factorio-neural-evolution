import asyncio
import time
from rcon.source import rcon

IP = '127.0.0.1'
PORT = 27015
PASSWORD = 'secret'


async def send_cmd(lua_command):
    try:
        response = await rcon(lua_command, host=IP, port=PORT, passwd=PASSWORD)
        return response
    except Exception as e:
        print(f"Ошибка RCON: {e}")
        return None

async def prepare_sandbox():
    await send_cmd("/c game.peaceful_mode = true")
    await send_cmd("/c game.players[1].surface.always_day = true")
    await send_cmd("/c game.forces['enemy'].kill_all_units()")
    await send_cmd("/c game.forces['enemy'].set_friend('player', true)")
    await send_cmd("/c game.forces['player'].set_friend('enemy', true)")

def give_item(item_name, item_count):
    return f"""/c 
    game.players[1].insert{{
        name="{item_name}", 
        count={item_count}
        }}"""

def spawn_entity(entity_name, x_offset=0, y_offset=0):
    # force=game.players[1].force делает объект НАШИМ
    return f"""/c 
    local p = game.players[1].position; 
    game.players[1].surface.create_entity{{
        name="{entity_name}", 
        position={{p.x + {x_offset}, p.y + {y_offset}}}, 
        force=game.players[1].force
    }}"""



def clear_area(radius=20):
    # Пишем в одну строку, никаких переносов
    return f"/c local p = game.players[1].position; local r = {radius}; local lt = {{x=p.x-r, y=p.y-r}}; local rb = {{x=p.x+r, y=p.y+r}}; for _, e in pairs(game.players[1].surface.find_entities_filtered{{area={{lt, rb}}}}) do if e.valid and e.name ~= 'character' then e.destroy() end end"

async def main():

    #await send_cmd("/c game.print('code1')")
    #await asyncio.sleep(2)
    #await prepare_sandbox()

    #await send_cmd(give_item("exoskeleton-equipment", 5))
    #await send_cmd(spawn_entity("inserter"))
    await send_cmd(clear_area(1000))

if __name__ == '__main__':
    asyncio.run(main())
