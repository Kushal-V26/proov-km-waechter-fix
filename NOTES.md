# Modernization & Acceptance Notes

## 1. What the agent got wrong that I caught
* The legacy codebase in `km_wachter.py` used integer floor division (`//`), which truncated fractional wear below 1 to 0% (such as 14,900 km / 15,000 km yielding 0% instead of ~99.3%). This masked almost every impending maintenance alert.
* I strictly verified that the core baseline parameters remained untouched: `SERVICE_INTERVAL_KM = 15000` and `WARN_AT_PERCENT = 80` in both code logic and `settings.cfg`.
* I ensured vehicles missing the `last_service_km` key default safely against their current odometer value to prevent crash exceptions or false warnings during fleet report generation.
* Replaced outdated `%` formatting with modern f-strings, added explicit type annotations and docstrings, and removed verbose `== True` comparisons and dead branches.

## 2. How I convinced myself the wear bug is fixed
* I inspected the calculation logic in `wear_percent` to confirm float division (`/`) produces accurate decimal ratios for edge cases (e.g. 12,000 km and 14,900 km against 15,000 km).
* Confirmed the 80% boundary logic flags vehicles at or above 80% wear while leaving those under 80% untouched.
* Ran the entire test suite using `pytest -v` to ensure all existing and newly added regression tests passed without errors.
* Executed `verify.py` locally to confirm all programmatic checks evaluate to PASS.

## 3. What the data actually said
* Total lifetime mileage (`odometer_km` ~53.4k km) and vehicle age (`age_years` ~5.9 years) are virtually identical between breakdown and non-breakdown cohorts, demonstrating that older or higher-mileage cars do not fail at higher rates.
* Breakdown risk is strongly predicted by accumulated distance since the last service (`km_since_service` showed the largest gap at +4,417 km), followed by high daily intensity (`avg_daily_km`) and higher cargo utilization (`load_factor`).