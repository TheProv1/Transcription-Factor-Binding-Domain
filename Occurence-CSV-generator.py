import os
import csv
import collections

JOBS = [
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "1.",
        "output_csv": "superclass_1_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "1.",
        "output_csv": "superclass_1_nonDBD_summary.csv"
    },
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "2.",
        "output_csv": "superclass_2_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "2.",
        "output_csv": "superclass_2_nonDBD_summary.csv"
    },
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "4.",
        "output_csv": "superclass_4_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "4.",
        "output_csv": "superclass_4_nonDBD_summary.csv"
    },
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "5.",
        "output_csv": "superclass_5_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "5.",
        "output_csv": "superclass_5_nonDBD_summary.csv"
    },
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "6.",
        "output_csv": "superclass_6_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "6.",
        "output_csv": "superclass_6_nonDBD_summary.csv"
    },
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "7.",
        "output_csv": "superclass_7_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "7.",
        "output_csv": "superclass_7_nonDBD_summary.csv"
    },
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "8.",
        "output_csv": "superclass_8_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "8.",
        "output_csv": "superclass_8_nonDBD_summary.csv"
    },
    {
        "input_dir": "DBD-region-Window-Output/3",
        "superclass_prefix": "9.",
        "output_csv": "superclass_9_DBD_summary.csv"
    },
    {
        "input_dir": "Non-DBD-Window-Output/3",
        "superclass_prefix": "9.",
        "output_csv": "superclass_9_nonDBD_summary.csv"
    }
]
MINIMUM_OCCURRENCE_COUNT: int = 3

def create_summary_csv(job_config: dict):
    input_dir = job_config["input_dir"]
    superclass_prefix = job_config["superclass_prefix"]
    output_csv = job_config["output_csv"]

    print(f"--- Starting job for: {output_csv} ---")

    if not os.path.isdir(input_dir):
        print(f"!!! ERROR: Input directory '{input_dir}' not found. Skipping job.")
        return

    all_frequent_triplets_header = set()
    all_file_data = {}
    
    target_files = [f for f in os.listdir(input_dir) if f.startswith(superclass_prefix) and f.endswith(".txt")]

    if not target_files:
        print("--- No matching files found for this job. Skipping.")
        return

    print(f"Pass 1: Analyzing {len(target_files)} files to find all frequent triplets...")

    for filename in target_files:
        filepath = os.path.join(input_dir, filename)
        current_file_counts = {}
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if " - " not in line or line.startswith(('#', '-', '=')):
                        continue
                    try:
                        parts = line.split(" - ")
                        triplet = parts[0].strip()
                        count = int(parts[1])
                        current_file_counts[triplet] = count
                        if count >= MINIMUM_OCCURRENCE_COUNT:
                            all_frequent_triplets_header.add(triplet)
                    except (ValueError, IndexError):
                        continue
            all_file_data[filename] = current_file_counts
        except Exception as e:
            print(f"!!! Warning: Could not process {filename}: {e}")

    if not all_frequent_triplets_header:
        print("--- No triplets with occurrences >= 3 found across all files. No CSV will be generated.")
        return

    print(f"Pass 2: Found {len(all_frequent_triplets_header)} unique frequent triplets for the header. Writing to {output_csv}...")
    
    header = ['transcription_factor'] + sorted(list(all_frequent_triplets_header))

    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for filename in sorted(all_file_data.keys()):
                row = [filename]
                file_counts = all_file_data[filename]

                for triplet_in_header in header[1:]:
                    count = file_counts.get(triplet_in_header, 0)
                    row.append(count)
                
                writer.writerow(row)
        print(f"--- Successfully created {output_csv} ---")

    except Exception as e:
        print(f"!!! ERROR: Could not write CSV file {output_csv}: {e}")

if __name__ == "__main__":
    
    for job in JOBS:
        create_summary_csv(job)
        print("-" * 50)

    print("\n\n" + "*" * 50)
    print("All summary CSV generation jobs are complete.")
    print("*" * 50)