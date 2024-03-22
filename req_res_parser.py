import sys
import argparse
import xml.etree.ElementTree as ET

def parse_burp_xml(input_file, parse_request, parse_response, output_file=None):
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()

        output = sys.stdout if output_file is None else open(output_file, 'w')

        with output:
        
            for item in root.findall('item'):
                request = item.find('request').text
                response = item.find('response').text

                if parse_request:
                    request_lines = request.split("\n")
                    if "" in request_lines:
                        empty_line_index = request_lines.index("")
                        request_body = "\n".join(request_lines[empty_line_index +1:])

                        output.write("\n\n")
                        output.write(request_body)
            
                if parse_response:
                    response_lines = response.split("\n")
                    if "" in response_lines:
                        empty_line_index = response_lines.index("")
                        response_body = "\n".join(response_lines[empty_line_index +1:])

                        output.write("\n\n")
                        output.write(response_body)

        if output_file:
            print(f"Parsed results saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except ET.ParseError:
        print(f"Error: Invalid XML format in '{input_file}'.")

def main():
    parser = argparse.ArgumentParser(description='Parse requests and responses from Burp Suite XML export.')
    parser.add_argument('-i', '--input', type=str, help='Path to the input XML file')
    parser.add_argument('-o', '--output', type=str, help='Path to the output file (optional)')
    parser.add_argument('-q', '--request', action='store_true', help='Parse the request body')
    parser.add_argument('-s', '--response', action='store_true', help='Parse the response body')
    
    args = parser.parse_args()

    if args.input:
        parse_burp_xml(args.input, args.request, args.response, args.output)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()