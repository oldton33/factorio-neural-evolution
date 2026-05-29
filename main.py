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

def give_item(item_name, item_count, item_quality="normal"):
    return f"""/c 
    game.players[1].insert{{
        name="{item_name}", 
        count={item_count},
        quality="{item_quality}"
        }}"""

def spawn_entity(entity_name, direction=0, x_offset=0, y_offset=0,):
    # force=game.players[1].force делает объект НАШИМ
    return f"""/c 
    local p = game.players[1].position; 
    game.players[1].surface.create_entity{{
        name="{entity_name}", 
        position={{p.x + {x_offset}, p.y + {y_offset}}}, 
        force=game.players[1].force,
        direction={direction}
    }}"""

def spawn_blueprint(blueprint_string, x_target=0, y_target=0):
    # Очищаем строку от возможных пробелов
    bp_clean = blueprint_string.strip()
    
    return f"""/c
    local player = game.players[1]
    local surf = player.surface
    
    -- 1. Создаем временный инвентарь из 1 слота и кладем туда чистый чертеж
    local inv = game.create_inventory(1)
    local stack = inv[1]
    stack.set_stack({{name="blueprint"}})
    
    -- 2. Загружаем в этот чертеж нашу закодированную строку
    stack.import_stack("{bp_clean}")
    
    -- 3. Разворачиваем чертеж на карту в целевые координаты
    stack.build_blueprint{{
        player = player,
        surface = surf,
        position = {{ {x_target}, {y_target} }},
        force = player.force,
        build_mode = defines.build_mode.force -- force заставит вырубить деревья, если они мешают
    }}
    
    -- 4. Уничтожаем временный инвентарь, чтобы не забивать память
    inv.destroy()
    """

cage = "0eNqV1lFrhDAMAOD/kuc62trW1r8yxvB2ZRS0inrbRPzv0zu2PczQ5k2l+UggJl3h0t78MIY4Q71CeOvjBPXzClN4j017fItN56GGae6jLz6btoWNQYhX/wW12F4Y+DiHOfhH3P1leY237uLH/QA7iWcw9NMe0sfD35lCyvJJM1igPh62jf2DZC4kfyB5DpXkjBBI5UI8AelcSCQgkwkJm4CqXMglIPsLXcM0tM1SDE3055ZJWI5gVQlLcAKmU1hukwuVaHIhyRKWE73NNSIpsqQQSZOrw3IyZAnLqSJXVyGSJUsGkRy5OkSSnCwh1Un6ILeIJMmSQ6SSXB0mKbKEVaep1ZUckQxZEohUUXcnKlnqqkIlR92emFRy6rJCJUHdn6iUPcerlJTd4yYlZfe4TknkOY5K5Dn++Fv2S2eYfbeH/d1eGXz4cboHaSOdck5bxSVXdtu+Abv/cPk="

def clear_area(radius=20):
    # Пишем в одну строку, никаких переносов
    return f"/c local p = game.players[1].position; local r = {radius}; local lt = {{x=p.x-r, y=p.y-r}}; local rb = {{x=p.x+r, y=p.y+r}}; for _, e in pairs(game.players[1].surface.find_entities_filtered{{area={{lt, rb}}}}) do if e.valid and e.name ~= 'character' then e.destroy() end end"

async def main():

    #await send_cmd("/c game.print('code1')")
    #await asyncio.sleep(2)
    #await prepare_sandbox()

    #await send_cmd(give_item("exoskeleton-equipment", 5))

    #await send_cmd(give_item("electric-energy-interface", 10))
    #await send_cmd(give_item("substation", 10, "legendary"))
    await send_cmd(spawn_blueprint(cage, x_target=0, y_target=0))

if __name__ == '__main__':
    asyncio.run(main())
