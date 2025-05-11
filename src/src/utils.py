import hashlib

def generate_document_hash(file_content: bytes) -> str:
    return hashlib.sha256(file_content).hexdigest()

def hex_to_bytes32(hex_string: str) -> bytes:
    return bytes.fromhex(hex_string.replace("0x", ""))

def read_file_binary(filepath: str) -> bytes:
    with open(filepath, "rb") as f:
        return f.read()
