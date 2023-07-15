import toml
import re
import argparse
import difflib
import markdown
import sys

'''
- For converting a TOML file to Markdown:
$ python toml_markdown.py -i input.toml -t toml

- For converting a Markdown file to TOML:
$ python toml_markdown.py -i input.md -t markdown

- For generating a full README.md from TOML file, use the --readme flag.
This will include all sections at the top and bottom of the output:
$ python toml_markdown.py -i input.toml -t toml --readme

- All of these commands print the result to standard output (the console),
but you can redirect this to a file like so:
$ python toml_markdown.py -i input.toml -t toml --readme > README.md
'''

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

section_top='''
# Awesome-Game-Analysis
This repository serves as a comprehensive collection of video game technology analysis resources.

Suggestions are welcome to be filed via the GitHub issue tracker for this repository, please use the issue tracker to submit your ideas.

***In order to maintain the structure of this repository, please don't directly make changes to the `README.md` file. Instead, read our [Contribution Guide](https://github.com/OTFCG/Awesome-Game-Analysis/blob/main/contribution_guide.md) before PRs.***
'''
section_reference='''
## References
- [Behind the Pretty Frames](https://mamoniem.com/category/behind-the-pretty-frames/)
- [imgself's Blog](https://imgeself.github.io/posts/)
- [Froyok's Blog](https://www.froyok.fr/articles.html)
- [Anton Schreiner's Blog](https://aschrein.github.io/)
- [Frame Analysis](https://alain.xyz/blog)
- [The Code Corsair](https://www.elopezr.com/)
- [Graphics Studies](https://www.adriancourreges.com/blog/)
- [Silent’s Blog](https://cookieplmonster.github.io/)
- [Nathan Gordon's Blog](https://medium.com/@gordonnl)
- [Thomas' Blog](https://blog.thomaspoulet.fr)
- [IRYOKU's Blog](https://www.iryoku.com/)
- [Game Art Tricks](https://simonschreibt.de/game-art-tricks/)
- [The Cutting Room Floor](https://tcrf.net/The_Cutting_Room_Floor)
- [Crytek Presentations](https://archive.org/download/crytek_presentations)
- [r/TheMakingOfGames](https://www.reddit.com/r/TheMakingOfGames/)
- [r/videogamescience](https://www.reddit.com/r/videogamescience/)
- [GDC Vault](https://www.gdcvault.com/)
- [GDC's Programming Talks](https://www.youtube.com/playlist?list=PL2e4mYbwSTbaw1l65rE0Gv6_B9ctOzYyW)
'''

def compare_files(file1, file2):
    # Open file for reading in text mode
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        # Read the lines of each file
        f1_text = f1.readlines()
        f2_text = f2.readlines()

    # Find and print the differences
    for line in difflib.unified_diff(f1_text, f2_text, fromfile=file1, tofile=file2):
        print(line)

def markdown_to_dict(file):
    with open(file, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    game_info_dict = {}
    table_pattern = r'\|(.+)\|'  
    table_matches = re.findall(table_pattern, markdown_text, re.MULTILINE)
    table_data = table_matches[2:]
    
    for row in table_data:
        game_info = [cell.strip() for cell in row.split('|')]
        title, developer, engine, year, analysis_raw = game_info
        analysis = re.findall(r'\[(.*?)\]\((.*?)\)', analysis_raw)
        game_info = {
            "Developer": developer,
            "Engine": engine,
            "Year": year,
            "Analysis": analysis,
        }
        game_info_dict[title] = game_info

    return game_info_dict

def toml_to_dict(toml_string):
    toml_dict = toml.loads(toml_string)
    del toml_dict["title"]
    return toml_dict
        
def check_change(olddict, newdict):
    for title, game_info in newdict.items():
        old_game_info = olddict.get(title)
        if old_game_info is not None:
            if (
                old_game_info["Developer"] != game_info["Developer"]
                or old_game_info["Engine"] != game_info["Engine"]
                or old_game_info["Year"] != game_info["Year"]
                or old_game_info["Analysis"] != game_info["Analysis"]
            ):
                return True
        else:
            return True
        
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Toml-Markdown Converter',
                        description='''This program converts between TOML blocks and markdown table entries. It's designed to help
                                    you generate markdown table entries or README.md files from TOML input. You can provide a file
                                    as input (-i, --input) and specify the type of the file (-t, --type). Currently, the script
                                    supports two types: 'toml' and 'markdown' (which can also be denoted as 'md').
                                    The script also allows you to check for the presence of a '--readme' flag,
                                    without any associated value. If this flag is provided, the script will
                                    generate the entire README.md content, including game analysis, top section and reference section.''')
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-t', '--type', required=True, choices=['toml', 'markdown', 'md'])
    parser.add_argument('--readme', required=False, action='store_true')

    args = parser.parse_args()

    # using the std output, you can redirect directly to the README.md or README.temp.md for comparasion
    with open(args.input, 'r') as f:
        if args.type == 'toml':
            if args.readme:
                try:
                    olddict = markdown_to_dict('README.md')
                    newdict = toml_to_dict(f.read())
                    change = check_change(olddict, newdict)
                    if not change :
                        sys.exit(1)
                    section_games='''## Analysis - Games\n\n|Game|Developer|Engine|Year|Analysis|\n|:---|:---|:---|:---|:---|'''.strip() + "\n"
                    f.seek(0)
                    section_games += toml_to_markdown(f.read())
                    res = ""
                    res += section_top
                    res += "\n---\n\n"
                    res += section_games
                    res += "\n---\n"
                    res += section_reference
                    readme = open("README.md", "w")
                    readme.write(res)
                    readme.close()
                except Exception as e:
                    print("Error occurred:", e)
                    sys.exit(-1)
            else:
                print(toml_to_markdown(f.read()))
        else:
            print(markdown_to_toml(f.read()))
