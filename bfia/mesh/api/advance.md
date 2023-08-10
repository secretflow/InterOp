# 传输层高级能力

## 1 本方节点写入

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
