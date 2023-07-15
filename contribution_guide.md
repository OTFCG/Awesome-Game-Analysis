# Contribution Guide

0. gather the game info(Game, Developer, Engine, Year, game analysis links), you could check out the wikipidea of the game.

1. add the game info with following format to the bottom of `games.toml`

```toml
["Game Name"]
Developer = "xxx"
Engine = "xxx"
Year = "xxx"
Analysis = [
  ["Link 1", "https://xxx.com"],
  ["Link 2", "https://bbb.com"],
  ....
]
```

2. generate the `README.md`
``` bash
$ python toml_markdown.py -i games.toml -t toml --readme > README.md
```

3. pull request with the changed `games.toml` and `README.md`
