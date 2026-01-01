# SCRIPT: filter_blast_results.py
import os
import csv

# --- CONFIGURATION ---
# The original, unfiltered BLAST result file.
BLAST_RESULTS_FILE: str = "similar_pairs.tsv"
# The final output CSV file.
DISSIMILAR_PAIRS_OUTPUT: str = "dissimilar_pairs_lt25_with_scores.csv"
# The similarity threshold. We will keep pairs with identity LESS THAN this value.
SIMILARITY_THRESHOLD: float = 25.0
# -------------------------------------------------------------------

if __name__ == "__main__":
    
    # --- Check if the input BLAST file exists ---
    if not os.path.exists(BLAST_RESULTS_FILE):
        print(f"!!! ERROR: BLAST results file '{BLAST_RESULTS_FILE}' not found.")
        print("    Please ensure you have run the `blastp` command first.")
        exit()

    print(f"Reading '{BLAST_RESULTS_FILE}' to find pairs with less than {SIMILARITY_THRESHOLD}% identity...")
    
    dissimilar_pairs_found = 0
    # Use a set to keep track of pairs we've already written to avoid duplicates (e.g., A vs B and B vs A)
    processed_pairs = set()

    try:
        with open(DISSIMILAR_PAIRS_OUTPUT, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the new three-column header
            writer.writerow(['Sequence_1', 'Sequence_2', 'Percent_Identity'])

            with open(BLAST_RESULTS_FILE, 'r') as f:
                for line in f:
                    try:
                        parts = line.strip().split('\t')
                        if len(parts) < 3: continue # Skip malformed lines

                        id1 = parts[0]
                        id2 = parts[1]
                        percent_identity = float(parts[2])

                        # --- This is the main filtering logic ---
                        if percent_identity < SIMILARITY_THRESHOLD:
                            
                            # Create a sorted tuple to uniquely identify the pair
                            sorted_pair = tuple(sorted((id1, id2)))

                            # If we haven't processed this pair yet, write it to the file
                            if sorted_pair not in processed_pairs:
                                writer.writerow([id1, id2, f"{percent_identity:.2f}"])
                                processed_pairs.add(sorted_pair)
                                dissimilar_pairs_found += 1
                    
                    except (ValueError, IndexError):
                        # Silently skip any line that can't be parsed correctly
                        continue
        
        print(f"\nSuccessfully identified and saved {dissimilar_pairs_found} unique dissimilar pairs.")
        print(f"Final results are in '{DISSIMILAR_PAIRS_OUTPUT}'.")

    except Exception as e:
        print(f"!!! An unexpected error occurred: {e}")