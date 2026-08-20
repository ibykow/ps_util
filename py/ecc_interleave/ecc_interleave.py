import os
import sys
import argparse
import struct  # Added to cleanly store original file size metadata
from reedsolo import RSCodec, ReedSolomonError

PARITY_BYTES = 32
CHUNK_SIZE = 223
BLOCK_SIZE = 255

# Initialize Reed-Solomon codec
rs = RSCodec(PARITY_BYTES)


def interleave_data(raw_bytes, stride=BLOCK_SIZE):
    """
    Arranges data into a grid of 'stride' width and reads it out column-by-column.
    Accepts bytearray or bytes, returns an interleaved bytearray.
    """
    remainder = len(raw_bytes) % stride
    if remainder != 0:
        padding_needed = stride - remainder
        # If it's a bytearray, we can extend in-place efficiently
        if isinstance(raw_bytes, bytearray):
            raw_bytes.extend(b'\x00' * padding_needed)
        else:
            raw_bytes += b'\x00' * padding_needed
        
    num_rows = len(raw_bytes) // stride
    interleaved = bytearray(len(raw_bytes))
    
    idx = 0
    for col in range(stride):
        for row in range(num_rows):
            interleaved[idx] = raw_bytes[row * stride + col]
            idx += 1
            
    return interleaved


def deinterleave_data(interleaved_bytes, stride=BLOCK_SIZE):
    """
    Reverses the grid mapping, scattering sequential burst errors 
    back into isolated rows.
    """
    num_rows = len(interleaved_bytes) // stride
    deinterleaved = bytearray(len(interleaved_bytes))
    
    idx = 0
    for col in range(stride):
        for row in range(num_rows):
            deinterleaved[row * stride + col] = interleaved_bytes[idx]
            idx += 1
            
    return deinterleaved


def encode_file(input_path, output_path):
    """Chunks a file, applies Reed-Solomon ECC, interleaves, and prefixes original size."""
    rs_encoded_data = bytearray()
    
    # Track original size to safely drop trailing null padding later
    original_size = os.path.getsize(input_path)
    
    with open(input_path, 'rb') as f_in:
        while True:
            chunk = f_in.read(CHUNK_SIZE)
            if not chunk:
                break
                
            if len(chunk) < CHUNK_SIZE:
                chunk = chunk.ljust(CHUNK_SIZE, b'\x00')
                
            encoded_chunk = rs.encode(chunk)
            rs_encoded_data.extend(encoded_chunk)
            
    # Interleave the mutable bytearray directly without casting
    interleaved_data = interleave_data(rs_encoded_data, stride=BLOCK_SIZE)
    
    with open(output_path, 'wb') as f_out:
        # Prepended 8-byte header storing the exact original file size (64-bit integer)
        # This guarantees your recovered files match bit-for-bit, zero padding removed.
        f_out.write(struct.pack("<Q", original_size))
        f_out.write(interleaved_data)
            
    print(f"[+] ECC and Global Interleaving complete. Saved to: {output_path}")


def decode_file(input_path, output_path):
    """Reads an ECC-encoded file, fixes errors, strips padding, and recovers data."""   
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        # Read the size header first
        header = f_in.read(8)
        if len(header) < 8:
            raise RuntimeError("Fatal: File is missing its size metadata header.")
        original_size = struct.unpack("<Q", header)[0]

        block_count = 0
        corrected_total = 0
        bytes_written = 0

        # Read and de-interleave the rest of the payload
        deinterleaved_data = deinterleave_data(f_in.read())
        view = memoryview(deinterleaved_data)
        chunks = (view[i : i + BLOCK_SIZE] for i in range(0, len(view), BLOCK_SIZE))

        for block in chunks:
            block_count += 1
            try:
                decoded_data, _, corrected_pos = rs.decode(block)
                if corrected_pos:
                    corrected_total += len(corrected_pos)
                    print(f"Block {block_count}: Fixed {len(corrected_pos)} bytes.")
                
                # Truncate any null padding on the final block write
                if bytes_written + len(decoded_data) > original_size:
                    remaining_bytes = original_size - bytes_written
                    f_out.write(decoded_data[:remaining_bytes])
                    bytes_written += remaining_bytes
                else:
                    f_out.write(decoded_data)
                    bytes_written += len(decoded_data)
                    
            except ReedSolomonError:
                raise RuntimeError(f"Fatal: Unrecoverable corruption in block {block_count}.")
                
    print(f"[+] ECC decoding complete. Total bytes repaired: {corrected_total}. Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Data ECC Interleaver")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encode", action="store_true")
    group.add_argument("-d", "--decode", action="store_true")
    parser.add_argument("filename")
    
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        print("[-] File not found.")
        sys.exit(1)
            
    if args.encode:
        encode_file(args.filename, f"{args.filename}.ecc")
    else:
        try:
            decode_file(args.filename, f"{args.filename}.decc")
        except RuntimeError as e:
            print(f"[-] {e}")

# Encode a 100 KB file to an audio track at 2400 baud
minimodem --tx 2400 -f payload.bin > data_track.wav

# Decode the recorded audio back into binary
minimodem --rx 2400 -f recorded_tape.wav > recovered_payload.bin

if __name__ == "__main__":
    main()