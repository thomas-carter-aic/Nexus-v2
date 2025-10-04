"""
Sequence packing: concatenate multiple short sequences into a single training sequence
for improved GPU efficiency.
"""

def pack_sequences(sequences: list, max_length: int = 512):
    """
    Args:
        sequences: list of token id lists
        max_length: max length per packed sequence
    """
    packed = []
    buffer = []

    for seq in sequences:
        if sum(len(s) for s in buffer) + len(seq) <= max_length:
            buffer.append(seq)
        else:
            packed.append([token for s in buffer for token in s])
            buffer = [seq]

    if buffer:
        packed.append([token for s in buffer for token in s])

    return packed
