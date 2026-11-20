import os

# Define file names
INPUT_FILE = 'learners.txt'
CLEAN_FILE = 'clean.txt'
ERROR_FILE = 'errors.log'
REPORT_FILE = 'report.txt'

def validate_record(line):
    """
    Validates a single line of data.
    Expected format: student number, name, mark1;mark2;mark3
    Returns a dictionary of valid data, or an error message string.
    """
    parts = line.strip().split(',')
    
    # Check if there are exactly 3 parts (ID, Name, Marks)
    if len(parts) != 3:
        return "Invalid format: Expected 'ID, Name, Marks'"
    
    student_id = parts[0].strip()
    name = parts[1].strip()
    marks_str = parts[2].strip()
    
    # Validate Student ID (ensure it's not empty)
    if not student_id:
        return "Invalid ID: Student number is missing."
    
    # Validate Marks format (must be separated by semicolons)
    marks_list = marks_str.split(';')
    if len(marks_list) != 3:
        return f"Invalid marks format for ID {student_id}: Expected 3 marks separated by ';'."
    
    # Validate each mark (must be a number between 0 and 100)
    valid_marks = []
    for mark in marks_list:
        try:
            mark_val = float(mark)
            if mark_val < 0 or mark_val > 100:
                return f"Invalid mark for ID {student_id}: Marks must be between 0 and 100."
            valid_marks.append(mark_val)
        except ValueError:
            return f"Invalid mark for ID {student_id}: '{mark}' is not a number."
            
    return {
        'id': student_id,
        'name': name,
        'marks': valid_marks,
        'raw_line': line.strip()
    }

def calculate_average(marks):
    """Calculates average using a basic loop (as requested in Step 5)."""
    total = 0
    count = 0
    for mark in marks:
        total += mark
        count += 1
    return total / count if count > 0 else 0

def manual_sort(students):
    """
    Sorts the list of students manually (Step 6).
    Using Bubble Sort to sort by average in descending order.
    """
    n = len(students)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Sort descending (highest average first)
            if students[j]['average'] < students[j+1]['average']:
                # Swap positions
                students[j], students[j+1] = students[j+1], students[j]
    return students

def main():
    valid_students = []
    error_logs = []
    
    # Step 1 & 2: Open file and Read lines
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please create it first.")
        return

    with open(INPUT_FILE, 'r') as file:
        lines = file.readlines()

    # Step 3 & 4: Strip, split, and Validate
    for line in lines:
        if not line.strip(): # Skip empty lines
            continue
            
        result = validate_record(line)
        
        if isinstance(result, dict):
            # Step 5: Calculate averages using loops
            result['average'] = calculate_average(result['marks'])
            valid_students.append(result)
        else:
            # It's an error message
            error_logs.append(f"Line: {line.strip()} | Error: {result}")

    # Step 6: Sort manually
    sorted_students = manual_sort(valid_students)

    # Step 7: Write report, clean file, and error log
    
    # 1. Write Error Log
    with open(ERROR_FILE, 'w') as err_file:
        if error_logs:
            for err in error_logs:
                err_file.write(err + '\n')
        else:
            err_file.write("No errors found.\n")

    # 2. Write Clean File (Just the valid raw lines)
    with open(CLEAN_FILE, 'w') as clean_file:
        for student in valid_students:
            clean_file.write(student['raw_line'] + '\n')

    # 3. Write Report File (Formatted with ranks)
    with open(REPORT_FILE, 'w') as rep_file:
        rep_file.write("="*50 + "\n")
        rep_file.write("           STUDENT RESULTS REPORT\n")
        rep_file.write("="*50 + "\n")
        rep_file.write(f"{'Rank':<6} | {'ID':<10} | {'Name':<20} | {'Average':<8}\n")
        rep_file.write("-" * 50 + "\n")
        
        rank = 1
        for student in sorted_students:
            rep_file.write(f"{rank:<6} | {student['id']:<10} | {student['name']:<20} | {student['average']:.2f}\n")
            rank += 1
            
    print("Processing complete! Check 'report.txt', 'clean.txt', and 'errors.log'.")

if __name__ == "__main__":
    main()