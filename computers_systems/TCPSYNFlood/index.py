import os

def main():
    # Get the current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    path =  f'{cwd}/syn-flood/synflood.pcap'
    
    
    data = read_pcap(path)
    read_packets(data['packets'], data['packet_max_len'])

def read_pcap(file_path: str):
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return None
    print(f"Reading pcap file: {file_path}")
    pcap = {}
    with open(file_path, 'rb') as f:
        # check https://www.ietf.org/archive/id/draft-gharris-opsawg-pcap-01.html
        ########## extract header information (24 octets) ##########
        pcap['header'] = f.read(24)  # 24 octets
        ## check magic number (first 4 octets)
        magic_number = pcap['header'][:4]
        if magic_number != b'\xd4\xc3\xb2\xa1' and magic_number != b'\x4d\x3c\xb2\xa1':
            print(f"Invalid magic number: {magic_number}")
            return None

        ## Major version (2 octets)
        pcap['major_version'] = int.from_bytes(pcap['header'][4:6], byteorder='little')

        ## Minor version (2 octets)
        pcap['minor_version'] = int.from_bytes(pcap['header'][6:8], byteorder='little')
        print(f'Version: {pcap["major_version"]}.{pcap["minor_version"]}')

        ## Maximum number of octets captured for each packet (4 octets)
        pcap['packet_max_len'] = int.from_bytes(pcap['header'][16:20], byteorder='little')
        
        ## LinkType (4 octets)
        pcap['linktype'] = int.from_bytes(pcap['header'][20:24], byteorder='little')

        ## Frame Cyclic Sequence (FCS) (4 bits)
        pcap['fcs'] = pcap['header'][24:25]

        ########## extract packets ##########
        f.seek(24)
        pcap['packets'] = f.read()
    print(pcap['packet_max_len'])
    return pcap

def read_packets(packets: bytes, snapLen: int):
    if packets is None:
        print("No packets to read.")
        return
    packets_len = len(packets)
    print(f"Total packets length: {packets_len} bytes")
    # Here you can implement further processing of the packets if needed
    # For example, you could parse individual packets based on the pcap format
    bytes_read = 0
    result = []
    while bytes_read < packets_len:
        # BSD loopback encapsulation header's size when linktype is 0 (https://www.tcpdump.org/linktypes.html)
        # Each packet has a header of 16 bytes followed by the packet data
        if (bytes_read + 16) > packets_len:
            print("Incomplete packet header found. Stopping.")
            break
        packet = {}
        packet["packet_header"] = packets[bytes_read:bytes_read + 16]
        # timestamp seconds (4 octets)
        packet["ts_sec"] = int.from_bytes(packet["packet_header"][0:4], byteorder='little')

        # timestamp microseconds (4 octets)
        packet["ts_usec"] = int.from_bytes(packet["packet_header"][4:8], byteorder='little')

        # Extract the included length and original length from the packet header
        packet["incl_len"] = int.from_bytes(packet["packet_header"][8:12], byteorder='little')
        packet["orig_len"] = int.from_bytes(packet["packet_header"][12:16], byteorder='little')
        
        #max_len = snapLen if snapLen < packet["incl_len"] else packet["incl_len"]

        # Packet data starts after the 16-byte header
        if bytes_read + 16 + packet["orig_len"] > packets_len:
            print("Incomplete packet data found. Stopping.")
            break
        #packet["actual_length"] = len(packets[bytes_read + 16:bytes_read + 16 + max_len])
        data = packets[bytes_read + 16:bytes_read + 16 + packet["orig_len"]]
        if len(data) > 13:
            packet["is_SYN"] = data[13] & 0x02 != 0  # Check if SYN flag is set
            packet["is_ACK"] = data[13] & 0x10 != 0  # Check if ACK flag is set
        else:
            packet["is_SYN"] = False
            packet["is_ACK"] = False
        # Move to the next packet
        bytes_read += 16 + packet["orig_len"]
    
        result.append(packet)

        ## parse TCP packet header and define packet type (ACK, SYN ACK/SYN, OTHERS)
    print(len(result))

    print(f"Result length: {len(result)} packets processed.")
    for packet in result:
        if packet["is_SYN"] or packet["is_ACK"]:
            print(packet)
    return result

if __name__ == "__main__":
    main()