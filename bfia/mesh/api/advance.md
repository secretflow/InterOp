# 传输层高级能力

## 1 本方节点写入

本方节点写入接口用于灵活支持节点信息自定义下的互联互通，各方通过改接口写入自定义节点信息时。需要尽量避免ID的冲突。node_id和inst_id会在请求头中进行识别和路由。优先以节点ID路由，次之以机构ID。

### 1.1	请求地址

> POST /v1/interconn/node/refresh

#### 请求体(Request Body)

| 参数名称      | 数据类型   | 默认值 | 不为空  | 描述      |
|-----------|--------|-----|------|---------|
| node_id   | string |     | true | 节点ID    |
| inst_id   | string |     | true | 机构ID    |
| name      | string |     | true | 名称      |
| address   | string |     | true | 对外可访问地址 |
| host_root | string |     | true | 节点根证书   |
| host_key  | string |     | true | 节点根证书私钥 |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

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

| 参数名称    | 数据类型   | 默认值 | 不为空  | 描述      |
|---------|--------|-----|------|---------|
| node_id | string |     | true | 节点ID    |
| inst_id | string |     | true | 机构ID    |
| name    | string |     | true | 名称      |
| address | string |     | true | 对外可访问地址 |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值         | 不为空  | 描述                         |
|---------|--------|-------------|------|----------------------------|
| code    | string | E0000000000 | true | 状态码，E0000000000表示成功，其余均为失败 |
| message | string | 成功          | true | 状态说明                       |

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
