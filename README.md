# Náboj Archive Generator

This is a simple set of scripts that we use to generate files for the web archive.

## Requirements

In order to run this, you will require:

- [Python 3](https://python.org)
- [Tectonic](https://tectonic-typesetting.github.io/)
- [WebTeX Render](https://github.com/naboj-org/webtex-render) saved as `wr` in the
  project root
- [dvisvgm](https://dvisvgm.de)
- [svgo](https://github.com/svg/svgo) optional, but recommended
- [tex4ht](https://tug.org/tex4ht/) experimental support

## Usage

Put input TeX files (see below) into `input` folder. Put any assets (images) into
`assets`. Then run:

```shell
./run.sh [template]
```

This will produce `output.zip` that can be uploaded to the web system.

We also provide an **experimental** support for generating archive HTML files using
TeX4ht, just use `run-tex4ht.sh` in place of `run.sh`.

## Available Templates

### Náboj Junior

```shell
./run.sh junior
```

`input` directory should contain one TeX file per language named `[lang_code].tex`.
(Note: Czech language code is `cs`, not `cz`!)
The TeX file should contain problems in the following format:

```tex
\begin{problem}{Collecting pebbles}
Alice and Bob are collecting pebbles at the beach. Alice has already $49$ more pebbles than Bob, so she decides to give him some. She gives Bob $11$ of her own pebbles. How many more pebbles does Alice now have in comparison to Bob?
\begin{solution}{$27$}
When Alice gives Bob eleven of her pebbles, she looses $11$ pebbles and Bob gains $11$ pebbles. So, the difference in the amount of pebbles they both have decreases by $11 + 11 = 22$. Thus, at the end Alice will have $49 - 22 = 27$ more pebbles than Bob.
\end{solution}
\end{problem}
```

## System Lifecycle

### Extraction

When running the generator, it first checks whether a file named `extract-[template].py`
exists and runs it.

This file handles conversion between competition's native TeX files and TeX files 
required used in the next steps.
The output should create the following files:

- `tex/[lang]/[problem]/statement.tex`
- `tex/[lang]/[problem]/answer.tex`
- `tex/[lang]/[problem]/solution.tex`

### WebTeX Render Templating

Our WebTeX Render tool allows you to use different templates. This is usually needed to
handle different requirements from different languages (for example the use of decimal
dot or comma in `siunitx`).

The generator expects to find a template file `templates/[template]/[lang].tex`. Most of
the time, most languages will share the same template, so it is a good idea to use
symlinks.

Note: most of the equations in problems are the same between all languages. The
generator will reuse generated files if they have the same template. This is determined
by looking at `templates/[template]/[lang].tex` and if it is a symlink, all languages
pointing to the same symlink will share the cache. *(See `junior` for example)*
