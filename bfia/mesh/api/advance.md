# 传输层高级能力

## 1 本方节点写入

本方节点写入接口用于灵活支持节点信息自定义下的互联互通，各方通过改接口写入自定义节点信息时。需要尽量避免ID的冲突。node_id和inst_id会在请求头中进行识别和路由。优先以节点ID路由，次之以机构ID。

### 1.1	请求地址

> POST /v1/interconn/node/refresh

#### 请求体(Request Body)

| 参数名称      | 数据类型   | 默认值 | 不为空   | 描述                         |
|-----------|--------|-----|-------|----------------------------|
| version   | string |     | true  | 节点版本                       |
| node_id   | string |     | true  | 节点ID                       |
| inst_id   | string |     | true  | 机构ID                       |
| inst_name | string |     | true  | 名称                         |
| address   | string |     | true  | 对外可访问地址                    |
| root_crt  | string |     | false | 节点根证书，不填会默认签发RSA2/2048证书   |
| root_key  | string |     | false | 节点根证书私钥，不填会默认签发RSA2/2048私钥 |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

#### 请求示例

```bash
curl --location 'http://10.99.28.33:7304/v1/interconn/node/refresh' --header 'Content-Type: application/json' --data '{
    "version": "1.0.0",
    "node_id": "LX0000010000280",
    "inst_id": "JG0100002800000000",
    "inst_name": "互联互通节点X",
    "root_crt": "-----BEGIN CERTIFICATE-----\nMIIEZTCCA02gAwIBAgIRAKkfFud6oGcbEmGOZ2i917wwDQYJKoZIhvcNAQELBQAw\ngZIxCzAJBgNVBAYTAkNOMQswCQYDVQQIEwJaSjELMAkGA1UEBxMCSFoxJDAiBgNV\nBAoTG0xYMDAwMDAxMDAwMDI3MC50cnVzdGJlLm5ldDEkMCIGA1UECxMbTFgwMDAw\nMDEwMDAwMjcwLnRydXN0YmUubmV0MR0wGwYDVQQDDBTok53osaHpm4blm6IyN+WF\nrOWPuDAgFw0yMjA5MjEwNjU1MTRaGA8yMTIyMDkyMTA2NTUxNFowgZIxCzAJBgNV\nBAYTAkNOMQswCQYDVQQIEwJaSjELMAkGA1UEBxMCSFoxJDAiBgNVBAoTG0xYMDAw\nMDAxMDAwMDI3MC50cnVzdGJlLm5ldDEkMCIGA1UECxMbTFgwMDAwMDEwMDAwMjcw\nLnRydXN0YmUubmV0MR0wGwYDVQQDDBTok53osaHpm4blm6IyN+WFrOWPuDCCASIw\nDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOy3fx+vyvaRBTg9hXSXW/XEz5A9\nazavO4KNMPB/Rp6UtQ9+ilireBQXqCM1Zzo5/cZ+FoRmQp+Rl6b1HYAnRaPSTNFM\n4JDTl3AczsLwJcvFlqobqap9/3k5ZEfEEKJp0LFcl3GR2Ral7Uhsmgzm87PSZVRX\nFYPgCgfkuWGbeJ9FwCB5ZDovPH77pyJeW0AzPu3JKLk3JnCtUvmXK4HzoxChK4k0\nqJF1DEVSPxG3JLOKQKQqe/fqSTkRfgrU7D7U/TEaEl5lLFPGi6ZT+3AbOUAasWWO\nMTYMGMG6qC2wlQ7WdJJ4KiWhEfA7aGQfzoW85PZyN1QzRyzW1vyXY5MKNXsCAwEA\nAaOBsTCBrjAOBgNVHQ8BAf8EBAMCArwwJwYDVR0lBCAwHgYIKwYBBQUHAwEGCCsG\nAQUFBwMCBggrBgEFBQcDATAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBSrXjQL\nGNwhXBQxqx5Sh+LQwXK3mzBDBgNVHREEPDA6ghtMWDAwMDAwMTAwMDAyNzAudHJ1\nc3RiZS5uZXSBG0xYMDAwMDAxMDAwMDI3MEB0cnVzdGJlLm5ldDANBgkqhkiG9w0B\nAQsFAAOCAQEAcRhabDb2O55lQfeMkHozqFz3V4fQwQKQzYW6gwf7FEUxPMaxmFrk\nPKK2rE5Li49mUxk/norXMVmEpBQdYgsu2PnY5J39RivFku0nObzIMFkyDPer05tp\nx7sKXS6sIy9gfaN6uZkzHZH+0MD2NlOj19SI5BNJxiwHzB9BZwGwbKtq3DVZzWRq\nVyZnAcXVTq1Pk9gypatvBgD7r6edXSBXEz2d8HMaidJfChweZPVp98uY8s9EzHnJ\nowsia5sPaVNqVFE72IgQ5TUrRQsQIBGOF81i37Bpsc9g/pf2s6eNGW4CV9a8yfN1\n+BLRh/2eCYXUNQOm5IovVXqBJ4MlhchAOQ==\n-----END CERTIFICATE-----\n",
    "root_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA7Ld/H6/K9pEFOD2FdJdb9cTPkD1rNq87go0w8H9GnpS1D36K\nWKt4FBeoIzVnOjn9xn4WhGZCn5GXpvUdgCdFo9JM0UzgkNOXcBzOwvAly8WWqhup\nqn3/eTlkR8QQomnQsVyXcZHZFqXtSGyaDObzs9JlVFcVg+AKB+S5YZt4n0XAIHlk\nOi88fvunIl5bQDM+7ckouTcmcK1S+ZcrgfOjEKEriTSokXUMRVI/Ebcks4pApCp7\n9+pJORF+CtTsPtT9MRoSXmUsU8aLplP7cBs5QBqxZY4xNgwYwbqoLbCVDtZ0kngq\nJaER8DtoZB/Ohbzk9nI3VDNHLNbW/Jdjkwo1ewIDAQABAoIBAQDAhzIu3HTQe/zp\n1CfSPzT9PLixETM9Q+K7+Qgf4vTWEA7/biUpnzTH6sHG+S1fT0FXir/XqbBwRiM5\nGM2IqOhcKLRv2v4e7OmTtup35IhpJui2rE8fquD5gLNOJ2p8HmItjyhhp4UQhZ3r\nNOFKsyDtVacypK2MF9EwwFgCykeeCbVwBj8PxmTunDuVlD/hSTUa9JK/lh3ssGfN\novPPiuL2TTPiZUy415y4Kd4dVvuQW0QIlm4yV+qMynSNgU7p8f6jyKY5R7FAG3MF\nBEO07LZSYzTOhfhd2zz6lQpi5t2srScIUs+6hQSyZlFqILwkKeIgKTYbvb1q+o+s\nk5XijuwBAoGBAP2JjcENSCUj5c1bRiOvczS/XkDrE5YIOwJMFLWjuwuMNZN++PV3\ngZ58cM4leJ2TmpVidfu9Rkcp6q95M5fZa7Ms7qtS8sFu2JZhWBpydToRrsFAApsG\nBU09cfoq7DhlqJyE+p/X0lmmKyTw2HNeWUGU5AjSPeVa/4da9CSjDn97AoGBAO8E\nHevtVODXCJC+VJXOjlvCff4zGQi3pFo5s9hCXUDk8KNmfieJwcLXlqz3MG/kbmHi\n0ywToeBK5wA/npImAFKXGR5U6ivOeTBML8dM0wG+2gVCwazxm3qO1d2jyD6d/o2H\n/pH3rmuj+Hi9QSZPVVp+nrJsrG2HtMkwGFWP+kIBAoGANtZsqafUxeu4xa0LQ6as\nNWl62nG9/8Jx+PI5vHvYdgvyfp+E+5rIl131DDGAoByP3+W2/ScYL0Y6s490gFCP\ngeajDL1ZMktmX0hYxQeioVe3w6azqZIozWcP4vsrspsSWCBPEQmePrO5Ozk4p+Nt\nTMkGdX3700LWaBFdIxt9hEcCgYAf7CvW49bPRMkHE/SWIYVP6hULy2VPjb9ssYI8\novhzf2BIYpr8yuBPFp4wMb+NYjP/7NyJaYHYRAjANr8GA/9NCJM5QtwXx7bV5YcI\nFlGkTQovY7AcWhSK9OLJfGN1QYLLAlvUwQDRrY+1CInYBQaAVKL7b5pD8rkJmdvW\nKamiAQKBgQCq3cjGNqvMBVWeq0qJRsouSXRaHFRTmS9hgrRD/GZ+GQJNuhsDwfV9\nhb74cz7EqaFhQVhLHZ2QP/AauqtZ+p9wIM5X9xJDCaEKGVR+95vvxilBIOqua5IK\nphkbWGfS/Wp0fWGDaBoc05xuMm3Zv7GdiNeKr6soT1dOOCA88L3eTQ==\n-----END RSA PRIVATE KEY-----\n"
}'
```

