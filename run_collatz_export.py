"""
This program exports collatz sequences to a csv file.
"""
import logging
from collatz import generator


# Main method to start the export
if __name__ == '__main__':
    N = 1000
    K_FACTORS = [1, 3, 5]
    MAX_START_VALUE = 100
    FILE_NAME = "./data/python_collatz_sequences.csv"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Exporting %d collatz sequences to file %s", N, FILE_NAME)

    # Generate frame to export
    OUTPUT_FRAME = generator.generate_random_sequences(
        n=N, max_start_value=MAX_START_VALUE, k_factors=K_FACTORS)

    # Write the frame to file
    OUTPUT_FRAME.to_csv(FILE_NAME, index=False)

    logging.info("Export finished successfully!")
