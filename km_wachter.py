# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Cleaned up and bugs fixed.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return how many percent of the service interval have been used up.

    Uses floating-point division so values below one full interval are
    non-zero (e.g. 14 900 of 15 000 km → 99.3 %, not 0 %).
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when the car has used at least WARN_AT_PERCENT of its interval.

    If the car has no 'last_service_km' reading the odometer value itself is
    used as the baseline, meaning the car is treated as just-serviced and will
    NOT be incorrectly flagged.
    """
    last = car.get("last_service_km", car["odometer"])
    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car whose wear is at or above the warning threshold."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
