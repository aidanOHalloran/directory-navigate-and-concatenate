import os
import chardet

def list_file_types(directory):
    """List all file types in a directory and its subdirectories."""
    file_types = set()
    for root, _, files in os.walk(directory):
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension:
                file_types.add(file_extension)
    return list(file_types)

def user_select(options, prompt):
    """Allow the user to select options from a list."""
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    selected_options = []
    print("\nEnter the numbers of your selections (comma-separated): ")
    selected_indices = input().split(',')

    for index in selected_indices:
        try:
            selected_options.append(options[int(index) - 1])
        except (ValueError, IndexError):
            print(f"Invalid selection: {index}")

    return selected_options

def read_file_with_encoding(file_path):
    """Read a file with the detected encoding."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"Could not read file {file_path} with detected encoding: {e}")
        # Fallback to reading the file with 'utf-8' and ignoring errors
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

def combine_files(input_directory, selected_file_types, output_file):
    """Combine the content of selected file types into one output file."""
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(input_directory):
            for file in files:
                if os.path.splitext(file)[1] in selected_file_types:
                    file_path = os.path.join(root, file)
                    try:
                        file_content = read_file_with_encoding(file_path)
                        outfile.write(f"--- {file} ---\n")
                        outfile.write(file_content)
                        outfile.write("\n")  # Add a newline between files
                    except Exception as e:
                        print(f"Could not read file {file_path}: {e}")
    print(f"Combined file saved as {output_file}")

def main():
    input_directory = input("Enter the full project directory: ").strip('\"')

    # Determine the script's directory and set the output directory to 'OutputFiles'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(script_dir, 'OutputFiles')

    # Ensure the 'OutputFiles' directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_types = list_file_types(input_directory)

    selected_file_types = user_select(file_types, "Select file types to include:")

    if selected_file_types:
        output_file = os.path.join(output_directory, "combined.txt")
        combine_files(input_directory, selected_file_types, output_file)
    else:
        print("No file types selected.")

if __name__ == "__main__":
    main()
