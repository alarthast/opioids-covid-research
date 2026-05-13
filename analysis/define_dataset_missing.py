###################################################################
# This script extracts age and sex for FULL cohort (no exclusions)
#   for quantification of number of people with missing age/sex
#
# Author: Andrea Schaffer
#   Bennett Institute for Applied Data Science
#   University of Oxford, 2024
#####################################################################

from ehrql import Dataset

from ehrql.tables.emisv2 import patients, practice_registrations

from dates import index_date

dataset = Dataset()

dataset.sex = patients.sex

dataset.age = patients.age_on(index_date)

# Define population #
dataset.define_population(
    (patients.date_of_death.is_after(index_date) | patients.date_of_death.is_null())
    & (practice_registrations.for_patient_on(index_date).exists_for_patient())
)


##############################################
