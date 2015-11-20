**************************************************
OpenFlow 相關類別及函式
**************************************************

.. py:currentmodule:: ryu.ofproto.ofproto_parser

OpenFlow 訊息所使用的基底類別（Base class）
---------------------------------------
註：本章節部分內容是直接採用程式碼中文件，並由程式自動產生，故部分內容無法直接翻譯。

..    XXX
..    the descrption of _TYPE is inlined from ryu/lib/stringify.py.
..    this is a work around for a sphinx bug.
..    https://bitbucket.org/birkenfeld/sphinx/issue/741/autodoc-inherited-members-wont-work-for

.. autoclass:: MsgBase
   :members: to_jsondict, from_jsondict

   .. attribute::
    _TYPE

    _TYPE 類別能夠標註屬性的形態。

    這種形態所包含的資訊被用來轉換類似 JSON 格式的 dictionary 資料結構。

    目前已實作的形態如下：

    ===== ==========
    型態   說明
    ===== ==========
    ascii US-ASCII
    utf-8 UTF-8
    ===== ==========

    範例::

        _TYPE = {
            'ascii': [
                'hw_addr',
            ],
            'utf-8': [
                'name',
            ]
        }

函式
---------

.. autofunction:: ofp_msg_from_jsondict
