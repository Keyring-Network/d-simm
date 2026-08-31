# D-SIMM

D-SIMM applies the International Swaps and Derivatives Association's Standard Initial Margin Model to margin limits for tokenised assets in decentralised lending. This first iteration focuses on tokenised funds.

[Read the latest compiled paper](./dsimm.pdf).

## Build

The paper requires a LaTeX installation with `latexmk` and BibTeX.

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error dsimm.tex
```

Run `latexmk -C` to remove generated build files.

## Contributions

Pull requests build the paper automatically. The workflow commits an updated PDF to branches in this repository and publishes a PDF artefact for pull requests from forks.
