setup-dev:
    echo "[INFO] Creating conda environment bc-dev"
    conda create -n bc-dev python
    echo "[INFO] Installing dependencies"
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