## 2 服务注册

服务注册接口提供算子/算法/应用的服务化注册能力，注册后所有业务只需要对mesh发起调用即可实现服务化调用负载。

### 2.1	请求地址

> POST /v1/interconn/registry/register

#### 请求体(Request Body)

| 参数名称        | 数据类型               | 默认值       | 不为空  | 描述         |
|-------------|--------------------|-----------|------|------------|
| instance_id | string             |           | true | 实例ID，具备唯一性 |
| name        | string             |           | true | 实例名称，应用名   |
| kind        | string             | "complex" | true | 注册元数据类型    |
| address     | string             |           | true | 服务可访问地址    |
| timestamp   | string             |           | true | 服务注册有效时长   |
| attachments | Map<string,string> |           | true | 补充信息       |
| content     | Metadata           |           | true | 注册内容       |

Metadata

```json
{
  "services": [
    {
      "urn": "/a/b/c",
      "kind": "Restful",
      "proto": "http",
      "codec": "json",
      "address": "IP:PORT",
      "lang": "Python3"
    },
    {
      "urn": "/a/b/c",
      "kind": "Restful",
      "proto": "grpc",
      "codec": "json",
      "address": "IP:PORT",
      "lang": "Python3"
    }
  ]
}
```

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

## 3 写入组网节点信息

