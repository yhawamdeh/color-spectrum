from console_gfx import ConsoleGfx


def to_hex_string(data):
    # Convert each number to hexadecimal without zero-padding, except for zero itself
    return ''.join(format(x, 'x') for x in data)


def count_runs(rle_data, limit=15):
    if not rle_data:
        return 0
    count = 1
    run_length = 1
    for i in range(1, len(rle_data)):
        if rle_data[i] == rle_data[i - 1]:
            run_length += 1
            if run_length > limit:
                count += 1  # Start a new run if the limit is exceeded
                run_length = 1  # Reset run length for the new run
        else:
            count += 1
            run_length = 1  # Reset run length for the new run
    return count


def encode_rle(flat_data, limit=15):
    if not flat_data:
        return []
    encoded_data = []
    count = 1
    for i in range(1, len(flat_data)):
        if flat_data[i] == flat_data[i - 1]:
            count += 1
            if count > limit:
                encoded_data.extend([limit, flat_data[i-1]])
                count = 1  # Reset count for the new run that starts with the same value
        else:
            encoded_data.extend([count, flat_data[i - 1]])
            count = 1
    encoded_data.extend([count, flat_data[-1]])
    return encoded_data


def get_decoded_length(rle_data):
    return sum(rle_data[i] for i in range(0, len(rle_data), 2))


def decode_rle(rle_data):
    decoded_data = []
    for i in range(0, len(rle_data), 2):
        decoded_data.extend([rle_data[i + 1]] * rle_data[i])
    return decoded_data


def string_to_data(data_string):
    # Adjusting to handle each hex character individually
    data = []
    for char in data_string:
        # Convert each hex character to an integer and append to the list
        data.append(int(char, 16))
    return data


def to_rle_string(rle_data):
    return ':'.join([f"{length}{format(value, 'x')}" if length != 15 else f"f{format(value, 'x')}" for length, value in zip(rle_data[::2], rle_data[1::2])])


def string_to_rle(rle_string):
    rle_data = []
    segments = rle_string.split(':')
    for segment in segments:
        if segment:  # Check if segment is not empty
            try:
                run_length = int(segment[:-1], 16) if segment[:-1] else 0
                value = int(segment[-1], 16)
                rle_data.extend([run_length, value])
            except ValueError as e:
                print(f"Error processing segment '{segment}': {e}")
                break
    return rle_data


def display_menu():
    print("\nRLE Menu")
    print("--------")
    print("0. Exit")
    print("1. Load File")
    print("2. Load Test Image")
    print("3. Read RLE String")
    print("4. Read RLE Hex String")
    print("5. Read Data Hex String")
    print("6. Display Image")
    print("7. Display RLE String")
    print("8. Display Hex RLE Data")
    print("9. Display Hex Flat Data\n")


def main():
    print('Welcome to the RLE image encoder!\n')
    print('Displaying Spectrum Image:')
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
    print("")

    image_data = None
    rle_data = None
    hex_data = None

    while True:
        display_menu()
        menu_option = input("Select a Menu Option: ")
        if menu_option == "0":
            break
        elif menu_option == "1":
            filename = input("Enter name of file to load: ")
            try:
                image_data = ConsoleGfx.load_file(filename)
            except FileNotFoundError:
                print(f"File not found: {filename}. Make sure the file exists.")
        elif menu_option == "2":
            image_data = ConsoleGfx.test_image
            print("Test image data loaded.")
        elif menu_option == "3":
            rle_string = input("Enter an RLE string to be decoded: ")
            try:
                rle_data = []
                for segment in rle_string.split(':'):
                    run_length = int(segment[:-1], 16)
                    value = int(segment[-1], 16)
                    rle_data.extend([run_length, value])
                decoded_data = decode_rle(rle_data)
            except ValueError as e:
                print(f"An error occurred processing the RLE string: {e}")
        elif menu_option == "4":
            hex_string = input("Enter the hex string holding RLE data: ")
            rle_data = string_to_data(hex_string)
        elif menu_option == "5":
            hex_string = input("Enter the hex string holding flat data: ")
            flat_data = string_to_data(hex_string)
        elif menu_option == "6":
            if image_data is not None:
                print("Displaying image...")
                ConsoleGfx.display_image(image_data)
            else:
                print("No image data to display. Please load an image first.")
        elif menu_option == "7":
            if rle_data is not None:
                print("RLE representation:", to_rle_string(rle_data))
            else:
                print("No RLE data to display.")
        elif menu_option == "8":
            if rle_data is not None:
                compact_hex = ''
                for i in range(0, len(rle_data), 2):
                    run_length, value = rle_data[i], rle_data[i + 1]
                    if run_length == 15:
                        compact_hex += 'f' + format(value, 'x')
                    else:
                        compact_hex += f"{run_length:x}" + format(value, 'x')
                print("RLE hex values:", compact_hex)
            else:
                print("No RLE data to display.")
        elif menu_option == "9":
            if image_data is not None:
                hex_flat_data = to_hex_string(image_data)
                print("Flat hex values:", hex_flat_data)
            else:
                print("No image data to display. Please load an image first.")
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
