"""
This program exports data on the alphas of collatz sequences
into a csv file. The sample is used to validate several mathematical
theorems.
"""
import logging
from math import log2
import pandas as pd
from collatz import commons


def _generate_sequence(start_value: int, k_factor: int, max_iterations: int):
    """
    This method generates a Collatz sequence, containing only odd numbers.

    :param start_value: The integer value to start with. The value must be a
    natural number > 0. If an even number is handed over, the next odd number will be used
    as start value.
    :param k_factor: The factor that is multiplied with odd numbers (default is 3).
    :param max_iterations: The maximum number of iterations performed
    before the method exits. Default is -1, meaning that no max number of iterations is set.
    :return: The collatz sequence as a pandas data frame.
    """
    odds = commons.odd_collatz_sequence(start_value, k_factor, max_iterations)
    next_odds = odds[1:]
    odds.pop()

    collatz_frame = pd.DataFrame({"v_i": odds})
    collatz_frame["sequence_id"] = SEQUENCE_ID
    collatz_frame["sequence_len"] = len(collatz_frame)
    collatz_frame["n"] = collatz_frame.index + 1
    collatz_frame["k_factor"] = k_factor

    collatz_frame["v_1"] = v_1
    collatz_frame["kv_i+1"] = collatz_frame["v_i"].apply(
        commons.next_collatz_number, args=(k_factor,))
    collatz_frame["v_i+"] = next_odds

    collatz_frame["terminal"] = \
        (collatz_frame["v_i+"] == collatz_frame["v_1"]) | \
        (collatz_frame["v_i+"] == 1)

    # Alpha
    collatz_frame["alpha_i"] = collatz_frame["kv_i+1"].apply(commons.trailing_zeros)
    collatz_frame["alpha_i"] = collatz_frame["alpha_i"].astype('int64')
    collatz_frame["alpha_i_max"] = log2(k_factor) + collatz_frame["v_i"].apply(log2)
    collatz_frame["alpha_i_max"] += (1 + 1 / (k_factor * collatz_frame["v_i"])).apply(log2)
    # Round result here to avoid loss of precision errors
    collatz_frame["alpha_i_max"] = collatz_frame["alpha_i_max"].round(9)
    collatz_frame["alpha"] = collatz_frame["alpha_i"].cumsum()
    collatz_frame["alpha_cycle"] = (log2(k_factor) * collatz_frame["n"]).astype('int64') + 1
    collatz_frame["alpha_max"] = log2(v_1) + (collatz_frame["n"] * log2(k_factor))
    collatz_frame["alpha_max"] = collatz_frame["alpha_max"].astype('int64') + 1

    # Lambda
    collatz_frame["bin_len"] = \
        collatz_frame["v_i"].apply(log2).astype('int64') + 1

    collatz_frame["next_bin_len"] = \
        collatz_frame["kv_i+1"].apply(log2).astype('int64') + 1

    collatz_frame["bin_diff"] = collatz_frame["next_bin_len"] - collatz_frame["bin_len"]
    collatz_frame["lambda_i"] = collatz_frame["bin_diff"]
    collatz_frame.loc[collatz_frame["lambda_i"] < 0, "lambda_i"] = 0
    collatz_frame["lambda"] = collatz_frame["lambda_i"].cumsum()

    collatz_frame["lambda_i_min"] = int(log2(k_factor))
    collatz_frame["lambda_i_max"] = int(log2(k_factor) + 1)

    collatz_frame["lambda_hyp"] = (collatz_frame["n"] * log2(k_factor))
    collatz_frame["lambda_min"] = collatz_frame["lambda_hyp"].astype('int64')
    collatz_frame["lambda_max"] = collatz_frame["lambda_hyp"].astype('int64') + 2

    # Omega
    collatz_frame["omega_i"] = collatz_frame["lambda_i"] - collatz_frame["alpha_i"]
    collatz_frame["omega"] = collatz_frame["lambda"] - collatz_frame["alpha"]

    collatz_frame["omega_i_max"] = collatz_frame["lambda_i_max"] - 1
    collatz_frame["omega_max"] = collatz_frame["lambda_max"] - collatz_frame["n"]

    result_frame = collatz_frame[[
        "sequence_id", "sequence_len", "n", "k_factor", "v_1",
        "v_i", "v_i+", "terminal", "alpha_i", "alpha_i_max", "alpha",
        "alpha_cycle", "alpha_max", "bin_len", "next_bin_len",
        "lambda_i", "lambda_i_min", "lambda_i_max",
        "lambda", "lambda_min", "lambda_max",
        "omega_i", "omega_i_max", "omega", "omega_max"]]

    result_frame.columns = [
        "sequence_id", "sequence_len", "n", "k", "v_1",
        "v_i", "v_i+", "terminal", "a_i", "a_i_max", "a",
        "a_cycle", "a_max", "bin_len", "next_bin_len",
        "l_i", "l_i_min", "l_i_max",
        "l", "l_min", "l_max",
        "o_i", "o_i_max", "o", "o_max"]

    return result_frame


# Main method to start the export
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

    for i, k in enumerate(K_FACTORS, start=0):
        logging.info("Generating sequences for k=%d", k)

        for v_1 in V_1_RANGE:
            # Create the sequence
            SEQUENCE_ID = SEQUENCE_ID + 1
            current_frame = _generate_sequence(v_1, k, MAX_ITERATIONS)

            if OUTPUT_FRAME is not None:
                OUTPUT_FRAME = OUTPUT_FRAME.append(current_frame)
            else:
                OUTPUT_FRAME = current_frame
        # Write the frame to file
        if i == 0:
            OUTPUT_FRAME.to_csv(
                FILE_NAME, mode='w', index=False, header=True)
        else:
            OUTPUT_FRAME.to_csv(
                FILE_NAME, mode='a', index=False, header=False)

        OUTPUT_FRAME = None

    # Export finished
    logging.info("Export finished successfully!")
