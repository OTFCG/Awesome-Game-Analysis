import toml
import re
import argparse

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
    index = 0
    if 'title' in toml_dict:
        title_section = toml_dict['title']
        index = 1
    md_table_entry=""
    for item in list(toml_dict.items())[index:]:
        title, game_info = item
        developer = game_info["Developer"]
        engine = game_info["Engine"]
        year = game_info["Year"]
        analysis = game_info["Analysis"]
        # Create markdown
        md_table_entry += f"|{title}|{developer}|{engine}|{year}|<details><summary>Expand</summary>"
        for a in analysis:
            md_table_entry += f"- [{a[0]}]({a[1]})<br>"
        md_table_entry += "</details>|\n"
    return md_table_entry

# Test
def test_single():
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

def test_multiple():
    markdown_list = """|Doom|id Software|id Tech 6|2016|<details><summary>Expand</summary>- [The Devil is in the details](https://advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pdf)<br>- [Graphics Study](https://www.adriancourreges.com/blog/2016/09/09/doom-2016-graphics-study/)<br>- [DigitalFoundry Interview](https://www.eurogamer.net/digitalfoundry-2016-doom-tech-interview)<br>- [GamesBeat Interview](https://venturebeat.com/games/the-definitive-interview-on-the-making-of-doom/)<br>- [DSOGaming Interview](https://www.dsogaming.com/interviews/id-software-tech-interview-dx12-vulkan-mega-textures-pbr-global-illumination-more/)<br>- [QuakeCon P1](https://www.twitch.tv/videos/81946710)<br>- [QuakeCon P2](https://www.twitch.tv/videos/81950107)</details>|
|Doom Eternal|id Software|id Tech 7|2020|<details><summary>Expand</summary>- [Simon Coenen's Blog](https://simoncoenen.com/blog/programming/graphics/DoomEternalStudy.html)</details>|
|Death Stranding|Kojima Productions|Decima|2019|<details><summary>Expand</summary>- [Behind the Pretty Frames](https://mamoniem.com/behind-the-pretty-frames-death-stranding/)</details>| 
|Diablo IV|Blizzard Albany, Team 3|Internal|2023|<details><summary>Expand</summary>- [Behind the Pretty Frames](https://mamoniem.com/behind-the-pretty-frames-diablo-iv/)<br>- [Blizzard](https://news.blizzard.com/en-us/diablo4/23964183/peeling-back-the-varnish-the-graphics-of-diablo-iv)</details>| 
|Resident-evil II Re|Capcom Division 1|RE Engine|2019|<details><summary>Expand</summary>- [Behind the Pretty Frames](https://mamoniem.com/behind-the-pretty-frames-resident-evil/)<br>- [Anton Schreiner's Blog](https://aschrein.github.io/2019/08/01/re2_breakdown.html)</details>|
|God of war 4|Santa Monica Studio|Internal|2018|<details><summary>Expand</summary>- [Behind the Pretty Frames](https://mamoniem.com/behind-the-pretty-frames-god-of-war/)</details>|""".strip().split('\n')

    toml_block_list="""
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
    """

    # markdown
    for item in markdown_list:
        print()
        print(markdown_to_toml(item))
        print()

    # toml
    print(toml_to_markdown(toml_block_list))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Toml-Markdown Converter',
                        description='Converting toml blocks and markdown table entries')
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-t', '--type', required=True, choices=['toml', 'markdown', 'md'])

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        if args.type == 'toml':
            print(toml_to_markdown(f.read()))
        else:
            print(markdown_to_toml(f.read()))
