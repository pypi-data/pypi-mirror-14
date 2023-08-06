OpenVPN 客户配置转换到阿里云解析DNS记录
=======================================

如何安装
--------

1. 因为AliDNS Python SDK 似乎没有正式发布, 没办法用pip安装,
   可从\ `这里 <https://help.aliyun.com/document_detail/dns/sdk/sdk.html>`__\ 下载
2. 运行 ``python setup.py install`` 安装SDK
3. 运行 ``pip install openvpn2alidns`` 安装软件
4. 配置 config.ini

   .. code:: ini

         [alidns]
         accessKey=
         accessSecret=
         regionId=cn-hangzhou
         productName=Alidns
         serviceAddr=alidns.aliyuncs.com
         domainName=genee.cn
         rrSuffix=server

如何使用
--------

1. 运行
   ``openvpn2alidns -c path/to/config.ini path/to/openvpn/client.d``