写入通信节点信息。

### 3.1	请求地址

> POST /v1/interconn/net/refresh

#### 请求体(Request Body)

| 参数名称       | 数据类型   | 默认值 | 不为空   | 描述                      |
|------------|--------|-----|-------|-------------------------|
| node_id    | string |     | true  | 节点ID                    |
| inst_id    | string |     | true  | 机构ID                    |
| name       | string |     | true  | 名称                      |
| address    | string |     | true  | 对外可访问地址                 |
| guest_root | string |     | false | 双向认证节点根证书，不填会默认使用节点证书通信 |
| guest_crt  | string |     | false | 双向认证节点证书，不填会默认使用节点证书通信  |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

#### 请求示例

```bash
curl --location 'http://10.99.27.33:7304/v1/interconn/net/refresh' --header 'Content-Type: application/json' --data '{
    "node_id": "LX0000010000280",
    "inst_id": "JG0100002800000000",
    "address": "192.168.100.63:27304",
    "guest_root": "",
    "guest_crt": ""
}'
```

## 4 节点组网申请

请求对方节点发起组网申请，组网申请为两阶段操作。

* 一阶段保存生成的证书私钥到本地
* 二阶段发送本方为对方颁发的通信证书和根证书到对方

### 4.1	请求地址

> POST /v1/interconn/net/weave

### 4.2 组网一阶段

一阶段保存生成的证书私钥到本地

#### 请求体(Request Body)

| 参数名称    | 数据类型   | 默认值 | 不为空  | 描述   |
|---------|--------|-----|------|------|
| node_id | string |     | true | 节点ID |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

### 4.3 组网二阶段

二阶段发送本方为对方颁发的通信证书和根证书到对方

#### 请求体(Request Body)

| 参数名称      | 数据类型   | 默认值 | 不为空  | 描述           |
|-----------|--------|-----|------|--------------|
| node_id   | string |     | true | 节点ID         |
| inst_id   | string |     | true | 机构ID         |
| name      | string |     | true | 名称           |
| address   | string |     | true | 对外可访问地址      |
| root_crt  | string |     | true | 对方根证书        |
| host_crt  | string |     | true | 对方颁发给本方的通信证书 |
| auth_code | string |     | true | 授权码          |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

## 5 节点组网授权

授权对方节点发起的组网申请，确认授权为两阶段操作。

* 一阶段保存生成的证书私钥到本地
* 二阶段发送本方为对方颁发的证书和根证书到对方

### 5.1	请求地址

> POST /v1/interconn/net/ack

### 5.2 授权一阶段

一阶段保存生成的证书私钥到本地

#### 请求体(Request Body)

| 参数名称    | 数据类型   | 默认值 | 不为空  | 描述   |
|---------|--------|-----|------|------|
| node_id | string |     | true | 节点ID |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

### 5.3 授权二阶段

二阶段发送本方为对方颁发的证书和根证书到对方

#### 请求体(Request Body)

| 参数名称      | 数据类型   | 默认值 | 不为空  | 描述           |
|-----------|--------|-----|------|--------------|
| node_id   | string |     | true | 节点ID         |
| inst_id   | string |     | true | 机构ID         |
| name      | string |     | true | 名称           |
| address   | string |     | true | 对外可访问地址      |
| root_crt  | string |     | true | 对方根证书        |
| host_crt  | string |     | true | 对方颁发给本方的通信证书 |
| auth_code | string |     | true | 授权码          |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |
