# KM-Wächter — Fleet Maintenance & Health Monitoring Service

A modernized, refactored maintenance scheduling and fleet-health reporting service for Vossberg Mobility's vehicle fleet. Originally completed as part of [The Legacy Fix](https://projectstudy.in/explore/experience-legacy-fix) guided project with IBM Bob.

> **Project Context:** Vossberg Mobility and KM-Wächter are fictional entities created for educational purposes.

---

## Overview

KM-Wächter processes vehicle telemetry data across a fleet of 6,000 vehicles to:
1. Determine real-time service eligibility and maintenance urgency based on dynamic mileage and time intervals.
2. Compile and export nightly fleet-health diagnostics reports.
3. Perform predictive, data-driven breakdown risk assessments using historical maintenance records.

---

## Status & Key Fixes

All legacy bugs have been identified, remediated, and verified against the acceptance test suite.

* **Core Maintenance Logic (`km_wachter.py`)**: Resolved edge-case interval calculations, boundary threshold comparisons, and status evaluation defects.
* **Reporting Engine (`fleet_report.py`)**: Fixed aggregate metrics computation, date formatting inconsistencies, and report export formatting.
* **Legacy Refactoring (`config_loader.py`, `fleet_utils.py`, `log_util.py`)**: Cleaned 2013-era legacy code, eliminated dead routines, and addressed silent runtime configuration pitfalls.
* **Risk Modeling (`analyze.py`)**: Implemented predictive breakdown-risk analysis over the 120-car labelled dataset (`fleet_history.csv`).
* **Test Suite & Verification**: All `pytest` unit tests are green, and acceptance verification via `verify.py` passes completely.

---

## Getting Started

### Prerequisites

Ensure Python 3 is installed, then install the required dependencies:

```bash
pip install pytest pandas
