def collect_data():
    game_data = {}
    game_data['Game'] = input("Please enter the Game: ")
    game_data['Developer'] = input("Please enter the Developer: ")
    game_data['Engine'] = input("Please enter the Engine: ")
    game_data['Year'] = input("Please enter the Year: ")

    break_down_data = []
    while True:
        print("Please enter the name and link for 'Break Down' section (enter '#' to quit): ")
        name = input("Name: ")
        if name == '#':
            break
        link = input("Link: ")
        if link == '#':
            break
        break_down_data.append((name, link))
    
    game_data['Break Down'] = break_down_data
    return game_data

def format_output(game_data):
    break_down_str = "<details><summary>Expand</summary>"
    for name, link in game_data['Break Down']:
        break_down_str += f"- [{name}]({link})<br>"
    break_down_str += "</details>"

    output = f"|Game|Developer|Engine|Year|Break Down|\n|:---|:---|:---|:---|:---|\n"
    output += f"|{game_data['Game']}|{game_data['Developer']}|{game_data['Engine']}|{game_data['Year']}|{break_down_str}|"

    return output

def main():
    game_data = collect_data()
    output = format_output(game_data)
    print(output)

if __name__ == "__main__":
    main()

