import os
import pkg_resources
import phizz

resource_package = phizz.__name__

disease_to_genes_path = pkg_resources.resource_filename(
    resource_package,
    "resources/ALL_SOURCES_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt.gz"
)
phenotypes_path = pkg_resources.resource_filename(
    resource_package,
    "resources/phenotypes.txt.gz"
)
genes_path = pkg_resources.resource_filename(
    resource_package,
    "resources/genes_37.txt.gz"
)
schema_path = pkg_resources.resource_filename(
    resource_package,
    "resources/schema.sql"
)
phizz_db = pkg_resources.resource_filename(
    resource_package,
    "resources/phizz.db"
)

config_file = pkg_resources.resource_filename(
    resource_package, 
    "resources/config.ini"
)
