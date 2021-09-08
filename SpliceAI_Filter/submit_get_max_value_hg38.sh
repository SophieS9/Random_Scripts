#!/bin/bash

#SBATCH --time=72:00:00
#SBATCH --partition=low

#Usage vcf=<VCF file>,out=<Output file>

cd "$SLURM_SUBMIT_DIR"

python get_max_value_hg38.py --vcf $vcf --out $out


