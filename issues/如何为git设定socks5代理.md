# 问题
由于网络限制的原因导致使用`git clone django`过于缓慢, 小飞机在这种情况下能派上用场.
那么如何为git设定socks5代理呢?

# 操作
1.&emsp;为git设定socks5代理
```
# socks5h 的意思是: 域名解析也交给小飞机来完成.
git config --global http.proxy socks5h://127.0.0.1:1080
```
2.&emsp;为git删除socks5代理配置
```
git config --global --unset http.proxy
git config --global --unset https.proxy
```

# 参考
[using a socks proxy with git for the http transport](https://stackoverflow.com/questions/15227130/using-a-socks-proxy-with-git-for-the-http-transport)   
[git how to remove proxy](https://stackoverflow.com/questions/32268986/git-how-to-remove-proxy/42602335)
