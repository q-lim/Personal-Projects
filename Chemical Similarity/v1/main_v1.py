"""
Chemical Similarity Calculator
Calculates the Tanimoto similarity of compounds based on their SMILES

Uses data stored in JSON files
"""

# For working with JSON files
import json

# For dataframe creation and data analysis
import pandas as pd

# Core RDKit chemistry toolkit
from rdkit import Chem

# Morgan Fingerprint Generator
from rdkit.Chem import rdFingerprintGenerator

# To calculate Tanimoto Similarity
from rdkit.DataStructs import TanimotoSimilarity


def load_smiles(json_file):
    """Load SMILES from JSON file"""

    with open(json_file, "r") as f:
        data = json.load(f)

    names = []
    mols = []

    for drug in data:
        
        # Generate a molecule object
        mol = Chem.MolFromSmiles(drug["smiles"])
        
        if mol:
            names.append(drug["name"])
            mols.append(mol)

    return names, mols



def compute_fingerprints(mols):
    """Compute Morgan fingerprint"""

    fps = []

    # Create Morgan fingerprint generator
    morgan_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

    for mol in mols:
        fp = morgan_gen.GetFingerprint(mol)
        fps.append(fp)

    return fps



def tanimoto_matrix(names, fps):
    """Generate Tanimoto matrix"""

    n = len(fps) # Length of fingerprint
    matrix = []

    # Compute Tanimoto similarity scores between compounds
    for i in range(n):
        row = []
        for j in range(n):
            score = TanimotoSimilarity(fps[i], fps[j])
            row.append(score)
        matrix.append(row)

    # Create dataframe of Tanimoto similarity scores
    df = pd.DataFrame(matrix, index=names, columns=names)

    return df



def main(json_file):
    """Main function: Analyze compounds in JSON file"""

    # Get the names and molecules
    names, mols = load_smiles(json_file)

    # Compute the Morgan Fingerprints for molecules
    fps = compute_fingerprints(mols)

    # Create the Tanimoto Similarity matrix
    df = tanimoto_matrix(names, fps)

    return df



if __name__ == "__main__":

    files = [
        "opioids_morphine_class.json",
        "fentanyl_class.json",
        "cannabinoids_class.json",
        "salbutamol_class.json",
        "paracetamol_class.json",
        "cetirizine_class.json"
    ]

    for f in files:

        df = main(f)

        print("\nSimilarity Matrix for:", f)
        print(df.round(3))
