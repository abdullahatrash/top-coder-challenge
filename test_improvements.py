#!/usr/bin/env python3
import json
import statistics
import subprocess

def load_data():
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    return data

def test_original_solution(days, miles, receipts):
    """Test with our proven calculate_reimbursement.py"""
    result = subprocess.run(['python3', 'calculate_reimbursement.py', str(days), str(miles), str(receipts)],
                           capture_output=True, text=True)
    if result.returncode == 0:
        return float(result.stdout.strip())
    return None

def test_improved_solution(days, miles, receipts):
    """Test with the new improved_reimbursement.py"""
    result = subprocess.run(['python3', 'improved_reimbursement.py', str(days), str(miles), str(receipts)],
                           capture_output=True, text=True)
    if result.returncode == 0:
        return float(result.stdout.strip())
    return None

def compare_solutions():
    data = load_data()

    print("🆚 COMPARING ORIGINAL vs IMPROVED SOLUTION")
    print("=" * 60)

    original_errors = []
    improved_errors = []
    improvements = 0
    degradations = 0

    sample_comparisons = []

    for i, case in enumerate(data):
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        expected = case['expected_output']

        # Test both solutions
        original_result = test_original_solution(days, miles, receipts)
        improved_result = test_improved_solution(days, miles, receipts)

        if original_result is None or improved_result is None:
            continue

        original_error = abs(original_result - expected)
        improved_error = abs(improved_result - expected)

        original_errors.append(original_error)
        improved_errors.append(improved_error)

        # Track improvements vs degradations
        if improved_error < original_error:
            improvements += 1
        elif improved_error > original_error:
            degradations += 1

        # Collect some sample comparisons
        if len(sample_comparisons) < 10 and abs(improved_error - original_error) > 5:
            sample_comparisons.append({
                'case': i,
                'input': f"{days}d, {miles}mi, ${receipts}",
                'expected': expected,
                'original': original_result,
                'improved': improved_result,
                'original_error': original_error,
                'improved_error': improved_error,
                'change': improved_error - original_error
            })

    # Calculate statistics
    original_avg = statistics.mean(original_errors)
    improved_avg = statistics.mean(improved_errors)

    original_max = max(original_errors)
    improved_max = max(improved_errors)

    print(f"📊 ORIGINAL SOLUTION:")
    print(f"   Average Error: ${original_avg:.2f}")
    print(f"   Max Error: ${original_max:.2f}")
    print(f"   Cases tested: {len(original_errors)}")
    print()

    print(f"📊 IMPROVED SOLUTION:")
    print(f"   Average Error: ${improved_avg:.2f}")
    print(f"   Max Error: ${improved_max:.2f}")
    print(f"   Cases tested: {len(improved_errors)}")
    print()

    change = improved_avg - original_avg
    if change < 0:
        print(f"🎯 IMPROVEMENT: ${abs(change):.2f} better average error!")
    else:
        print(f"📉 REGRESSION: ${change:.2f} worse average error")

    print(f"📈 Individual case results:")
    print(f"   Improvements: {improvements}")
    print(f"   Degradations: {degradations}")
    print(f"   No change: {len(original_errors) - improvements - degradations}")

    if sample_comparisons:
        print(f"\n🔍 SAMPLE COMPARISONS (largest differences):")
        print("-" * 80)
        for comp in sample_comparisons[:5]:
            change_str = f"{comp['change']:+.2f}"
            print(f"Case {comp['case']}: {comp['input']}")
            print(f"  Expected: ${comp['expected']:.2f}")
            print(f"  Original: ${comp['original']:.2f} (error: ${comp['original_error']:.2f})")
            print(f"  Improved: ${comp['improved']:.2f} (error: ${comp['improved_error']:.2f}) [{change_str}]")
            print()

if __name__ == "__main__":
    compare_solutions()