
def split_ip(ip_address, subnet_mask):
    network_portion = []
    host_portion = []

    # for each byte in the ip address and subnet mask, zip them together
    # ex. 192.168.17.2 and 255.0.0.0 the 192 and the 255 get paired together, then the 168 and 0 get paired together etc.
    for ip_byte, mask_byte in zip(ip_address, subnet_mask):
        # AND the IP byte with the mask byte to keep only the network bits.
        network_portion.append(ip_byte & mask_byte)
        # invert the mask byte (& 0xff keeps it a positive 0-255 value),
        # then AND with the IP byte to keep only the host bits.
        host_portion.append(ip_byte & (~mask_byte & 0xff))

    return (network_portion, host_portion)


print(split_ip([192,168,17,2], [255,0,0,0]))
print(split_ip([192,168,17,2], [255,255,0,0]))
print(split_ip([192,168,17,2], [255,255,255,0]))
print(split_ip([192,168,17,2], [255,192,0,0]))
print(split_ip([192,168,17,2], [255,255,248,0]))