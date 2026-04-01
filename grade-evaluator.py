import csv
import sys
import os

EXPECTED_TOTAL_WEIGHT = 100.0
EXPECTED_FORMATIVE_WEIGHT = 60.0
EXPECTED_SUMMATIVE_WEIGHT = 40.0
PASS_MARK = 50.0
WEIGHT_TOLERANCE = 1e-6

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group': row['group'].strip().title(),
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def is_close(value, expected, tolerance=WEIGHT_TOLERANCE):
    return abs(value - expected) <= tolerance


def calculate_group_average(items):
    total_weight = sum(item['weight'] for item in items)
    if not items or is_close(total_weight, 0):
        return 0.0
    weighted_total = sum(item['score'] * item['weight'] for item in items)
    return weighted_total / total_weight


def get_grade_details(final_grade):
    if final_grade >= 90:
        return "A", 4.0
    if final_grade >= 80:
        return "B", 3.0
    if final_grade >= 70:
        return "C", 2.0
    if final_grade >= 60:
        return "D", 1.0
    return "F", 0.0

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    if not data:
        print("Error: No assignment data was found in the CSV file.")
        return
    
    # a) Check if all scores are percentage based (0-100)
    invalid_scores = [item for item in data if not (0 <= item['score'] <= 100)]
    if invalid_scores:
        print("Error: Some scores are not between 0 and 100.")
        for item in invalid_scores:
            print(f"  {item['assignment']}: {item['score']}")
        return

    invalid_weights = [item for item in data if item['weight'] < 0]
    if invalid_weights:
        print("Error: Assignment weights must be zero or greater.")
        for item in invalid_weights:
            print(f"  {item['assignment']}: {item['weight']}")
        return

    allowed_groups = {"Formative", "Summative"}
    invalid_groups = [item for item in data if item['group'] not in allowed_groups]
    if invalid_groups:
        print("Error: Some assignment groups are invalid. Use only Formative or Summative.")
        for item in invalid_groups:
            print(f"  {item['assignment']}: {item['group']}")
        return
    
    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    total_weight = sum(item['weight'] for item in data)
    if not is_close(total_weight, EXPECTED_TOTAL_WEIGHT):
        print(f"Error: Total weight is {total_weight:.2f}, should be {EXPECTED_TOTAL_WEIGHT:.0f}.")
        return
    
    formative = [item for item in data if item['group'] == 'Formative']
    summative = [item for item in data if item['group'] == 'Summative']
    
    formative_weight = sum(item['weight'] for item in formative)
    summative_weight = sum(item['weight'] for item in summative)
    
    if not is_close(formative_weight, EXPECTED_FORMATIVE_WEIGHT) or not is_close(summative_weight, EXPECTED_SUMMATIVE_WEIGHT):
        print(
            "Error: Category weights are incorrect. "
            f"Formative = {formative_weight:.2f} (should be {EXPECTED_FORMATIVE_WEIGHT:.0f}), "
            f"Summative = {summative_weight:.2f} (should be {EXPECTED_SUMMATIVE_WEIGHT:.0f})."
        )
        return
    
    # c) Calculate the Final Grade and GPA
    final_grade = sum(item['score'] * item['weight'] for item in data) / EXPECTED_TOTAL_WEIGHT
    
    letter, gpa = get_grade_details(final_grade)
    
    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_score = calculate_group_average(formative)
    summative_score = calculate_group_average(summative)
    
    pass_formative = formative_score >= PASS_MARK
    pass_summative = summative_score >= PASS_MARK
    passed = pass_formative and pass_summative
    
    # e) Check for failed formative assignments (< 50%)
    #     and determine which one(s) have the highest weight for resubmission.
    failed_formative = [item for item in formative if item['score'] < 50]
    if failed_formative:
        max_weight = max(item['weight'] for item in failed_formative)
        resubmission = [item for item in failed_formative if item['weight'] == max_weight]
    else:
        resubmission = []
    
    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print(f"Final Grade: {final_grade:.2f}%")
    print(f"Letter Grade: {letter}")
    print(f"GPA: {gpa:.1f}")
    print(f"Formative Score: {formative_score:.2f}%")
    print(f"Summative Score: {summative_score:.2f}%")
    print(f"Status: {'PASSED' if passed else 'FAILED'}")
    if not passed:
        if not pass_formative:
            print("Reason: Formative average is below 50%.")
        if not pass_summative:
            print("Reason: Summative average is below 50%.")
    if resubmission:
        print("Resubmission options:")
        for item in resubmission:
            print(f"  {item['assignment']} (weight: {item['weight']:.2f})")
    else:
        print("Resubmission options: None")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
