***************
網路拓樸瀏覽器
***************

ryu.app.gui_topology.gui_topology 提供了拓樸視覺化的功能

以下 Ryu 應用程式為本程式在執行階段所需要之相關應用程式。


===================== =================================================
ryu.app.rest_topology 取得所有節點（交換器）以及連結資訊
ryu.app.ws_topology   在新增連結與中斷連結時會對前端程式送出觸發
ryu.app.ofctl_rest    從交換器上取得 FlowEntry
===================== =================================================

使用方式
=======

執行 Mininet 網路模擬器（或是實體網路拓樸）::

    $ sudo mn --controller remote --topo tree,depth=3

執行 Ryu 圖形化應用程式::

    $ PYTHONPATH=. ./bin/ryu run --observe-links ryu/app/gui_topology/gui_topology.py

在瀏覽器連接中輸入::

    http://<您的主機位址（IP Address）>:8080

預覽畫面
==========

.. image:: gui.png
   :width: 640 px

