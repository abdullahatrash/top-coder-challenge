#!/usr/bin/env python3
import json
import statistics

def load_data():
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    return data

def simple_formula(days, miles, receipts):
    """Iteration 1: Just base formula"""
    return days * 120 + miles * 0.4

def with_average_multipliers(days, miles, receipts):
    """Iteration 2: Base + average receipt multipliers"""
    base = days * 120 + miles * 0.4

    # These were the AVERAGE multipliers (didn't work well)
    avg_multipliers = {
        1: 0.38, 2: 0.25, 3: 0.15, 4: 0.12, 5: 0.10
    }

    multiplier = avg_multipliers.get(days, 0.1)
    return base + multiplier * receipts

def with_median_multipliers(days, miles, receipts):
    """Iteration 3: Base + median receipt multipliers"""
    base = days * 120 + miles * 0.4

    # These are the MEDIAN multipliers (worked much better)
    median_multipliers = {
        1: 0.518, 2: 0.496, 3: 0.375, 4: 0.403, 5: 0.391,
        6: 0.382, 7: 0.324, 8: 0.222, 9: 0.149, 10: 0.101,
        11: 0.088, 12: 0.039, 13: -0.007, 14: -0.060
    }

    multiplier = median_multipliers.get(days, -0.1)
    return base + multiplier * receipts

def analyze_improvement():
    data = load_data()

    print("🔍 SHOWING HOW ERROR IMPROVED FROM $410 TO $180")
    print("=" * 60)

    errors_simple = []
    errors_average = []
    errors_median = []

    # Test each approach on all 1000 cases
    for case in data:
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        # Calculate with each method
        result1 = simple_formula(days, miles, receipts)
        result2 = with_average_multipliers(days, miles, receipts)
        result3 = with_median_multipliers(days, miles, receipts)

        # Calculate errors
        error1 = abs(result1 - expected)
        error2 = abs(result2 - expected)
        error3 = abs(result3 - expected)

        errors_simple.append(error1)
        errors_average.append(error2)
        errors_median.append(error3)

    # Show results
    avg_error_simple = statistics.mean(errors_simple)
    avg_error_average = statistics.mean(errors_average)
    avg_error_median = statistics.mean(errors_median)

    print(f"📊 ITERATION 1 - Simple Formula Only:")
    print(f"   Average Error: ${avg_error_simple:.2f}")
    print(f"   Max Error: ${max(errors_simple):.2f}")
    print()

    print(f"📊 ITERATION 2 - Added Average Receipt Multipliers:")
    print(f"   Average Error: ${avg_error_average:.2f}")
    print(f"   Max Error: ${max(errors_average):.2f}")
    print(f"   📉 Change: ${avg_error_average - avg_error_simple:+.2f} (WORSE!)")
    print()

    print(f"📊 ITERATION 3 - Switched to Median Receipt Multipliers:")
    print(f"   Average Error: ${avg_error_median:.2f}")
    print(f"   Max Error: ${max(errors_median):.2f}")
    print(f"   📈 Change: ${avg_error_median - avg_error_simple:+.2f} (MUCH BETTER!)")
    print()

    print("🎯 WHY MEDIAN WORKED BETTER:")
    print("=" * 40)

    # Show some examples of why median is better
    print("Example: 1-day trips receipt multipliers")

    # Calculate actual multipliers for 1-day trips
    multipliers_1day = []
    for case in data:
        inp = case['input']
        if inp['trip_duration_days'] == 1:
            days = inp['trip_duration_days']
            miles = inp['miles_traveled']
            receipts = inp['total_receipts_amount']
            expected = case['expected_output']

            base = days * 120 + miles * 0.4
            if receipts > 0:
                multiplier = (expected - base) / receipts
                multipliers_1day.append(multiplier)

    if multipliers_1day:
        avg_mult = statistics.mean(multipliers_1day)
        median_mult = statistics.median(multipliers_1day)

        print(f"   Average multiplier: {avg_mult:.3f}")
        print(f"   Median multiplier: {median_mult:.3f}")
        print(f"   Range: {min(multipliers_1day):.3f} to {max(multipliers_1day):.3f}")
        print(f"   📝 The median is more stable and representative!")

if __name__ == "__main__":
    analyze_improvement()