import os

def main():
    # Get the current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    path =  f'{cwd}/syn-flood/synflood.pcap'
    
    ## Read pcap file's header and extract packets
    data = read_pcap(path)
    ## Read packets headers from pcap file and return a list of packets with their information
    if data['linktype'] == 0:
        data['packets'] = read_TCP_IP_packets(data['packets'], data['packet_max_len'])
    else:
        print('packets not from loopback')


## Read pcap file and return a dictionary with file header (24 octets) and data
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

## Read packets header (16 octets)and data, and return a list of packets with their information
def read_TCP_IP_packets(packets: bytes, snapLen: int):
    if packets is None:
        print("No packets to read.")
        return
    bytes_read = 0
    count_SYN = 0
    count_ACK = 0
    responses = 0
    questions = 0
    result = []
    packets_len = len(packets)
    while bytes_read < packets_len:
        # Each packet has a header of 16 bytes followed by the packet data
        if (bytes_read + 16) > packets_len:
            print("Incomplete packet header found. Stopping.")
            break
        packet = {}
        packet["packet_header"] = packets[bytes_read:bytes_read + 16]

        # timestamps (4 octets)
        packet["ts_sec"] = int.from_bytes(packet["packet_header"][0:4], byteorder='little')
        packet["ts_usec"] = int.from_bytes(packet["packet_header"][4:8], byteorder='little')

        # Extract the included length and original length from the packet header
        packet["incl_len"] = int.from_bytes(packet["packet_header"][8:12], byteorder='little')
        packet["orig_len"] = int.from_bytes(packet["packet_header"][12:16], byteorder='little')
        
        # Packet data starts after the 16-byte header
        if bytes_read + 16 + packet["orig_len"] > packets_len:
            print("Incomplete packet data found. Stopping.")
            break
        packet['packet_payload'] = packets[bytes_read + 16 :bytes_read + 16 + packet["incl_len"]]

        # BSD loopback encapsulation header's size when linktype is 0 (https://www.tcpdump.org/linktypes.html)
        # for linktype 0, header is 4 octets
        packet["packet_link_layer_header"] = int.from_bytes(packet['packet_payload'][:4], byteorder='little')
        ## should be ipv4
        assert packet["packet_link_layer_header"] == 2

        # IPv4 header (https://en.wikipedia.org/wiki/IPv4#Header)
        ## check protocol is TCP
        packet["protocol"] = int.from_bytes(packet['packet_payload'][4 + 9:4 + 9 + 1], byteorder='big')
        assert packet["protocol"] == 6

        ## ip_header_length is the number of 32 bits word (<< 2 to have it in number of bytes)
        packet["ip_header_length"] = (packet['packet_payload'][4: 4 + 1][0] & 0x0f) << 2
        packet["source_ip"] = int.from_bytes(packet['packet_payload'][4 + 12 : 4 + 12 + 4], byteorder='big')

        # TCP header
        packet["TCP"] = packet['packet_payload'][4 + packet["ip_header_length"]:]
        TCP_flags = packet["TCP"][13]
        is_SYN = TCP_flags & 0x02 != 0
        is_ACK = TCP_flags & 0x10 != 0
        
        if is_SYN:
            count_SYN += 1
        if is_ACK :
            count_ACK += 1
        
        source_port = int.from_bytes(packet["TCP"][:2], byteorder='big')
        destination_port = int.from_bytes(packet["TCP"][2:4], byteorder='big')
        print(destination_port, source_port)
        if source_port == 80 and is_ACK:
            responses += 1

        if destination_port == 80 and is_SYN and not is_ACK:
            questions += 1
  



        """ read_TCP_IP_packets(data['packets'])

        data = packets[bytes_read + 16:bytes_read + 16 + packet["orig_len"]]
        if len(data) > 13:
            packet["is_SYN"] = data[13] & 0x02 != 0  # Check if SYN flag is set
            packet["is_ACK"] = data[13] & 0x10 != 0  # Check if ACK flag is set
        else:
            packet["is_SYN"] = False
            packet["is_ACK"] = False
        # Move to the next packet
        
     """
        bytes_read += 16 + packet["orig_len"]
        result.append(packet)
    print('count_SYN: ', count_SYN)
    print('count_ACK: ', count_ACK)
    print(f'{(responses / float(questions))*100} %')

    return result
        ## parse TCP packet header and define packet type (ACK, SYN ACK/SYN, OTHERS)
"""     print(len(result))

    print(f"Result length: {len(result)} packets processed.")
    for packet in result:
        if packet["is_SYN"] or packet["is_ACK"]:
            print(packet) """
    


if __name__ == "__main__":
    main()