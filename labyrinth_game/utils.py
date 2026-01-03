
import math

from labyrinth_game.constants import COMMANDS, ROOMS


# Вспомогательные функции игры:
# Описание текущей комнаты в игре:
def describe_current_room(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    print(f"\n== {current_room_name.upper()} ==")
    print(room['description'])
    
    if room['items']:
        print("\nЗаметные предметы:", ", ".join(room['items']))
    else:
        print("\nЗаметные предметы: нет")
    
    if room['exits']:
        exits_str = ", ".join(room['exits'].keys())
        print(f"Выходы: {exits_str}")
    else:
        print("Выходы: нет")
    
    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

# Псевдослучайный генератор:
def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)

# Активация ловушки:
def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    
    if game_state['player_inventory']:
        inventory_len = len(game_state['player_inventory'])
        item_index = pseudo_random(game_state['steps_taken'], inventory_len)
        lost_item = game_state['player_inventory'].pop(item_index)
        print(f"Вы потеряли: {lost_item}!")
    else:
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        if damage_chance < 3:
            print("Ловушка нанесла смертельный урон! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам повезло - вы уцелели, но погибель была близка!")

# Случайное событие:
def random_event(game_state):
    if pseudo_random(game_state['steps_taken'], 10) == 0:
        event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
        
        if event_type == 0:
            # Положительный бонус - монетка
            current_room = ROOMS[game_state['current_room']]
            if 'coin' not in current_room['items']:
                current_room['items'].append('coin')
                print("Вы нашли на полу древнюю монетку!")
        
        elif event_type == 1:
            # Напряжение - шорох из темноты
            print("Вы слышите чей-то шорох из темноты...")
            if 'sword' in game_state['player_inventory']:
                print("Но ваш меч отпугивает призрак.")
        
        elif event_type == 2:
            # Ловушка (только в trap_room без факела)
            if (game_state['current_room'] == 'trap_room' and
                    'torch' not in game_state['player_inventory']):
                print("Вы не заметили ловушку в темноте!")
                trigger_trap(game_state)

# Решение загадок:
def solve_puzzle(game_state):
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    if current_room['puzzle'] is None:
        print("Загадок здесь нет.")
        return
    
    question, correct_answer = current_room['puzzle']
    print(question)
    
    user_answer = input("Ваш ответ: ").strip().lower()
    
    alternative_answers = {
        '10': ['десять', '10'],
        'шаг шаг шаг': ['шаг шаг шаг', 'шагшагшаг'],
        'резонанс': ['резонанс'],
        '1000': ['1 000']
    }
    
    correct_answers = alternative_answers.get(
        correct_answer,
        [correct_answer.lower()]
    )
    
    if user_answer in correct_answers:
        print("Верно! Загадка решена!")
        current_room['puzzle'] = None
        
        if current_room_name == 'trap_room':
            print("Плиты перестали дрожать. Теперь здесь безопасно.")
        
    else:
        print("Неверно. Попробуйте снова.")
        if current_room_name == 'trap_room':
            print("Плиты содрогаются!")
            trigger_trap(game_state)

# Открытие сундука:
def attempt_open_treasure(game_state):
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    if current_room_name != 'treasure_room':
        print("Здесь нет сундука с сокровищами.")
        return
        
    has_rusty_key = 'rusty_key' in game_state['player_inventory']
    has_small_key = ('small_key' in game_state['player_inventory']) \
                    and ('bronze_box' in game_state['player_inventory'])
    
    if has_rusty_key or has_small_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        # Удаляем сундук из комнаты
        if 'treasure_chest' in current_room['items']:
            current_room['items'].remove('treasure_chest')
                
        print('В сундуке сокровище! Вы победили!')
        game_state['game_over'] = True
        return
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. У вас нет ключа.")
    if current_room['puzzle'] is not None:
        use_code = input("Попробовать ввести код? (да/нет): ").strip().lower()
        if use_code == 'да':
            question, correct_answer = current_room['puzzle']
            print(f"\n{question}")
            user_code = input("Введите код: ").strip()
            
            if user_code == correct_answer:
                print("Код верный! Сундук открыт! Вы победили!")
                # Удаляем сундук из комнаты
                if 'treasure_chest' in current_room['items']:
                    current_room['items'].remove('treasure_chest')
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остается запертым.")
        else:
            print("Вы отступаете от сундука.")
    else:
        print("Нет возможности открыть сундук без ключа.")

# Помошь:
def show_help():
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")