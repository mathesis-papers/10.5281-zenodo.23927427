# Resolving Question III.5 of Stepanov–Herrmann–Guhr (arXiv:2104.08966v1, p. 7)

For each point in the remaining domain of arXiv:2104.08966v1, Question III.5
(p. 7), eventual existence of correlation matrices whose top-eigenvector
weight is not maximal holds exactly when the standard deviation exceeds
the positive mean correlation. The note gives the full proof and an extension:
throughout `c > 0`, `sigma > 0`, `c^2 + sigma^2 < 1`, eventual existence is
equivalent to `c < 1/2` and `sigma > c`.
On the entire legal half-disc `sigma >= 0`, `c^2 + sigma^2 <= 1`, the
classification is `0 <= c < 1/2`, `sigma > c`, `c^2 + sigma^2 < 1`.
Further corollaries give the majority and acute-angle bound for `sigma <= c`,
the exact criterion in terms of spectral-projection masses and eigenspace
dimensions, and a centered obstruction for arbitrary symmetric matrices.

## Contents and construction

- `note.tex`: self-contained LaTeX, including its bibliography.
- `metadata.json`: title, authors, license, problem identifier and formal scope.
- `verify.py`: exact rational checks using Python 3's standard library.
- `checks.json`: expected exact checker output.

Build the PDF using Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, use an ordinary LaTeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded in `note.tex`, so BibTeX is unnecessary.
Packages required are `geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`,
`array`, `fontenc`, `lmodern`, `hyperref` and `microtype`.

Run the finite checks with:

```sh
python3 verify.py
```

The command writes `checks.json` deterministically. It checks four correlation
matrices in dimensions 16, 17, 24 and 100, with positive-definiteness and
two-direction spectral certificates. For dimension 16 it also checks explicit
eigenvectors, eigenvalues and weights `3/7` and `4/7`. It tests the centered
two-point energy inequality on 2,100 integer controls and its equality on 28
controls. These are finite checks; the all-parameter statements have written
proofs in the note.
It additionally checks 37 exact zero-mean witnesses in dimensions 4 through 40
and 851 rank-one circular-boundary controls in the same dimension range.
For a rank-one boundary matrix the universal gap is equivalent to `c < 0`.

## Formal scope

The pinned declaration `D5.S3.Estimation.CorrelationTopEigenvectorWeight.result`
in [CorrelationTopEigenvectorWeight.lean](https://github.com/the-omega-institute/trureturing/blob/8c3421e2977f07cb0b5d9b30b7ede138d9951cb5/D5/S3/Estimation/CorrelationTopEigenvectorWeight.lean)
proves the eventual equivalence on the source's remaining domain `D`, using
the universal-eigenbasis definition of the weight gap. The explicit
finite-dimensional inequalities, extension to the whole positive parameter
domain and legal half-disc, compact uniformity, majority/angle bound,
eigenspace criterion, zero-mean and circular-boundary corollaries,
symmetric-matrix obstruction and rational examples have written proofs
in the note. The checker establishes the specified finite identities.

## Authors and license

1. Haobo Ma — ChronoAI Pte Ltd, Singapore.
2. Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (`cc-by-4.0`).
