import base64
import argparse

def reconstruct(path):
    ''' Arg: Path to the file containing the base64 encdoded bytestring'''
    with open(path, 'rb') as file:
        data = file.read()

    decoding = base64.decodebytes(data)
    image_result = open('reconstructed', 'wb')
    image_result.write(decoding)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='decode b64 svg')
    parser.add_argument("--path", required=True, help="Path to Encoding File ")
    args = vars(parser.parse_args())
    reconstruct(args['path'])

