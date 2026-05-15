# 安全策略

## URL 抓取边界

seo-agents 将用户输入的 URL 视为不可信输入。核心网络命令会在请求前校验 URL，并拒绝：

- 非 HTTP(S) scheme。
- 空 host 或畸形 host。
- authority 中的 userinfo。
- 反斜杠和 percent-encoding authority 混淆。
- loopback、private、link-local、multicast、reserved 和 metadata endpoint。
- 十进制、十六进制、八进制、短 IPv4 等混淆写法。
- redirect 到不安全目标。

## DNS Rebinding

validator 会检查解析出的 A/AAAA 记录，只允许公网可路由地址。fetch 会重新校验每个 redirect 目标。浏览器渲染是 optional；当 Playwright 可用时，route protection 会校验子资源请求。

## 漏洞报告

请提供最小复现、受影响命令、预期行为和实际行为。不要在 issue 中公开真实凭据或客户 URL。
