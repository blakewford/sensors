import socket

mqtt_port = 1883

# Control packet type
RESERVED=0,
CONNECT=1,
CONNACK=2,
PUBLISH=3,
PUBACK=4,
PUBREC=5,
PUBREL=6,
PUBCOMP=7,
SUBSCRIBE=8,
SUBACK=9,
UNSUBSCRIBE=10,
UNSUBACK=11,
PINGREQ=12,
PINGRESP=13,
DISCONNECT=14,
#RESERVED=15

class packet_header:
    def __init__(self, mqtt_type, remaining):
        self.mqtt_type = mqtt_type
        self.remaining = remaining

class connect_header:
    header = packet_header(0x10, 0x2C)
    protocol = 'MQTT'
    protocol_length = len(protocol)
    level = 0x04
    flags = 0xC2
    keep_alive = 0x3C

    # Technically variable
    client_id = 'MONITOR'
    client_id_length = len(client_id)

class mqtt:
    def __init__(self, address, username, password, simulated):
        self.address = address
        self.username = username
        self.password = password
        self.simulated = simulated
        if(not simulated):
            self.socket = socket.socket()
            self.socket.connect(socket.getaddrinfo('homeassistant.lan', mqtt_port)[0][-1])

    def connect(self):
        header = connect_header()
        b = bytearray()
        b.extend(header.header.mqtt_type.to_bytes(1, 'big'))
        b.extend(header.header.remaining.to_bytes(1, 'big'))
        b.extend(header.protocol_length.to_bytes(2, 'big'))
        b.extend(header.protocol.encode('utf-8'))
        b.extend(header.level.to_bytes(1, 'big'))
        b.extend(header.flags.to_bytes(1, 'big'))
        b.extend(header.keep_alive.to_bytes(2, 'big'))
        b.extend(header.client_id_length.to_bytes(2, 'big'))
        b.extend(header.client_id.encode('utf-8'))

        b.extend(len(self.username).to_bytes(2, 'big'))
        b.extend(self.username)
        b.extend(len(self.password).to_bytes(2, 'big'))
        b.extend(self.password)

        packet = bytes(b)
        if(self.simulated):
            print(packet)
        else:
            self.socket.write(packet)
            data = self.socket.read(4)
        return
    def publish(self, topic, message):
        topic_length = len(topic)
        payload_length = len(message)

        header = packet_header(0x30, topic_length + payload_length + 2)
        b = bytearray()
        b.extend(header.mqtt_type.to_bytes(1, 'big'))
        b.extend(header.remaining.to_bytes(1, 'big'))
        b.extend(topic_length.to_bytes(2, 'big'))
        b.extend(topic)
        b.extend(message)
        packet = bytes(b)
        if(self.simulated):
            print(packet)
        else:
            self.socket.write(packet)
        return
    def disconnect(self):
        if(not self.simulated):
            self.socket.close()
        return