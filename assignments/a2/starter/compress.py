"""
Assignment 2 starter code
CSC148, Winter 2020
Instructors: Bogdan Simion, Michael Liut, and Paul Vrbik

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik, Dan Zingaro
"""
from __future__ import annotations
import time
from typing import Dict, Tuple
from utils import *
from huffman import HuffmanTree


# ====================
# Functions for compression


def build_frequency_dict(text: bytes) -> Dict[int, int]:
    """ Return a dictionary which maps each of the bytes in <text> to its
    frequency.

    >>> d = build_frequency_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    # TODO: Implement this function
    dict_b = {}
    for b in text:
        if b in dict_b:
            dict_b[b] += 1
        else:
            dict_b[b] = 1
    return dict_b


def build_huffman_tree(freq_dict: Dict[int, int]) -> HuffmanTree:
    """ Return the Huffman tree corresponding to the frequency dictionary
    <freq_dict>.

    Precondition: freq_dict is not empty.

    >>> freq = {2: 6, 3: 4}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> t == result
    True
    >>> freq = {2: 6, 3: 4, 7: 5}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(2), \
                             HuffmanTree(None, HuffmanTree(3), HuffmanTree(7)))
    >>> t == result
    True
    >>> import random
    >>> symbol = random.randint(0,255)
    >>> freq = {symbol: 6}
    >>> t = build_huffman_tree(freq)
    >>> any_valid_byte_other_than_symbol = (symbol + 1) % 256
    >>> dummy_tree = HuffmanTree(any_valid_byte_other_than_symbol)
    >>> result = HuffmanTree(None, HuffmanTree(symbol), dummy_tree)
    >>> t.left == result.left or t.right == result.left
    True
    """
    # TODO: Implement this function
    if len(freq_dict) == 0:
        return HuffmanTree()
    elif len(freq_dict) == 1:
        left = None
        right = None
        for item in freq_dict:
            left = HuffmanTree(item)
            right = HuffmanTree((item + 1) % 256)
        return HuffmanTree(None, left, right)
    else:  # freq_dict has more than one item.
        lst = []  # list of tuple where (freq, node)
        for value in freq_dict:
            lst.append((freq_dict[value], HuffmanTree(value)))
        lst.sort(reverse=True)

        while len(lst) > 1:
            left_f, left = lst.pop()
            right_f, right = lst.pop()

            tree = HuffmanTree(None, left, right)
            new_f = left_f + right_f
            lst.append((new_f, tree))
            lst.sort(reverse=True)

        return lst.pop()[1]


def get_codes(tree: HuffmanTree) -> Dict[int, str]:
    """ Return a dictionary which maps symbols from the Huffman tree <tree>
    to codes.

    >>> tree = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    """
    # TODO: Implement this function
    if tree.symbol is None and tree.left is None and tree.right is None:
        return {}
    else:
        code_map = {}
        _get_codes_helper(tree, code_map, '')
        return code_map


def _get_codes_helper(tree: HuffmanTree, code_map: dict, curr_code: str) ->\
        None:
    """ Helper function for get_codes. Recursively goes through the tree and
    creates a code for each leaf.
    """
    if tree.is_leaf():
        code_map[tree.symbol] = curr_code
    else:
        _get_codes_helper(tree.left, code_map, curr_code + '0')
        _get_codes_helper(tree.right, code_map, curr_code + '1')


def number_nodes(tree: HuffmanTree) -> None:
    """ Number internal nodes in <tree> according to postorder traversal. The
    numbering starts at 0.

    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(None, HuffmanTree(9), HuffmanTree(10))
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    # TODO: Implement this function
    if not tree.is_leaf():
        _number_nodes_helper(tree, 0)


def _number_nodes_helper(tree: HuffmanTree, num_node: int) -> int:
    """ Helper function for number_nodes. Numbers each internal node in
    postorder starting at 0, until all internal nodes have been numbered.

    """
    if not tree.left.is_leaf():
        num_node = _number_nodes_helper(tree.left, num_node)
    if not tree.right.is_leaf():
        num_node = _number_nodes_helper(tree.right, num_node)
    tree.number = num_node
    return num_node + 1


def avg_length(tree: HuffmanTree, freq_dict: Dict[int, int]) -> float:
    """ Return the average number of bits required per symbol, to compress the
    text made of the symbols and frequencies in <freq_dict>, using the Huffman
    tree <tree>.

    The average number of bits = the weighted sum of the length of each symbol
    (where the weights are given by the symbol's frequencies), divided by the
    total of all symbol frequencies.

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(9)
    >>> tree = HuffmanTree(None, left, right)
    >>> avg_length(tree, freq)  # (2*2 + 7*2 + 1*1) / (2 + 7 + 1)
    1.9
    """
    # TODO: Implement this function
    if freq_dict == {}:
        return 0

    code_map = get_codes(tree)
    all_symbol_freq = 0
    for value in freq_dict:
        if value in code_map:
            all_symbol_freq += freq_dict[value]

    weighted_sum_symbols = 0
    for value in freq_dict:
        if value in code_map:
            weighted_sum_symbols += freq_dict[value] * len(code_map[value])

    return weighted_sum_symbols / all_symbol_freq


