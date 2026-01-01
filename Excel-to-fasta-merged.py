# SCRIPT: merge_sequences.py
import pandas as pd

# --- CONFIGURATION ---
EXCEL_FILE: str = "Human-TFs-PDB.xls"
FASTA_FILE: str = "ExtraIDs.fasta"

# --- Sheet and Column Names from your file ---
TARGET_SHEET: str = "All-Human"
EXTRA_IDS_SHEET: str = "ExtraIDs"

# --- Column Names from your file ---
ID_COLUMN_TARGET: str = '#PDB_chainID'
SEQUENCE_COLUMN_NAME: str = 'Sequence'
ID_COLUMN_EXTRA_INDEX: int = 0
# -------------------------------------------------------------------

def parse_fasta_file(fasta_filepath: str) -> dict:
    """
    Reads a FASTA file and returns a dictionary mapping sequence IDs to sequences.
    Correctly parses IDs like '>7QOD_1|Chains...'.
    """
    sequences = {}
    current_seq_id = None
    
    try:
        with open(fasta_filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('>'):
                    current_seq_id = line[1:].split('|')[0].strip()
                    sequences[current_seq_id] = ""
                elif current_seq_id:
                    sequences[current_seq_id] += line
        print(f"Successfully parsed {len(sequences)} sequences from {fasta_filepath}.")
        return sequences
    except FileNotFoundError:
        print(f"!!! ERROR: FASTA file not found at '{fasta_filepath}'")
        return None

if __name__ == "__main__":
    
    fasta_sequences = parse_fasta_file(FASTA_FILE)
    if fasta_sequences is None:
        exit()

    try:
        print(f"Reading sheets from {EXCEL_FILE}...")
        xls = pd.ExcelFile(EXCEL_FILE, engine='xlrd')
        
        if TARGET_SHEET not in xls.sheet_names or EXTRA_IDS_SHEET not in xls.sheet_names:
            print(f"!!! ERROR: One or both required sheets ('{TARGET_SHEET}', '{EXTRA_IDS_SHEET}') not found.")
            print(f"    Available sheets are: {xls.sheet_names}")
            exit()
            
        main_df = pd.read_excel(xls, sheet_name=TARGET_SHEET)
        extra_ids_df = pd.read_excel(xls, sheet_name=EXTRA_IDS_SHEET)
        
        id_column_extra_name = extra_ids_df.columns[ID_COLUMN_EXTRA_INDEX]

        new_rows = []
        found_count = 0
        
        existing_ids = set(main_df[ID_COLUMN_TARGET].astype(str))
        
        print("\nMatching IDs from 'ExtraIDs' sheet with sequences from FASTA file...")
        
        # --- MODIFIED LOGIC: Smart Matching ---
        # Create a list of all the IDs from the FASTA file
        fasta_id_list = list(fasta_sequences.keys())

        for excel_id in extra_ids_df[id_column_extra_name]:
            excel_id_str = str(excel_id).strip()
            
            # This flag will help us find the first match and stop.
            match_found_for_this_id = False

            # Now, loop through the list of actual FASTA IDs
            for fasta_id in fasta_id_list:
                # Check if the Excel ID is the start of the FASTA ID
                if fasta_id.startswith(excel_id_str):
                    
                    # We found a match! Now check if it's a duplicate.
                    if fasta_id in existing_ids:
                        print(f"  - ID '{fasta_id}' already exists in '{TARGET_SHEET}'. Skipping.")
                        match_found_for_this_id = True
                        break # Stop searching for this Excel ID

                    # If it's a new, valid match, get the sequence and prepare the row.
                    sequence = fasta_sequences[fasta_id]
                    new_rows.append({
                        ID_COLUMN_TARGET: fasta_id, # Use the full, correct ID from the FASTA file
                        SEQUENCE_COLUMN_NAME: sequence
                    })
                    found_count += 1
                    match_found_for_this_id = True
                    # IMPORTANT: Remove the found ID from the list to prevent it from being matched again
                    # (in case of IDs like 'ABC' and 'ABC_1')
                    fasta_id_list.remove(fasta_id)
                    break # Stop searching and move to the next Excel ID

            if not match_found_for_this_id:
                 print(f"  - WARNING: No sequence found in FASTA file for ID starting with '{excel_id_str}'.")

        print(f"\nFound {found_count} new sequences to add.")

        if new_rows:
            new_rows_df = pd.DataFrame(new_rows)
            combined_df = pd.concat([main_df, new_rows_df], ignore_index=True)
            output_excel_file = "Human-TFs-PDB_MERGED.xlsx"
            
            print(f"Saving combined data to '{output_excel_file}'...")
            
            combined_df.to_excel(output_excel_file, sheet_name=TARGET_SHEET, index=False, engine='openpyxl')
            
            print("\n" + "="*50)
            print("Merge complete!")
            print(f"Original '{TARGET_SHEET}' had {len(main_df)} rows.")
            print(f"New file '{output_excel_file}' has {len(combined_df)} rows.")
            print("="*50)
        else:
            print("\nNo new sequences were added. The output file was not created.")

    except FileNotFoundError:
        print(f"!!! ERROR: Excel file not found at '{EXCEL_FILE}'")
    except Exception as e:
        print(f"!!! An unexpected error occurred: {e}")