# SCRIPT: merged_excel_to_fasta.py
import pandas as pd

# --- CONFIGURATION ---
# The merged Excel file you just created.
INPUT_EXCEL_FILE: str = "Human-TFs-PDB_MERGED.xlsx"
# The name of the sheet inside the Excel file.
SHEET_NAME: str = "All-Human"

# --- Column names ---
ID_COLUMN_NAME: str = '#PDB_chainID'
SEQUENCE_COLUMN_NAME: str = 'Sequence'

# The name for the final, combined FASTA file.
OUTPUT_FASTA_FILE: str = "all_sequences.fasta"
# -------------------------------------------------------------

if __name__ == "__main__":
    try:
        # Use openpyxl engine for modern .xlsx files.
        df = pd.read_excel(INPUT_EXCEL_FILE, sheet_name=SHEET_NAME, engine='openpyxl')
        print(f"Successfully read sheet '{SHEET_NAME}' from {INPUT_EXCEL_FILE}.")

        file_count = 0
        with open(OUTPUT_FASTA_FILE, 'w') as out_file:
            for index, row in df.iterrows():
                seq_id = str(row[ID_COLUMN_NAME]).strip()
                sequence = str(row[SEQUENCE_COLUMN_NAME]).strip()

                if seq_id and sequence and 'No sequence' not in sequence:
                    out_file.write(f">{seq_id}\n")
                    out_file.write(f"{sequence}\n")
                    file_count += 1
        
        print(f"Successfully wrote {file_count} total sequences to '{OUTPUT_FASTA_FILE}'.")

    except Exception as e:
        print(f"!!! An unexpected error occurred: {e}")
