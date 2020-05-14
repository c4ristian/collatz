"""
This program exports data on the alphas of collatz sequences
into a csv file. The sample is used to validate several mathematical
theorems.
"""
import logging
from math import log2
import pandas as pd
from collatz import commons


def _calculate_alphas(odd_list, k_factor):
    """
    This method calculates the alphas (divisions by two) for a list of
    odd Collatz numbers.

    :param odd_list: The list of odd numbers
    :return: A list of alphas
    """
    alpha_list = []
    for odd in odd_list:
        even = commons.next_collatz_number(odd, k_factor)
        alpha_list.append(commons.calculate_alpha(even))

    return alpha_list


# Main method to start the export
if __name__ == '__main__':
    K_FACTORS = [1, 3, 5, 7, 9]
    MAX_START_VALUE = 3999
    V1_RANGE = range(1, MAX_START_VALUE + 1, 2)
    MAX_ITERATIONS = 100
    N = ((MAX_START_VALUE + 1) / 2) * len(K_FACTORS)
    FILE_NAME = "./data/alpha_sequences.csv"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Exporting %d Collatz sequences to file %s", N, FILE_NAME)

    OUTPUT_FRAME = None
    SEQUENCE_ID = 0

    for k in K_FACTORS:
        for v1 in V1_RANGE:
            # Create the sequence
            SEQUENCE_ID = SEQUENCE_ID + 1
            odds = commons.odd_collatz_sequence(v1, k, MAX_ITERATIONS)
            next_odds = odds[1:]
            odds.pop()

            alphas = _calculate_alphas(odds, k)

            current_frame = pd.DataFrame({"vi": odds})
            current_frame["vi+1"] = next_odds
            current_frame["sequence_id"] = SEQUENCE_ID
            current_frame["sequence_len"] = len(current_frame)
            current_frame["v1"] = v1
            current_frame["n"] = current_frame.index + 1
            current_frame["k_factor"] = k

            current_frame["alpha_i"] = pd.Series(alphas).astype('int64')
            current_frame["alpha_i_max"] = log2(k) + current_frame["vi"].apply(log2)
            current_frame["alpha_i_max"] += (1 + 1/(k * current_frame["vi"])).apply(log2)
            # Round result here to avoid loss of precision errors
            current_frame["alpha_i_max"] = current_frame["alpha_i_max"].round(9)
            current_frame["alpha_sum"] = current_frame["alpha_i"].cumsum()
            current_frame["alpha_pred"] = (log2(k) * current_frame["n"]).astype('int64') + 1
            current_frame["alpha_max"] = log2(v1) + (current_frame["n"] * log2(k))
            current_frame["alpha_max"] = current_frame["alpha_max"].astype('int64') + 1

            print_frame = current_frame[[
                "sequence_id", "sequence_len", "n", "k_factor", "v1",
                "vi", "vi+1", "alpha_i", "alpha_i_max", "alpha_sum",
                "alpha_pred", "alpha_max"]]

            print_frame.columns = [
                "sequence_id", "sequence_len", "n", "k", "v1",
                "vi", "vi+1", "a_i", "a_i_max", "a_sum",
                "a_pred", "a_max"]

            if OUTPUT_FRAME is not None:
                OUTPUT_FRAME = OUTPUT_FRAME.append(print_frame)
            else:
                OUTPUT_FRAME = print_frame

    # Write the frame to file
    print(OUTPUT_FRAME.head().to_string(index=False))
    OUTPUT_FRAME.to_csv(FILE_NAME, index=False)

    logging.info("Export finished successfully!")
