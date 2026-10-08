# D-SIMM

D-SIMM applies the International Swaps and Derivatives Association's Standard Initial Margin Model to margin limits for tokenised assets in decentralised lending. It covers tokenised funds and linear, long-only tokenised single equities. Funds use attested issuer-redemption capacity. Single equities use the underlying share’s SIMM bucket and concentration threshold, with a sale horizon derived from the whole supply cap and observed trading volume. All published risk parameters remain on SIMM v2.6.

[Read the latest compiled paper](./dsimm.pdf).

## Build

The paper requires a LaTeX installation with `latexmk` and BibTeX.

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error dsimm.tex
```

Run `latexmk -C` to remove generated build files.

## Validation

Check the SIMM equity parameter table and worked-example arithmetic with Python 3:

```sh
python3 -m unittest discover -s tests -v
```

## Contributions

Pull requests build the paper automatically. The workflow commits an updated PDF to branches in this repository and publishes a PDF artefact for pull requests from forks.
