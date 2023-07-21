# hdx-scraper-hdro-v2

## Development

Be sure to install `pre-commit`, which is run every time
you make a git commit:

```shell
pip install pre-commit
pre-commit install
```

The configuration file for this project is in a
non-start location. Thus, you will need to edit your
`.git/hooks/pre-commit` file to reflect this. Change
the line that begins with `ARGS` to:

```shell
ARGS=(hook-impl --config=.config/pre-commit-config.yaml --hook-type=pre-commit)
```

With pre-commit, all code is formatted according to
[black]("https://github.com/psf/black") and
[ruff]("https://github.com/charliermarsh/ruff") guidelines.

To check if your changes pass pre-commit without committing, run:

```shell
pre-commit run --all-files --config=.config/pre-commit-config.yaml
```
