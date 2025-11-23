import os
import collections
import matplotlib.pyplot as plt
import seaborn as sns

ANALYSIS_BASE_DIR: str = "output"
TARGET_WINDOW_SIZE: int = 3
MINIMUM_OCCURRENCE_COUNT: int = 3
HISTOGRAM_OUTPUT_DIR: str = "frequent_triplet_histograms"

def create_amino_acid_histogram(amino_acid_counts: collections.Counter, source_filename: str, output_path: str):
    if not amino_acid_counts: return

    amino_acid_order = sorted(list("ACDEFGHIKLMNPQRSTVWY"))
    
    plot_data = {aa: amino_acid_counts.get(aa, 0) for aa in amino_acid_order}
    
    plt.figure(figsize=(15, 8))
    ax = sns.barplot(x=list(plot_data.keys()), y=list(plot_data.values()), palette="viridis")
    
    for bar in ax.patches:
        height = bar.get_height()
        if height > 0:
            ax.text(
                x=bar.get_x() + bar.get_width() / 2,
                y=height,
                s=f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=8
            )
    
    plt.title(f"Amino Acid Distribution in Frequent Triplets (Count >= {MINIMUM_OCCURRENCE_COUNT})\n(Source: {source_filename})", fontsize=16)
    plt.xlabel("Amino Acid", fontsize=12)
    plt.ylabel("Total Weighted Count in Frequent Triplets", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def analyze_file_for_frequent_triplets(filepath: str, output_dir: str):
    pattern_counts = {}
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if " - " not in line or line.startswith(('#', '-', '=')):
                    continue
                
                try:
                    parts = line.split(" - ")
                    pattern = parts[0].strip()
                    count = int(parts[1])
                    pattern_counts[pattern] = count
                except (ValueError, IndexError):
                    continue
    
    except Exception as e:
        print(f"!!! Could not read or process file {filepath}: {e}")
        return

    if not pattern_counts:
        print(f"--- No valid data found in {os.path.basename(filepath)}. Skipping.")
        return

    aa_distribution = collections.Counter()
    frequent_patterns_found = False

    for pattern, count in pattern_counts.items():
        if count >= MINIMUM_OCCURRENCE_COUNT:
            frequent_patterns_found = True
            for amino_acid in pattern:
                aa_distribution[amino_acid] += count

    if not frequent_patterns_found:
        print(f"--- No patterns with count >= {MINIMUM_OCCURRENCE_COUNT} found in {os.path.basename(filepath)}. Skipping.")
        return

    base_name, _ = os.path.splitext(os.path.basename(filepath))
    histogram_filename = f"{base_name}_histogram.png"
    full_output_path = os.path.join(output_dir, histogram_filename)
    
    create_amino_acid_histogram(aa_distribution, os.path.basename(filepath), full_output_path)
    print(f"--- Generated histogram for {os.path.basename(filepath)}")

if __name__ == "__main__":
    
    target_dir = os.path.join(ANALYSIS_BASE_DIR, str(TARGET_WINDOW_SIZE))
    
    if not os.path.isdir(target_dir):
        print(f"Error: The target directory '{target_dir}' was not found.")
        print("Please ensure the sliding window analysis has been run and the output exists.")
        exit()

    os.makedirs(HISTOGRAM_OUTPUT_DIR, exist_ok=True)
    print(f"Histograms will be saved in the '{HISTOGRAM_OUTPUT_DIR}' directory.\n")

    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            if filename.endswith(".txt"):
                full_filepath = os.path.join(dirpath, filename)
                analyze_file_for_frequent_triplets(full_filepath, HISTOGRAM_OUTPUT_DIR)

    print("\n\n" + "*" * 50)
    print("Histogram generation is complete.")
    print("*" * 50)