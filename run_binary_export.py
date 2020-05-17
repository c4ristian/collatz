"""
This program exports binary data of collatz sequences to a csv file.
"""
import logging
from math import log2
import pandas as pd
from collatz import commons

# Main method to start the export
if __name__ == '__main__':
    K_FACTORS = [1, 3, 5, 7, 9]
    MAX_START_VALUE = 3999
    V1_RANGE = range(1, MAX_START_VALUE + 1, 2)
    MAX_ITERATIONS = 100
    N = ((MAX_START_VALUE + 1) / 2) * len(K_FACTORS)
    FILE_NAME = "./data/binary_sequences.csv"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Exporting %d Collatz sequences to file %s", N, FILE_NAME)

    OUTPUT_FRAME = None
    SEQUENCE_ID = 0

    for k in K_FACTORS:
        logging.info("Generating sequences for k=%d", k)

        for v1 in V1_RANGE:
            # Create the sequence
            SEQUENCE_ID = SEQUENCE_ID + 1
            odds = commons.odd_collatz_sequence(v1, k, MAX_ITERATIONS)
            next_odds = odds[1:]
            odds.pop()

            # Derive new fields
            current_frame = pd.DataFrame({"vi": odds})
            current_frame["kvi+1"] = current_frame["vi"].apply(
                commons.next_collatz_number, args=(k,))
            current_frame["vi_1"] = next_odds
            current_frame["sequence_id"] = SEQUENCE_ID
            current_frame["sequence_len"] = len(current_frame)
            current_frame["v1"] = v1
            current_frame["n"] = current_frame.index + 1
            current_frame["k_factor"] = k

            current_frame["bin_len"] = \
                current_frame["vi"].apply(log2).astype('int64') + 1

            current_frame["next_bin_len"] = \
                current_frame["kvi+1"].apply(log2).astype('int64') + 1

            current_frame["bin_diff"] = current_frame["next_bin_len"] - current_frame["bin_len"]
            current_frame["lambda_i"] = current_frame["bin_diff"]
            current_frame.loc[current_frame["lambda_i"] < 0, "lambda_i"] = 0
            current_frame["lambda_sum"] = current_frame["lambda_i"].cumsum()

            current_frame["lambda_i_min"] = int(log2(k))
            current_frame["lambda_i_max"] = int(log2(k) + 1)

            current_frame["lambda_hyp"] = (current_frame["n"] * log2(k))
            current_frame["lambda_min"] = current_frame["lambda_hyp"].astype('int64')
            current_frame["lambda_max"] = current_frame["lambda_hyp"].astype('int64') + 2

            current_frame["alpha_i"] = current_frame["kvi+1"].apply(commons.trailing_zeros)
            current_frame["alpha_i"] = current_frame["alpha_i"].astype('int64')
            current_frame["alpha_sum"] = current_frame["alpha_i"].cumsum()
            current_frame["alpha_pred"] = (log2(k) * current_frame["n"]).astype('int64') + 1
            current_frame["alpha_max"] = log2(v1) + (current_frame["n"] * log2(k))
            current_frame["alpha_max"] = current_frame["alpha_max"].astype('int64') + 1

            current_frame["omega_i"] = current_frame["lambda_i"] - current_frame["alpha_i"]
            current_frame["omega_sum"] = current_frame["lambda_sum"] - current_frame["alpha_sum"]

            current_frame["omega_i_max"] = current_frame["lambda_i_max"] - 1
            current_frame["omega_max"] = current_frame["lambda_max"] - current_frame["n"]

            print_frame = current_frame[[
                "sequence_id", "sequence_len", "n", "k_factor", "v1",
                "vi", "kvi+1", "vi_1", "alpha_i", "alpha_sum",
                "alpha_pred", "alpha_max", "bin_len", "next_bin_len",
                "lambda_i", "lambda_i_min", "lambda_i_max",
                "lambda_sum", "lambda_min", "lambda_max",
                "omega_i", "omega_i_max", "omega_sum", "omega_max"
            ]]

            print_frame.columns = [
                "sequence_id", "sequence_len", "n", "k", "v1",
                "vi", "kvi+1", "vi_1", "a_i", "a_sum",
                "a_pred", "a_max", "bin_len", "next_bin_len",
                "l_i", "l_i_min", "l_i_max",
                "l_sum", "l_min", "l_max",
                "o_i", "o_i_max", "o_sum", "o_max"
            ]

            if OUTPUT_FRAME is not None:
                OUTPUT_FRAME = OUTPUT_FRAME.append(print_frame)
            else:
                OUTPUT_FRAME = print_frame

    # Write the frame to file
    print(OUTPUT_FRAME.head().to_string(index=False))
    OUTPUT_FRAME.to_csv(FILE_NAME, index=False)

    logging.info("Export finished successfully!")
