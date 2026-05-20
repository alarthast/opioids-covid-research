####################################################################
# This script fetches all of the codelists identified in
# codelists.txt from OpenCodelists.
#
# Author: Andrea Schaffer
#   Bennett Institute for Applied Data Science
#   University of Oxford, 2024
#####################################################################


# --- IMPORT STATEMENTS ---
import csv
from pathlib import Path


## Import code building blocks from cohort extractor package
def codelist_from_csv(filename, *, column, category_column=None):
    filename = Path(filename)
    with filename.open("r") as f:
        return codelist_from_csv_lines(
            f, column=column, category_column=category_column
        )


def codelist_from_csv_lines(lines, *, column, category_column=None):
    if category_column is None:
        category_column = column
        return_list = True
    else:
        return_list = False
    # Using `restval=""` ensures we never get None instead of string, so we can always
    # call `.strip()` without blowing up
    reader = csv.DictReader(iter(lines), restval="")
    code_map = {row[column].strip(): row[category_column].strip() for row in reader}
    # Discard any empty codes
    code_map.pop("", None)
    if return_list:
        return list(code_map)
    else:
        return code_map


def get_extra_codes(filepath):
    return list(codelist_from_csv(filepath, column="code"))


# --- CODELISTS ---

## Care home - use primis based on Schultze et al report (10.12688/wellcomeopenres.16737.1)
carehome_primis_codes = list(
    codelist_from_csv(
        "codelists/primis-covid19-vacc-uptake-longres.csv",
        column="code",
    )
) + get_extra_codes("codelists/carehome_primis_codes_extra_codes.csv")

## Cancer

###  Cancer - excluding lung/haem
oth_ca_codes = list(
    codelist_from_csv(
        "codelists/opensafely-cancer-excluding-lung-and-haematological-snomed.csv",
        column="id",
    )
) + get_extra_codes("codelists/oth_ca_codes_extra_codes.csv")

### Cancer - lung
lung_ca_codes = list(
    codelist_from_csv("codelists/opensafely-lung-cancer-snomed.csv", column="id")
) + get_extra_codes("codelists/lung_ca_codes_extra_codes.csv")

### Cancer - haematological
haem_ca_codes = list(
    codelist_from_csv(
        "codelists/opensafely-haematological-cancer-snomed.csv", column="id"
    )
) + get_extra_codes("codelists/haem_ca_codes_extra_codes.csv")

### All cancer combined
cancer_codes = oth_ca_codes + lung_ca_codes + haem_ca_codes

## Medication DM&D
### High dose, long-acting opioids
hi_opioid_codes = list(
    codelist_from_csv(
        "codelists/opensafely-high-dose-long-acting-opioids-openprescribing-dmd.csv",
        column="code",
    )
) + get_extra_codes("codelists/hi_opioid_codes_extra_codes.csv")

### Buccal opioids
buc_opioid_codes = list(
    codelist_from_csv(
        "codelists/opensafely-opioid-containing-medicines-buccal-nasal-and-oromucosal-excluding-drugs-for-substance-misuse-dmd.csv",
        column="code",
    )
) + get_extra_codes("codelists/buc_opioid_codes_extra_codes.csv")

### Inhaled opioids
inh_opioid_codes = list(
    codelist_from_csv(
        "codelists/opensafely-opioid-containing-medicines-inhalation-excluding-drugs-for-substance-misuse-dmd.csv",
        column="code",
    )
) + get_extra_codes("codelists/inh_opioid_codes_extra_codes.csv")

### Oral opioids
oral_opioid_codes = list(
    codelist_from_csv(
        "codelists/opensafely-opioid-containing-medicines-oral-excluding-drugs-for-substance-misuse-dmd.csv",
        column="code",
    )
) + get_extra_codes("codelists/oral_opioid_codes_extra_codes.csv")

### Parenteral opioids
par_opioid_codes = list(
    codelist_from_csv(
        "codelists/opensafely-opioid-containing-medicines-parenteral-excluding-drugs-for-substance-misuse-dmd.csv",
        column="code",
    )
) + get_extra_codes("codelists/par_opioid_codes_extra_codes.csv")

### Rectal opioids
rec_opioid_codes = list(
    codelist_from_csv(
        "codelists/opensafely-opioid-containing-medicines-rectal-excluding-drugs-for-substance-misuse-dmd.csv",
        column="code",
    )
) + get_extra_codes("codelists/rec_opioid_codes_extra_codes.csv")

### Transdermal opioids
trans_opioid_codes = list(
    codelist_from_csv(
        "codelists/opensafely-opioid-containing-medicines-transdermal-excluding-drugs-for-substance-misuse-dmd.csv",
        column="code",
    )
) + get_extra_codes("codelists/trans_opioid_codes_extra_codes.csv")


### Other opioid
oth_opioid_codes = buc_opioid_codes + inh_opioid_codes + rec_opioid_codes

### Any opioid
opioid_codes = (
    buc_opioid_codes
    + inh_opioid_codes
    + oral_opioid_codes
    + par_opioid_codes
    + rec_opioid_codes
    + trans_opioid_codes
)

## Ethnicity
ethnicity_codes_16 = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column="snomedcode",
    category_column="Grouping_16",
)
alien_ethnicities_16 = codelist_from_csv(
    "codelists/ethnicity_aliens_extra_codes.csv",
    column="code",
    category_column="Grouping_16",
)
assert isinstance(ethnicity_codes_16, dict)
assert isinstance(alien_ethnicities_16, dict)
ethnicity_codes_16 = {**ethnicity_codes_16, **alien_ethnicities_16}

## Ethnicity
ethnicity_codes_6 = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column="snomedcode",
    category_column="Grouping_6",
)
alien_ethnicities_6 = codelist_from_csv(
    "codelists/ethnicity_aliens_extra_codes.csv",
    column="code",
    category_column="Grouping_6",
)
assert isinstance(ethnicity_codes_6, dict)
assert isinstance(alien_ethnicities_6, dict)
ethnicity_codes_6 = {**ethnicity_codes_6, **alien_ethnicities_6}
