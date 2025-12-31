# 隐私计算互联互通算法组件层 API

- [隐私计算互联互通算法组件层 API](#隐私计算互联互通算法组件层-api)
  - [1 整体框架](#1-整体框架)
  - [2 算法组件自描述文件](#2-算法组件自描述文件)
  - [3 算法组件与控制层交互](#3-算法组件与控制层交互)
    - [3.1 报文规范](#31-报文规范)
      - [3.1.1  通用规范](#311--通用规范)
      - [3.1.2  通用报文头规范](#312--通用报文头规范)
      - [3.1.3  公共出参](#313--公共出参)
    - [3.2 接口定义](#32-接口定义)
      - [3.2.1 任务信息查询接口](#321-任务信息查询接口)
    - [3.3 静态环境变量定义](#33-静态环境变量定义)
      - [3.3.1 系统环境变量](#331-系统环境变量)
      - [3.3.2 组件配置信息](#332-组件配置信息)
    - [3.4 动态环境变量定义](#34-动态环境变量定义)
      - [3.4.1 算法组件名称](#341-算法组件名称)
      - [3.4.2 算法组件参数](#342-算法组件参数)
      - [3.4.3 算法输入数据](#343-算法输入数据)
      - [3.4.4 算法输出数据](#344-算法输出数据)
  - [4 算法组件与存储层交互](#4-算法组件与存储层交互)
    - [4.1 存储服务配置](#41-存储服务配置)
    - [4.2 数据集文件存储](#42-数据集文件存储)
  - [5 算法组件与计算引擎交互](#5-算法组件与计算引擎交互)
  - [6 算法组件与传输层交互](#6-算法组件与传输层交互)
    - [6.1 报文规范](#61-报文规范)
    - [6.2 接口定义](#62-接口定义)
      - [6.2.1 数据发送接口](#621-数据发送接口)
      - [6.2.2 接收数据接口](#622-接收数据接口)
      - [6.2.3 快速获取数据接口](#623-快速获取数据接口)
      - [6.2.4 会话释放接口](#624-会话释放接口)
  - [7 安全算子服务接口](#7-安全算子服务接口)
    - [7.1 报文规范](#71-报文规范)
    - [7.2 接口定义](#72-接口定义)
      - [7.2.1 算子服务化接口](#721-算子服务化接口)
      - [7.2.2 算子表达式查询请求](#722-算子表达式查询请求)
      - [7.2.3 异步化关闭接口](#723-异步化关闭接口)
      - [7.2.4 异步化辅助查询接口](#724-异步化辅助查询接口)


## 1 整体框架

算法组件以容器镜像的形式打包存储，每一个算法组件需要具备针对该组件的算法自描述文件以供他方算法注册与使用加载。此外，算法组件层与控制层（调度层）、传输层以及系统层（计算、存储）等均有信息交互，需要遵循相应的规范和接口。由于框架图如下：

<div align="center">
    <img src="./figure/算法组件层架构.png">
</div>

**文档版本**

```
v1.2.0
```

## 2 算法组件自描述文件

每个算法组件应提供配套的算法组件自描述文件以增强算法的可扩展性。其中应包含算法功能、超参数、输入数据、输出结果等描述信息。算法自描述模板参考如下：

```
{
    componentName: "${componentName}", //算法组件名称，跟算法容器的环境变量相对应

    title: "${title}", //页面显示名称

    provider: "${provider}", //算法提供商

    version: "${version}", //算法版本

    description: "${description}", //算法描述

    roleList: "${roleList}", //[必须]算法支持的角色定义,数组类型。例如：["guest", "host","arbiter"]

    desVersion: "${desVersion}", //[可选]描述文件采用的版本

    storageEngine:"${storageEngine}",//[必须]说明算法组件所支持的存储引擎，数组类型。如：["s3", "hdfs","eggroll"]

    /**
     * 描述算法输入参数
     * 输入参数这里是指如算法超参相关的信息,和算法组件输入的数据区分开来,参考inputData的描述
     **/
    inputParam: [{
        name: "${name}", //输入字段的形式参数名称，跟算法容器的环境变量相对应
        title: "${title}", //页面显示字段标题
        description: "${description}", //参数描述
        type: "${type}", //描述输入字段的类型
        /**
         * 以下给出常用的几种数据类型:
         * string：字符串类型
         * int: 整数类型
         * float: 浮点数类型
         * boolean: 布尔类型
         * integer: 整型对象，可以为null
         * number: 数值型，包括整数和小数（当不具体区分整型和浮点型时采用该种类型）
         * object: 复杂类型,可以使用json表示,前端就具体的json数据结构可扩展相关控件。
         * ...等其他类型
        **/
        bindingData: "${bindingData}", //[可选],可枚举的静态绑定数据,可以引用外部其它函数获取控件绑定的数据,如可渲染下拉菜单、单选框、多选框等的数据获取方式       
        /**
         * 例如1:静态绑定数据
         * bindingData:"[{label: "${label}",value: "${value}"}]",其中是可以执行的 kv Json，格式参考为kv数组。
         *
         * 例如2:动态绑定数据
         * bindingData:"call_function getKV()"。//定义一个调用的回调函数获取数据，
         * 这里的call_function作为一个函数调用的标识符使用，解析执行器使用call_function作为标识符判断，用于与静态值区别，
         * 后面的getKV()，解析执行器需要保障执行上下文中存在可调用的getKV()函数，getKV()的函数命名，在实际使用中，可自定义。
        **/
        optional: "${optional}", //[必选],表示该参数是必须的还是可选的,默认为true表示可选,false表示必填
        defaultValue: "${defaultValue}", //[可选],输入的默认值。
        validator: "${validator}", //[可选],选择一个字段校验器,如可以写成 regular:'正则表达式',来做正则验证；使用（inf,sup）来对数值的上下界限进行限定
        dependsOn: "${dependsOn}", //[可选]只用于bindingData,表示算法的条件参数，用于组件内部依赖关系展示,默认为空值。若依赖于上游参数，则提供依赖列表，如：["param.value",""]
        /*以下字段跟前端显示及渲染有关，供前端展示参考*/
        UIPattern: "${UIPattern}", //[可选],表示字段的UI模式,默认为editeable,此外有readOnly表示只读,hidden,表示隐藏控件
        groupTag: "${groupTag}", //[可选] 分组标签,用于分组显示,如[默认分组-显示、高级分组-默认不显示]
        UIType: "${UIType}" //[可选],表示前端采用的控件类型,默认为input,其它的比如textArea,numberPicker、checkbox、redio、switch、select、selectTree等
    }],


    /**
     * 
     * 描述算法组件在运行时的输入数据
     * 
     **/
    inputData: [{

        name: "${name}", //输入数据的形式参数名称，跟算法容器的环境变量相对应

        description: "${description}", //输入数据描述信息

        category: "${category}", //输入数据的类型 model、dataset、training_set、test_set、datasets（多个数据文件）

        dataFormat:"${dataFormat}" //[可选]自持的输入数据文件格式，数组类型，默认取第一个。如：["csv","pmml","json","yaml","zip"]

    }],

    /**
     * 
     * 描述算法组件在运行时的输出数据
     * 
     **/
    outputData: [{

        name: "${name}", //输出数据的形式参数名称，跟算法容器的环境变量相对应

        description: "${description}", //输出数据描述信息

        category: "${category}" ,//输出数据的类型 model、dataset、training_set、test_set、report、metric

        dataFormat:"${dataFormat}" //[可选]支持的输出数据文件格式，数组类型，默认取第一个。如：["csv","pmml","json","yaml","zip"]

        
    }],
    /**
     * 
     * 描述算法组件的异常
     * 
     **/
    result: [{
        resultCode: "${resultCode}",

        resultMessage: "${resultMessage}"
    }]
}
```

**示例：**

```json
{
    "componentName": "HeteroLR",
        "title": "纵向逻辑回归算法",
    "provider": "FATE",
    "version": "2.0.0",
    "description": "纵向逻辑回归算法",
    "roleList": ["guest", "host", "arbiter"],
    "desVersion": "1.2.0",
        "storageEngine": ["s3","hdfs"],
    "inputParam": [
                {
                        "name": "id",
                        "title": "id列",
                        "description": "id字段名",
                        "type": "string",
                        "optional": "true",
                        "defaultValue": "id",
                        "validator": "regular-正则项", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input",
                },
                {
                        "name": "label",
                        "title": "标签",
                        "description": "label字段名",
                        "type": "string",
                        "optional": "true",
                        "defaultValue": "y",
                        "validator": "regular-正则项", 
                        "dependsOn": "",
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input",
                },
                {
                        "name": "penalty",
                        "title": "正则项",
                        "description": "正则项",
                        "type": "string",
                        "bindingData": [
                                {
                                        "label": "L1正则",
                                        "value": "L1"
                                },
                                {
                                        "label": "L2正则",
                                        "value": "L2"
                                }
                        ],
                        "optional": "true",
                        "defaultValue": "L2", 
                        "validator": "regular-正则项", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "select"
                },
                {
                        "name": "tol",
                        "title": "最小损失值",
                        "description": "最小损失值",
                        "type": "float",
                        "optional": "true",
                        "defaultValue": "0.0001",
                        "validator": "regular-正则项", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input"
                },
                {
                        "name": "alpha",
                        "title": "惩罚因子",
                        "description": "惩罚因子",
                        "type": "float",
                        "optional": "true",
                        "defaultValue": "0.01",
                        "validator": "regular-正则项", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input"
                },
                {
                        "name": "optimizer",
                        "title": "优化方法",
                        "description": "优化方法",
                        "type": "string",
                        "bindingData": [
                                {
                                        "label": "rmsprop",
                                        "value": "rmsprop"
                                },
                                {
                                        "label": "sgd",
                                        "value": "sgd"
                                },
                                {
                                        "label": "adam",
                                        "value": "adam"
                                },
                                {
                                        "label": "sqn",
                                        "value": "sqn"
                                },
                                {
                                        "label": "adagrad",
                                        "value": "adagrad"
                                },
                                {
                                        "label": "nesterov_momentum_sgd",
                                        "value": "nesterov_momentum_sgd"
                                }
                        ],        
                        "optional": "true",
                        "defaultValue": "rmsprop",
                        "validator": "regular-正则项", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "select"
                },
                {
                        "name": "batch_size",
                        "title": "批量梯度下降样本量",
                        "description": "每轮迭代抽取数据计算梯度的size",
                        "type": "integer",
                        "bindingData": [
                                {
                                        "label": "all",
                                        "value": "all"
                                },
                                {
                                        "label": "2048",
                                        "value": "2048"
                                },
                                {
                                        "label": "4096",
                                        "value": "4096"
                                },
                                {
                                        "label": "8192",
                                        "value": "8192"
                                }
                        ],
            "optional": "true",
                        "defaultValue": "2048",
                        "validator": "(0,1000)", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "select"
                },
                {
                        "name": "learning_rate",
                        "title": "学习率",
                        "description": "学习率",
                        "type": "float",
                        "optional": "true",
                        "defaultValue": "0.15",
                        "validator": "regular-正则项", 
                        "dependsOn": ["optimizer.sgd", "optimizer.adam"],
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input",                
                },
                {
                        "name": "init_param",
                        "title": "初始化参数",
                        "description": "初始化参数",
                        "type": "string",
                        "optional": "true",
                        "defaultValue": " ",
                        "validator": "regular-正则项", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input"
                },
                {
                        "name": "init_method",
                        "title": "初始化方式",
                        "description": "初始化方式",
                        "type": "string",
                        "optional": "true",
                        "defaultValue": "zeros",
                        "validator": "regular-正则项", 
                        "dependsOn": ["init_param"],
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input"
                },
                {
                        "name": "max_iter",
                        "title": "迭代次数",
                        "description": "迭代次数",
                        "type": "integer",
                        "optional": "true",
                        "defaultValue": "2",
                        "validator": "(0,1000)", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "input"
                },
                {
                        "name": "early_stop",
                        "title": "早停策略",
                        "description": "早停策略",
                        "type": "string",
                        "bindingData": [
                                {
                                        "label": "weight_diff",
                                        "value": "weight_diff"
                                },
                                {
                                        "label": "diff",
                                        "value": "diff"
                                }
                        ],
                        "optional": "true",
                        "defaultValue": "diff",
                        "validator": "regular-正则项", 
                        "UIPattern": "editeable",
                        "groupTag": "默认分组-显示",
                        "UIType": "select"
                }
        ],
    "inputData": [{
        "name": "train_data",
        "description": "训练集数据",
        "category": "dataset",
                "dataFormat": ["csv"]
    }],
    "outputData": [
                {
                        "name": "data0",
                        "description": "数据",
                        "category": "dataset",
                        "dataFormat": ["csv"]
                },
                {
                        "name": "model0",
                        "description": "模型文件",
                        "category": "model",
                        "dataFormat": ["json"]
                },
                {
                        "name": "report0",
                        "description": "loss值",
                        "category": "report",
                        "dataFormat": ["json"]
                }
        ],
    "result": [{
        "resultCode": "4444",
        "resultMessage": "算法执行失败"
    }]
}
```

## 3 算法组件与控制层交互

算法组件与控制层交互的接口与控制层的 callback 接口（详见控制层定义）为两个反向接口，callback 接口为算法调用控制层的接口以同步算法运行状态；该节 3.2.1 的任务信息查询接口为控制层调用算法组件层的接口以获取算法运行状态。

### 3.1 报文规范

#### 3.1.1  通用规范

```python
Content-Type：application/json
HTTP Method：读GET，写POST
```

#### 3.1.2  通用报文头规范

```
Request Header： 
x-auth-sign：        required 利用签约时指定的算法构造的签名值，用于安全校验，节点信息查询、合作申请、更新合作意向接口header无需包含X-Auth-Sign，节点签约完成后才能生成签名值；
x-csrf-protection:   required 避免跨站点请求伪造攻击， POST时必选
x-source-node-id:    required 请求方节点id；
x-target-node-id:    required 目的方节点id；
x-nonce：            required 系统生成的防重放随机串，如 UUID；
x-trace-id：         required 业务自定义标识，用于全链路跟踪；
x-timestamp：        required 调用方毫秒时间戳（Unix epoch time，具有时区无关性）。
x-mprac-token-set：  required 多方资源访问控制的许可凭证，用于多方资源访问控制，是资源的使用方向资源的持有方发资源操作时，所需要的凭证集合,集合元组之间，用逗号分割，单个许可凭证的格式定义如下为：统一资源名称/资源等级/资源授权令牌
```

#### 3.1.3  公共出参

状态码 **0**

| 名称 | 类型   | 必选 | 中文名       | 说明             |
| ---- | ------ | ---- | ------------ | ---------------- |
| code | int32  | true | 状态码       | 0 正常，否则错误 |
| msg  | string | true | 错误信息     | none             |
| data | object | true | 响应数据内容 | none             |

### 3.2 接口定义

算法组件与控制层需要按照约定的参数传递规范与算法控制接口进行信息交互，算法对外端口由system.control_port静态环境变量指定。具体接口包括以下：

#### 3.2.1 任务信息查询接口

> POST /v1/platform/algorithm/task/query

**接口描述**

某个参与方的调度层获取算法组件层的任务运行状态时调用的接口

**请求体**

| 名称    | 位置 | 类型   | 必选 | 中文名  | 说明 |
| ------- | ---- | ------ | ---- | ------- | ---- |
| task_id | body | string | 是   | 任务 ID | none |

> Body 请求参数

```json
{
  "task_id": "string"
}
```

**返回结果**

| 状态码 | 状态码含义                                              | 说明 | 数据模型 |
| ------ | ------------------------------------------------------- | ---- | -------- |
| 0      | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | 成功 | Inline   |

**返回数据结构**

状态码 **0**

| 名称   | 类型    | 必选 | 约束 | 中文名   | 说明                     |
| ------ | ------- | ---- | ---- | -------- | ------------------------ |
| code   | integer | true | none | 状态码   | 0 正常，否则错误         |
| status | string  | true | none | 任务状态 | RUNNING、SUCCESS、FAILED |
| role   | string  | true | none | 角色     | 任务节点所属角色         |

> 返回示例

> 0 Response

```json
{
  "code": 0,
  "status": "RUNNING",
  "role": "host",
}
```

### 3.3 静态环境变量定义

#### 3.3.1 系统环境变量

| **标识名称**     | **可选性** | **标识含义**     | **描述**                                     |
| ---------------- | ---------- | ---------------- | -------------------------------------------- |
| system.storage   | 必选       | 存储层服务地址   | 支持配置多个存储服务地址                     |
| system.callback  | 必选     | 调度层回调地址   | 可通过接口回调，也可通过容器运行结果，或其他 |
| system.transport | 必选       | 传输服务地址     | 填写传输地址信息                             |
| system.compute   | 可选       | 计算引擎服务地址 | 填写引擎服务地址信息                         |
| system.control_port   | 可选       | 信息查询端口 | 填写算法容器对外的信息查询端口，默认10086         |

#### 3.3.2 组件配置信息

| **标识名称**                   | **可选性** | **标识含义**                                                                                                                                       | **描述**           |
| ------------------------------ | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| config.self_role               | 必选       | 当前组件运行任务的角色 +index，多个是用英文逗号分割                                                                                                | guest/host/arbiter |
| config.task_id                 | 必选       | 组件运行的任务 ID                                                                                                                                  | task_id            |
| config.node_id.<role>.<role_n> | 必选       | 角色对应的节点 ID                                                                                                                                  | 数据传输时需要     |
| config.inst_id.<role>.<role_n> | 必选       | 角色对应的机构 ID                                                                                                                                  |                    |
| config.session_id              | 必选       | 传输 SDK 需要的会话 ID                                                                                                                             |                    |
| config.trace_id                | 必选       | 链路 ID                                                                                                                                            |                    |
| config.token                   | 必选       | 对应管理面 ResourcePermit 实体中的 token，用于传输接收方进行权限校验**注：目前两个以上参与方时暂不确定传参方式，所以暂不建议对此进行字段进行校验** |                    |
| config.log.path                | 必选       | log 日志路径（容器内）                                                                                                                             |                    |
| config.n_threads               | 可选       | 存储 SDK 上传、下载数据的并行数                                                                                                                    | 存储层需要         |
| config.chunk_size              | 可选       | 存储 SDK 上传、下载数据的块大小                                                                                                                    |                    |

### 3.4 动态环境变量定义

#### 3.4.1 算法组件名称

| **标识名称**           | **可选性** | **标识含义**       | **描述** |
| ---------------------- | ---------- | ------------------ | -------- |
| runtime.component.name | 必选       | 当前运行的组件名称 | 组件名称 |

#### 3.4.2 算法组件参数

| **标识名称**                       | **可选性** | **标识含义**                   | **描述** |
| ---------------------------------- | ---------- | ------------------------------ | -------- |
| runtime.component.parameter.<name> | 必选       | 组件运行期的参数<name>对应的值 | 参数列表 |

#### 3.4.3 算法输入数据

| **标识名称**                   | **可选性** | **标识含义**                         | **描述** |
| ------------------------------ | ---------- | ------------------------------------ | -------- |
| runtime.component.input.<name> | 必选       | 组件运行期的输入<name>对应的文件标识 | 输入数据 |

#### 3.4.4 算法输出数据

| **标识名称**                    | **可选性** | **标识含义**                         | **描述** |
| ------------------------------- | ---------- | ------------------------------------ | -------- |
| runtime.component.output.<name> | 必选       | 组件运行期的输出<name>对应的文件标识 | 输出数据 |

## 4 算法组件与存储层交互

算法组件应支持本地存储或主流的存储引擎接口，并在自描述文件中说明所支持的存储引擎类型。算法组件宜支持大数据量输入与输出情形的处理。

算法容器根据调度层下发的环境变量获取数据集地址及结果集的输出地址

- 算法容器从指定地址获取并加载数据集信息
- 算法容器输出计算结果集到指定数据地址

### 4.1 存储服务配置

调度层生成存储服务的配置信息，并通过环境变量 env 下发给算法组件层：

1. S3 存储：s3://{host}:{port}?username={username}&password={password}&bucket={bucket_name}

| **字段** | **说明**          |
| -------- | ----------------- |
| host     | s3 服务的 ip 地址 |
| port     | s3 服务的服务端口 |
| username | s3 服务的用户名   |
| password | s3 服务的用户密码 |
| bucket   | s3 服务的桶名称   |

**示例：**

system.storage=s3://192.168.1.1:9000?username=admin&password=123456&bucket=storage

2. HDFS 存储：hdfs://{host}:{port}?username={username}&password={password}&dir={dir}

| **字段** | **说明**            |
| -------- | ------------------- |
| host     | hdfs 服务的 ip 地址 |
| port     | hdfs 服务的服务端口 |
| username | hdfs 服务的用户名   |
| password | hdfs 服务的用户密码 |

**示例：**

system.storage=hdfs://192.168.1.1:9000?username=admin&password=123456&dir=storage

3. NFS 存储和本地存储：file://XXX//XXX

**示例：**

system.storage=file:///opt/iopy/

### 4.2 数据集文件存储

算法组件容器根据存储服务配置和输入、输出数据的 namespace、name 等信息，生成文件路径：

1. S3 存储：

数据集：s3://{bucket_name}/{namespace}/{name}/data_{partition}

数据集 meta：s3://{bucket_name}/{namespace}/{name}/metadata

| **字段**    | **说明**       |
| ----------- | -------------- |
| bucket_name | s3 桶名        |
| namespace   | 数据集所属库名 |
| name        | 数据集名称     |
| parition    | 数据集分区序号 |

2. HDFS 存储：

数据集：hdfs://{dir}/{namespace}/{name}/data_{partition}

数据集 meta：hdfs://{dir}/{namespace}/{name}/metadata

| **字段**  | **说明**       |
| --------- | -------------- |
| dir       | 存储一级目录   |
| namespace | 数据集所属库名 |
| name      | 数据集名称     |
| parition  | 数据集分区序号 |

3. NFS 存储和本地存储：

数据集：file:///{dir1}//{dir2}

## 5 算法组件与计算引擎交互

算法组件应支持本地计算或主流的计算引擎接口，并在自描述文件中说明所支持的计算引擎类型。算法组件宜支持算力的水平或垂直扩展，如计算集群或者硬件加速：

1. 本地计算：算法组件基于内存方式完成计算任务，无需额外定义环境变量
2. 计算引擎：算法组件基于常用的分布式计算引擎完成计算任务，需要定义计算引擎相关的环境变量

- spark：client 端执行算法容器，通过 Spark 的 DAG 调度服务，将计算任务下发至 worker 节点中的 executer 组件，执行 map-reduce 操作。

示例：

system.compute=spark://192.168.1.1:7077

- eggroll：算法容器通过 eggroll-client 组件将计算任务下发至 nodemanager 计算引擎中，执行 map-reduce 操作。

示例：

system.compute=eggroll://192.168.1.1:4670

## 6 算法组件与传输层交互

算法模块应支持与传输模块所约定的接口与报文规范，实现与多方协作通信完成算法任务，该部分接口在[传输层 API 文档](../4.传输层接口/隐私计算互联互通传输层API.md)中的容器调用通信模块接口部分有相同的定义。

### 6.1 报文规范

算法容器调用通信模块接口，采用 HTTP 协议为基础，所以此处定义了基于 HTTP 协议的报文和接口。

**报头**

```python
x-ptp-tech-provider-code:    required 厂商编码
x-ptp-trace-id:              required 链路追踪ID
x-ptp-token:                 required 认证令牌
x-ptp-session-id:            required 通信会话号，全网唯一
x-ptp-target-node-id:        required 接收端节点编号，全网唯一
x-ptp-target-inst-id:        optional 接收端机构编号，全网唯一
```

**报文**

● 互联互通下节点间通信报文透传二进制报文，复用 HTTP 协议 Body 传输。

### 6.2 接口定义

内部通信协议接口定义包含，数据发送、接收数据、快速获取数据、会话释放四个接口。

接口功能支持以下内容：

a) 发送信息：向通信信道中发送数据；

b) 接收信息：接收信息两种模式，主动模式和被动模式，主动模式必选，被动模式可选：

主动模式即为算法容器主动向传输模块发起请求获取通道中的数据，应包括： (1)获取信息，阻塞情况下，从通信信道中读取数据； (2)快速查询，非阻塞情况下，从通信信道中读取数据；
被动模式即为算法容器启动时监听端口，传输模块收到信息后直接转发给算法容器端口。

c) 会话释放：释放会话资源，可选。

#### 6.2.1 数据发送接口

> POST /v1/interconn/chan/push

**接口描述**

> 容器调用通信模块发送数据

**请求体**

| 参数名称 | 数据类型 | 默认值 | 是否必填 | 描述                                                 |
| -------- | -------- | ------ | -------- | ---------------------------------------------------- |
| payload  | byte[]   | 空     | true     | 消息序列化后的字节数组                               |
| topic    | string   | 空     | false    | 会话主题，相同信道具有唯一性，用于同一信道的传输隔离 |
| metadata | object   | 空     | false    | 保留参数，用于扩展性                                 |

**响应体**

| 参数名称 | 类型   | 默认值      | 是否必填 | 描述                                       |
| -------- | ------ | ----------- | -------- | ------------------------------------------ |
| code     | string | E0000000000 | true     | 状态码，E0000000000 表示成功，其余均为失败 |
| message  | string | 成功        | true     | 状态说明                                   |

#### 6.2.2 接收数据接口

> POST /v1/interconn/chan/pop

**接口描述**

> 容器调用通信模块接口获取数据，该接口会从通信信道中阻塞读取一次数据，如信道中无数据，会一直阻塞等待触发超时返回空

**请求体**

| 参数名称 | 数据类型 | 默认值 | 是否必填 | 描述                                                 |
| -------- | -------- | ------ | -------- | ---------------------------------------------------- |
| timeout  | byte[]   | 空     | false    | 阻塞超时时间，默认 120s                              |
| topic    | string   | 空     | false    | 会话主题，相同信道具有唯一性，用于同一信道的传输隔离 |

**响应体**

| 参数名称 | 类型   | 默认值      | 是否必填 | 描述                                       |
| -------- | ------ | ----------- | -------- | ------------------------------------------ |
| code     | string | E0000000000 | true     | 状态码，E0000000000 表示成功，其余均为失败 |
| message  | string | 成功        | true     | 状态说明                                   |
| content  | byte[] | 空          | false    | 消息序列化后的字节数组                     |

#### 6.2.3 快速获取数据接口

> POST /v1/interconn/chan/peek

**接口描述**

> 容器调用通信模块接口快速获取数据，即在非阻塞情况下从通信信道中读取一次数据，若信道中有数据则返回数据，无数据则返回空

**请求体**

| 参数名称 | 数据类型 | 默认值 | 是否必填 | 描述                                                 |
| -------- | -------- | ------ | -------- | ---------------------------------------------------- |
| topic    | string   | 空     | false    | 会话主题，相同信道具有唯一性，用于同一信道的传输隔离 |

**响应体**

| 参数名称 | 类型   | 默认值      | 是否必填 | 描述                                       |
| -------- | ------ | ----------- | -------- | ------------------------------------------ |
| code     | string | E0000000000 | true     | 状态码，E0000000000 表示成功，其余均为失败 |
| message  | string | 成功        | true     | 状态说明                                   |
| content  | byte[] | 空          | false    | 消息序列化后的字节数组                     |

#### 6.2.4 会话释放接口

> POST /v1/interconn/chan/release

**接口描述**

> 容器调用通信模块接口，清理掉以 x-ptp-session-id 标记的会话，调用该接口会释放会话中未读取的数据

**请求体**

| 参数名称 | 数据类型 | 默认值 | 是否必填 | 描述                                                 |
| -------- | -------- | ------ | -------- | ---------------------------------------------------- |
| timeout  | byte[]   | 空     | false    | 释放最长等待时间，默认 10s                           |
| topic    | string   | 空     | false    | 会话主题，相同信道具有唯一性，用于同一信道的传输隔离 |

**响应体**

| 参数名称 | 类型   | 默认值      | 是否必填 | 描述                                       |
| -------- | ------ | ----------- | -------- | ------------------------------------------ |
| code     | string | E0000000000 | true     | 状态码，E0000000000 表示成功，其余均为失败 |
| message  | string | 成功        | true     | 状态说明                                   |

## 7 安全算子服务接口

### 7.1 报文规范

安全算子服务模块采用 HTTP 协议为基础，所以此处定义了基于 HTTP 协议的报文和接口。

**报头**

```python
x-ptp-tech-provider-code:    required 厂商编码
x-ptp-trace-id:              required 链路追踪ID
x-ptp-token:                 required 认证令牌
x-ptp-session-id:            required 通信会话号，全网唯一
x-ptp-target-node-id:        required 接收端节点编号，全网唯一
x-ptp-target-inst-id:        optional 接收端机构编号，全网唯一
```

**报文**

● 互联互通下节点间通信报文透传二进制报文，复用 HTTP 协议 Body 传输。

### 7.2 接口定义

#### 7.2.1 算子服务化接口

> POST /secure_operate/v1/execute

**接口描述**

算子服务化主接口，执行一个表达式并定义输出结果

**请求体**

| 参数名称        | 数据类型      | 可选  | 描述                                                                                                                                                                                                                                                            |
| --------------- | ------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| taskId          | string        | false | 任务 ID，用于约定对齐算子、算法上下文的任务编号                                                                                                                                                                                                                 |
| subTaskId       | string        | true  | [可选]子任务 ID，用于算法对任务进行拆分或并行计算时使用，一般编码方式是 taskId+ 分片后缀。                                                                                                                                                                      |
| token           | string        | false | 控制面下发的 Token，用于多方之间处理权限核验                                                                                                                                                                                                                    |
| asyncMode       | boolean       | true  | [可选]同步或异步模式，默认为 false，false 表示同步调用，同步情况下，算子服务需要在计算任务完成之后返回结果，上层算法阻塞等待。true 表示采用异步调用，异步调用情况下，算子服务在受理服务请求后，即可返回，算法层会根据 outputMethod 约定的存储位置异步获取结果。 |
| timeout         | int32         | true  | [可选]超时时间，单位为秒，默认为 0 表示不设置超时时间。算子服务如果超时，会强制结束任务，并返回错误。                                                                                                                                                           |
| mpcProtocol     | object        | false | 多方安全计算协议名称，用于约定算子实现的技术路线。                                                                                                                                                                                                              |
| ⇥ protocolCode | string        | false | 协议名称编码                                                                                                                                                                                                                                                    |
| ⇥ providerCode | string        | false | 提供厂商名称编码                                                                                                                                                                                                                                                |
| ⇥ version      | string        | false | 协议版本号                                                                                                                                                                                                                                                      |
| ⇥ param        | object        | false | 协议超参                                                                                                                                                                                                                                                        |
| expression      | string        | false | 用于描述算子计算操作，比如 mvm 表示矩阵向量乘法，matmul 表示矩阵乘法；                                                                                                                                                                                          |
| parties         | array[string] | false | 参与方 ID 列表，由发起方（或协调方）制定，该列表中个参与方的位置在一次计算任务重，是固定的，各参与方不允许对其调整，因为在计算过程                                                                                                                              |
| localPartyId    | string        | false | 本方的参与方 ID                                                                                                                                                                                                                                                 |
| resultParties   | array[string] | false | 结果获取方列表，由发起方（或协调方）进行设置。                                                                                                                                                                                                                  |
| inputs          | array[object] | false | 数据输入                                                                                                                                                                                                                                                        |
| ⇥ dataValueTag | object        | false | 对一个算子输入、输出参数的描述信息                                                                                                                                                                                                                              |
| ⇥⇥ type       | string        | false | 标记数据传输方式，Direct,标识直接传值，如果希望使用存储引擎来传值，可以使用引擎名称，例如 myRedis。                                                                                                                                                             |
| ⇥⇥ name       | string        | false | 与表达式中的对应参数 name 进行关联， 让表达式能够根据 name 定位的数据。                                                                                                                                                                                         |
| ⇥⇥ uri        | string        | false | 非 Direct 情况下使用，使用存储引擎时， 指定存储引擎的资源定位符                                                                                                                                                                                                 |
| ⇥⇥ key        | string        | false | 非 Direct 情况下使用，使用存储引擎时，使用的 key 用于数据读写。                                                                                                                                                                                                 |
| ⇥⇥ dtype      | string        | false | 用于标记输入输出数据的类型，在数据传输过程中，数据块以字节数组的形式进行传输，dtype 对数据块的格式进行描述，用于将字节数据转换为所需要的数据类型，详细说明，参考 dtype 枚举说明。                                                                               |
| ⇥⇥ shape      | array[int32]  | false | 用于标记输入输出数据的形状，shape 的元素给出了相应维度上的数组尺寸的长度。                                                                                                                                                                                      |
| ⇥⇥ delete     | boolean       | false | 默认为 false,数据使用完成之后，是否清理。                                                                                                                                                                                                                       |
| ⇥ directValue  | string        | false | 直接传值的数据，如果不采集直接传值的方式，则该值为空。该字段的处理方式上，是将要传输的数据块的转换为字节数组，再通过 Base64 编码后                                                                                                                              |
| outputMethod    | array[object] | false | 数据返回方式                                                                                                                                                                                                                                                    |
| ⇥ type         | string        | false | 标记数据传输方式，Direct,标识直接传值，如果希望使用存储引擎来传值，可以使用引擎名称，例如 myRedis。                                                                                                                                                             |
| ⇥ name         | string        | false | 与表达式中的对应参数 name 进行关联， 让表达式能够根据 name 定位的数据。                                                                                                                                                                                         |
| ⇥ uri          | string        | false | 非 Direct 情况下使用，使用存储引擎时， 指定存储引擎的资源定位符                                                                                                                                                                                                 |
| ⇥ key          | string        | false | 非 Direct 情况下使用，使用存储引擎时，使用的 key 用于数据读写。                                                                                                                                                                                                 |
| ⇥ dtype        | string        | false | 用于标记输入输出数据的类型，在数据传输过程中，数据块以字节数组的形式进行传输，dtype 对数据块的格式进行描述，用于将字节数据转换为所需要的数据类型，详细说明，参考 dtype 枚举说明。                                                                               |
| ⇥ shape        | array[int32]  | false | 用于标记输入输出数据的形状，shape 的元素给出了相应维度上的数组尺寸的长度。                                                                                                                                                                                      |
| ⇥ delete       | boolean       | false | 默认为 false,数据使用完成之后，是否清理。                                                                                                                                                                                                                       |
| phases          | string        | true  | [可选] 有状态服务的执行阶段，缺省为无状态服务，可分阶段执行，可指定一个或多个阶段执行，定义为三个阶段，PREPAR（准备阶段）、CALCULATE（计算阶段）,RETRIEVE（恢复阶段）                                                                                           |

**响应体**

0 响应数据格式：JSON

| 参数名称        | 数据类型      | 可选  | 描述                                                                                                                                                                                                                                                                                                                         |
| --------------- | ------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| code            | int32         | false | 0 正常，否则错误码 错误码分段: 100-199 表示系统层面的异常，比如算子服务未正常启动； 200-299 表示依赖本地环境所产生的异常，如依赖的节点内存储系统发生异常； 300-399 表示节点间的处理异常，包括节点间通信和节点间的系统异常； 400-999 表示内部的逻辑错误，比如参数错误产生的异常，数据格式错误、表达式不存在、算子异常终止等。 |
| msg             | string        | false | 返回信息描述                                                                                                                                                                                                                                                                                                                 |
| result          | array[object] | false | 本次计算返回的结果，如果是异步调用模式下，则不立即返回此参数，可通过异步结果查询接口，获取此参数。                                                                                                                                                                                                                           |
| ⇥ dataValueTag | object        | false | 对算子输入输出一个参数的描述。                                                                                                                                                                                                                                                                                               |
| ⇥⇥ type       | string        | false | 标记数据传输方式，Direct,标识直接传值，如果希望使用存储引擎来传值，可以使用引擎名称，例如 myRedis。                                                                                                                                                                                                                          |
| ⇥⇥ name       | string        | false | 与表达式中的对应参数 name 进行关联， 让表达式能够根据 name 定位的数据。                                                                                                                                                                                                                                                      |
| ⇥⇥ uri        | string        | false | 非 Direct 情况下使用，使用存储引擎时， 指定存储引擎的资源定位符                                                                                                                                                                                                                                                              |
| ⇥⇥ key        | string        | false | 非 Direct 情况下使用，使用存储引擎时，使用的 key 用于数据读写。                                                                                                                                                                                                                                                              |
| ⇥⇥ dtype      | string        | false | 用于标记输入输出数据的类型，在数据传输过程中，数据块以字节数组的形式进行传输，dtype 对数据块的格式进行描述，用于将字节数据转换为所需要的数据类型，详细说明，参考 dtype 枚举说明。                                                                                                                                            |
| ⇥⇥ shape      | array[int32]  | false | 用于标记输入输出数据的形状，shape 的元素给出了相应维度上的数组尺寸的长度。                                                                                                                                                                                                                                                   |
| ⇥⇥ delete     | boolean       | false | 默认为 false,数据使用完成之后，是否清理。                                                                                                                                                                                                                                                                                    |
| ⇥ directValue  | string        | false | 直接传值的数据，如果不采集直接传值的方式，则该值为空。该字段的处理方式上，是将要传输的数据块的转换为字节数组，再通过 Base64 编码后得到字符串形式的值，以便支持不同类型的 RPC 协议。数据块转换到字节数组的方式，由 DataValueTag 中的 dtype 和 shape 确定。                                                                    |

#### 7.2.2 算子表达式查询请求

> POST /secure_operate/v1/expressions

**接口描述**

算子表达式查询请求， 用于查询当前算子服务支持的表达式

**响应体**

0 响应数据格式：JSON

| 参数名称        | 数据类型      | 可选  | 描述                               |
| --------------- | ------------- | ----- | ---------------------------------- |
| expressions     | array[object] | false | 表达式信息数组                     |
| ⇥ protocolCode | string        | false | 协议名称编码                       |
| ⇥ providerCode | string        | false | 提供厂商名称编码                   |
| ⇥ version      | string        | false | 协议版本号                         |
| ⇥ expression   | string        | false | 表达式名称                         |
| ⇥ params       | array[object] | false | 表达式超参                         |
| ⇥⇥ paramKey   | string        | false | 超参的形参编码                     |
| ⇥⇥ type       | string        | false | 参数的数据类型，限于基本数据类型。 |
| ⇥⇥ comment    | string        | false | 超参说明                           |
| ⇥⇥ paramDemo  | string        | false | 参数实例                           |

#### 7.2.3 异步化关闭接口

> POST /secure_operate/v1/kill

**接口描述**

异步化关闭接口,用于关闭一个已发起的异步任务

**请求体**

| 参数名称     | 数据类型 | 可选  | 描述                                                                                       |
| ------------ | -------- | ----- | ------------------------------------------------------------------------------------------ |
| taskId       | string   | false | 任务 ID，用于约定对齐算子、算法上下文的任务编号                                            |
| subTaskId    | string   | true  | [可选]子任务 ID，用于算法对任务进行拆分或并行计算时使用，一般编码方式是 taskId+ 分片后缀。 |
| localPartyId | string   | false | 本方的参与方 ID                                                                            |

**响应体**

0 响应数据格式：JSON

| 参数名称        | 数据类型      | 可选  | 描述                                                                                                                                     |
| --------------- | ------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| code            | int32         | false | 0 正常，否则错误码 错误码分段: 100-199 表示系统层面的异常，比如算子服务未正常启动；                                                      |
| msg             | string        | false | 返回信息描述                                                                                                                             |
| result          | array[object] | false | 本次计算返回的结果，如果是异步调用模式下，则不立即返回此参数，可通过异步结果查询接口，获取此参数。                                       |
| ⇥ dataValueTag | object        | false | 对算子输入输出一个参数的描述。                                                                                                           |
| ⇥⇥ type       | string        | false | 标记数据传输方式，Direct,标识直接传值，如果希望使用存储引擎来传值，可以使用引擎名称，例如 myRedis。                                      |
| ⇥⇥ name       | string        | false | 与表达式中的对应参数 name 进行关联， 让表达式能够根据 name 定位的数据。                                                                  |
| ⇥⇥ uri        | string        | false | 非 Direct 情况下使用，使用存储引擎时， 指定存储引擎的资源定位符                                                                          |
| ⇥⇥ key        | string        | false | 非 Direct 情况下使用，使用存储引擎时，使用的 key 用于数据读写。                                                                          |
| ⇥⇥ dtype      | string        | false |                                                                                                                                          |
| ⇥⇥ shape      | array[int32]  | false | 用于标记输入输出数据的形状，shape 的元素给出了相应维度上的数组尺寸的长度。                                                               |
| ⇥⇥ delete     | boolean       | false | 默认为 false,数据使用完成之后，是否清理。                                                                                                |
| ⇥ directValue  | string        | false | 直接传值的数据，如果不采集直接传值的方式，则该值为空。该字段的处理方式上，是将要传输的数据块的转换为字节数组，再通过 Base64 编码后得到字 |

#### 7.2.4 异步化辅助查询接口

> POST /secure_operate/v1/query

**接口描述**

异步化辅助查询接口，用于查询一个已发起的异步任务的执行结果

**请求体**

| 参数名称     | 数据类型 | 可选  | 描述                                                                                       |
| ------------ | -------- | ----- | ------------------------------------------------------------------------------------------ |
| taskId       | string   | false | 任务 ID，用于约定对齐算子、算法上下文的任务编号                                            |
| subTaskId    | string   | false | [可选]子任务 ID，用于算法对任务进行拆分或并行计算时使用，一般编码方式是 taskId+ 分片后缀。 |
| localPartyId | string   | false | 本方的参与方 ID                                                                            |

**响应体**

0 响应数据格式：JSON

| 参数名称        | 数据类型      | 可选  | 描述                                                                                                                                                                                                                                                                                                                         |
| --------------- | ------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| code            | int32         | false | 0 正常，否则错误码 错误码分段: 100-199 表示系统层面的异常，比如算子服务未正常启动； 200-299 表示依赖本地环境所产生的异常，如依赖的节点内存储系统发生异常； 300-399 表示节点间的处理异常，包括节点间通信和节点间的系统异常； 400-999 表示内部的逻辑错误，比如参数错误产生的异常，数据格式错误、表达式不存在、算子异常终止等。 |
| msg             | string        | false | 返回信息描述                                                                                                                                                                                                                                                                                                                 |
| result          | array[object] | false | 本次计算返回的结果，如果是异步调用模式下，则不立即返回此参数，可通过异步结果查询接口，获取此参数。                                                                                                                                                                                                                           |
| ⇥ dataValueTag | object        | false | 对算子输入输出一个参数的描述。                                                                                                                                                                                                                                                                                               |
| ⇥⇥ type       | string        | false | 标记数据传输方式，Direct,标识直接传值，如果希望使用存储引擎来传值，可以使用引擎名称，例如 myRedis。                                                                                                                                                                                                                          |
| ⇥⇥ name       | string        | false | 与表达式中的对应参数 name 进行关联， 让表达式能够根据 name 定位的数据。                                                                                                                                                                                                                                                      |
| ⇥⇥ uri        | string        | false | 非 Direct 情况下使用，使用存储引擎时， 指定存储引擎的资源定位符                                                                                                                                                                                                                                                              |
| ⇥⇥ key        | string        | false | 非 Direct 情况下使用，使用存储引擎时，使用的 key 用于数据读写。                                                                                                                                                                                                                                                              |
| ⇥⇥ dtype      | string        | false | 用于标记输入输出数据的类型，在数据传输过程中，数据块以字节数组的形式进行传输，dtype 对数据块的格式进行描述，用于将字节数据转换为所需要的数据类型，详细说明，参考 dtype 枚举说明。                                                                                                                                            |
| ⇥⇥ shape      | array[int32]  | false | 用于标记输入输出数据的形状，shape 的元素给出了相应维度上的数组尺寸的长度。                                                                                                                                                                                                                                                   |
| ⇥⇥ delete     | boolean       | false | 默认为 false,数据使用完成之后，是否清理。                                                                                                                                                                                                                                                                                    |
| ⇥ directValue  | string        | false | 直接传值的数据，如果不采集直接传值的方式，则该值为空。该字段的处理方式上，是将要传输的数据块的转换为字节数组，再通过 Base64 编码后得到字符串形式的值，以便支持不同类型的 RPC 协议。数据块转换到字节数组的方式，由 DataValueTag 中的 dtype 和 shape 确定。                                                                    |
