## Brent Grossman
## CS372 
## In Class Challenge 1.1 Character Encoding and Decoding

print_bytes = lambda s: print(' '.join(f'{b:02x}' for b in s))

## step 1
uni_str = "Hi 🙂"

## step 2
utf8_bytes = uni_str.encode('utf-8')
## step 4
"ascii_bytes = uni_str.encode('ascii')"  ## this causes a UnicodeEncodeError 'ascii' code can't encode char '\U0001f642' in position 3: ordinal not in range(128)
## step 5
utf16_bytes = uni_str.encode('utf-16')

## step 3 PRINT THE BYTES utf-8
print_bytes(utf8_bytes)
"print_bytes(ascii_bytes)"
## step 6 PRINT THE BYTES utf-16 they differ from utf-8 in length and what hex values are printed out
print_bytes(utf16_bytes)

## step 7
"utf16_decode_utf8 = utf16_bytes.decode('utf-8')"  ## this causes UnicodeDecodeError 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
"print_bytes(utf16_decode_utf8)"

## step 8 it does match the original string
decode_utf16_bytes = utf16_bytes.decode('utf-16')
print(decode_utf16_bytes)