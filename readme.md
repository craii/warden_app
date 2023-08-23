# 使用方法
1. 修改`.env.bak`文件中的以下参数
  - corpid=企业微信企业id
  - corpsecret=企业微信企业秘钥
  - agentid=企业微信企业appid
2. 去除.bak后缀
3. 修改 `listener.py` 或 `punch_listener.py` 中 `send_text(）`函数中的参数，确定接收消息的员工昵称 
