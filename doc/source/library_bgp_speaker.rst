*******************
BGP speaker 函式庫
*******************

簡介
============

Ryu BGP speaker 函式庫可以讓開發者能夠去操作以及廣播 BGP 協定的訊息。
這一套函式庫支援了 ipv4, ipv4 vpn 以及 ipv6 vpn 相關網路定址協定

範例
=======

以下範例程式說明了如何去產生一個 AS 編號為 64512 以及路由編號（Route ID）為 10.0.0.1
的 BGP 實體。它會使用自身的資訊（IP 為 192.168.117.32，AS 為 64512）
去試圖建立一個 BGP session。這一個 BGP 實體會在他執行階段中去新增一些 prefix.

.. code-block:: python

    import eventlet

    # BGPSpeaker needs sockets patched
    eventlet.monkey_patch()

    # initialize a log handler
    # this is not strictly necessary but useful if you get messages like:
    #    No handlers could be found for logger "ryu.lib.hub"
    import logging
    import sys
    log = logging.getLogger()
    log.addHandler(logging.StreamHandler(sys.stderr))

    from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker

    def dump_remote_best_path_change(event):
        print 'the best path changed:', event.remote_as, event.prefix,\
            event.nexthop, event.is_withdraw

    def detect_peer_down(remote_ip, remote_as):
        print 'Peer down:', remote_ip, remote_as

    if __name__ == "__main__":
        speaker = BGPSpeaker(as_number=64512, router_id='10.0.0.1',
                             best_path_change_handler=dump_remote_best_path_change,
                             peer_down_handler=detect_peer_down)

        speaker.neighbor_add('192.168.177.32', 64513)
	# uncomment the below line if the speaker needs to talk with a bmp server.
	# speaker.bmp_server_add('192.168.177.2', 11019)
        count = 1
        while True:
            eventlet.sleep(30)
            prefix = '10.20.' + str(count) + '.0/24'
            print "add a new prefix", prefix
            speaker.prefix_add(prefix)
            count += 1
            if count == 4:
                speaker.shutdown()
                break
