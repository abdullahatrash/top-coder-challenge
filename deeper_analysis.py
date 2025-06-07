#!/usr/bin/env python3
import json
import statistics
from collections import defaultdict

def load_data():
    """Load the public cases data."""
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    return data

def test_simple_formula(data):
    """Test the simple formula against all data to see patterns in errors."""
    print("=== TESTING SIMPLE FORMULA: days * 120 + miles * 0.4 ===")

    errors = []
    large_errors = []

    for i, case in enumerate(data):
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        predicted = days * 120 + miles * 0.4
        error = abs(predicted - expected)
        errors.append(error)

        if error > 100:  # Large errors
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
    print(f"Cases with error > $100: {len(large_errors)} ({len(large_errors)/len(data)*100:.1f}%)")

    # Look at the large error cases
    print("\n=== LARGE ERROR CASES ===")
    large_errors.sort(key=lambda x: x['error'], reverse=True)
    for case in large_errors[:10]:
        print(f"Case {case['case_num']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.2f} → expected ${case['expected']:.2f}, got ${case['predicted']:.2f}, error ${case['error']:.2f}")

    return large_errors

def analyze_receipt_impact(data):
    """Analyze how receipts affect the calculation."""
    print("\n=== RECEIPT IMPACT ANALYSIS ===")

    # Group cases by similar days and miles, see how receipts affect outcome
    grouped = defaultdict(list)

    for case in data:
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        # Group by rounded days and miles
        key = (days, round(miles / 50) * 50)  # Round miles to nearest 50
        grouped[key].append({
            'receipts': receipts,
            'expected': expected,
            'base_formula': days * 120 + miles * 0.4
        })

    # Look for groups with multiple cases to see receipt impact
    for key, cases in grouped.items():
        if len(cases) >= 3:  # At least 3 cases
            days, miles_group = key
            cases.sort(key=lambda x: x['receipts'])

            print(f"\n{days} days, ~{miles_group} miles:")
            for case in cases[:5]:  # First 5 cases
                difference = case['expected'] - case['base_formula']
                print(f"  ${case['receipts']:7.2f} receipts → expected ${case['expected']:6.2f}, base ${case['base_formula']:6.2f}, diff ${difference:+6.2f}")

def analyze_high_receipt_cases(data):
    """Focus on cases with high receipts to see the pattern."""
    print("\n=== HIGH RECEIPT CASES ===")

    high_receipt_cases = []
    for case in data:
        inp = case['input']
        if inp['total_receipts_amount'] > 500:
            days = inp['trip_duration_days']
            miles = inp['miles_traveled']
            receipts = inp['total_receipts_amount']
            expected = case['expected_output']
            base_formula = days * 120 + miles * 0.4

            high_receipt_cases.append({
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'expected': expected,
                'base_formula': base_formula,
                'difference': expected - base_formula,
                'receipt_contribution': (expected - base_formula) / receipts if receipts > 0 else 0
            })

    high_receipt_cases.sort(key=lambda x: x['receipts'])

    print("High receipt cases (>$500):")
    for case in high_receipt_cases[:15]:
        print(f"  {case['days']}d, {case['miles']:3.0f}mi, ${case['receipts']:7.2f} → ${case['expected']:7.2f} (base: ${case['base_formula']:6.2f}, +${case['difference']:+6.2f}, ${case['receipt_contribution']:.3f}/receipt$)")

def find_receipt_patterns(data):
    """Try to find patterns in how receipts are processed."""
    print("\n=== RECEIPT PATTERN ANALYSIS ===")

    # Test various receipt formulas
    receipt_multipliers = []

    for case in data:
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        base_formula = days * 120 + miles * 0.4
        receipt_contribution = expected - base_formula

        if receipts > 0 and abs(receipt_contribution) < 1000:  # Filter extreme cases
            multiplier = receipt_contribution / receipts
            receipt_multipliers.append({
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'multiplier': multiplier
            })

    # Group by trip characteristics
    by_days = defaultdict(list)
    for case in receipt_multipliers:
        by_days[case['days']].append(case['multiplier'])

    print("Receipt multipliers by trip length:")
    for days in sorted(by_days.keys()):
        multipliers = by_days[days]
        if len(multipliers) > 5:
            avg_mult = statistics.mean(multipliers)
            median_mult = statistics.median(multipliers)
            print(f"  {days} days: avg {avg_mult:.3f}, median {median_mult:.3f} (from {len(multipliers)} cases)")

def main():
    data = load_data()

    large_errors = test_simple_formula(data)
    analyze_receipt_impact(data)
    analyze_high_receipt_cases(data)
    find_receipt_patterns(data)

if __name__ == "__main__":
    main()