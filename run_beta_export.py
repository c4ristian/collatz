"""
This program exports betas of collatz sequences to a csv file.
"""
import logging
from collatz import generator
from collatz.commons import trailing_zeros


# Main method to start the export
if __name__ == '__main__':
    K_FACTORS = [1]
    MAX_START_VALUE = 1000
    MAX_ITERATIONS = -1
    N = MAX_START_VALUE
    FILE_NAME = "./data/python_beta_sequences_1.csv"

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

            current_frame["beta"] = 1 + 1 / (k * current_frame["collatz"])
            current_frame["beta_prod"] = current_frame["beta"].cumprod()

            filtered_frame = current_frame.tail(1)

            if OUTPUT_FRAME is not None:
                OUTPUT_FRAME = OUTPUT_FRAME.append(filtered_frame)
            else:
                OUTPUT_FRAME = filtered_frame

    # Write the frame to file
    OUTPUT_FRAME = OUTPUT_FRAME.sort_values(by='beta_prod', ascending=False)

    print(OUTPUT_FRAME.head().to_string(index=False))
    OUTPUT_FRAME.to_csv(FILE_NAME, index=False)

    logging.info("Export finished successfully!")
