#!/usr/bin/python3

import re
from huffman.file import File
from huffman.tree import Tree
import sys


def compress(filename: str, filecompress:str):
    file = File(filename,filecompress)
    file.countBytes()
    file.calculateProbabilities()
    tree = Tree()
    tree.build(file.byteProbabilities)
    rawCodebook = tree.countLabelByLength()
    canonicalTree = Tree()
    canonicalCodebook = canonicalTree.canonicallyBuild(rawCodebook)
    # tree.print()
    # print(rawCodebook)
    # for k, v in canonicalCodebook.items():
    #     print(k)
    #     print(v)
    # print(canonicalCodebook)
    file.calculateSize(canonicalCodebook)
    file.compress(rawCodebook, canonicalCodebook)
    file.probStat()


def decompress(filename: str,fileextract:str):
    file = File(filename, fileextract)
    codebook = file.readHeader()
    tree = Tree()
    # print(tree.canonicallyBuild(codebook))
    tree.canonicallyBuild(codebook)
    file.decompress(tree)


def main():
    #if len(sys.argv) == 3:
    #    if sys.argv[1] == '-c':
    #        compress(sys.argv[2])
    #    elif sys.argv[1] == '-d':
    #        if re.search('.compressed$', sys.argv[2]):
    #            decompress(sys.argv[2])
    #    else:
    #        print('Invalid comand !!!')
    #else:
    #    print('Command not found !!!')

    file_in = 'static_huffman\Lena.raw'
    file_compress = 'static_huffman\compress'
    compress(file_in, file_compress)
    file_extract = 'static_huffman\extract.raw'
    decompress(file_compress,file_extract)
    print("Extracting:.........")
    print("Extract Completed!")
    input("Press ENTER to exit...")

if __name__ == "__main__":
    main()
