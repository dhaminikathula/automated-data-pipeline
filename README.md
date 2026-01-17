# Automated Data Pipeline with Terraform, Docker & LocalStack

## Overview
-> This project demonstrates a fully automated data pipeline using Infrastructure as Code, containerized ETL, and CI/CD.
-> For CI reliability, a schema-accurate sample of the NYC TLC dataset is used instead of the full monthly file.

## Architecture
Terraform provisions an S3 bucket in LocalStack.
A Dockerized Python ETL reads raw data, transforms it, and writes processed output.
GitHub Actions automates the entire workflow.

## Local Setup
```bash
docker compose up
