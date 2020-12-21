import os
import subprocess
def main():

    while True:
        print("Choose the choise:")
        print("[1]: Compress and Decompress with Static Huffman Code")
        print("[2]: Compress and Decompress with Adaptive Huffman Code")
        choise = input("Enter your choise: ")
        if choise == '1':
            os.system("start python static_huffman/huffman.py")
        if choise == '2':
            os.system("start python adaptive_huffman/main.py")
        os.system("cls")

if __name__ == '__main__':
    main()
