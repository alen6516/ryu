#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct
from . import packet_base


class dns(packet_base.PacketBase):
    """DNS header encoder/decoder class.

    An instance has the following attributes at least.
    __init__ takes the corresponding args in this order.

    =================================== ========================================================
    Attribute                           Description
    =================================== ========================================================
    Identification                      Transaction ID, used to match the response to the query
    QR                                  query/response flag
    Opcode                              operation code
    DNSFlag                             dns flags
    RCode                               return code
    Total Questions                     number of questions
    Total Answers                       number of answers
    Total Authority Resource Records    number of authority resource records
    Total Additional Resource Records   number of additional resource records
    =================================== ========================================================
    """

    _PACK_STR = '!HHHHHH'
    _MIN_LEN = struct.calcsize(_PACK_STR)

    def __init__(self,
        identification,
        qr,
        opcode,
        dnsflags,
        rcode,
        total_questions,
        total_answers,
        total_authority,
        total_additional):

        super(dns, self).__init__()
        self.identification = identification
        self.qr = qr
        self.opcode = opcode
        self.dnsflags = dnsflags
        self.rcode = rcode
        self.total_questions = total_questions
        self.total_answers = total_answers
        self.total_authority = total_authority
        self.total_additional = total_additional


    @classmethod
    def parser(cls, buf):
        identification, temp_data, total_questions, total_answers, total_authority, total_additional = struct.unpack_from(cls._PACK_STR, buf)
        qr, opcode, dnsflags, rcode = unpack_second_word(temp_data)
        dnsflags = unpack_dns_flags(dnsflags)
        next_cls = dns_question

        if qr == 1:
            next_cls = dns_answer

        return (cls(
            identification,
            qr,
            opcode,
            dnsflags,
            rcode,
            total_questions,
            total_answers,
            total_authority,
            total_additional
            ),
            next_cls,
            buf[dns._MIN_LEN:])

    def serialize(self, payload, prev):
        dnsflags = pack_dns_flags(self.dnsflags)
        temp_data = pack_second_word(self.qr, self.opcode, dnsflags, self.rcode)

        return struct.pack(dns._PACK_STR,
                           self.identification,
                           temp_data,
                           self.total_questions,
                           self.total_answers,
                           self.total_authority,
                           self.total_additional)

    def __str__(self):
        # for debugging
        return "ID : " + str(self.identification) + "\n" +\
               "qr : "  + str(self.qr) + "\n" +\
               "opcode : " + str(self.opcode) + "\n" +\
               "dnsflags : " + str(self.dnsflags) + "\n" +\
               "rcode : " + str(self.rcode) + "\n" +\
               "total_questions : " + str(self.total_questions) + "\n" +\
               "total_answers : " + str(self.total_answers) + "\n" +\
               "total_authority : " + str(self.total_authority) + "\n" +\
               "total_additional : " + str(self.total_additional) + "\n"

def unpack_second_word(temp_data):
    qr = temp_data >> 15
    opcode = (temp_data >> 11) & 0xf
    dnsflags = (temp_data >> 4) & 0x7f
    rcode = temp_data & 0xf
    return (qr, opcode, dnsflags, rcode)

def pack_second_word(qr, opcode, dnsflags, rcode):
    temp_data = 0
    temp_data = temp_data | qr << 15
    temp_data = temp_data | opcode << 11
    temp_data = temp_data | dnsflags << 4
    temp_data = temp_data | rcode
    return temp_data


def unpack_dns_flags(dnsflags):
    # flags
    # use dict to save it
    # {'AA':0, 'TC': 0, 'RD': 0, 'RA': 0, 'Z': 0, 'AD': 0, 'CD': 0}
    AA = dnsflags >> 6
    TC = (dnsflags >> 5) & 0x01
    RD = (dnsflags >> 4) & 0x01
    RA = (dnsflags >> 3) & 0x01
    Z  = (dnsflags >> 2) & 0x01
    AD = (dnsflags >> 1) & 0x01
    CD = dnsflags & 0x01
    return {'AA':AA, 'TC': TC, 'RD': RD, 'RA': RA, 'Z': Z, 'AD': AD, 'CD': CD}