def compress_bytes(text: bytes, codes: Dict[int, str]) -> bytes:
    """ Return the compressed form of <text>, using the mapping from <codes>
    for each symbol.

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = compress_bytes(text, d)
    >>> result == bytes([184])
    True
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = compress_bytes(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """
    # TODO: Implement this function
    ans = ''.join([codes[byte] for byte in text if byte in codes])
    ans_b = [bits_to_byte(ans[i:i + 8]) for i in range(0, len(ans), 8)]
    return bytes(ans_b)


def tree_to_bytes(tree: HuffmanTree) -> bytes:
    """ Return a bytes representation of the Huffman tree <tree>.
    The representation should be based on the postorder traversal of the tree's
    internal nodes, starting from 0.

    Precondition: <tree> has its nodes numbered.

    >>> tree = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> right = HuffmanTree(5)
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    >>> tree = build_huffman_tree(build_frequency_dict(b"helloworld"))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))\
            #doctest: +NORMALIZE_WHITESPACE
    [0, 104, 0, 101, 0, 119, 0, 114, 1, 0, 1, 1, 0, 100, 0, 111, 0, 108,\
    1, 3, 1, 2, 1, 4]
    """
    # TODO: Implement this function
    if tree.symbol is None and tree.left is None and tree.right is None:
        return bytes([])
    else:
        byte_l = []
        _tree_to_byte_helper(byte_l, tree)
        return bytes(byte_l)


def _tree_to_byte_helper(byte_l: list, tree: HuffmanTree) -> None:
    """ Mutates byte_l to match the byte representation of tree_to_bytes.

    """
    if not tree.left.is_leaf():
        _tree_to_byte_helper(byte_l, tree.left)
    if not tree.right.is_leaf():
        _tree_to_byte_helper(byte_l, tree.right)

    if tree.left.is_leaf() and tree.right.is_leaf():
        byte_l.extend([0, tree.left.symbol])
        byte_l.extend([0, tree.right.symbol])
    elif tree.left.is_leaf() and not tree.right.is_leaf():
        byte_l.extend([0, tree.left.symbol])
        byte_l.extend([1, tree.right.number])
    elif not tree.left.is_leaf() and tree.right.is_leaf():
        byte_l.extend([1, tree.left.number])
        byte_l.extend([0, tree.right.symbol])
    elif not tree.left.is_leaf() and not tree.right.is_leaf():
        byte_l.extend([1, tree.left.number])
        byte_l.extend([1, tree.right.number])


def compress_file(in_file: str, out_file: str) -> None:
    """ Compress contents of the file <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = build_frequency_dict(text)
    tree = build_huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (tree.num_nodes_to_bytes() + tree_to_bytes(tree) +
              int32_to_bytes(len(text)))
    result += compress_bytes(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression

def generate_tree_general(node_lst: List[ReadNode],
                          root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes nothing about the order of the tree nodes in the list.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(10, None, None), \
HuffmanTree(12, None, None)), \
HuffmanTree(None, HuffmanTree(5, None, None), HuffmanTree(7, None, None)))
    """
    # TODO: Implement this function
    if len(node_lst) == 0:
        return HuffmanTree()
    else:
        return _gen_tree_g_helper(node_lst, root_index)


def _gen_tree_g_helper(node_lst: List[ReadNode],
                       root_index: int) -> HuffmanTree:
    """ Returns a Huffman tree according to generate_tree_general docstring.

    """
    root = node_lst[root_index]
    if root.l_type == 0:
        left = HuffmanTree(root.l_data)
    else:
        left = _gen_tree_g_helper(node_lst, root.l_data)

    if root.r_type == 0:
        right = HuffmanTree(root.r_data)
    else:
        right = _gen_tree_g_helper(node_lst, root.r_data)

    return HuffmanTree(None, left, right)


