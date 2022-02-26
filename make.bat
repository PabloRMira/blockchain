@echo off

if "%1" == "setup-dev-py" (
    echo "[INFO] Creating conda environment bc-dev" ^
    && conda create -n bc-dev python ^
    && echo "[INFO] Installing dependencies" ^
    && pip install -r requirements.txt ^
    && pip install -r requirements-dev.txt
) else (
    echo No option %1 available
)
