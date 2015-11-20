**************
Packet 函式庫
**************

簡介
============

Ryu 提供的封包函式庫可以讓開發者去解析封包的內容，或是以現有的資料去產生一個
自定義的封包。另一方面，dpkt 函式庫與此函式庫的木但相同，但是他並沒有辦法處理
部分網路協定，例如 vlan, mpls, gre 等等，因此我們在 Ryu 中實作了我們自己的
封包處理函式庫。

網路位址
=================

除非有其他的定，否則網路位址如 MAC/IPv4/IPv6 位址都會是可讀的，舉例來說：
'08:60:6e:7f:74:e7', '192.0.2.1', 'fe80::a60:6eff:fe7f:74e7' 等等

解析封包
==============

下方範例程式中，我們使用了封包解析函式庫去解析來自 OFPacketIn 訊息所夾帶的封包
資料。

.. code-block:: python
       
    from ryu.lib.packet import packet
    
    @handler.set_ev_cls(ofp_event.EventOFPPacketIn, handler.MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        pkt = packet.Packet(array.array('B', ev.msg.data))
        for p in pkt.protocols:
            print p

你可以直接使用接收到的原始資料去產生一個 Packet 物件。這一個物件會去解析
輸入的原始資料，並且將這些資料轉換成為各個針對不同協定的類別物件，這些物件當中
各自包含了該協定的資料（例如 ipv4 包含了 IP 位址）。

在 Packet 中，protocols 這一個屬性是這一個封包所包含的協定物件列表，我們可以從此列表
中取得這一個封包所有的網路協定。

當一個 TCP 封包被控制器接收到並解析，我們可以看到類似下方的協定列表::

    <ryu.lib.packet.ethernet.ethernet object at 0x107a5d790>
    <ryu.lib.packet.vlan.vlan object at 0x107a5d7d0>
    <ryu.lib.packet.ipv4.ipv4 object at 0x107a5d810>
    <ryu.lib.packet.tcp.tcp object at 0x107a5d850>

如果該封包不包含 vlan，則我們可以獲得像是下方的列表::

    <ryu.lib.packet.ethernet.ethernet object at 0x107a5d790>
    <ryu.lib.packet.ipv4.ipv4 object at 0x107a5d810>
    <ryu.lib.packet.tcp.tcp object at 0x107a5d850>

我們可以隨意的去存取各種不同協定所產生的物件，下方是一個將 VLAN 資料
取出的的範例程式：

.. code-block:: python
       
    from ryu.lib.packet import packet
    
    @handler.set_ev_cls(ofp_event.EventOFPPacketIn, handler.MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        pkt = packet.Packet(array.array('B', ev.msg.data))
        for p in pkt:
            print p.protocol_name, p
            if p.protocol_name == 'vlan':
                print 'vid = ', p.vid

你可以看到類似下方的結果::

    ethernet <ryu.lib.packet.ethernet.ethernet object at 0x107a5d790>
    vlan <ryu.lib.packet.vlan.vlan object at 0x107a5d7d0>
    vid = 10
    ipv4 <ryu.lib.packet.ipv4.ipv4 object at 0x107a5d810>
    tcp <ryu.lib.packet.tcp.tcp object at 0x107a5d850>



產生一個封包
===============

開發者可以自行透過此函式庫去產生一個封包，在產生一個 Packet 類別物件之後，透過
add_protocol 這一個方法，我們可以在一個封包當中新增不同的網路協定以及資料，
當一個封包被製作好之後，我們將該封包物件序列化（serialize）產生資料（raw data）
，並將這一分資料送出，下方範例程式示範了如何透過程式產生一個自定義的封包。

.. code-block:: python

    from ryu.ofproto import ether
    from ryu.lib.packet import ethernet, arp, packet

    e = ethernet.ethernet(dst='ff:ff:ff:ff:ff:ff',
                          src='08:60:6e:7f:74:e7',
                          ethertype=ether.ETH_TYPE_ARP)
    a = arp.arp(hwtype=1, proto=0x0800, hlen=6, plen=4, opcode=2,
                src_mac='08:60:6e:7f:74:e7', src_ip='192.0.2.1',
                dst_mac='00:00:00:00:00:00', dst_ip='192.0.2.2')
    p = packet.Packet()
    p.add_protocol(e)
    p.add_protocol(a)
    p.serialize()
    print repr(p.data)  # the on-wire packet
