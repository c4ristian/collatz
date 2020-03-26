"""
This program exports binary data of collatz sequences to a csv file.
"""
import logging
from math import log2
from collatz import generator
from collatz import cycles
from collatz.commons import trailing_zeros


# Helper method to predict the alpha that would lead to a cycle
def _predict_alpha(cycle_length: int):
    return cycles.predict_cycle_alpha(k, cycle_length)


# Main method to start the export
if __name__ == '__main__':
    K_FACTORS = [3]
    MAX_START_VALUE = 10000
    MAX_ITERATIONS = 300
    N = MAX_START_VALUE
    FILE_NAME = "./data/python_binary_sequences.csv"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Exporting %d collatz sequences to file %s", N, FILE_NAME)

    OUTPUT_FRAME = None

    for k in K_FACTORS:
        for x1 in range(1, MAX_START_VALUE, 2):
            # Analyse the sequence
            current_frame = generator.generate_collatz_sequence(x1, k, MAX_ITERATIONS)
            current_frame["x1"] = x1

            # Filter for odd numbers
            current_frame = current_frame[current_frame["odd"] == 1]
            current_frame = current_frame.reset_index(drop=True)
            current_frame["collatz_index"] = current_frame.index + 1

            # Derive additional fields
            current_frame["alpha"] = current_frame["next_collatz"].apply(
                trailing_zeros).astype('int64')
            current_frame["alpha_sum"] = current_frame["alpha"].cumsum()
            current_frame["alpha_pred"] = current_frame["collatz_index"].apply(
                _predict_alpha)

            current_frame["growth"] = current_frame["next_odd"] - current_frame["x1"]
            current_frame["next_bin_len"] = current_frame["next_odd"].apply(
                log2).astype('int64') + 1

            current_frame["bin_growth"] = \
                current_frame["next_bin_len"] - current_frame["bin_len"]

            current_frame["bin_growth_sum"] = current_frame["bin_growth"].cumsum()

            current_frame["beta"] = 1 + 1 / (k * current_frame["collatz"])
            current_frame["beta_prod"] = current_frame["beta"].cumprod()

            if OUTPUT_FRAME is not None:
                OUTPUT_FRAME = OUTPUT_FRAME.append(current_frame)
            else:
                OUTPUT_FRAME = current_frame

    # Write the frame to file
    print(OUTPUT_FRAME.head().to_string(index=False))
    OUTPUT_FRAME.to_csv(FILE_NAME, index=False)

    logging.info("Export finished successfully!")
