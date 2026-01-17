# Automated Data Pipeline (Terraform + LocalStack + Docker + GitHub Actions)

## Project Overview

This project demonstrates an **end-to-end automated data pipeline** using modern Data Engineering tools and best practices. The pipeline provisions cloud infrastructure using **Terraform**, simulates AWS services locally using **LocalStack**, processes data via a **Dockerized ETL job**, and is fully validated through **GitHub Actions CI**.

The goal of this project is to show how production-grade data pipelines can be built, tested, and validated automatically without relying on real cloud resources.

---

##  Architecture

**Workflow:**

1. GitHub Actions CI triggers on every push to `main`
2. LocalStack starts (AWS S3 emulation)
3. Terraform provisions an S3 bucket
4. Input CSV is uploaded to S3
5. Dockerized ETL job processes data
6. Output is written back to S3
7. CI verifies processed output

---

##  Tech Stack

* **Terraform** – Infrastructure as Code (IaC)
* **AWS S3 (LocalStack)** – Cloud service emulation
* **Docker** – Containerized ETL processing
* **Python** – ETL logic
* **GitHub Actions** – CI/CD automation
* **AWS CLI** – Resource interaction & validation

---

##  Project Structure

```
automated-data-pipeline/
│
├── .github/workflows/
│   └── ci.yml                # CI pipeline definition
│
├── terraform/
│   ├── main.tf               # S3 bucket resource
│   ├── provider.tf           # AWS provider (LocalStack)
│   ├── variables.tf          # Terraform variables
│   └── output.tf             # Terraform outputs
│
├── etl/
│   ├── etl.py                # ETL script
│   └── Dockerfile            # ETL Docker image
│
├── data/
│   └── raw/input.csv         # Input dataset
│
├── docker-compose.yml        # Local development stack
└── README.md
```

---

## ⚙️ Local Execution (Before CI)

### 1️ Start LocalStack

```bash
docker-compose up -d localstack
```

Verify LocalStack:

```bash
curl http://localhost:4566/_localstack/health
```

---

### 2️ Run Terraform

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

---

### 3️ Upload Input Data

```bash
aws --endpoint-url=http://localhost:4566 s3 cp data/raw/input.csv \
  s3://localstack-etl-bucket/raw/input.csv
```

---

### 4️ Run ETL Job

```bash
docker build -t etl-job ./etl

docker run --rm \
  --network host \
  -e AWS_ACCESS_KEY_ID=test \
  -e AWS_SECRET_ACCESS_KEY=test \
  -e AWS_DEFAULT_REGION=us-east-1 \
  -e AWS_ENDPOINT_URL=http://localhost:4566 \
  -e S3_BUCKET_NAME=localstack-etl-bucket \
  etl-job
```

---

### 5️ Verify Output

```bash
aws --endpoint-url=http://localhost:4566 s3 ls \
  s3://localstack-etl-bucket/processed/
```

Expected output:

```
output.csv
```

---

##  CI/CD Pipeline

* Triggered on every push to `main`
* Runs the **full pipeline automatically**
* Fails if:

  * Terraform provisioning fails
  * ETL job fails
  * Output is missing in S3

This ensures **reproducibility, reliability, and correctness**.

---

##  Key Learnings

* Infrastructure as Code with Terraform
* Cloud service emulation using LocalStack
* Docker networking in CI environments
* Debugging CI/CD failures
* Safe Git practices (ignoring provider binaries)

---

## 📈 Future Improvements

* Add data validation tests
* Add CI status badge
* Add CloudWatch / logging simulation
* Parameterize environments (dev/prod)

---

## 👤 Author

**Dhamini Kathula**


 If you found this project useful, feel free to star the repository!
