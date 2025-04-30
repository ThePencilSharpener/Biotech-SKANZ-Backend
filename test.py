import pandas as pd
import numpy as np

# Load the parquet file
df = pd.read_parquet('train_correct.parquet')

# Keep only the 'question' and 'topic' columns
df = df[['question', 'topic']]

# Filter rows to only keep chemistry, biology, or physics topics
df = df[df['topic'].isin(['chemistry', 'biology', 'physics'])]

# Optional: Reset the index after filtering
df = df.reset_index(drop=True)


# Show the cleaned dataframe
print(df.head(8))

# If you want to save the cleaned file back to parquet:
df.to_parquet('traincleaned_file.parquet', index=False)

