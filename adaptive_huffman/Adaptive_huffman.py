from Tree import Node, NYT, exchange
from bitarray import bitarray,bits2bytes
import operator
from tqdm import tqdm
class Adaptive_huffman:
    def __init__(self, byte_seq):
        range = (0, 255)
        self.range_size = abs(range[0] - range[1]) + 1
        self.current_num = self.range_size * 2 - 1
        self.byte_seq = byte_seq
        self.tree = Node(0,self.current_num, data=NYT)
        self.all_nodes = [self.tree]
        self.nyt = self.tree

    def encode(self):
        
        def bin_str2bool_list(binary_string):
            return [c == '1' for c in binary_string]
        print("[+]Origin File Size: ",end="")
        print(len(self.byte_seq))
        code = bitarray()
        for symbol in tqdm(self.byte_seq,desc="COMPRESSING",colour='green',unit='bytes'):
            result = self.tree.search(symbol)
            if result['first_appearance']:
                code.extend(result['code'])
                code.frombytes(bytes([symbol]))
            else:
                code.extend(result['code'])
            self.update(symbol,result['first_appearance'])


        remaining_length = bits2bytes(len(code)+3)*8 - (len(code)+3)
        code = (bitarray(bin_str2bool_list('{:03b}'.format(remaining_length))) + code)
        return code
    
    def decode(self):
        def bool_list2int(boolean_list):
            return sum(v << i for i, v in enumerate(reversed(boolean_list)))
        code = bitarray()
        bit_seq = bitarray()
        bit_seq.frombytes(self.byte_seq)
        remaining_length = bool_list2int(bit_seq[:3])
        bit_len = bit_seq.length() - remaining_length
        index = 3
        current_node = None
        print("[+]Origin File Size: ",end="")
        print(len(self.byte_seq))
        pbar = tqdm(total=len(bit_seq))
        while index < bit_len:
            current_node = self.tree
            while current_node.left or current_node.right:
                bit = bit_seq[index]
                current_node = current_node.right if bit else current_node.left
                index += 1
                pbar.update(1)
            if current_node.data == NYT:
                is_first = True
                dec = bit_seq[index:index+8]
                code += dec
                index += 8
                pbar.update(8)
            else:
                is_first = False
                dec = current_node.data
                code += dec
                pbar.update(len(dec))
            self.update(dec, is_first)
            
            pbar.desc = "EXTRACTING"
            pbar.unit = "bits"
            pbar.colour = "yellow"
        return code
    def update(self, data, is_first):
        def find_node(data):
            for node in self.all_nodes:
                if node.data == data:
                    return node
            raise KeyError(f'Cannot find the target node given {data}.')
        current_node = None
        while True:
            if is_first:
                current_node = self.nyt
                self.current_num -= 1
                new_external = Node(1, self.current_num, data=data)
                current_node.right = new_external
                self.all_nodes.append(new_external)

                self.current_num -= 1
                self.nyt = Node(0,self.current_num, data=NYT)
                current_node.left = self.nyt
                self.all_nodes.append(self.nyt)

                current_node.weight += 1
                current_node.data = None
                self.nyt = current_node.left
            else:
                if not current_node:
                    current_node = find_node(data)
                node_max_num = max(
                    (
                        n for n in self.all_nodes
                        if n.weight == current_node.weight
                    ),
                    key=operator.attrgetter('num')
                )
                if node_max_num not in (current_node, current_node.parent):
                    exchange(node_max_num,current_node)
                    current_node = node_max_num
                current_node.weight += 1
            if not current_node.parent:
                break
            current_node = current_node.parent
            is_first = False

def compress(file_in, file_compress):
    in_file = open(file_in,"rb")
    content = in_file.read()
    ada_huff = Adaptive_huffman(content)
    code = ada_huff.encode()

    out_file = open(file_compress,"wb")
    code.tofile(out_file)
def extract(file_in, file_extract):
    in_file = open(file_in, "rb")
    content = in_file.read()
    ada_huff = Adaptive_huffman(content)
    code = ada_huff.decode()

    out_file = open(file_extract,"wb")
    code.tofile(out_file)