# Contribution Guide

This guide outlines the steps to contribute to our game information repository. We appreciate your interest and effort to help improve our database.

Example PR: [click here](https://github.com/OTFCG/Awesome-Game-Analysis/pull/12).

## Step 0: Gather Game Information

Before you begin contributing, make sure you've collected all the required game information. This includes:

- The title of the game
- The game's developer(studio)
- The engine used to develop the game
- The year the game was released
- Any links relevant to the game's analysis

Such information can be obtained from reliable sources like official game websites, developer interviews, or public resources like Wikipedia.

## Step 1: Add the Game Information

After you've collected all the necessary data, add it to the `data/games.toml` file following the provided format. Please append this information to the end of the file.

The required format is as follows:

```toml
["Game Name"]
Developer = "Developer"
Engine = "Engine Used"
Year = "Year of Release"
Analysis = [
  ["Title of Link 1", "https://link1.com"],
  ["Title of Link 2", "https://link2.com"],
  ....
]
```

Replace the placeholders with the appropriate game information. For the Analysis section, list all the analysis links you've obtained in the same way.

## Step 2 (optional): Test README.md File Generation

Once you've added the game information to the `data/games.toml` file, it's good practice to check if the `README.md` file generation works correctly.

Run the following command in the `scripts/toml_markdown.py` script:

``` bash
$ python scripts/toml_markdown.py -i data/games.toml -t toml --readme
```

This command converts the `data/games.toml` file into a `README.md` file. Note that the file conversion is automatically executed by our Continuous Integration (CI) system.


## Step 3: Create a Pull Request

Finally, create a pull request with the changes you made to the `data/games.toml` file. Please provide a brief yet comprehensive description of the changes you've made (e.g., new game entries, typo corrections) in the pull request.

We appreciate your contribution and efforts to enhance our game information repository. Thank you for making our community stronger and more informed!
