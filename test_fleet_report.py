# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_survives_missing_last_service_km():
    # A car with no 'last_service_km' must not crash fleet_summary.
    # VOS-7788 has never had a reading; it should be treated as just-serviced (0 % wear).
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},           # no last_service_km
    ]
    result = fleet_summary(fleet)
    assert "average_wear" in result                      # did not crash
    assert result["due"] == 1                            # only VOS-4471 is flagged
    # VOS-7788 contributes 0 % wear; average = (99.33 + 0) / 2 ≈ 49.67
    assert abs(result["average_wear"] - 49.67) < 1.5
