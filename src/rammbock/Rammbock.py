from Client import UDPClient, TCPClient
from Server import UDPServer, TCPServer
import Server
import Client
import Encode
from XmlParser import xml2obj
from os import getcwd

class Rammbock(object):

    def __init__(self):
        self.message = None
        self._servers = {}
        self._clients = {}

    def start_udp_server(self, nwinterface, port, ip=Server.DEFAULT_IP, name=Server.DEFAULT_NAME):
        self._servers[name] = UDPServer(name)
        self._servers[name].server_startup(nwinterface, ip, port)

    def start_tcp_server(self, nwinterface, port, ip=Server.DEFAULT_IP, name=Server.DEFAULT_NAME):
        self._servers[name] = TCPServer(name)
        self._servers[name].server_startup(nwinterface, ip, port)

    def check_server_status(self, name=Server.DEFAULT_NAME):
        return name in self._servers

    def check_client_status(self, name=Client.DEFAULT_NAME):
        return name in self._clients

    def connect_to_udp_server(self, host, port, ifname = False, client=Client.DEFAULT_NAME):
        self._clients[client].establish_connection_to_server(host, port, ifname)

    def connect_to_tcp_server(self, host, port, ifname = False, client=Client.DEFAULT_NAME):
        self._clients[client].establish_connection_to_server(host, port, ifname)

    def accept_tcp_connection(self, server=Server.DEFAULT_NAME):
        self._servers[server].accept_connection()

    def close_server(self, name=Server.DEFAULT_NAME):
        self._servers[name].close()
        del self._servers[name]

    def create_udp_client(self, name=Client.DEFAULT_NAME):
        self._clients[name] = UDPClient(name)

    def create_tcp_client(self, name=Client.DEFAULT_NAME):
        self._clients[name] = TCPClient(name)

    def close_client(self, name=Client.DEFAULT_NAME):
        self._clients[name].close()
        del self._clients[name] 

    def client_sends_data(self, packet, name=Client.DEFAULT_NAME): 
        self._clients[name].send_packet(packet)

    def server_receives_data(self, name=Server.DEFAULT_NAME):
        return self._servers[name].server_receives_data()

    def client_receives_data(self, name=Client.DEFAULT_NAME):
        return self._clients[name].receive_data()

    def server_sends_data(self, packet, name=Server.DEFAULT_NAME): 
        self._servers[name].send_data(packet)

    def client_sends_message(self, client_name=Client.DEFAULT_NAME, server_name=Server.DEFAULT_NAME):
        data_bin = Encode.encode_to_bin(self.message)
        self.client_send_data(data_bin)

    def use_application_protocol(self, name, version=1):
        self.application_protocol = name
        self.version = version

    def create_message(self, name):
        print getcwd()
        file = open(getcwd() + '/xml/' + name + '.xml')
        self.message = xml2obj(file)

    def get_header_field(self, name):
        for hdr in self.message.header:
            if hdr.name == name:
                return hdr.data

    def get_information_element(self, name):
        splitted = name.rsplit('.')
        fetchable = next(x for x in self.message.ie if x.name == splitted[0])
        for name in splitted[1:]:
            fetchable = next(x for x in fetchable.ie if x.name == name)
            if fetchable.name == name:
                break
        return fetchable.data
