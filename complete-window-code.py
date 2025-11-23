import os
import collections

BASE_FOLDER: str = "/mnt/d/NR_HI_IU" 
OUTPUT_BASE_DIR: str = "output"

def count_pattern_occurrences(sequence: str, window_size: int) -> collections.Counter:
    if not sequence or len(sequence) < window_size:
        return collections.Counter()
    pattern_counts = collections.Counter()
    for i in range(len(sequence) - window_size + 1):
        pattern = sequence[i : i + window_size]
        pattern_counts[pattern] += 1
    return pattern_counts

def analyze_transcription_factors_in_file(filepath: str, window_size: int, output_root: str):
    base_name, _ = os.path.splitext(os.path.basename(filepath))
    output_directory = os.path.join(output_root, str(window_size), base_name)
    os.makedirs(output_directory, exist_ok=True)

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        all_residues = []
        for line in lines:
            if line.strip().lower().startswith('pos'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    pos = int(parts[0])
                    res = parts[1]
                    all_residues.append((pos, res))
                except (ValueError, IndexError):
                    continue
        
        if not all_residues:
            return

        factor_start_indices = [0]
        for i in range(1, len(all_residues)):
            current_pos = all_residues[i][0]
            previous_pos = all_residues[i-1][0]
            if current_pos < previous_pos:
                factor_start_indices.append(i)

        for i in range(len(factor_start_indices)):
            factor_num = i + 1
            
            start_index = factor_start_indices[i]
            end_index = factor_start_indices[i+1] if i + 1 < len(factor_start_indices) else len(all_residues)
            
            factor_residue_chunk = all_residues[start_index:end_index]
            
            sequence_list = [res_tuple[1] for res_tuple in factor_residue_chunk]
            if not sequence_list: continue

            output_filename_simple = f"{base_name}_TF_{factor_num}_WS{window_size}.txt"
            full_output_path = os.path.join(output_directory, output_filename_simple)
            sequence_str = "".join(sequence_list)
            total_occurrences = count_pattern_occurrences(sequence_str, window_size)
            
            with open(full_output_path, 'w') as out_file:
                out_file.write(f"--- Analysis for Transcription Factor #{factor_num} ---\n")
                out_file.write(f"Source File: {filepath}\n")
                out_file.write(f"Window Size: {window_size}\n")
                out_file.write("=" * 50 + "\n\n")
                out_file.write(f"Transcription factor: {sequence_str}\n\n")
                out_file.write("Output (Unique Patterns and their Total Counts):\n")
                if len(sequence_str) >= window_size:
                    for pattern, count in sorted(total_occurrences.items()):
                        out_file.write(f"  {pattern} - {count}\n")
                else:
                    out_file.write(f"  (Sequence too short for window size {window_size})\n")

    except Exception as e:
        print(f"!!! An error occurred while processing the file {filepath}: {e}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    print(f"All analysis output will be saved in the '{OUTPUT_BASE_DIR}' directory.")
    for window_size in range(3, 12):
        print("\n" + "#" * 70)
        print(f"###   STARTING ANALYSIS FOR ALL FILES WITH WINDOW SIZE = {window_size}   ###")
        print("#" * 70 + "\n")
        for dirpath, _, filenames in os.walk(BASE_FOLDER):
            for filename in filenames:
                if filename.endswith(".txt"):
                    full_filepath = os.path.join(dirpath, filename)
                    print(f"--- Processing file: {full_filepath} ---")
                    analyze_transcription_factors_in_file(full_filepath, window_size, OUTPUT_BASE_DIR)
    print("\n\n" + "*" * 70)
    print("All analyses for all window sizes are complete.")
    print("*" * 70)