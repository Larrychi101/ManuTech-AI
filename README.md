# ManuTech-AI

This repository contains an Azure Developer CLI project for deploying a minimal Azure-based application.

## Deployment

The project includes:

- `azure.yaml` — Azure Developer CLI environment configuration
- `infra/main.bicep` — minimal Bicep template that deploys an Azure Storage account

## Local setup

1. Create a virtual environment and activate it:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies as needed.

## GitHub

This repository is licensed under the Apache License 2.0.

## Notes

- Do not commit `.env` or `.azure/`.
- The repo already ignores `.venv/`, `.env`, `.env.lock`, and `.azure/`.
