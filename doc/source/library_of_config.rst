*****************
OF-Config 支援
*****************

Ryu 提供了一套支援 OF-Config 協定的函式庫。

NETCONFIG 以及 OFConfig 所用到的的 XML 設定檔案
============================================
NETCONFIG 以及 OFConfig 所用到的的 XML 設定檔案是從 LINC 中所提取
，並以 Apache 2.0 授權釋出。
這些檔案僅支援部分 OF-Config 中所定義的規格，所以它僅能夠在一些有限的
設備上面執行。

當更多支援 OF-Config 的交換機被這一套函式庫測試之後，這一個函式庫將會去更新
原有的 XML 設定檔，而當它們被更新之後，函式庫就可以支援更多不同的網路設備。

參考
==========
* `NETCONF ietf <http://datatracker.ietf.org/wg/netconf/>`_,
* `NETCONF ietf wiki <http://tools.ietf.org/wg/netconf/trac/wiki>`_,
* `OF-Config spec <https://www.opennetworking.org/standards/of-config>`_,
* `ncclient <http://ncclient.grnet.gr/>`_,
* `ncclient repo <https://github.com/leopoul/ncclient/>`_,
* `LINC git repo <https://github.com/FlowForwarding>`_
