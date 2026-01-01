import os
import collections
import matplotlib.pyplot as plt
import seaborn as sns

JOBS = [
    {
        "input_dir": "DBD-Region",
        "output_subdir": "DBD_normalized_scores",
        "region_name": "DBDs"
    },
    {
        "input_dir": "Non-DBD-Region",
        "output_subdir": "nonDBD_normalized_scores",
        "region_name": "non-DBDs"
    }
]
OUTPUT_BASE_DIR: str = "amino_acid_normalized_disorder"
SUPERCLASSES = ["1.", "2.", "4.", "5.", "6.", "7.", "8.", "9."]

AMINO_ACID_ORDER_BY_DISORDER = [
    'P', 
    'E', 
    'S', 
    'Q', 
    'K', 
    'A', 
    'G', 
    'D', 
    'T', 
    'R', 
    'M', 
    'N',
    'V', 
    'H', 
    'L', 
    'F', 
    'Y', 
    'I', 
    'W',
    'C'
]

RESIDUE_COLUMN_INDEX: int = 1
IU_COLUMN_INDEX: int = 2

def analyze_superclass_normalized_disorder(superclass_prefix: str, input_dir: str, output_dir: str, region_name: str):
    print(f"\n--- Analyzing Superclass '{superclass_prefix.strip('.')}' in '{region_name}' ---")

    individual_ordered_counts = collections.Counter()
    individual_disordered_counts = collections.Counter()
    
    files_to_process = [f for f in os.listdir(input_dir) if f.startswith(superclass_prefix) and f.endswith(".txt")]

    if not files_to_process:
        print(f"No files found for this superclass. Skipping.")
        return

    print(f"Found {len(files_to_process)} files to process...")

    for filename in files_to_process:
        filepath = os.path.join(input_dir, filename)
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()[1:]
                for line in lines:
                    parts = line.split()
                    if len(parts) > max(RESIDUE_COLUMN_INDEX, IU_COLUMN_INDEX):
                        try:
                            residue = parts[RESIDUE_COLUMN_INDEX]
                            iu_score = float(parts[IU_COLUMN_INDEX])
                            
                            if iu_score < 0.5:
                                individual_ordered_counts[residue] += 1
                            else:
                                individual_disordered_counts[residue] += 1
                        except (ValueError, IndexError):
                            continue
        except Exception as e:
            print(f"!!! Warning: Could not process {filename}: {e}")

    total_ordered_count = sum(individual_ordered_counts.values())
    total_disordered_count = sum(individual_disordered_counts.values())

    scores = {}
    for aa in AMINO_ACID_ORDER_BY_DISORDER:
        Di = individual_disordered_counts.get(aa, 0)
        Oi = individual_ordered_counts.get(aa, 0)
        
        freq_disordered = Di / total_disordered_count if total_disordered_count > 0 else 0.0
        freq_ordered = Oi / total_ordered_count if total_ordered_count > 0 else 0.0
        
        numerator = freq_disordered - freq_ordered
        denominator = freq_disordered + freq_ordered

        score = numerator / denominator if denominator > 0 else 0.0
        scores[aa] = score
        
    plt.figure(figsize=(15, 8))
    ax = sns.barplot(x=list(scores.keys()), y=list(scores.values()), palette="coolwarm_r")
    
    plt.axhline(0.0, color='black', linestyle='--', linewidth=1.0)
    
    plt.title(f"Normalized Disorder Preference Score in {region_name}\n(Superclass {superclass_prefix.strip('.')})", fontsize=16)
    plt.xlabel("Amino Acid", fontsize=12)
    plt.ylabel("Preference Score (-1=Ordered, 1=Disordered)", fontsize=12)
    plt.ylim(-1, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in ax.patches:
        height = bar.get_height()
        ax.text(
            x=bar.get_x() + bar.get_width() / 2,
            y=height,
            s=f'{height:+.2f}',
            ha='center',
            va='bottom' if height >= 0 else 'top',
            fontsize=8
        )

    output_filename = f"superclass_{superclass_prefix.strip('.')}_normalized_scores.png"
    full_output_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_output_path, bbox_inches='tight')
    plt.close()
    print(f"Plot saved to '{full_output_path}'")

if __name__ == "__main__":
    
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    
    for job in JOBS:
        input_dir = job["input_dir"]
        output_subdir = job["output_subdir"]
        region_name = job["region_name"]
        
        print("\n" + "="*80)
        print(f"STARTING JOB FOR REGION: '{region_name}'")
        print("="*80)
        
        if not os.path.isdir(input_dir):
            print(f"!!! ERROR: Input directory '{input_dir}' not found. Skipping this job.")
            continue

        job_output_dir = os.path.join(OUTPUT_BASE_DIR, output_subdir)
        os.makedirs(job_output_dir, exist_ok=True)
        print(f"Normalized score plots will be saved in '{job_output_dir}'")
        
        for superclass in SUPERCLASSES:
            analyze_superclass_normalized_disorder(superclass, input_dir, job_output_dir, region_name)
        
        print(f"\nJOB FOR '{region_name}' COMPLETE.")

    print("\n\n" + "*" * 50)
    print("All analyses are complete.")
    print("*" * 50)