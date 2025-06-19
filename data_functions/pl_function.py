import polars as pl

"""
When creating a DF from an Excel/csv/other file format, users may have
entered data in ways non-accessible to Polars, such as non-unix characters.
This seems to at least sometimes result in a column being of type "binary",
and must be resolved outside of Polars.

"""

def pldf_binary2str(df: pl.DataFrame, binary_colname: str) -> pl.DataFrame:
    fix_string = df.select(pl.col(binary_colname))
    new = fix_string.to_dict(as_series=False)
    decoded = []
    for item in new[binary_colname]:
        item = item.decode("ascii")
        decoded.append(item)
    newcolumn = pl.Series(binary_colname, decoded)
    return df.replace_column(1, newcolumn)