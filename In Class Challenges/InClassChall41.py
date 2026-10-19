
def pack_ip(ip):
    # IMPLEMENT ME
    ip_bytes = b""
    ip_nums = ip.split(".")
    for nums in ip_nums:
        byte = int(nums)
        ip_bytes += bytes([byte])
    return ip_bytes

    
    
test_data = (
    ("0.0.0.0", b'\x00\x00\x00\x00'),
    ("127.0.0.1", b'\x7f\x00\x00\x01'),
    ("255.0.255.0", b'\xff\x00\xff\x00'),
    ("127.1.127.1", b'\x7f\x01\x7f\x01'),
    ("16.16.16.16", b'\x10\x10\x10\x10'),
    ("1.1.1.1", b'\x01\x01\x01\x01'),
    ("1.2.3.4", b'\x01\x02\x03\x04'),
)

for ip, packed_ip in test_data:
    output = f"testing: {ip} -> {packed_ip}"
    print(f"{output:<45}", end="")
    print('OK' if pack_ip(ip) == packed_ip else 'FAIL')