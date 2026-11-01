# Real Planet or False Alarm? Classifying Kepler Exoplanet Candidates

CT4101 Machine Learning – Portfolio Project
Keelan O'Dowd (23440916), University of Galway
Repository: https://github.com/keelanOdowd/Kepler-exoplanet-classification

## Project question

Using only transit-signal and host-star measurements, can a model predict whether a Kepler Object of Interest (KOI) is a confirmed exoplanet or a false positive?

This is a binary classification task. The intended use is to help astronomers prioritise candidates for follow-up observation. The model is meant to support expert vetting, not replace it.

## Dataset

| | |
|---|---|
| **Source** | NASA Exoplanet Archive – Kepler Objects of Interest (KOI) Cumulative Table |
| **Citation** | NASA Exoplanet Archive (2019). *Kepler Objects of Interest Cumulative Table*. https://doi.org/10.26133/NEA4 |
| **Size** | 9,564 rows × 153 columns (accessed 04/10/2026) |
| **Target** | `koi_disposition`: CONFIRMED (1) vs FALSE POSITIVE (0). CANDIDATE rows are excluded from training and evaluation. |
| **Labelled set** | 7,587 rows, 36.2% confirmed |

The data is **not stored in this repository**. It is downloaded automatically the first time notebook 01 runs. See [`data/README.md`](data/README.md) for the download link, access date, licence and citation.

## Evaluation protocol

| | |
|---|---|
| **Prediction moment** | After the transit fit and stellar characterisation, before vetting and follow-up |
| **Test set** | 20%, grouped by star (`kepid`) and stratified, saved to `data/split.csv`. Grouped because 938 stars host several KOIs that share stellar features. Used once, at the end. |
| **Cross-validation** | 5-fold `StratifiedGroupKFold` on the training set, with the same folds for every model |
| **Metrics** | PR-AUC (primary, since positives are the minority and the task is ranking); F1, precision, recall and ROC-AUC (secondary) |
| **Baselines** | Dummy, planet-radius rule, logistic regression |
| **Leakage control** | Vetting outputs, centroid diagnostics and follow-up columns are dropped (`src/features.py`, `reports/leakage_register.csv`). Preprocessing is fitted inside a `Pipeline` on training folds only. |
| **Preprocessing** | Signed log for long-tailed features, then scaling, then median imputation with missing-value indicators |
| **Reproducibility** | `random_state=42` everywhere, pinned packages, dataset shape and SHA-256 checked on load. Experiments are recorded in `reports/experiment_log.md`. |

## Results so far

| Model | PR-AUC (5-fold grouped CV) |
|---|---|
| Dummy | 0.362 |
| Planet-radius rule | 0.545 ± 0.009 |
| Logistic regression | 0.877 ± 0.009 |

## Repository structure

```
├── README.md
├── requirements.txt           # pinned package versions
├── .gitignore
├── data/
│   └── README.md              # dataset source, licence, download instructions
├── notebooks/
│   ├── 01_audit.ipynb         # data audit, leakage analysis, train/test split
│   ├── 02_preprocessing.ipynb # preprocessing pipeline and checks
│   └── 03_baselines.ipynb     # evaluation design and baseline results
├── src/
│   ├── data.py                # download, integrity checks, loading the split
│   ├── features.py            # feature list and drop list
│   └── preprocessing.py       # preprocessing pipeline
└── reports/
    ├── figures/
    ├── data_dictionary.csv
    ├── leakage_register.csv
    ├── baseline_results.csv
    └── experiment_log.md
```

## Setup

Requires **Python 3.14** (developed on Windows 11).

```bash
git clone https://github.com/keelanOdowd/Kepler-exoplanet-classification.git
cd Kepler-exoplanet-classification

python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

python -m pip install -r requirements.txt
python -m ipykernel install --user --name kepler --display-name "Python (kepler)"
```

## How to run

1. Start JupyterLab from the repository root: `jupyter lab`
2. Open the notebooks in `notebooks/` **in numbered order**, select the **Python (kepler)** kernel, and run each with **Kernel → Restart Kernel and Run All Cells**.

Notebook 01 downloads the data on first run and creates the train/test split, so it must run before 02 and 03. If the download fails, wait and rerun, or follow the manual steps in `data/README.md`.

## Project status

- [x] Milestone 1 – Proposal
- [x] Milestone 2 – Data audit, preprocessing and baseline
- [ ] Milestone 3 – Model comparison
- [ ] Milestone 4 – Final portfolio

## Limitations (summary)

- **Label bias:** the model learns from Kepler's own vetting decisions, so it inherits their habits.
- **Stellar-source provenance:** about 14% of training rows use older stellar catalogues and are almost all false positives, so stellar features may partly reveal the label. The effect will be measured in Milestone 3.
- **Excluded candidates:** CANDIDATE rows (the hardest, unresolved cases) are not in the evaluation, so real-world performance may be lower.
- **Generalisation:** results may not transfer to other missions (e.g. TESS) or to under-represented star types.

## Acknowledgements

This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.
