#!/usr/bin/env python3
"""
Improved Travel Reimbursement Calculator
Based on analysis of employee interviews and data patterns

Key Insights Incorporated:
1. Lisa: Base per diem ~$100/day, 5-day trips get bonuses, mileage is tiered
2. Kevin: Efficiency bonuses for 180-220 miles/day, receipt multipliers vary by trip length
3. Marcus: System remembers history, end of quarter variations, "magic numbers"
4. Lisa: Rounding bug for receipts ending in 49¢/99¢
5. Jennifer: Sweet spot around 4-6 days for trip length
"""

import sys
import math

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Refined reimbursement calculation based on systematic analysis.
    Building on the working base formula with targeted improvements.
    """

    # === REFINED BASE FORMULA ===
    # Start with the working base that showed ~$80 average error
    # But refine based on patterns observed in the data
    base_reimbursement = trip_duration_days * 115 + miles_traveled * 0.42

    # === ADVANCED MILEAGE ADJUSTMENTS ===
    # Lisa mentioned mileage drops off for longer trips - implement tiers
    if miles_traveled > 800:
        # Very high mileage trips get reduced rate on excess
        excess_miles = miles_traveled - 800
        base_reimbursement -= excess_miles * 0.15
    elif miles_traveled > 400:
        # High mileage trips get slight reduction
        excess_miles = miles_traveled - 400
        base_reimbursement -= excess_miles * 0.05

    # === REFINED RECEIPT PROCESSING ===
    # Use the proven median multipliers but with refinements
    multipliers = {
        1: 0.520, 2: 0.500, 3: 0.380, 4: 0.410, 5: 0.395,
        6: 0.385, 7: 0.330, 8: 0.225, 9: 0.150, 10: 0.105,
        11: 0.090, 12: 0.040, 13: -0.005, 14: -0.055
    }

    receipt_multiplier = multipliers.get(trip_duration_days, -0.08)

    # Improved receipt processing for extreme amounts
    if total_receipts_amount > 2000:
        # Very high receipts: cap the effect
        capped_receipts = 2000 + (total_receipts_amount - 2000) * 0.2
        receipt_contribution = capped_receipts * receipt_multiplier
    elif total_receipts_amount > 1000:
        # High receipts: diminishing returns
        base_receipts = 1000 * receipt_multiplier
        excess_receipts = (total_receipts_amount - 1000) * receipt_multiplier * 0.6
        receipt_contribution = base_receipts + excess_receipts
    else:
        # Normal receipt processing
        receipt_contribution = total_receipts_amount * receipt_multiplier

    # === SPECIAL CASE ADJUSTMENTS ===

    # Kevin's efficiency bonus (refined and smaller)
    efficiency_bonus = 0
    if trip_duration_days > 0:
        miles_per_day = miles_traveled / trip_duration_days
        if 200 <= miles_per_day <= 300:
            # Sweet spot for efficiency
            efficiency_bonus = min(trip_duration_days * 8, 40)  # Max $40 bonus

    # Lisa's 5-day bonus (refined)
    if trip_duration_days == 5:
        efficiency_bonus += 20  # Additional bonus for 5-day trips

    # Marcus's quarterly adjustment (simulate with random factor based on trip characteristics)
    quarter_adjustment = 0
    if trip_duration_days >= 3:
        # Simulate end-of-quarter generosity based on trip characteristics
        trip_hash = (trip_duration_days * 17 + int(miles_traveled * 13) + int(total_receipts_amount * 7)) % 100
        if trip_hash < 15:  # ~15% of trips get quarterly bonus
            quarter_adjustment = trip_duration_days * 5

    # === ROUNDING BUG IMPLEMENTATION ===
    # Lisa: receipts ending in 49¢ or 99¢ get extra money
    cents = int((total_receipts_amount * 100) % 100)
    rounding_bonus = 0
    if cents == 49:
        rounding_bonus = 8  # Small bonus for 49¢
    elif cents == 99:
        rounding_bonus = 12  # Slightly larger for 99¢

    # === FINAL CALCULATION ===
    total_reimbursement = (base_reimbursement +
                          receipt_contribution +
                          efficiency_bonus +
                          quarter_adjustment +
                          rounding_bonus)

    # Minimum reimbursement floor
    min_reimbursement = trip_duration_days * 85
    if total_reimbursement < min_reimbursement:
        total_reimbursement = min_reimbursement

    # Round to 2 decimal places
    return round(total_reimbursement, 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 improved_reimbursement.py <trip_duration_days> <miles_traveled> <total_receipts_amount>")
        sys.exit(1)

    try:
        trip_duration_days = int(sys.argv[1])
        miles_traveled = float(sys.argv[2])
        total_receipts_amount = float(sys.argv[3])

        result = calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount)
        print(result)

    except ValueError as e:
        print(f"Error: Invalid input format - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()