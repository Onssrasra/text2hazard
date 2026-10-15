# Text2Data

Final notebooks and required data for the TU Berlin project **Artificial Intelligence in Human-Water Systems**.

Research question:

> Does task decomposition improve hazard-information extraction compared with a single end-to-end LLM prompt?

Workflow A performs one end-to-end extraction per chunk. Workflow B uses four calls per chunk for hazard events, locations, times, and impacts. Both use the same documents, chunks, schema, model settings, and deterministic document-level merge.

## Contents

```text
notebooks/
    01_data_exploration.ipynb
    02_data_preparation.ipynb
    03_llm_extraction.ipynb
    04_evaluation.ipynb
    05_results_and_error_analysis.ipynb

src/
    extraction_schema.py
    llm_client.py
    workflows.py

data/
    text2data_document_metadata.xlsx
    prepared_documents.csv
    evaluation/
        manifest.json
        selection.json
        manual_annotations.csv
        documents/
    final_results/
        experiment_summary.csv
        workflow_a/
        workflow_b/

outputs/
    unsupported_evidence_cases.csv
```

`data/evaluation/manual_annotations.csv` is the manually created reference annotation file. The model never receives this file. The nine cleaned Markdown inputs are stored in `data/evaluation/documents/`, and the frozen extraction outputs used by Notebooks 04 and 05 are stored in `data/final_results/`.

`data/text2data_document_metadata.xlsx` is the manually reviewed metadata workbook used by Notebooks 01 and 02. It contains the document source types and language information used in the data exploration and preparation steps.

## Setup

Python 3.12 or later is recommended:

```powershell
python -m pip install -e .
```

Notebook 03 requires an NVIDIA token only when making new API calls. Copy `.env.example` to `.env` and insert the token locally. Never upload the real `.env` file. `RUN_LLM=False` is the default, so the frozen experiment is not rerun automatically.

Notebooks 01 and 02 use the included metadata workbook together with the original course archive. The archive is expected at `data/text_2_data.zip`, but at approximately 407 MB it exceeds GitHub's normal single-file limit and is not included. The dataset is available from the [TU Berlin cloud](https://tubcloud.tu-berlin.de/s/b22diMygiPR8Xpd?dir=/text_2_data). The final executed notebooks, prepared CSV, nine evaluation texts, annotations, and frozen results are included.


