import os
import csv

BASE_FOLDER: str = "DBD_Split"
IU_COLUMN_INDEX: int = 2

def calculate_disorder_ratio(filepath: str) -> float:
    total_anchor_residues = 0
    disordered_residues = 0

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()[1:] 

            for line in lines:
                parts = line.split()
                if len(parts) <= IU_COLUMN_INDEX:
                    continue 

                total_anchor_residues += 1
                
                try:
                    iu_score = float(parts[IU_COLUMN_INDEX])
                    if iu_score > 0.5:
                        disordered_residues += 1
                except ValueError:
                    continue
        
        if total_anchor_residues == 0:
            return -1.0
        
        return disordered_residues / total_anchor_residues

    except Exception as e:
        print(f"!!! Could not read or process file {filepath}: {e}")
        return -1.0

if __name__ == "__main__":
    
    threshold_percentage = -1
    while True:
        try:
            user_input = input("Enter the disorder percentage threshold: ")
            threshold_percentage = float(user_input)
            if 0 <= threshold_percentage <= 100:
                break
            else:
                print("Error: Please enter a number between 0 and 100.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

    threshold_ratio = threshold_percentage / 100.0
    print("-" * 50)
    print(f"Searching for ANCHOR regions with disorder >= {threshold_percentage}%\n")

    found_files_with_ratios = []
    if not os.path.isdir(BASE_FOLDER):
        print(f"Error: The input directory '{BASE_FOLDER}' was not found.")
        print("Please ensure the script is in the same directory as your 'DBD_Split' folder.")
    else:
        for dirpath, _, filenames in os.walk(BASE_FOLDER):
            for filename in filenames:
                if filename.endswith(".txt"):
                    full_filepath = os.path.join(dirpath, filename)
                    
                    ratio = calculate_disorder_ratio(full_filepath)

                    if ratio >= threshold_ratio:
                        found_files_with_ratios.append((full_filepath, ratio))

    if found_files_with_ratios:
        sorted_files = sorted(found_files_with_ratios)
        
        print(f"Found {len(sorted_files)} files matching the criteria:")
        for f_path, ratio in sorted_files:
            print(f_path)
            
        csv_filename = f"DBD_disorder_above_{int(threshold_percentage)}.csv"
        print(f"\nSaving the results to '{csv_filename}'...")
        
        try:
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['filename', 'disorder_percentage'])
                for f_path, ratio in sorted_files:
                    filename_only = os.path.basename(f_path)
                    percentage = ratio * 100.0
                    writer.writerow([filename_only, f"{percentage:.2f}"])
            print("Successfully saved the CSV file.")
        except Exception as e:
            print(f"!!! Error writing CSV file: {e}")

    else:
        print("No files were found that meet the specified disorder threshold.")