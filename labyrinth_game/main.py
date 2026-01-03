#!/usr/bin/env python3

from labyrinth_game import player_actions, utils


# Определение начального состояния игры:
def create_initial_game_state():
    return {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,    
        'steps_taken': 0
    }

# Основная функция - функция управления игрой:
def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    game_state = create_initial_game_state()
    utils.describe_current_room(game_state)
    print("\nИгра началась! Введите 'help' для списка команд.")
    
    while not game_state['game_over']:
        try:
            command = input("\n> ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("Спасибо за игру! Ждем Вас снова!")
                game_state['game_over'] = True
            elif command == 'help':
                utils.show_help()
            elif command == 'look':
                utils.describe_current_room(game_state)
            elif command == 'inventory':
                if game_state['player_inventory']:
                    print(
                        "Ваш инвентарь:",
                        ", ".join(game_state['player_inventory'])
                    )
                else:
                    print("Ваш инвентарь пуст.")
            elif command.startswith('go '):
                direction = command[3:].strip()
                player_actions.move_player(game_state, direction)
                utils.describe_current_room(game_state)
            elif command in ['north', 'south', 'east', 'west']:
                player_actions.move_player(game_state, command)
                utils.describe_current_room(game_state)
            elif command.startswith('take '):
                item_name = command[5:].strip()
                player_actions.take_item(game_state, item_name)
            elif command.startswith('use '):
                item_name = command[4:].strip()
                player_actions.use_item(game_state, item_name)
            elif command == 'solve':
                if game_state['current_room'] == 'treasure_room':
                    utils.attempt_open_treasure(game_state)
                else:
                    utils.solve_puzzle(game_state)
            else:
                msg = f"Неизвестная команда: '{command}'. "
                msg += "Введите 'help' для списка команд."
                print(msg)        
        except (KeyboardInterrupt, EOFError):
            print("\n\nВыход из игры. До скорых встречь!")
            game_state['game_over'] = True
    print("Игра завершена.")

if __name__ == "__main__":
    main()