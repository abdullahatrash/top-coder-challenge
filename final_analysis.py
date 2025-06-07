#!/usr/bin/env python3
import json
import statistics
from collections import defaultdict

def load_data():
    """Load the public cases data."""
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    return data

def current_formula(trip_duration_days, miles_traveled, total_receipts_amount):
    """Current implementation formula."""
    base_reimbursement = trip_duration_days * 120 + miles_traveled * 0.4

    # Receipt multipliers (median values)
    multipliers = {
        1: 0.518, 2: 0.496, 3: 0.375, 4: 0.403, 5: 0.391,
        6: 0.382, 7: 0.324, 8: 0.222, 9: 0.149, 10: 0.101,
        11: 0.088, 12: 0.039, 13: -0.007, 14: -0.060
    }

    receipt_multiplier = multipliers.get(trip_duration_days, -0.1)
    receipt_contribution = total_receipts_amount * receipt_multiplier

    return base_reimbursement + receipt_contribution

def analyze_current_errors(data):
    """Analyze errors with the current implementation."""
    print("=== CURRENT IMPLEMENTATION ERROR ANALYSIS ===")

    errors = []
    large_errors = []

    for i, case in enumerate(data):
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        predicted = current_formula(days, miles, receipts)
        error = abs(predicted - expected)
        errors.append(error)

        if error > 200:  # Large errors
            large_errors.append({
                'case_num': i,
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'expected': expected,
                'predicted': predicted,
                'error': error
            })

    print(f"Average error: ${statistics.mean(errors):.2f}")
    print(f"Median error: ${statistics.median(errors):.2f}")
    print(f"Cases with error > $200: {len(large_errors)} ({len(large_errors)/len(data)*100:.1f}%)")

    # Look at the largest error cases
    print("\n=== LARGEST ERROR CASES ===")
    large_errors.sort(key=lambda x: x['error'], reverse=True)
    for case in large_errors[:15]:
        print(f"Case {case['case_num']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.2f} → expected ${case['expected']:.2f}, got ${case['predicted']:.2f}, error ${case['error']:.2f}")

    return large_errors

def analyze_mileage_nonlinearity(data):
    """Look for non-linear mileage patterns."""
    print("\n=== MILEAGE NON-LINEARITY ANALYSIS ===")

    # Group by days and low receipts to isolate mileage effects
    by_days = defaultdict(list)

    for case in data:
        inp = case['input']
        if inp['total_receipts_amount'] < 100:  # Low receipt cases
            days = inp['trip_duration_days']
            miles = inp['miles_traveled']
            expected = case['expected_output']
            predicted = current_formula(days, miles, inp['total_receipts_amount'])

            by_days[days].append({
                'miles': miles,
                'expected': expected,
                'predicted': predicted,
                'error': abs(expected - predicted),
                'miles_per_day': miles / days if days > 0 else 0
            })

    # Look for patterns in mileage errors
    for days in sorted(by_days.keys())[:6]:  # First 6 day lengths
        cases = by_days[days]
        if len(cases) > 5:
            cases.sort(key=lambda x: x['miles'])
            print(f"\n{days}-day trips (low receipts):")

            # Check if there are patterns in high-mileage vs low-mileage
            high_mileage = [c for c in cases if c['miles'] > 300]
            low_mileage = [c for c in cases if c['miles'] < 100]

            if high_mileage and low_mileage:
                avg_error_high = statistics.mean([c['error'] for c in high_mileage])
                avg_error_low = statistics.mean([c['error'] for c in low_mileage])
                print(f"  High mileage (>300mi) avg error: ${avg_error_high:.2f}")
                print(f"  Low mileage (<100mi) avg error: ${avg_error_low:.2f}")

                # Show some examples
                for case in high_mileage[:3]:
                    print(f"    {case['miles']}mi → expected ${case['expected']:.2f}, got ${case['predicted']:.2f}, error ${case['error']:.2f}")

def find_additional_patterns(data):
    """Look for other patterns that might improve accuracy."""
    print("\n=== SEARCHING FOR ADDITIONAL PATTERNS ===")

    # Look at cases with very low errors to see what they have in common
    accurate_cases = []

    for i, case in enumerate(data):
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        predicted = current_formula(days, miles, receipts)
        error = abs(predicted - expected)

        if error < 10:  # Very accurate cases
            accurate_cases.append({
                'case_num': i,
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'expected': expected,
                'predicted': predicted,
                'error': error,
                'miles_per_day': miles / days if days > 0 else 0,
                'receipts_per_day': receipts / days if days > 0 else receipts
            })

    print(f"Found {len(accurate_cases)} cases with error < $10")

    if accurate_cases:
        # Look for patterns in accurate cases
        print("\nMost accurate cases:")
        accurate_cases.sort(key=lambda x: x['error'])
        for case in accurate_cases[:10]:
            print(f"  {case['days']}d, {case['miles']}mi, ${case['receipts']:.2f} → ${case['expected']:.2f} (error: ${case['error']:.2f})")

def main():
    data = load_data()

    large_errors = analyze_current_errors(data)
    analyze_mileage_nonlinearity(data)
    find_additional_patterns(data)

if __name__ == "__main__":
    main()