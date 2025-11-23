import os
import collections

# --- IMPORTANT: SET THIS TO THE FULL PATH OF THE FILE YOU WANT TO ANALYZE ---
TARGET_FILE_PATH: str = "/mnt/d/NR_HI_IU/1/1.1/1.1.1/1.1.1.1.txt"
# -----------------------------------------------------------------------------

# --- CONFIGURATION: SET THE WINDOW SIZE FOR THE ANALYSIS ---
# Change this integer value to 3, 4, 5, etc., as required by your professor.
WINDOW_SIZE: int = 3
# -----------------------------------------------------------------------------

def count_pattern_occurrences(sequence: str, window_size: int) -> collections.Counter:
    """
    Counts the total occurrences of every unique pattern (k-mer) in the
    entire sequence for a given window size.
    """
    if not sequence or len(sequence) < window_size:
        return collections.Counter()

    pattern_counts = collections.Counter()
    
    for i in range(len(sequence) - window_size + 1):
        pattern = sequence[i : i + window_size]
        pattern_counts[pattern] += 1
        
    return pattern_counts

def analyze_transcription_factors_in_file(filepath: str, window_size: int):
    """
    Reads a file, identifies each separate transcription factor, and saves the
    step-by-step sliding window analysis into an organized directory structure.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'")
        return

    print(f"Analyzing all transcription factors in file: {filepath}")
    print(f"Using a fixed WINDOW SIZE of: {window_size}\n")
    
    # Get the base name of the input file (e.g., "1.1.1.1")
    base_name, _ = os.path.splitext(os.path.basename(filepath))
    
    # --- Create the directory structure: base_name/window_size/ ---
    output_directory = os.path.join(base_name, str(window_size))
    os.makedirs(output_directory, exist_ok=True)
    print(f"Output will be saved in: '{output_directory}/'\n")

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()[1:]  # Skip header
            
            factor_counter = 1
            last_pos_hi, last_pos_iu = 0, 0
            current_sequence_list = []

            # This helper function processes a completed sequence and saves it to a file
            def process_sequence(factor_num, sequence_list):
                if not sequence_list: return
                
                # Create the simple filename
                output_filename_simple = f"{base_name}_TF_{factor_num}_WS{window_size}.txt"
                # Create the full path including the new directory structure
                full_output_path = os.path.join(output_directory, output_filename_simple)

                print(f"Processing Transcription Factor #{factor_num}... Saving results to '{full_output_path}'")

                sequence_str = "".join(sequence_list)
                total_occurrences = count_pattern_occurrences(sequence_str, window_size)
                
                # Write the analysis to the designated file
                with open(full_output_path, 'w') as out_file:
                    out_file.write(f"--- Analysis for Transcription Factor #{factor_num} ---\n")
                    out_file.write(f"Source File: {filepath}\n")
                    out_file.write(f"Window Size: {window_size}\n")
                    out_file.write("=" * 50 + "\n\n")
                    
                    out_file.write(f"Transcription factor: {sequence_str}\n\n")
                    out_file.write("Output:\n")
                    
                    if len(sequence_str) >= window_size:
                        for i in range(len(sequence_str) - window_size + 1):
                            pattern = sequence_str[i : i + window_size]
                            count = total_occurrences[pattern]
                            out_file.write(f"  {pattern} - {count}\n")
                    else:
                        out_file.write(f"  (Sequence too short for window size {window_size})\n")

            # Iterate through each line to build sequences
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        current_pos_hi = int(parts[0])
                        current_pos_iu = int(parts[4])
                        
                        # Chain Break Logic
                        if current_pos_hi < last_pos_hi or current_pos_iu < last_pos_iu:
                            process_sequence(factor_counter, current_sequence_list)
                            factor_counter += 1
                            current_sequence_list = []

                        current_sequence_list.append(parts[1])
                        
                        last_pos_hi, last_pos_iu = current_pos_hi, current_pos_iu
                    except (ValueError, IndexError):
                        continue
            
            # Process the very last transcription factor in the file
            process_sequence(factor_counter, current_sequence_list)

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")


# --- Main execution block ---
if __name__ == "__main__":
    
    analyze_transcription_factors_in_file(TARGET_FILE_PATH, WINDOW_SIZE)
    print("\nAnalysis complete.")