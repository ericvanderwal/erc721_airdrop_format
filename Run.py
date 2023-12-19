import csv
import os
import re
import json

# Variables
path = 'addresses.csv'
output_path = 'chunked_address.txt'
chunk_size = 100
start_token_id = 1000


def read_column_a(file_path):
    """
    Reads the first column of a CSV file into a list.
    :param file_path: The path to the CSV file.
    :return: A list of values in the first column.
    """
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader if row]


def count_lines_in_column_a(column_a_values):
    """
    Counts the number of lines in the provided list.
    :param column_a_values: List of values from Column A.
    :return: Total count of lines.
    """
    return len(column_a_values)


def find_duplicates(column_a_values):
    """
    Identifies duplicates in the provided list.
    :param column_a_values: List of values from Column A.
    :return: Dictionary of duplicates and their occurrences.
    """
    seen = {}
    duplicates = {}
    for i, value in enumerate(column_a_values):
        if value in seen:
            duplicates.setdefault(value, []).append(i)
        else:
            seen[value] = i

    for addr, indices in duplicates.items():
        print(f"Address '{addr}' appears {len(indices)} times at lines {indices}")
    return duplicates


def is_valid_eth_address(address):
    """
    Validates Ethereum address.
    :param address: Ethereum address to validate.
    :return: True if valid, False otherwise.
    """
    return len(address) == 42 and re.fullmatch(r'0x[a-fA-F0-9]{40}', address)


def chunk_addresses(column_a_values, chunk_size, start_token_id, output_file_path='chunked_address.txt'):
    """
    Chunks the addresses and writes them to a file in JSON format.
    :param column_a_values: List of Ethereum addresses.
    :param chunk_size: Size of each chunk.
    :param start_token_id: Starting token ID.
    :param output_file_path: Path to the output file.
    """
    with open(output_file_path, 'w') as file:
        for i in range(0, len(column_a_values), chunk_size):
            chunk = column_a_values[i:i + chunk_size]
            formatted_chunk = [
                {"recipient": address, "tokenId": start_token_id + j}
                for j, address in enumerate(chunk)
            ]
            json_chunk = json.dumps(formatted_chunk)
            file.write(json_chunk + "\n\n")
            start_token_id += len(chunk)

# print(f"Chunked addresses written to {output_file_path}")


# Main code executes here
if os.path.exists(path):

    #Get addresses and print the total number found in debug
    column_a_values = read_column_a(path)
    print(f"Total addresses: {count_lines_in_column_a(column_a_values)}")

    # Check the addresses are valid using a basic check
    invalid_addresses = [addr for addr in column_a_values if not is_valid_eth_address(addr)]
    if invalid_addresses:
        print("Invalid Ethereum Addresses:")
        for addr in invalid_addresses:
            print(addr)
    else:
        print("All addresses are valid.")

    # Check for any duplicates.
    duplicates = find_duplicates(column_a_values)
    if duplicates:
        print("Duplicates found.")
    else:
        print("No duplicates found.")

    # Save the chunked and formatted files to a text file
    chunk_addresses(column_a_values, chunk_size, start_token_id, output_path)

else:
    print(f"File not found: {path}")
