# Contribution Guide

This guide outlines the steps to contribute to our game information repository. We appreciate your interest and effort to help improve our database.


## Step 0: Gather Game Information

Before you start contributing, gather the necessary game information. This includes the **game** title, the **developer**, the **engine** used, the **year** of release, and any relevant **links** for game analysis. You can find this information from reliable sources like Wikipedia.


## Step 1: Add the Game Information

Once you have gathered all the necessary information, add it to the `games.toml` file, adhering to the given format. Append this information at the end of the file.

Here's the format you must follow:

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

Replace the placeholders with the respective game information. For Analysis, list all the analysis links you've gathered in the above manner.

## Step 2: Generate the README.md File

After adding the game information to the `games.toml` file, generate the `README.md` file using the below command (in `scripts/toml_markdown.py`):

``` bash
$ python scripts/toml_markdown.py -i games.toml -t toml --readme > README.md
```

This command will convert the games.toml file into a README.md file.

## Step 3: Create a Pull Request

Once you've generated the `README.md` file successfully, create a pull request with the changes you made in the `games.toml` and `README.md` files. Ensure to provide a brief description of the changes in the pull request.

Remember, your contributions are valuable to us. Thank you for helping us improve our game information repository!
