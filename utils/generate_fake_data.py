import pandas as pd
import numpy as np
import os
from helpers import load_cfg

CFG_PATH = "./utils/config.yaml"

#if __name__ == "__main__": Đây là một cấu trúc phổ biến trong Python để kiểm tra xem script hiện tại có 
# đang được chạy trực tiếp hay không. Nếu script được chạy trực tiếp, đoạn mã bên trong khối này sẽ được thực thi.
#  Nếu script được import như một module, đoạn mã bên trong khối này sẽ không được thực thi.
if __name__ == "__main__":
    # Range of timestamp to generate
    start_ts = "26-09-2022"
    end_ts = "25-09-2023"

    # Features to generate
    features = ["pressure", "velocity", "speed"]

    # Create the timestamp column
    #ts = pd.date_range(start=start_ts, end=end_ts, freq="H"): Tạo một dãy thời gian từ start_ts đến end_ts với tần suất mỗi giờ.
    ts = pd.date_range(start=start_ts, end=end_ts, freq="H")
    #df = pd.DataFrame(ts, columns=["event_timestamp"]): Tạo một DataFrame với cột thời gian.
    df = pd.DataFrame(ts, columns=["event_timestamp"])

    # Random floats in the half-open interval [0.0, 1.0)
    # to add other columns in the dataframe
    for feature in features:
        df[feature] = np.random.random_sample((len(ts),))

    # Load our pre-defined config to find where the
    # fake data path will reside in
    cfg = load_cfg(CFG_PATH)
    fake_data_cfg = cfg["fake_data"]
    num_files = fake_data_cfg["num_files"]

    # Create the destination folder to save
    # parquet files if not existing
    if not os.path.exists(fake_data_cfg["folder_path"]):
        os.makedirs(fake_data_cfg["folder_path"], exist_ok=True)

    # Split data frame by num_files, then write each
    # to a parquet file
    df_splits = np.array_split(df, num_files)
    for i in range(num_files):
        df_splits[i].reset_index().to_parquet(
            os.path.join(fake_data_cfg["folder_path"], f"part_{i}.parquet")
        )
