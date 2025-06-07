#!/usr/bin/env python3
import sys
import math

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Reverse-engineered reimbursement calculation based on data analysis.
    Base formula: days * 120 + miles * 0.4
    With improvements for extreme cases
    """

    # Base formula that matches many cases closely
    base_reimbursement = trip_duration_days * 120 + miles_traveled * 0.4

    # Handle extreme mileage cases - very high miles per day get reduced rate
    miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else miles_traveled
    if miles_per_day > 600:  # Extreme cases
        excess_miles = miles_traveled - (600 * trip_duration_days)
        base_reimbursement -= excess_miles * 0.2  # Reduce excessive mileage bonus

    # Receipt processing with median values and caps
    multipliers = {
        1: 0.518, 2: 0.496, 3: 0.375, 4: 0.403, 5: 0.391,
        6: 0.382, 7: 0.324, 8: 0.222, 9: 0.149, 10: 0.101,
        11: 0.088, 12: 0.039, 13: -0.007, 14: -0.060
    }

    receipt_multiplier = multipliers.get(trip_duration_days, -0.1)

    # Cap receipt contributions for extreme amounts
    capped_receipts = total_receipts_amount
    if total_receipts_amount > 1500:
        # Diminishing returns for very high receipts
        excess = total_receipts_amount - 1500
        capped_receipts = 1500 + excess * 0.3

    receipt_contribution = capped_receipts * receipt_multiplier

    total_reimbursement = base_reimbursement + receipt_contribution

    # Special adjustments for problematic long trips
    if trip_duration_days >= 13 and total_receipts_amount < 500:
        # Long trips with low receipts seem to have different behavior
        total_reimbursement *= 0.85

    # Round to 2 decimal places
    return round(total_reimbursement, 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <trip_duration_days> <miles_traveled> <total_receipts_amount>")
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