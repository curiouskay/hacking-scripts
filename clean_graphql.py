import sys
import argparse
import re

def parse_burp_xml(input_file, output_file=None, filters=None):
    if filters is None:
        filters = ["Float", "String", "Boolean", "typename"]
    try:
        with open(input_file, 'r') as file:
            input_text = file.read().replace('\\n', ' ')
            cleaned_text = re.sub(r'[^a-zA-Z0-9\_ ]+', ' ', input_text)
            words = cleaned_text.split()
            filtered_words = [word for word in words if word not in filters]
            sorted_unique_words = sorted(set(filtered_words))
            output_text = "\n".join(sorted_unique_words)
            output = sys.stdout if output_file is None else open(output_file, 'w')
            with output:
                output.write(output_text)
            if output_file:
                print(f"Parsed results saved to '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")

def main():
    parser = argparse.ArgumentParser(description='Clean up graphql to only contain keywords. Sorted and unqiue.')
    parser.add_argument('-i', '--input', type=str, help='Path to the input XML file')
    parser.add_argument('-o', '--output', type=str, help='Path to the output file (optional)')
    parser.add_argument('-f', '--filter', nargs='+', help='List of words to filter out (by default: Float, String, Boolean, typename)')
    args = parser.parse_args()

    if args.input:
        parse_burp_xml(args.input, args.output, args.filter)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()