def generate_tree_postorder(node_lst: List[ReadNode],
                            root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes that the list represents a tree in postorder.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(5, None, None), \
HuffmanTree(7, None, None)), \
HuffmanTree(None, HuffmanTree(10, None, None), HuffmanTree(12, None, None)))
    """
    # TODO: Implement this function
    if len(node_lst) == 0:
        return HuffmanTree()
    else:
        return _gen_tree_p_helper(node_lst, root_index)


def _gen_tree_p_helper(node_lst: List[ReadNode],
                       root_index: int) -> HuffmanTree:
    """ Returns a Huffman tree according to generate_tree_general docstring.

    """
    root = node_lst[root_index]
    if root.l_type == 0 and root.r_type == 0:
        return HuffmanTree(None, HuffmanTree(root.l_data),
                           HuffmanTree(root.r_data))
    elif root.l_type == 1 and root.r_type == 0:
        left = _gen_tree_p_helper(node_lst, root_index - 1)
        return HuffmanTree(None, left, HuffmanTree(root.r_data))
    elif root.l_type == 0 and root.r_type == 1:
        right = _gen_tree_p_helper(node_lst, root_index - 1)
        return HuffmanTree(None, HuffmanTree(root.l_data), right)
    else:  # root.l_type == 1 and root.r_type == 1
        left = _gen_tree_p_helper(node_lst, root_index - 2)
        right = _gen_tree_p_helper(node_lst, root_index - 1)
        return HuffmanTree(None, left, right)


def decompress_bytes(tree: HuffmanTree, text: bytes, size: int) -> bytes:
    """ Use Huffman tree <tree> to decompress <size> bytes from <text>.

    >>> tree = build_huffman_tree(build_frequency_dict(b'helloworld'))
    >>> number_nodes(tree)
    >>> decompress_bytes(tree, \
             compress_bytes(b'helloworld', get_codes(tree)), len(b'helloworld'))
    b'helloworld'
    """
    # TODO: Implement this function
    d = get_codes(tree)
    d_inv = {}

    for key in d:
        d_inv[d[key]] = key

    msg_c = ''.join([byte_to_bits(byte) for byte in text])

    curr_code = ''
    uncoded = []
    for num in msg_c:
        curr_code += num
        if curr_code in d_inv:
            uncoded.append(d_inv[curr_code])
            curr_code = ''
        if len(uncoded) == size:
            break

    return bytes(uncoded)


def decompress_file(in_file: str, out_file: str) -> None:
    """ Decompress contents of <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_int(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(decompress_bytes(tree, text, size))


# ====================
# Other functions

def improve_tree(tree: HuffmanTree, freq_dict: Dict[int, int]) -> None:
    """ Improve the tree <tree> as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to the dictionary of
    symbol frequencies <freq_dict>.

    >>> left = HuffmanTree(None, HuffmanTree(99, None, None), \
    HuffmanTree(100, None, None))
    >>> right = HuffmanTree(None, HuffmanTree(101, None, None), \
    HuffmanTree(None, HuffmanTree(97, None, None), HuffmanTree(98, None, None)))
    >>> tree = HuffmanTree(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> avg_length(tree, freq)
    2.49
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    # TODO: Implement this function

    if not tree.is_leaf():
        tree_dict = get_codes(tree)
        tree_dict_c = {}

        for value in tree_dict:
            if value in freq_dict:
                tree_dict_c[value] = freq_dict[value]

        tree_dict_c_inv = {}
        for key in tree_dict_c:
            tree_dict_c_inv[tree_dict_c[key]] = key

        left_h = _huffman_tree_height(tree.left)
        right_h = _huffman_tree_height(tree.right)

        if left_h >= right_h:
            _improve_tree_helper_left(tree, tree_dict_c_inv)
        else:
            _improve_tree_helper_right(tree, tree_dict_c_inv)


def _improve_tree_helper_right(tree: HuffmanTree, freq_dict_inv: dict) -> dict:
    """ Mutates the tree to fit the docstring description of
    improve_tree.
    """
    if not tree.right.is_leaf():
        freq_dict_inv = _improve_tree_helper_right(tree.right, freq_dict_inv)
    if not tree.left.is_leaf():
        freq_dict_inv = _improve_tree_helper_right(tree.left, freq_dict_inv)
    if tree.left.is_leaf():
        lowest = min(freq_dict_inv)
        tree.left.symbol = freq_dict_inv[lowest]
        del freq_dict_inv[lowest]
    if tree.right.is_leaf():
        lowest = min(freq_dict_inv)
        tree.right.symbol = freq_dict_inv[lowest]
        del freq_dict_inv[lowest]
    return freq_dict_inv


def _improve_tree_helper_left(tree: HuffmanTree, freq_dict_inv: dict) -> dict:
    """ Mutates the tree to fit the docstring description of
    improve_tree.
    """
    if not tree.left.is_leaf():
        freq_dict_inv = _improve_tree_helper_left(tree.left, freq_dict_inv)
    if not tree.right.is_leaf():
        freq_dict_inv = _improve_tree_helper_left(tree.right, freq_dict_inv)
    if tree.left.is_leaf():
        lowest = min(freq_dict_inv)
        tree.left.symbol = freq_dict_inv[lowest]
        del freq_dict_inv[lowest]
    if tree.right.is_leaf():
        lowest = min(freq_dict_inv)
        tree.right.symbol = freq_dict_inv[lowest]
        del freq_dict_inv[lowest]
    return freq_dict_inv


def _huffman_tree_height(tree: HuffmanTree) -> int:
    """ Returns the height of the Huffman Tree.

    """
    if tree.is_leaf():
        return 1
    else:
        l_h = _huffman_tree_height(tree.left)
        r_h = _huffman_tree_height(tree.right)

        return 1 + max(l_h, r_h)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compress_file', 'decompress_file'],
        'allowed-import-modules': [
            'python_ta', 'doctest', 'typing', '__future__',
            'time', 'utils', 'huffman', 'random'
        ],
        'disable': ['W0401']
    })

    mode = input("Press c to compress, d to decompress, or other key to exit: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress_file(fname, fname + ".huf")
        print("Compressed {} in {} seconds."
              .format(fname, time.time() - start))
    elif mode == "d":
        fname = input("File to decompress: ")
        start = time.time()
        decompress_file(fname, fname + ".orig")
        print("Decompressed {} in {} seconds."
              .format(fname, time.time() - start))
