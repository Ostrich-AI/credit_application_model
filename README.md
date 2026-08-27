## Ostrich Model Inference (Docker)

This project is a small, opinionated layout for running **user-provided machine learning models** inside a **Docker container**.  
Users provide a model, dataset, inference script, and `requirements.txt`. The Docker image then runs inference and writes predictions to `output/output.csv`.

---

### Folder & Filename Contract

Everything is relative to the project root:

- **`model/`**
  - **`model.<ext>`** – required. Base name must be `model`. Extension must be one of:
    - `.pt`, `.pth`, `.h5`, `.onnx`, `.pkl`, `.pb`, `.joblib`, `.json`, `.params`, `.safetensors`, `.bin`
- **`dataset/`**
  - **`input.csv`** – required. The input dataset for inference. No other files are allowed in this folder.
- **`scripts/`**
  - **`inference.py`** – required. User-provided inference entrypoint.
  - **`setup.sh`** – optional. Shell script executed inside the container **before** `inference.py` (e.g. extra system setup).
- **`output/`**
  - **`output.csv`** – output file produced by the inference run. This file may or may not exist before a run; if it exists, it will be overwritten.
- **Project root**
  - **`requirements.txt`** – required. All Python dependencies needed by the user’s inference code.
  - **`Dockerfile`** – required in the Docker-only flow. Defines how to build the image that will run inference.

If any of these rules are violated (missing folders/files, extra files, wrong names, or unsupported model extensions), the orchestration code will fail fast with a clear error message.

---

### Upload Fields → Folder Mapping

When using the UI with four upload fields, the files are mapped into the project like this:

- **Model Artifacts**
  - Upload your serialized model file here.
  - The system will place it into the `model/` folder as **`model.<ext>`**.
  - Supported extensions: `.pt`, `.pth`, `.h5`, `.onnx`, `.pkl`, `.pb`, `.joblib`, `.json`, `.params`, `.safetensors`, `.bin`.

- **Inference Script**
  - Upload the Python file that implements inference.
  - This file **must be named** `inference.py`.
  - It will be placed at **`scripts/inference.py`** inside the project.

- **Startup Script** (optional)
  - Upload a shell script (`.sh`) with any extra setup commands (e.g. OS packages, downloads).
  - This file will be placed at **`scripts/setup.sh`**.
  - At container runtime, the Docker image will:
    - `chmod +x scripts/setup.sh`
    - Execute it **before** running `scripts/inference.py`.

- **Additional files**
  - Upload a **`.zip`** containing extra project files.
  - This archive **must contain a file named exactly `requirements.txt` at its root**, listing all Python dependencies.
  - It may also include:
    - `dataset/input.csv`
    - `Dockerfile`
    - Any other supporting files needed by your inference code.
  - After extraction, the overall layout must match the folder contract described above.

---

### Inference Contract (`scripts/inference.py`)

The user-supplied `scripts/inference.py` must follow this contract:

- **Input**:
  - **Reads feature-only data** from `dataset/input.csv` (or accepts a `--data` flag that defaults to that path).
  - The input file **must not** contain `target` or `prediction` columns.
- **Model**:
  - **Loads the model** from `model/model.<ext>` (or accepts a `--model` flag that defaults to `model/model.<ext>`).
- **Output**:
  - **Writes predictions** to `output/output.csv` (or accepts an `--output` flag that defaults to that path).
  - The output file **must contain exactly one column** named `target`, holding all predicted values.

The reference implementation in `scripts/inference.py`:

- **Uses** `pandas` to load the input CSV.
- **Validates** that no `target` or `prediction` columns exist in the input.
- **Runs** `model.predict(features)` on all rows.
- **Writes** a new CSV with a single `target` column of predictions.

You can replace this file with your own logic, as long as you respect the same I/O locations, filenames, and the input/output column contract described above.

---

### Quickstart: Build and Run with Docker Only

From the project root:

- **Build the image**

```bash
docker build -t inferenceupload:latest .
```

- **Run inference and persist outputs to the host**

```bash
docker run --rm \
  -v "$PWD/output":/app/output \
  inferenceupload:latest
```

- **What this does**
  - **Build**: Uses the provided `Dockerfile` which:
    - Installs dependencies from `requirements.txt`.
    - Copies the entire project (`model/`, `dataset/`, `scripts/`, etc.) into `/app`.
    - Ensures `output/` exists inside the image.
    - Sets a default `CMD` that:
      - Runs `scripts/setup.sh` if present.
      - Then runs `scripts/inference.py`.
  - **Run**:
    - `-v "$PWD/output":/app/output` binds your local `output/` folder into the container.
    - When the container writes `/app/output/output.csv`, you will see it as `output/output.csv` on the host.

After a successful run you should see predictions in `output/output.csv` on your machine.

---

### Optional: Using `prepare_iris_example.py`

For local testing, this repo includes `prepare_iris_example.py`, which can bootstrap a working Iris example:

1. **Creates directories**: `model/`, `dataset/`, `scripts/`, and `output/` if they do not exist.
2. **Builds a dataset**: loads the Iris dataset from `sklearn.datasets`, saves it as `dataset/input.csv` (features only).
3. **Trains a model**: trains a simple `RandomForestClassifier` and saves it as `model/model.pkl`.
4. **Prepares inference**: writes a minimal `scripts/inference.py` **only if one does not already exist**.

You can then:

```bash
python prepare_iris_example.py
docker build -t inferenceupload:latest .
docker run --rm -v "$PWD/output":/app/output inferenceupload:latest
```

You should see predictions in `output/output.csv` after the container finishes.

---

### Tests: Model Format Notebooks (`tests/`)

For manual validation of all supported model extensions, this repo includes a set of Jupyter notebooks under `tests/`:

- Each subfolder corresponds to one extension:
  - `tests/pt/`, `tests/pth/`, `tests/h5/`, `tests/onnx/`, `tests/pkl/`, `tests/pb/`, `tests/joblib/`, `tests/json/`, `tests/params/`, `tests/safetensors/`, `tests/bin/`.
- Inside each folder you will find:
  - `test_<ext>.ipynb` – notebook with **Train** and **Inference** sections.
  - Expected paths:
    - Input: `input/input.csv`
    - Model: `model/model.<ext>`
    - Output: `output/output.csv`
- The notebooks:
  - Train a small scikit-learn classifier on `input/input.csv`.
  - Save the model to `model/model.<ext>` (using pickle/joblib, content is the same model with different extension names).
  - Reload it and run inference, writing predictions to `output/output.csv` with a single `target` column, mirroring `scripts/inference.py`.

To use them:

1. Place or copy your test CSV to the appropriate `tests/<ext>/input/input.csv`.
2. Open `tests/<ext>/test_<ext>.ipynb` in Jupyter.
3. Run all cells; inspect `tests/<ext>/output/output.csv` for the predictions.

---

### Notes & Integration Tips

- **Backend integration**
  - **Prepare a working directory** using the folder contract above.
  - **Write user uploads** into that directory:
    - Place `model.<ext>` into `model/` as `model.<ext>`.
    - Place `input.csv` into `dataset/` as `input.csv`.
    - Place the inference script into `scripts/inference.py`.
    - Optionally place extra setup commands into `scripts/setup.sh`.
    - Provide `requirements.txt` and a `Dockerfile`.
  - **Build and run** the Docker image:
    - `docker build -t <some-tag> .`
    - `docker run --rm -v "<absolute-output-path>":/app/output <some-tag>`
  - **Read back** `output/output.csv` from the bound output directory and return it to the caller.

- **Lifecycle**
  - This project does **not** delete any user-provided files or outputs.
  - Containers are run with `--rm` in the examples so they are removed automatically after completion.

