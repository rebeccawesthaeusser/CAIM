import pandas as pd
import pingouin as pg
import glob 

csv_folder = "glm/*.csv"
csv_files = glob.glob(csv_folder)

# loop through every file
for file in csv_files:

    df = pd.read_csv(file, sep="\t", header=None)
    df.columns = ["Rater1", "Rater2", "Rater3"]

    df_long = df.melt(var_name="Rater", value_name="Score", ignore_index=False)
    df_long["Item"] = df_long.index + 1  # add Item-number (1 to 100)

    # calculate Intraclass Correlation Coefficient (ICC)
    icc_results = pg.intraclass_corr(data=df_long, targets="Item", raters="Rater", ratings="Score")

    # print ICC(2,1) and ICC(2,k)
    icc_filtered = icc_results[icc_results["Type"].isin(["ICC2", "ICC2k"])]

    file_name = file.split("/")[-1]
    print(f"ICC {file_name}")
    print(icc_filtered[["Type", "ICC", "CI95%"]])
