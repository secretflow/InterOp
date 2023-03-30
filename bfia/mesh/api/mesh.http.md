# 传输层规范

[toc]

## 1	基础信息

### 1.1 联系方式

| 联系人 | 邮箱                       |
|-----|--------------------------|
| 樊昕晔 | fanxinye@ebchinatech.com |
| 王超  | congying.wang@trustbe.cn |
| 曾成  | coyzeng@gmail.com        |

### 1.2 开源协议

| 协议名        | 地址                                              |
|------------|-------------------------------------------------|
| Apache 2.0 | http://www.apache.org/licenses/LICENSE-2.0.html |

### 1.3 文档版本

```
1.0.0
```

## 2	环境变量

| 参数名     | 字段值                   |
|---------|-----------------------|
| baseUrl | http://127.0.0.1:7304 |

## 3	传输接口

### 3.1	发送信息

> POST /v1/interconn/chan/push

#### 请求体(Request Body)

| 参数名称     | 数据类型          | 默认值 | 不为空   | 描述                         |
|----------|---------------|-----|-------|----------------------------|
| payload  | array[object] |     | true  | 消息序列化后的字节数组                |
| topic    | string        |     | false | 会话主题，相同信道具有唯一性，用于同一信道的传输隔离 |
| metadata | object        |     | false | 保留参数，用于扩展性                 |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型     | 默认值 | 不为空  | 描述               |
|---------|--------|-----|------|------------------|
| code    | string | 0   | true | 状态码，0表示成功，其余均为失败 |
| message | string | 成功  | true | 状态说明             |

### 3.2	获取信息

> GET /v1/interconn/chan/pop

#### 请求参数(Query Param)

| 参数名称  | 默认值 | 描述 |
|-------|-----|----|
| param |     |    |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型            | 默认值 | 不为空   | 描述               |
|---------|---------------|-----|-------|------------------|
| code    | string        | 0   | true  | 状态码，0表示成功，其余均为失败 |
| message | string        | 成功  | true  | 状态说明             |
| content | array[object] |     | false | 消息序列化后的字节数组      |

### 3.3	快速查询

> GET /v1/interconn/chan/peek

#### 请求参数(Query Param)

| 参数名称  | 默认值 | 描述 |
|-------|-----|----|
| param |     |    |

#### 响应体

● 200 响应数据格式：JSON

| 参数名称    | 类型            | 默认值 | 不为空   | 描述               |
|---------|---------------|-----|-------|------------------|
| code    | string        | 0   | true  | 状态码，0表示成功，其余均为失败 |
| message | string        | 成功  | true  | 状态说明             |
| content | array[object] |     | false | 消息序列化后的字节数组      |

## 4	传输报文

<table>
    <tr>
        <th>报文结构</th><th>编码</th><th>不为空</th><th>描述</th>
    </tr>
    <tr>
        <td rowspan="9">报文头</td><td>x-ptp-version</td><td>true</td><td>协议版本号</td>
    </tr>
    <tr>
        <td>x-ptp-tech-provider-code</td><td>true</td><td>厂商编码</td>
    </tr>
    <tr>
        <td>x-ptp-trace-id</td><td>true</td><td>全链路追踪编号</td>
    </tr>
    <tr>
        <td>x-ptp-token</td><td>true</td><td>认证令牌</td>
    </tr>
    <tr>
        <td>x-ptp-source-node-id</td><td>true</td><td>发送方节点编号</td>
    </tr>
    <tr>
        <td>x-ptp-target-node-id</td><td>true</td><td>接收端节点编号</td>
    </tr>
    <tr>
        <td>x-ptp-source-inst-id</td><td>false</td><td>发送端机构编号</td>
    </tr>
    <tr>
        <td>x-ptp-target-inst-id</td><td>false</td><td>接收端机构编号</td>
    </tr>
    <tr>
        <td>x-ptp-session-id</td><td>true</td><td>会话编号，全网唯一，用于建立有状态会话的通信，和对token的有效性验证</td>
    </tr>
    <tr>
        <td rowspan="2">输入报文</td><td>metadata</td><td>false</td><td>报头，预留扩展，序列化协议由通信层实现</td>
    </tr>
    <tr>
        <td>payload</td><td>true</td><td>报文，承载上层通信内容，序列化协议由上层基于SPI可插拔</td>
    </tr>
    <tr>
        <td rowspan="4">输出报文</td><td>metadata</td><td>false</td><td>报头，预留扩展，序列化协议由通信层实现</td>
    </tr>
    <tr>
        <td>payload</td><td>true</td><td>报文，承载上层通信内容，序列化协议由上层基于SPI可插拔</td>
    </tr>
    <tr>
        <td>code</td><td>true</td><td>状态码</td>
    </tr>
    <tr>
        <td>message</td><td>true</td><td>状态说明</td>
    </tr>
</table>

## 5	传输状态码

| 编码          | 描述           |
|-------------|--------------|
| E0000000000 | 请求成功         |
| E0000000404 | 请求资源不存在      |
| E0000000500 | 系统异常         |
| E0000000503 | 循环请求服务不可达    |
| E0000000400 | 请求非法         |
| E0000000403 | 请求资源未被授权     |
| E0000000520 | 未知异常         |
| E0000000600 | 系统不兼容        |
| E0000000601 | 请求超时         |
| E0000000602 | 无服务实例        |
| E0000000603 | 数字证书校验异常     |
| E0000000604 | 节点授权码已过期     |
| E0000000605 | 节点组网时间已过期    |
| E0000000606 | 对方节点已禁用网络    |
| E0000000607 | 网络不通         |
| E0000000614 | 接口未被许可调用     |
| E0000000615 | 证书签名非法       |
| E0000000616 | 报文编解码异常      |
| E0000000617 | 下游版本不匹配服务不存在 |
| E0000000618 | 节点或机构未组网     |
| E0000000619 | 地址非法或无法访问    |