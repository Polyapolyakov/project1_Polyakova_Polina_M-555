
from labyrinth_game.constants import ROOMS


# Описание возможных действий:
# Перемещение:
def move_player(game_state, direction):
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    if direction in current_room['exits']:
        next_room_name = current_room['exits'][direction]
        
        # Проверка доступа в treasure_room
        if next_room_name == 'treasure_room':
            if ('rusty_key' in game_state['player_inventory']) \
            or ('small_key' in game_state['player_inventory']):
                print(
            "Вы используете найденный ключ, чтобы открыть "
            "путь в комнату сокровищ."
                    )
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False
        
        game_state['current_room'] = next_room_name
        game_state['steps_taken'] += 1
        print(f"Вы переместились {direction}.")
        
        from labyrinth_game.utils import random_event
        random_event(game_state)
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False

# Взятие предмета:
def take_item(game_state, item_name):
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    if item_name in current_room['items']:
        game_state['player_inventory'].append(item_name)
        current_room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
        return True
    else:
        print("Такого предмета здесь нет.")
        return False

# Использование предмета:
def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return False
    
    if item_name == 'torch':
        print("Вы зажигаете факел. Ваш путь освещен!")
        return True
    elif item_name == 'sword':
        print("Меч теперь при Вас, враги Вам не страшны!")
        return True
    elif item_name == 'rusty_key':
        print("Ржавый ключ от двери или может от сундука?")
        return True
    elif item_name == 'small_key':
        print("Маленький ключ от шкатулки, но что же внутри?.")
        return True
    elif item_name == 'coin':
        print("Древняя монетка. Орел или решка?")
        return True
    elif item_name == 'bronze_box':
        print("У Вас есть шкатулка, может внутри есть ключ от сокровищ?")
        return True
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
        return False