def pack_dns_flags(dnsflags):
    _dnsflags = 0
    _dnsflags = _dnsflags | dnsflags['CD']
    _dnsflags = _dnsflags | (dnsflags['AD'] << 1)
    _dnsflags = _dnsflags | (dnsflags['Z']  << 2)
    _dnsflags = _dnsflags | (dnsflags['RA'] << 3)
    _dnsflags = _dnsflags | (dnsflags['RD'] << 4)
    _dnsflags = _dnsflags | (dnsflags['TC'] << 5)
    _dnsflags = _dnsflags | (dnsflags['AA'] << 6)
    return _dnsflags



class dns_question(packet_base.PacketBase):
    """DNS question class

    An instance has the following attributes at least.
    __init__ takes the corresponding args in this order.

    =================================== ========================================================
    Attribute                           Description
    =================================== ========================================================
    domain_name                         The domain name being queried
    type                                The resource records being requested
    class                               The Resource Record(s) class being requested,
                                        for instance, internet, chaos etc.
    =================================== ========================================================
    """

    _Q_PACK_STR = "!HH"
    _MIN_LEN = struct.calcsize(_Q_PACK_STR) + 3

    def __init__(self, domain_name, qtype, qclass):
        super(dns_question, self).__init__()
        self.domain_name = domain_name
        self.qtype = qtype
        self.qclass = qclass

    @classmethod
    def parser(cls, buf):
        labels = []
        label_len = ord(buf[0])
        buf = buf[1:]

        while label_len != 0:
            labels.append(buf[:label_len])
            buf = buf[label_len:]
            label_len = ord(buf[0])
            buf = buf[1:]

        qtype, qclass = struct.unpack_from(cls._Q_PACK_STR, buf)
        buf = buf[struct.calcsize(cls._Q_PACK_STR):]

        return (cls(".".join(labels), qtype, qclass), None, buf)

    def __str__(self):
        return "Domain name : " + str(self.domain_name) +\
               "\nQType : " + str(self.qtype) +\
               "\nQClass : " + str(self.qclass)

class dns_answer(packet_base.PacketBase):
    """DNS answer class

    An instance has the following attributes at least.
    __init__ takes the corresponding args in this order.

    =================================== ========================================================
    Attribute                           Description
    =================================== ========================================================
    name 	    	    	    	    The name being returned e.g. www or ns1.example.net
                                        If the name is in the same domain as the question then
                                        typically only the host part (label) is returned,
                                        if not then a FQDN is returned.
    rr_type 	                        The RR type, for example, SOA or AAAA
    rr_class                            The RR class, for instance, Internet, Chaos etc.
    ttl 	                            The TTL in seconds of the RR, say, 2800
    rlength 	                        The length of RR specific data in octets, for example, 27
    rdata 	                            The RR specific data (see Binary RR Formats below)
                                        whose length is defined by RDLENGTH, for instance,
                                        192.168.254.2
    =================================== ========================================================
    """

    _R_PACK_STR = "!HHIH"
    _MIN_LEN = struct.calcsize(_R_PACK_STR) + 3

    def __init__(self, name, rr_type, rr_class, ttl, rlength, rdata):
        self.name = name
        self.rr_type = rr_type
        self.rr_class = rr_class
        self.ttl = ttl
        self.rlength = rlength
        self.rdata = rdata

    def __str__(self):
        "name : " + self.name +\
        "\nrr_type : " + self.rr_type +\
        "\nrr_class : " + self.rr_class +\
        "\nttl : " + self.ttl +\
        "\nrlength : " + self.rlength +\
        "\nrdata : " + self.rdata

    @classmethod
    def parser(cls, buf):
        pointer = None

        # name, if first 2 bit equals to "11", pointer used
        if ord(buf[0]) & 0x0c == 0x0c:
            pointer = struct.unpack_from("!H", buf)
            pointer = pointer & 0x3fff # pop first 2 bits
            buf = buf[2:]

        labels = []
        label_len = ord(buf[0])
        buf = buf[1:]

        while label_len != 0:
            labels.append(buf[:label_len])
            buf = buf[label_len:]
            label_len = ord(buf[0])
            buf = buf[1:]

        if pointer:
            labels = labels[pointer:]

        rr_type, rr_class, ttl, rlength = struct.unpack_from(cls._R_PACK_STR, buf)
        buf = buf[struct.calcsize(_R_PACK_STR):]
        rdata = buf[:rlength]
        buf = buf[rlength:]

        return (cls(".".join(labels), rr_type, rr_class, ttl, rlength, rdata), None, buf)
