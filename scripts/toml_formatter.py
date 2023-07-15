import toml
import argparse

def escape_quotes(s):
    return s.replace('"', '\\"')

def format_value(value):
    if isinstance(value, list):
        print(' = [')
        for item in value:
            print('  [', end='')
            print(', '.join([f'"{x}"' if isinstance(x, str) else str(x) for x in item]), end='')
            print('],')
        print(']')
    else:
        print(f' = "{escape_quotes(str(value))}"')

def format_toml(toml_string):
    data = toml.loads(toml_string)

    for key, value in data.items():
        if isinstance(value, dict):
            print(f'["{key}"]')
            for sub_key, sub_value in value.items():
                print(f'{sub_key}', end='')
                format_value(sub_value)
        else:
            print(f'{key} = "{value}"')
        print("\n\n")

def test():
    original_toml = """
    title = "Analysis - Games"

    [Doom]
    Developer = "id Software"
    Engine = "id Tech 6"
    Year = 2016
    Analysis = [ [ "The Devil is in the details", "https://advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pdf",], [ "Graphics Study", "https://www.adriancourreges.com/blog/2016/09/09/doom-2016-graphics-study/",], [ "DigitalFoundry Interview", "https://www.eurogamer.net/digitalfoundry-2016-doom-tech-interview",], [ "GamesBeat Interview", "https://venturebeat.com/games/the-definitive-interview-on-the-making-of-doom/",], [ "DSOGaming Interview", "https://www.dsogaming.com/interviews/id-software-tech-interview-dx12-vulkan-mega-textures-pbr-global-illumination-more/",], [ "QuakeCon P1", "https://www.twitch.tv/videos/81946710",], [ "QuakeCon P2", "https://www.twitch.tv/videos/81950107",],]

    ["Doom Eternal"]
    Developer = "id Software"
    Engine = "id Tech 7"
    Year = 2020
    Analysis = [ [ "Simon Coenen's Blog", "https://simoncoenen.com/blog/programming/graphics/DoomEternalStudy.html",],]

    ["Death Stranding"]
    Developer = "Kojima Productions"
    Engine = "Decima"
    Year = 2019
    Analysis = [ [ "Behind the Pretty Frames", "https://mamoniem.com/behind-the-pretty-frames-death-stranding/",],]
    """
    format_toml(original_toml)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='The TOML file to format')
    args = parser.parse_args()

    with open(args.file, 'r') as file:
        toml_data = file.read()
        format_toml(toml_data)

if __name__ == "__main__":
    main()
