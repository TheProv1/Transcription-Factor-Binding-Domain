import os

BASE_FOLDER: str = "/mnt/d/NR_HI_IU"
OUTPUT_BASE_DIR: str = "DBD_Split"

POSITION_COLUMN_INDEX: int = 4
ANCHOR_COLUMN_INDEX: int = 7

def extract_and_save_anchor_regions(filepath: str, output_root: str):
    """
    Reads a file, identifies each transcription factor using only the POS_IU
    column, isolates when column 8 is "Yes", and saves only the DBD region to an organized directory.
    """
    try:
        family_name = os.path.basename(os.path.dirname(filepath))
        base_name, _ = os.path.splitext(os.path.basename(filepath))
        
        output_directory = os.path.join(output_root, family_name)
        os.makedirs(output_directory, exist_ok=True)

        with open(filepath, 'r') as f:
            lines = f.readlines()

        NEW_HEADER = "POS_IU\tRES_IU\tIU\tANCHOR\n"
        all_residue_lines = []

        for line in lines:
            if not line.strip().lower().startswith('pos'):
                if len(line.split()) > ANCHOR_COLUMN_INDEX:
                    all_residue_lines.append(line)
        
        if not all_residue_lines:
            return

        factor_start_indices = [0]
        for i in range(1, len(all_residue_lines)):
            try:
                current_pos = int(all_residue_lines[i].split()[POSITION_COLUMN_INDEX])
                previous_pos = int(all_residue_lines[i-1].split()[POSITION_COLUMN_INDEX])
                if current_pos < previous_pos:
                    factor_start_indices.append(i)
            except (ValueError, IndexError):
                continue

        for i in range(len(factor_start_indices)):
            factor_num = i + 1
            
            start_index = factor_start_indices[i]
            end_index = factor_start_indices[i+1] if i + 1 < len(factor_start_indices) else len(all_residue_lines)
            
            factor_lines_chunk = all_residue_lines[start_index:end_index]
            
            reformatted_anchor_lines = []
            for line in factor_lines_chunk:
                try:
                    parts = line.split()
                    if parts[ANCHOR_COLUMN_INDEX].strip() == "Yes":
                        selected_columns = [parts[4], parts[5], parts[6], parts[7]]
                        new_line = "\t".join(selected_columns) + "\n"
                        reformatted_anchor_lines.append(new_line)
                except (ValueError, IndexError):
                    continue
            
            if not reformatted_anchor_lines:
                continue

            output_filename = f"{base_name}_TF_{factor_num}_ANCHOR.txt"
            full_output_path = os.path.join(output_directory, output_filename)
            
            with open(full_output_path, 'w') as out_file:
                out_file.write(NEW_HEADER)
                out_file.writelines(reformatted_anchor_lines)

    except Exception as e:
        print(f"!!! An error occurred while processing the file {filepath}: {e}")

if __name__ == "__main__":
    
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    print(f"All extracted ANCHOR regions will be saved in the '{OUTPUT_BASE_DIR}' directory.")

    for dirpath, _, filenames in os.walk(BASE_FOLDER):
        for filename in filenames:
            if filename.endswith(".txt"):
                full_filepath = os.path.join(dirpath, filename)
                print(f"--- Processing: {full_filepath} ---")
                
                extract_and_save_anchor_regions(full_filepath, OUTPUT_BASE_DIR)

    print("\n\n" + "*" * 50)
    print("ANCHOR region extraction and reformatting is complete.")
    print("*" * 50)