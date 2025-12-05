import os

BASE_FOLDER: str = "/mnt/d/NR_HI_IU"
DBD_OUTPUT_DIR: str = "DBD-Region"
NON_DBD_OUTPUT_DIR: str = "Non-DBD-Region"

POSITION_COLUMN_INDEX: int = 4
ANCHOR_COLUMN_INDEX: int = 7

def process_file_for_splitting(filepath: str):
    try:
        base_name, _ = os.path.splitext(os.path.basename(filepath))

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
            
            reformatted_dbd_lines = []
            reformatted_nondbd_lines = []

            for line in factor_lines_chunk:
                try:
                    parts = line.split()
                    selected_columns = [parts[4], parts[5], parts[6], parts[7]]
                    new_line = "\t".join(selected_columns) + "\n"

                    if parts[ANCHOR_COLUMN_INDEX].strip() == "Yes":
                        reformatted_dbd_lines.append(new_line)
                    else:
                        reformatted_nondbd_lines.append(new_line)
                except (ValueError, IndexError):
                    continue
            
            if reformatted_dbd_lines:
                output_filename = f"{base_name}_TF_{factor_num}.txt"
                full_output_path = os.path.join(DBD_OUTPUT_DIR, output_filename)
                with open(full_output_path, 'w') as out_file:
                    out_file.write(NEW_HEADER)
                    out_file.writelines(reformatted_dbd_lines)

            if reformatted_nondbd_lines:
                output_filename = f"{base_name}_TF_{factor_num}.txt"
                full_output_path = os.path.join(NON_DBD_OUTPUT_DIR, output_filename)
                with open(full_output_path, 'w') as out_file:
                    out_file.write(NEW_HEADER)
                    out_file.writelines(reformatted_nondbd_lines)

    except Exception as e:
        print(f"!!! An error occurred while processing the file {filepath}: {e}")

if __name__ == "__main__":
    os.makedirs(DBD_OUTPUT_DIR, exist_ok=True)
    os.makedirs(NON_DBD_OUTPUT_DIR, exist_ok=True)
    print(f"DBD regions will be saved in '{DBD_OUTPUT_DIR}'")
    print(f"Non-DBD regions will be saved in '{NON_DBD_OUTPUT_DIR}'")

    for dirpath, _, filenames in os.walk(BASE_FOLDER):
        for filename in filenames:
            if filename.endswith(".txt"):
                full_filepath = os.path.join(dirpath, filename)
                print(f"--- Splitting: {full_filepath} ---")
                process_file_for_splitting(full_filepath)

    print("\n\n" + "*" * 50)
    print("All files have been split and processed.")
    print("*" * 50)