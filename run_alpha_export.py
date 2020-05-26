"""
This program exports data on the alphas of collatz sequences
into a csv file. The sample is used to validate several mathematical
theorems.
"""
import logging
from math import log2
import pandas as pd
from collatz import commons


# Main method to start the export
# pylint: disable=duplicate-code
# Code duplication is ok here
if __name__ == '__main__':
    K_FACTORS = [1, 3, 5, 7, 9]
    MAX_START_VALUE = 3999
    V_1_RANGE = range(1, MAX_START_VALUE + 1, 2)
    MAX_ITERATIONS = 100
    N = ((MAX_START_VALUE + 1) / 2) * len(K_FACTORS)
    FILE_NAME = "./data/alpha_sequences.csv"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Exporting %d Collatz sequences to file %s", N, FILE_NAME)

    OUTPUT_FRAME = None
    SEQUENCE_ID = 0

    for k in K_FACTORS:
        logging.info("Generating sequences for k=%d", k)

        for v_1 in V_1_RANGE:
            # Create the sequence
            SEQUENCE_ID = SEQUENCE_ID + 1
            odds = commons.odd_collatz_sequence(v_1, k, MAX_ITERATIONS)
            next_odds = odds[1:]
            odds.pop()

            current_frame = pd.DataFrame({"v_i": odds})
            current_frame["sequence_id"] = SEQUENCE_ID
            current_frame["sequence_len"] = len(current_frame)
            current_frame["n"] = current_frame.index + 1
            current_frame["k_factor"] = k
            current_frame["v_1"] = v_1
            current_frame["kv_i+1"] = current_frame["v_i"].apply(
                commons.next_collatz_number, args=(k,))
            current_frame["v_i+"] = next_odds
            current_frame["terminal"] = \
                (current_frame["v_i+"] == current_frame["v_1"]) | \
                (current_frame["v_i+"] == 1)

            current_frame["alpha_i"] = current_frame["kv_i+1"].apply(commons.trailing_zeros)
            current_frame["alpha_i"] = current_frame["alpha_i"].astype('int64')
            current_frame["alpha_i_max"] = log2(k) + current_frame["v_i"].apply(log2)
            current_frame["alpha_i_max"] += (1 + 1/(k * current_frame["v_i"])).apply(log2)
            # Round result here to avoid loss of precision errors
            current_frame["alpha_i_max"] = current_frame["alpha_i_max"].round(9)
            current_frame["alpha"] = current_frame["alpha_i"].cumsum()
            current_frame["alpha_cycle"] = (log2(k) * current_frame["n"]).astype('int64') + 1
            current_frame["alpha_max"] = log2(v_1) + (current_frame["n"] * log2(k))
            current_frame["alpha_max"] = current_frame["alpha_max"].astype('int64') + 1

            print_frame = current_frame[[
                "sequence_id", "sequence_len", "n", "k_factor", "v_1",
                "v_i", "v_i+", "terminal", "alpha_i", "alpha_i_max", "alpha",
                "alpha_cycle", "alpha_max"]]

            print_frame.columns = [
                "sequence_id", "sequence_len", "n", "k", "v_1",
                "v_i", "v_i+", "terminal", "a_i", "a_i_max", "a",
                "a_cycle", "a_max"]

            if OUTPUT_FRAME is not None:
                OUTPUT_FRAME = OUTPUT_FRAME.append(print_frame)
            else:
                OUTPUT_FRAME = print_frame

    # Write the frame to file
    print(OUTPUT_FRAME.head().to_string(index=False))
    OUTPUT_FRAME.to_csv(FILE_NAME, index=False)

    logging.info("Export finished successfully!")
