"""Estimation of clonal architecture using SciClone.

SciClone builds clusters of variant frequencies in non-CNV, non-LOH
regions to infer population heterogeneity. It requires deeply sequenced data
for reliable estimates of allele frequencies. It can infer histories
from tumor samples taken at multiple time points.

http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4125065/
https://github.com/genome/sciclone
"""
import os

from bcbio import utils
from bcbio.pipeline import datadict as dd

def run(vrn_info, cnvs_by_name, somatic_info):
    """Run SciClone, given variant calls, CNVs and tumor/normal files.
    """
    work_dir = _cur_workdir(somatic_info.tumor_data)
    # XXX ToDo
    # -- Generalize to pass multiple variant callers to heterogeneity input
    # -- Extract LOH estimates from VarScan2
    # -- Extract CNV calls from CNVkit
    # -- Extract variant frequencies and counts from VarDict

def _cur_workdir(data):
    return utils.safe_makedir(os.path.join(data["dirs"]["work"], "heterogeneity",
                                           dd.get_sample_name(data), "sciclone"))
