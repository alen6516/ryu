*****************
Ryu 的主要元件
*****************
註：本章節部分內容是直接採用程式碼中文件，並由程式自動產生，故部分內容無法直接翻譯。

可執行的
===========

bin/ryu-manager
---------------

Ryu 最主要的執行檔


基礎元件
===============

ryu.base.app_manager
--------------------
.. automodule:: ryu.base.app_manager


OpenFlow 控制器
===================

ryu.controller.controller
-------------------------
.. automodule:: ryu.controller.controller

ryu.controller.dpset
--------------------
.. automodule:: ryu.controller.dpset

ryu.controller.ofp_event
------------------------
.. automodule:: ryu.controller.ofp_event

ryu.controller.ofp_handler
--------------------------
.. automodule:: ryu.controller.ofp_handler

OpenFlow 協定之編碼器(encoder)及解碼器(decoder)
=====================================================

ryu.ofproto.ofproto_v1_0
------------------------
.. automodule:: ryu.ofproto.ofproto_v1_0

ryu.ofproto.ofproto_v1_0_parser
-------------------------------
.. automodule:: ryu.ofproto.ofproto_v1_0_parser

ryu.ofproto.ofproto_v1_2
------------------------
.. automodule:: ryu.ofproto.ofproto_v1_2

ryu.ofproto.ofproto_v1_2_parser
-------------------------------
.. automodule:: ryu.ofproto.ofproto_v1_2_parser

ryu.ofproto.ofproto_v1_3
------------------------
.. automodule:: ryu.ofproto.ofproto_v1_3

ryu.ofproto.ofproto_v1_3_parser
-------------------------------
.. automodule:: ryu.ofproto.ofproto_v1_3_parser

ryu.ofproto.ofproto_v1_4
------------------------
.. automodule:: ryu.ofproto.ofproto_v1_4

ryu.ofproto.ofproto_v1_4_parser
-------------------------------
.. automodule:: ryu.ofproto.ofproto_v1_4_parser

ryu.ofproto.ofproto_v1_5
------------------------
.. automodule:: ryu.ofproto.ofproto_v1_5

ryu.ofproto.ofproto_v1_5_parser
-------------------------------
.. automodule:: ryu.ofproto.ofproto_v1_5_parser


Ryu 預設可使用的應用程式
============================

ryu.app.cbench
--------------
.. automodule:: ryu.app.cbench

ryu.app.simple_switch
---------------------
.. automodule:: ryu.app.simple_switch

ryu.topology
------------
.. automodule:: ryu.topology


函式庫
=========

ryu.lib.packet
--------------
.. automodule:: ryu.lib.packet

ryu.lib.ovs
-----------
.. automodule:: ryu.lib.ovs

ryu.lib.of_config
-----------------
.. automodule:: ryu.lib.of_config

ryu.lib.netconf
---------------
.. automodule:: ryu.lib.netconf

ryu.lib.xflow
-------------
.. automodule:: ryu.lib.xflow


第三方函式庫
=====================

ryu.contrib.ovs
---------------

Open vSwitch python binding. Used by ryu.lib.ovs.

ryu.contrib.oslo.config
-----------------------

Oslo configuration library. Used for ryu-manager's command-line options
and configuration files.

ryu.contrib.ncclient
--------------------

Python library for NETCONF client. Used by ryu.lib.of_config.
