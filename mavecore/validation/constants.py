import re

"""
Null Constant definitions
"""
NA_STRING = "NA"
null_values_list = (
    "nan",
    "na",
    "none",
    "",
    "undefined",
    "n/a",
    "null",
    "nil",
    NA_STRING,
)

null_values_re = re.compile(
    r"^\s+$|none|nan|na|undefined|n/a|null|nil|{}".format(NA_STRING), flags=re.IGNORECASE
)

readable_null_values_list = [f"'{s}'" for s in null_values_list] + ["whitespace"]

hgvs_nt_column = "hgvs_nt"
hgvs_splice_column = "hgvs_splice"
hgvs_pro_column = "hgvs_pro"
hgvs_columns = sorted([hgvs_nt_column, hgvs_pro_column, hgvs_splice_column])
meta_data = "meta_data"
score_columns = "score_columns"
count_columns = "count_columns"
variant_score_data = "score_data"
variant_count_data = "count_data"
required_score_column = "score"

valid_dataset_columns = [score_columns, count_columns]
valid_variant_columns = [variant_score_data, variant_count_data]

variant_to_scoreset_column = {
    variant_score_data: score_columns,
    variant_count_data: count_columns,
}
scoreset_to_variant_column = {v: k for k, v in variant_to_scoreset_column.items()}
