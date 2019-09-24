#!/usr/bin python3

# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE

# Written by Nathan Hamiel (2010)



from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import urllib.request
import sys
import xml.dom.minidom
import socket

# Globals
port = 38080

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = self.path
        fileLog = open("output"+ str(port) + ".log", "a")
        print("----- Message Received (GET) -----")
        lineString = urllib.parse.unquote_plus(request_path, encoding='utf-8') + "\n"
        print("Message (URL Decoded): \n", lineString)
        fileLog.write(lineString)
        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()
        fileLog.close()

    def do_POST(self):
        request_path = self.path
        fileLog = open("output"+ str(port) + ".log", "a")
        print("----- Message Received (POST) -----")
        print("Message:", request_path)
        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0
        xml_string = str(self.rfile.read(length), 'utf-8')      # Note: self.rfile.read(length) returns in bytes NOT in string
        dom = xml.dom.minidom.parseString(xml_string)
        xml_string_fixed = dom.toprettyxml()                    # Makes the XML more pretty
        print("Message content (XML Fixed): \n", xml_string_fixed)
        fileLog.write(xml_string_fixed)
        xml_string_response = '<?xml version="1.0" ?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><POSTMSGOUT xmlns="urn:xeu:connector-bridge:v1"><AssignedON/></POSTMSGOUT></soap:Body></soap:Envelope>'
        self.send_response(200)
        self.send_header("Content-type", "text/application-xml")
        self.end_headers()
        self.wfile.write(xml_string_response.encode("utf-8"))
        fileLog.close()

    do_PUT = do_POST

    do_DELETE = do_GET


def main():

    arg = sys.argv
    global port
    port = int(arg[1])
    print('Listening on', socket.gethostbyname(socket.gethostname()), port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()

    main()