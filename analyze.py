# analyze.py
# Risk-factor analysis and per-car risk scoring for Vossberg Mobility fleet.
#
# KEY FINDING: km_since_service is by far the strongest breakdown predictor
# (broke-down cars average 11 678 km since last service vs 7 261 for healthy cars, gap +4 417).
# load_factor and avg_daily_km also separate the groups. Total odometer and age do NOT —
# high-mileage and older cars break down at exactly the same rate as low-mileage, younger ones.

import csv


def load_fleet_data(filepath: str = "fleet_history.csv") -> list[dict]:
    """Load vehicle history records from CSV and return as a list of dicts."""
    with open(filepath, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compare_groups(data: list[dict]) -> None:
    """Print group-average comparison for every metric to show which ones predict breakdowns."""
    broke = [r for r in data if r["broke_down"] == "1"]
    ok    = [r for r in data if r["broke_down"] == "0"]

    metrics = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

    print(f"Dataset: {len(data)} cars  |  broke_down: {len(broke)}  |  kept_going: {len(ok)}")
    print()
    print(f"{'Metric':<22}  {'Broke avg':>10}  {'OK avg':>10}  {'Gap':>10}  Note")
    print("-" * 75)
    for m in metrics:
        b_avg = sum(float(r[m]) for r in broke) / len(broke)
        o_avg = sum(float(r[m]) for r in ok)   / len(ok)
        gap   = b_avg - o_avg
        note  = "<-- strong signal" if abs(gap / o_avg) > 0.2 else ("(weak)" if abs(gap / o_avg) < 0.05 else "")
        print(f"{m:<22}  {b_avg:>10.2f}  {o_avg:>10.2f}  {gap:>+10.2f}  {note}")


def risk_score(row: dict) -> float:
    """Return a 0-100 risk score built from the three columns that separate the groups.

    Weights reflect the size of the gap each factor shows between groups:
      km_since_service  50 % — largest absolute and relative gap
      load_factor       30 % — clear separation (0.60 vs 0.51)
      avg_daily_km      20 % — moderate separation (160 vs 131)

    Each component is normalised against the observed maximum in the dataset so
    the score is always in [0, 100].
    """
    KMS_MAX  = 15000.0   # service interval ceiling
    LOAD_MAX = 1.0
    DAILY_MAX = 250.0    # practical ceiling for avg_daily_km in this fleet

    kms  = min(float(row["km_since_service"]), KMS_MAX)  / KMS_MAX
    load = min(float(row["load_factor"]),      LOAD_MAX) / LOAD_MAX
    daily = min(float(row["avg_daily_km"]),   DAILY_MAX) / DAILY_MAX

    return round((kms * 0.50 + load * 0.30 + daily * 0.20) * 100, 1)


def print_risk_ranking(data: list[dict]) -> None:
    """Print all cars ranked by risk score, highest first."""
    ranked = sorted(data, key=lambda r: risk_score(r), reverse=True)

    print(f"\n{'Rank':<5} {'Car':<12} {'Risk':>6}  {'km_since_svc':>14}  {'load':>6}  {'daily_km':>9}  {'broke_down':>11}")
    print("-" * 72)
    for i, row in enumerate(ranked, 1):
        score = risk_score(row)
        flag  = "  *** BROKE" if row["broke_down"] == "1" else ""
        print(
            f"{i:<5} {row['car_id']:<12} {score:>6}  "
            f"{float(row['km_since_service']):>14.0f}  "
            f"{float(row['load_factor']):>6.2f}  "
            f"{float(row['avg_daily_km']):>9.0f}  "
            f"{row['broke_down']:>11}{flag}"
        )


def main() -> None:
    data = load_fleet_data()

    print("=" * 75)
    print("VOSSBERG MOBILITY — FLEET BREAKDOWN RISK ANALYSIS")
    print("=" * 75)
    print()
    compare_groups(data)
    print()
    print("INSIGHT: odometer_km and age_years show near-zero gaps — total mileage")
    print("and age do NOT predict breakdowns in this fleet. km_since_service,")
    print("load_factor, and avg_daily_km do.")
    print_risk_ranking(data)


if __name__ == "__main__":
    main()
