#!/usr/bin/env python3
import json
import statistics
from collections import defaultdict

def load_data():
    """Load the public cases data."""
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    return data

def analyze_basic_patterns(data):
    """Analyze basic patterns in the data."""
    print("=== BASIC PATTERN ANALYSIS ===")

    # Extract data
    days = []
    miles = []
    receipts = []
    outputs = []

    for case in data:
        inp = case['input']
        days.append(inp['trip_duration_days'])
        miles.append(inp['miles_traveled'])
        receipts.append(inp['total_receipts_amount'])
        outputs.append(case['expected_output'])

    print(f"Total cases: {len(data)}")
    print(f"Days range: {min(days)} - {max(days)}")
    print(f"Miles range: {min(miles)} - {max(miles)}")
    print(f"Receipts range: ${min(receipts):.2f} - ${max(receipts):.2f}")
    print(f"Output range: ${min(outputs):.2f} - ${max(outputs):.2f}")
    print()

    return days, miles, receipts, outputs

def analyze_per_day_patterns(data):
    """Analyze patterns by trip length."""
    print("=== PER DAY ANALYSIS ===")

    by_days = defaultdict(list)

    for case in data:
        days = case['input']['trip_duration_days']
        output = case['expected_output']
        by_days[days].append(output)

    for days in sorted(by_days.keys()):
        outputs = by_days[days]
        avg_output = statistics.mean(outputs)
        avg_per_day = avg_output / days
        print(f"{days} days: {len(outputs)} cases, avg total ${avg_output:.2f}, avg per day ${avg_per_day:.2f}")

    print()

def analyze_mileage_patterns(data):
    """Analyze mileage-related patterns."""
    print("=== MILEAGE ANALYSIS ===")

    # Look at cases with similar days and receipts but different miles
    simple_cases = []
    for case in data:
        inp = case['input']
        if inp['total_receipts_amount'] < 50:  # Focus on low receipt cases
            simple_cases.append({
                'days': inp['trip_duration_days'],
                'miles': inp['miles_traveled'],
                'receipts': inp['total_receipts_amount'],
                'output': case['expected_output']
            })

    # Group by days
    by_days = defaultdict(list)
    for case in simple_cases:
        by_days[case['days']].append(case)

    for days in sorted(by_days.keys())[:5]:  # First 5 day lengths
        cases = by_days[days]
        if len(cases) > 5:
            cases.sort(key=lambda x: x['miles'])
            print(f"\n{days}-day trips (low receipts):")
            for case in cases[:10]:  # First 10 cases
                miles_contribution = case['output'] - (days * 100)  # Assume base $100/day
                per_mile = miles_contribution / case['miles'] if case['miles'] > 0 else 0
                print(f"  {case['miles']:3d} miles, ${case['receipts']:5.2f} receipts → ${case['output']:6.2f} (${per_mile:.3f}/mile estimate)")

def analyze_simple_cases(data):
    """Look at very simple cases to understand base logic."""
    print("\n=== SIMPLE CASES ANALYSIS ===")

    # Find cases with minimal receipts
    simple = []
    for case in data:
        inp = case['input']
        if inp['total_receipts_amount'] < 10 and inp['miles_traveled'] < 100:
            simple.append({
                'days': inp['trip_duration_days'],
                'miles': inp['miles_traveled'],
                'receipts': inp['total_receipts_amount'],
                'output': case['expected_output']
            })

    simple.sort(key=lambda x: (x['days'], x['miles']))

    print("Simple cases (receipts < $10, miles < 100):")
    for case in simple[:20]:
        base_estimate = case['days'] * 100 + case['miles'] * 0.5
        print(f"  {case['days']}d, {case['miles']:2d}mi, ${case['receipts']:4.2f} → ${case['output']:6.2f} (est: ${base_estimate:.2f})")

def find_exact_patterns(data):
    """Try to find exact mathematical relationships."""
    print("\n=== PATTERN SEARCH ===")

    # Test simple formulas
    close_matches = []

    for case in data[:100]:  # Test first 100 cases
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        # Test various formulas
        formulas = [
            ('days * 100 + miles * 0.58', days * 100 + miles * 0.58),
            ('days * 110 + miles * 0.5', days * 110 + miles * 0.5),
            ('days * 100 + miles * 0.6 + receipts * 0.5', days * 100 + miles * 0.6 + receipts * 0.5),
            ('days * 120 + miles * 0.4', days * 120 + miles * 0.4),
        ]

        for formula_name, result in formulas:
            error = abs(result - expected)
            if error < 20:  # Close match
                close_matches.append((formula_name, error, case))

    if close_matches:
        close_matches.sort(key=lambda x: x[1])
        print("Close matches found:")
        for formula, error, case in close_matches[:10]:
            print(f"  {formula}: error ${error:.2f} for case {case}")

def main():
    data = load_data()

    days, miles, receipts, outputs = analyze_basic_patterns(data)
    analyze_per_day_patterns(data)
    analyze_mileage_patterns(data)
    analyze_simple_cases(data)
    find_exact_patterns(data)

if __name__ == "__main__":
    main()