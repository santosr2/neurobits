---
title: "Airflow Community Chart"
date: 2025-05-24
summary: "The standard Helm chart for deploying Apache Airflow on Kubernetes."
description: "Production-ready Airflow deployments on Kubernetes. Originally created in 2017, now the community standard."
status: "maintained"
tags:
  - kubernetes
  - helm
  - airflow
github: "https://github.com/santosr2/airflow-community-chart"
stack:
  - Helm
  - Kubernetes
weight: 4
draft: false
---

The Airflow Community Helm Chart is the standard way to deploy Apache Airflow on Kubernetes.

## Features

- **Production-ready** — Battle-tested by thousands of companies
- **Flexible** — Executor options (Celery, Kubernetes, Local)
- **Observable** — Built-in metrics and logging configuration
- **Secure** — RBAC, secrets management, network policies

## Quick Start

```bash
helm repo add airflow https://santosr2.github.io/airflow-community-chart
helm install airflow airflow/airflow
```

Fork maintained with custom patches and improvements.
