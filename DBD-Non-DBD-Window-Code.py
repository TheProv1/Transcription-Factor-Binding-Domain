import os
import collections

JOBS = [
    {
        "input_dir": "DBD-Region",
        "output_dir": "DBD-region-Window-Output"
    },
    {
        "input_dir": "Non-DBD-Region",
        "output_dir": "Non-DBD-Window-Output"
    }
]
AMINO_ACID_COLUMN_INDEX: int = 1

def count_pattern_occurrences(sequence: str, window_size: int) -> collections.Counter:
    if not sequence or len(sequence) < window_size:
        return collections.Counter()
    pattern_counts = collections.Counter()
    for i in range(len(sequence) - window_size + 1):
        pattern = sequence[i : i + window_size]
        pattern_counts[pattern] += 1
    return pattern_counts

def extract_sequence_from_split_file(filepath: str) -> str:
    """Extracts the amino acid sequence from the new 4-column files."""
    sequence_list = []
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                parts = line.split()
                if len(parts) > AMINO_ACID_COLUMN_INDEX:
                    sequence_list.append(parts[AMINO_ACID_COLUMN_INDEX])
    except Exception as e:
        print(f"!!! Error reading sequence from {filepath}: {e}")
    return "".join(sequence_list)

def perform_window_analysis_on_directory(input_dir: str, output_root: str):
    """
    Main function to run the full sliding window analysis on a given directory.
    """
    if not os.path.isdir(input_dir):
        print(f"Warning: Input directory '{input_dir}' not found. Skipping this job.")
        return

    os.makedirs(output_root, exist_ok=True)
    
    for window_size in range(3, 12):
        print("\n" + "#" * 70)
        print(f"###   WINDOW SIZE = {window_size} for '{input_dir}'   ###")
        print("#" * 70 + "\n")

        for filename in os.listdir(input_dir):
            if filename.endswith(".txt"):
                full_filepath = os.path.join(input_dir, filename)
                print(f"--- Analyzing: {filename} ---")
                
                sequence_str = extract_sequence_from_split_file(full_filepath)
                if not sequence_str:
                    continue
                
                total_occurrences = count_pattern_occurrences(sequence_str, window_size)
                
                output_dir_ws = os.path.join(output_root, str(window_size))
                os.makedirs(output_dir_ws, exist_ok=True)
                
                base_name, _ = os.path.splitext(filename)
                output_filename = f"{base_name}_WS{window_size}.txt"
                full_output_path = os.path.join(output_dir_ws, output_filename)

                with open(full_output_path, 'w') as out_file:
                    out_file.write(f"--- Analysis for: {filename} ---\n")
                    out_file.write(f"Window Size: {window_size}\n")
                    out_file.write("=" * 50 + "\n\n")
                    out_file.write(f"Sequence: {sequence_str}\n\n")
                    out_file.write("Output (Sliding Window Step - Total Count of that Pattern):\n")
                    
                    if len(sequence_str) >= window_size:
                        for i in range(len(sequence_str) - window_size + 1):
                            pattern = sequence_str[i : i + window_size]
                            count = total_occurrences[pattern]
                            out_file.write(f"  {pattern} - {count}\n")
                    else:
                        out_file.write(f"  (Sequence too short for window size {window_size})\n")

if __name__ == "__main__":
    
    for job in JOBS:
        print("\n" + "="*80)
        print(f"STARTING JOB FOR INPUT DIRECTORY: '{job['input_dir']}'")
        print("="*80)
        perform_window_analysis_on_directory(job['input_dir'], job['output_dir'])
        print(f"\nJOB FOR '{job['input_dir']}' COMPLETE.")

    print("\n\n" + "*" * 50)
    print("All sliding window analyses are complete.")
    print("*" * 50)