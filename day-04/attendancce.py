import json
import os

# Define file names
INPUT_FILE = 'attendance.json'
REPORT_FILE = 'attendance_report.txt'
ERROR_FILE = 'invalid_records.log'

def validate_record(record, index):
    """
    Validates a single attendance record.
    Returns a dictionary of valid data, or an error message string.
    Expected JSON structure per record:
    {
        "ID": "string",
        "name": "string",
        "sessions": {"total": int, "attended": int},
        "late_submissions": int
    }
    """
    try:
        # Check if required keys exist
        if not all(k in record for k in ["ID", "name", "sessions", "late_submissions"]):
            return f"Record {index + 1}: Missing one or more required fields (ID, name, sessions, late_submissions)."
        
        # Extract data
        student_id = str(record["ID"]).strip()
        name = str(record["name"]).strip()
        late_submissions = int(record["late_submissions"])
        
        # Check nested sessions dictionary
        if "total" not in record["sessions"] or "attended" not in record["sessions"]:
            return f"Record {index + 1} (ID: {student_id}): 'sessions' must contain 'total' and 'attended'."
            
        total_sessions = int(record["sessions"]["total"])
        attended_sessions = int(record["sessions"]["attended"])

        # Logic Validation
        if total_sessions <= 0:
            return f"Record {index + 1} (ID: {student_id}): Total sessions must be greater than 0."
        if attended_sessions < 0 or attended_sessions > total_sessions:
            return f"Record {index + 1} (ID: {student_id}): Attended sessions must be between 0 and total sessions."
        if late_submissions < 0:
            return f"Record {index + 1} (ID: {student_id}): Late submissions cannot be negative."
        if not student_id or not name:
            return f"Record {index + 1}: ID and Name cannot be empty."

        # If all validation passes, return clean data
        return {
            "id": student_id,
            "name": name,
            "total": total_sessions,
            "attended": attended_sessions,
            "late": late_submissions
        }
        
    except ValueError:
        return f"Record {index + 1}: Data type error. Sessions and late submissions must be integers."
    except Exception as e:
        return f"Record {index + 1}: Unexpected error - {str(e)}"


def determine_risk(percentage, late_submissions):
    """
    Applies risk rules based on attendance percentage and late submissions.
    (Note: These specific thresholds are assumed based on common academic rules).
    """
    if percentage < 50.0 or late_submissions >= 5:
        return "High Risk"
    elif percentage < 75.0 or late_submissions >= 3:
        return "Medium Risk"
    else:
        return "Low Risk"

def main():
    # Step 1: Load JSON
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please create it first.")
        return

    try:
        with open(INPUT_FILE, 'r') as file:
            data = json.load(file) # Step 2: Read records
    except json.JSONDecodeError:
        print(f"Error: {INPUT_FILE} contains invalid JSON formatting.")
        return

    if not isinstance(data, list):
        print("Error: JSON file should contain a list (array) of records.")
        return

    valid_students = []
    error_logs = []
    
    # Dictionary to count risk groups (Step 6)
    risk_counts = {
        "High Risk": 0,
        "Medium Risk": 0,
        "Low Risk": 0
    }

    # Iterate through records
    for index, record in enumerate(data):
        # Step 3: Validate attendance
        result = validate_record(record, index)
        
        if isinstance(result, dict):
            # Step 4: Calculate attendance percentage
            # Formula: (attended / total) * 100
            percentage = (result["attended"] / result["total"]) * 100
            
            # Step 5: Apply risk rules
            risk_level = determine_risk(percentage, result["late"])
            
            # Add to our valid list
            result["percentage"] = percentage
            result["risk_level"] = risk_level
            valid_students.append(result)
            
            # Step 6: Count risk groups
            risk_counts[risk_level] += 1
        else:
            # Log invalid record
            error_logs.append(result)

    # Step 7: Save report
    
    # 1. Write Invalid Records Log
    with open(ERROR_FILE, 'w') as err_file:
        if error_logs:
            for err in error_logs:
                err_file.write(err + '\n')
        else:
            err_file.write("No invalid records found.\n")

    # 2. Write Attendance Report
    with open(REPORT_FILE, 'w') as rep_file:
        rep_file.write("="*65 + "\n")
        rep_file.write("                STUDENT ATTENDANCE RISK REPORT\n")
        rep_file.write("="*65 + "\n\n")
        
        rep_file.write("--- RISK GROUP SUMMARY ---\n")
        rep_file.write(f"High Risk Students   : {risk_counts['High Risk']}\n")
        rep_file.write(f"Medium Risk Students : {risk_counts['Medium Risk']}\n")
        rep_file.write(f"Low Risk Students    : {risk_counts['Low Risk']}\n")
        rep_file.write(f"Total Valid Records  : {len(valid_students)}\n")
        rep_file.write(f"Total Invalid Records: {len(error_logs)}\n\n")
        
        rep_file.write("--- STUDENTS REQUIRING SUPPORT (High Risk) ---\n")
        rep_file.write(f"{'ID':<10} | {'Name':<20} | {'Attended':<10} | {'Late':<5} | {'Percentage'}\n")
        rep_file.write("-" * 65 + "\n")
        
        # Filter and sort high risk students by lowest percentage
        high_risk_students = [s for s in valid_students if s['risk_level'] == "High Risk"]
        high_risk_students.sort(key=lambda x: x['percentage'])
        
        if high_risk_students:
            for student in high_risk_students:
                rep_file.write(f"{student['id']:<10} | {student['name']:<20} | {student['attended']}/{student['total']:<7} | {student['late']:<5} | {student['percentage']:.2f}%\n")
        else:
            rep_file.write("No high-risk students found. Excellent!\n")

    print("Processing complete!")
    print(f"-> Check '{REPORT_FILE}' for the summary and risk groups.")
    print(f"-> Check '{ERROR_FILE}' for any data validation errors.")

if __name__ == "__main__":
    main()