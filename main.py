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


async def main():

    await send_cmd("/c game.print('code1')")
    await asyncio.sleep(2)
    for i in range (1,10):
        for j in range(1,10):
            await send_cmd(f"/c local p = game.players[1].position; game.players[1].surface.create_entity{{name='stone-wall', position={{p.x + {i + 10}, p.y + {j + 10}}}}}")
            await send_cmd(f"/c local p = game.players[1].position; game.players[1].surface.create_entity{{name='stone-wall', position={{p.x + {i - 10}, p.y + {j - 10}}}}}")

if __name__ == '__main__':
    asyncio.run(main())
