import toml
import re

def markdown_to_toml(md_table_entry):
    lines = md_table_entry.split("\n")
    # Extract table data
    game_info = [i.strip() for i in lines[0].split('|') if i.strip()]
    title, developer, engine, year, analysis_raw = game_info
    # Extract links
    analysis = re.findall(r'\[(.*?)\]\((.*?)\)', analysis_raw)
    # Create toml
    toml_dict = {title: {"Developer": developer, "Engine": engine, "Year": int(year), "Analysis": analysis}}
    return toml.dumps(toml_dict)

def toml_to_markdown(toml_string):
    toml_dict = toml.loads(toml_string)
    title, game_info = list(toml_dict.items())[0]
    developer = game_info["Developer"]
    engine = game_info["Engine"]
    year = game_info["Year"]
    analysis = game_info["Analysis"]
    # Create markdown
    md_table_entry = f"|{title}|{developer}|{engine}|{year}|<details><summary>Expand</summary>"
    for a in analysis:
        md_table_entry += f"- [{a[0]}]({a[1]})<br>"
    md_table_entry += "</details>|"
    return md_table_entry

# Test
def test():
    markdown_table_entry = """
    |Doom|id Software|id Tech 6|2016|<details><summary>Expand</summary>- [The Devil is in the details](https://advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pdf)<br>- [Graphics Study](https://www.adriancourreges.com/blog/2016/09/09/doom-2016-graphics-study/)<br>- [DigitalFoundry Interview](https://www.eurogamer.net/digitalfoundry-2016-doom-tech-interview)<br>- [GamesBeat Interview](https://venturebeat.com/games/the-definitive-interview-on-the-making-of-doom/)<br>- [DSOGaming Interview](https://www.dsogaming.com/interviews/id-software-tech-interview-dx12-vulkan-mega-textures-pbr-global-illumination-more/)<br>- [QuakeCon P1](https://www.twitch.tv/videos/81946710)<br>- [QuakeCon P2](https://www.twitch.tv/videos/81950107)</details>|
    """.strip()

    toml_blocks = """
    [Doom]
    Developer="id Software"
    Engine="id Tech 6"
    Year=2016
    Analysis=[
    ["The Devil is in the details","https://advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pdf"],
    ["Graphics Study","https://www.adriancourreges.com/blog/2016/09/09/doom-2016-graphics-study/"],
    ["DigitalFoundry Interview","https://www.eurogamer.net/digitalfoundry-2016-doom-tech-interview"],
    ["GamesBeat Interview","https://venturebeat.com/games/the-definitive-interview-on-the-making-of-doom/"],
    ["DSOGaming Interview","https://www.dsogaming.com/interviews/id-software-tech-interview-dx12-vulkan-mega-textures-pbr-global-illumination-more/"],
    ["QuakeCon P1","https://www.twitch.tv/videos/81946710"],
    ["QuakeCon P2","https://www.twitch.tv/videos/81950107"],
    ]
    """.strip()

    # Testing markdown_to_toml
    print("-- Testing markdown_to_toml --")
    print("```")
    print(markdown_to_toml(markdown_table_entry))
    print("```")

    # Testing toml_to_markdown
    print("\n-- Testing toml_to_markdown --")
    print("```")
    print(toml_to_markdown(toml_blocks))
    print("```")

test()
