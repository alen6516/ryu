***************
開始使用
***************

什麼是 Ryu ?
==========
Ryu 是一個以元件為基礎(component-based)的軟體定義網路(SDN)開發框架。

透過 Ryu 所提供的 API，開發者可以很輕鬆的去實作他們需要的網路管理功能，
而 Ryu 也提供了許多軟體定義網路管理協定的開發介面，如 OpenFlow, NetConf, OF-config 等等
OpenFlow 的部份，Ryu 能夠完整支援 1.0, 1.2, 1.3, 1.4 以及 Nicira 擴充版本。

所有 Ryu 的程式碼都是基於 Python 所撰寫，並且使用 Apache 2.0 授權


快速開始
===========
如果要安裝 Ryu，只需要在終端機中輸入以下指令::

   % pip install ryu

如果你想要使用原始碼來安裝 Ryu，只需要在終端機中輸入以下指令::

   % git clone git://github.com/osrg/ryu.git
   % cd ryu; python ./setup.py install

如果你想要在 `OpenStack <http://openstack.org/>`_ 中使用 Ryu,
請參考 `networking-ofagent project <https://github.com/stackforge/networking-ofagent>`_

如果你想要撰寫自己的 Ryu 應用程式，請參考：
`Writing ryu application <http://ryu.readthedocs.org/en/latest/writing_ryu_app.html>`_
轉寫完 Ryu 應用程式之後，直接輸入以下指令即可執行::

   % ryu-manager yourapp.py


額外的函式庫需求
=====================

在 Ryu 中，部分的功能可能會需要安裝其他的函式庫：

- OF-Config 需要安裝 lxml
- NETCONF 需要安裝 paramiko
- BGP speaker (ssh console) 需要安裝 paramiko

如果您想要使用上述功能，使用 pip 去安裝需要的函式庫即可::

    % pip install lxml
    % pip install paramiko


支援
=======
Ryu 的官方頁面為 `<http://osrg.github.io/ryu/>`_

如果您有任何問題、建議或是提供補丁(patch)，請來信至 Ryu 的
If you have any questions, suggestions, and patches, the mailing list is available at
`郵件討論串
<https://lists.sourceforge.net/lists/listinfo/ryu-devel>`_
(mailing list)與其他人討論

討論串也可以至 `Gmane <http://dir.gmane.org/gmane.network.ryu.devel>`_ 觀看

