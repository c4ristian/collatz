"""
This program exports basic data on Collatz sequences into a csv file.
Both even and odd Collatz numbers are included. The sample is used
for the training of machine learning models.
"""

import shutil
import logging
from math import log2
import pandas as pd
from collatz import commons


def _generate_full_sequence(sequence_id: int, start_value: int,
                            k_factor: int, max_iterations: int):
    """
    This method generates a full Collatz sequence containing odd and even numbers.

    :param sequence_id: ID of the sequence.
    :param start_value: The integer value to start with. The value must be a
        natural number > 0.
    :param k_factor: The factor by which odd numbers are multiplied in the sequence.
    :param max_iterations: The maximum number of iterations performed
        before the method exits.
    :return: The Collatz sequence as a pandas data frame.
    """
    collatz = commons.collatz_sequence(
        start_value, k_factor, max_iterations=max_iterations)

    next_collatz = collatz[1:]
    collatz.pop()

    collatz_frame = pd.DataFrame({"x_i": collatz})
    collatz_frame["sequence_id"] = sequence_id
    collatz_frame["sequence_len"] = len(collatz_frame)
    collatz_frame["n"] = collatz_frame.index + 1
    collatz_frame["k_factor"] = k_factor
    collatz_frame["x_i_odd"] = collatz_frame["x_i"] % 2 == 1
    collatz_frame["x_i+"] = next_collatz
    collatz_frame["x_1"] = start_value

    # Logs
    collatz_frame["x_i_log2"] = collatz_frame["x_i"].apply(log2)
    collatz_frame["x_i+_log2"] = collatz_frame["x_i+"].apply(log2)
    collatz_frame["x_1_log2"] = log2(start_value)

    collatz_frame["terminal"] = collatz_frame["x_i+"] == 1
    collatz_frame["cycle"] = collatz_frame["x_i+"] == collatz_frame["x_1"]

    result_frame = collatz_frame[[
        "sequence_id", "sequence_len", "n", "k_factor", "x_1",
        "x_i", "x_i_odd", "x_i+", "x_i_log2", "x_i+_log2", "x_1_log2",
        "terminal", "cycle"]]

    result_frame.columns = [
        "sequence_id", "sequence_len", "n", "k", "x_1",
        "x_i", "x_i_odd", "x_i+", "x_i_log2", "x_i+_log2", "x_1_log2",
        "terminal", "cycle"]

    return result_frame


def _main():
    """
    This method executes the program.
    :return: None.
    """
    k_factors = [1, 3, 5, 7, 9]
    max_start_value = 2000
    x_1_range = range(1, max_start_value + 1)
    max_iterations = 100
    sequence_count = max_start_value * len(k_factors)

    export_name = "basic_export"
    dest_file_name = "./data/" + export_name + ".csv"
    tmp_file_name = "./data/" + export_name + "_tmp" + ".csv"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Exporting %d Collatz sequences to file %s", sequence_count, dest_file_name)

    sequence_id = 0
    write_mode = True

    for k in k_factors:
        logging.info("Generating sequences for k=%d", k)

        for x_1 in x_1_range:
            # Create the sequence
            sequence_id = sequence_id + 1
            current_frame = _generate_full_sequence(
                sequence_id, x_1, k, max_iterations)

            # Write the frame to file
            mode_char = "w" if write_mode else "a"
            current_frame.to_csv(
                tmp_file_name, mode=mode_char, index=False, header=write_mode)
            write_mode = False

    # Moving tmp file to destination file
    logging.info("Moving temp file to destination file")
    shutil.move(tmp_file_name, dest_file_name)

    # Export finished
    logging.info("Export finished successfully!")


# Main method to start the export
if __name__ == '__main__':
    _main()
