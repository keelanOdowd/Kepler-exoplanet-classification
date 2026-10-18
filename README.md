# Real Planet or False Alarm? Classifying Kepler Exoplanet Candidates

CT4101 Machine Learning – Portfolio Project
Keelan O'Dowd (23440916), University of Galway

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

The data is **not stored in this repository**. It is downloaded automatically the first time the code runs. See [`data/README.md`](data/README.md) for the download link, access date, licence and citation.

## Key design decisions

- **Grouped split:** 938 stars host more than one KOI, so all splits are grouped by star (`kepid`) using `StratifiedGroupKFold`. This prevents the same star appearing in both training and test data.
- **Protected test set:** an 80/20 grouped, stratified split with `random_state=42`. Tuning uses 5-fold cross-validation on the training set only, and the test set is used once, at the end.
- **Leakage control:** NASA's vetting outputs (disposition flags, scores, comments) and columns that reflect follow-up observations are removed. Every dropped column and the reason for dropping it is documented in `notebooks/01_audit.ipynb`.
- **Preprocessing inside a pipeline:** imputation, signed log transform and scaling are fitted on training folds only, using scikit-learn `Pipeline` and `ColumnTransformer`.
- **Metrics:** PR-AUC and F1 are the primary metrics, because the classes are imbalanced. Precision, recall, ROC-AUC and confusion matrices are also reported.

## Repository structure

```
├── README.md
├── requirements.txt       # pinned package versions
├── .gitignore
├── data/
│   └── README.md          # dataset source, licence, download instructions
├── notebooks/
│   ├── 01_audit.ipynb     # data audit, leakage analysis, drop list
│   ├── 02_baseline.ipynb  # split design, pipeline, baseline models
│   ├── 03_models.ipynb    # model comparison and tuning
│   └── 04_final.ipynb     # final evaluation, error analysis, candidate scoring
├── src/                   # reusable code: data loading, feature lists, pipeline builder
├── tests/                 # pytest checks (e.g. no leaky columns in feature lists)
└── reports/
    └── figures/
```

## Setup

Requires **Python X.Y** (TODO: fill in from `python --version`).

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

1. Start JupyterLab: `jupyter lab`
2. Open the notebooks in `notebooks/` **in numbered order** and select the **Python (kepler)** kernel.
3. Run each notebook with **Kernel → Restart Kernel and Run All Cells**.

The first notebook downloads the dataset into `data/` if it is not already there.

To run the tests:

```bash
pytest
```

## Project status

- [x] Milestone 1 – Proposal
- [ ] Milestone 2 – Data audit and baseline
- [ ] Milestone 3 – Model comparison
- [ ] Milestone 4 – Final portfolio

## Limitations (summary)

- **Label bias:** the model learns from Kepler's own vetting decisions, so it inherits their habits.
- **Excluded candidates:** CANDIDATE rows (the hardest, unresolved cases) are not in the evaluation, so real-world performance may be lower.
- **Generalisation:** results may not transfer to other missions (e.g. TESS) or to under-represented star types.

## Acknowledgements and assistance declaration

This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

Use of generative AI and coding assistants is declared in `AI_DECLARATION.md` (TODO).