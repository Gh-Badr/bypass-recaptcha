import re

def calculate_accuracy():
    # Initialize counters
    true_positives = 0
    true_negatives = 0
    total_choices = 0

    # Function to parse a line using regex
    def parse_csv_line(line):
        pattern = r'(.*?),(.*\[.*\]),(\d+)'
        match = re.match(pattern, line)
        if match:
            return match.groups()
        else:
            return None, None, None

    def parse_list(list_str, is_response=False):
        list_str = list_str.strip("[]")
        if is_response:
            # Handle response format
            return set(int(x.strip().strip("'\"")) for x in list_str.split(',')) if list_str else set()
        else:
            # Handle correct answer format
            return set(map(int, list_str.split(','))) if list_str else set()

    # Open and process the files
    with open('reordered_human_responses.csv', mode='r') as file1, open('reordered_responses.csv', mode='r') as file2:
        for line1, line2 in zip(file1, file2):
            _, list_str1, size_str1 = parse_csv_line(line1.strip())
            _, list_str2, size_str2 = parse_csv_line(line2.strip())

            # Verify that both lines are parsed correctly
            if None in (list_str1, size_str1, list_str2, size_str2):
                continue

            # Convert size to integer
            size = int(size_str1)

            # Process only if size is 3
            if size == 4:
                total_choices += 9  # Total choices for size 3

                # Parse lists
                correct_answers = parse_list(list_str1)
                student_responses = parse_list(list_str2, is_response=True)

                # Count True Positives and True Negatives
                true_positives += len(correct_answers.intersection(student_responses))
                all_choices = set(range(1, 10))
                true_negatives += len(all_choices - (correct_answers.union(student_responses)))

    # Calculate accuracy
    accuracy = (true_positives + true_negatives) / total_choices if total_choices > 0 else 0
    return accuracy

# Print the calculated accuracy
print(f"Accuracy: {int(calculate_accuracy()*100)}%")