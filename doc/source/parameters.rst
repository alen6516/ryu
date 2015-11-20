:orphan:

.. _getting_started:

***************
開始使用
***************

關於/什麼是 Ryu ？
================================================
Ryu 是一個基於 Apache 2.0 授權的開放原始碼網路作業系統。
他支援 OpenFlow 協定

如果你不熟悉軟體定義網路（SDN）以及OpenFlow 控制器，請參考
`openflow org <http://www.openflow.org/>`_ 。

Ryu 的信件討論串為
`ryu-devel ML <https://lists.sourceforge.net/lists/listinfo/ryu-devel>`_

安裝 Ryu 網路作業系統
=======================================
下載並解壓縮原始碼並執行::

   % python ./setup.py install

之後，執行 ryu-manager
在預設的情況下，它會監聽 0.0.0.0 上的 6633 埠口（port）
接著，讓您的交換器（實際硬體或是軟體交換器）連上 ryu-manager。

若您使用的是 OpenvSwitch，則可以使用以下指令::

  % ovs-vsctl set-controller <你的 bridge>  tcp:<ip 位址>[:<埠口: 預設為 6633>]

目前 ryu-manager 僅支援 tcp 協定。
如果你想要搭配 OpenStack 中的 nova 以及 quantum OVS 插件使用，請參考
 :ref:`using_with_openstack`

執行應用程式以及設定
======================================
在 ryu-manager 後方加上參數即可直接設定 ryu-manager 在執行階段的設定::

  ryu-manager [generic/application specific options...]

目前以下的 Ryu 應用程式可以直接使用（未來會新增更多的應用程式）

  * ryu.app.bmpstation
  * ryu.app.cbench
  * ryu.app.gre_tunnel
  * ryu.app.gui_topology.gui_topology
  * ryu.app.ofctl_rest
  * ryu.app.rest
  * ryu.app.rest_conf_switch
  * ryu.app.rest_firewall
  * ryu.app.rest_nw_id
  * ryu.app.rest_qos
  * ryu.app.rest_quantum
  * ryu.app.rest_router
  * ryu.app.rest_topology
  * ryu.app.rest_tunnel
  * ryu.app.simple_isolation
  * ryu.app.simple_switch
  * ryu.app.simple_switch_12
  * ryu.app.simple_switch_13
  * ryu.app.simple_switch_14
  * ryu.app.simple_switch_igmp
  * ryu.app.simple_switch_lacp
  * ryu.app.simple_switch_snort
  * ryu.app.simple_switch_stp
  * ryu.app.simple_switch_websocket_13
  * ryu.app.simple_vlan
  * ryu.app.ws_topology

其他可以使用參數的如下::

  --app-lists: 後方為欲執行的應用程式模組名稱
    若需要多個應用程式，只需要重複本選項即可
  --help: 顯示幫助訊息

下列選項用於設定 Rest 伺服器::

  --wsapi-host: 網路程式監聽主機位址（host）
    (預設: '')
  --wsapi-port: 網路程式監聽埠口（port）
    (預設: 8080)
    (內容為一個整數)

下列選項用於設定 OpenFlow 控制器::

  --ofp-listen-host: OpenFlow 監聽主機位址（host）
    (預設: '')
  --ofp-tcp-listen-port: OpenFlow tcp 監聽埠口（port）
    (預設: 6633)
    (內容為一個整數)

下列選項用於設定日誌（log）::

  --default-log-level: 預設日誌等級
    (內容為一個整數)
  --log-dir: log 檔案目錄
  --log-file: log 檔案名稱
  --log-file-mode: 預設日誌檔案權限
    (預設: '0644')
  --[no]use-stderr: 輸出日誌到標準錯誤中（standard error）
    (預設: 'true')
  --use-syslog: 輸出至系統日誌（syslog）
    (預設: 'false')
  --[no]verbose: 輸出除錯日誌（debug output）
    (預設: 'false')

下列選項用於設定 oslo.config.cfg::

  --config-file: 設定檔檔案路徑，可給予多個參數設定檔案。
    (default: [])
  --config-dir: 設定檔案目錄，程式會引用該目錄中附檔名為 conf 之檔案，
    引用的檔案經過排序，重複的設定會以最後的為主。這一個設定會在 --config-file
    之後，而重複的設定也會以上述規則覆寫。


執行範例
================
執行的範例如下::

    % PYTHONPATH=. ./bin/ryu-manager --wsapi-port 8081 --verbose --app-lists ryu.app.simple_isolation,ryu.app.rest
    loading app ryu.app.simple_isolation
    loading app ryu.app.rest
    loading app ryu.controller.ofp_handler
    creating context dpset
    creating context wsgi
    creating context network
    instantiating app ryu.app.simple_isolation
    instantiating app ryu.app.rest
    instantiating app ryu.controller.ofp_handler
    BRICK dpset
      CONSUMES EventOFPStateChange
      CONSUMES EventOFPPortStatus
      CONSUMES EventOFPSwitchFeatures
    BRICK ofp_event
      PROVIDES EventOFPStateChange TO ['dpset']
      PROVIDES EventOFPPortStatus TO ['dpset', 'SimpleIsolation']
      PROVIDES EventOFPPacketIn TO ['SimpleIsolation']
      PROVIDES EventOFPSwitchFeatures TO ['dpset', 'SimpleIsolation']
      CONSUMES EventOFPEchoRequest
      CONSUMES EventOFPErrorMsg
      CONSUMES EventOFPSwitchFeatures
      CONSUMES EventOFPHello
    BRICK network
    BRICK RestAPI
    BRICK SimpleIsolation
      CONSUMES EventOFPPacketIn
      CONSUMES EventOFPPortStatus
      CONSUMES EventOFPSwitchFeatures
