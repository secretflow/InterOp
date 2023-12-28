# 隐私计算互联互通 TEE 统一远程证明规范

- [隐私计算互联互通 TEE 统一远程证明规范](#隐私计算互联互通-tee-统一远程证明规范)
  
  - [1 整体框架](#1-整体框架)
  
  - [2 TEE 远程证明流程抽象模型](#2-tee-远程证明流程抽象模型)
  - [3 统一远程证明报告接口抽象](#3-统一远程证明报告接口抽象)
    - [3.1 报告生成接口](#31-报告生成接口)
    - [3.2 报告校验接口](#32-报告校验接口)
  - [4 统一远程证明报告格式抽象](#4-统一远程证明报告格式抽象)
    - [4.1 统一远程证明报告格式](#41-统一远程证明报告格式)
    - [4.2 SGX1 具体报告格式](#42-sgx1-具体报告格式)
    - [4.3 SGX2 具体报告格式](#43-sgx2-具体报告格式)
    - [4.4 HyperEnclave 具体报告格式](#44-hyperenclave-具体报告格式)
    - [4.5 华为鲲鹏具体报告格式](#45-华为鲲鹏具体报告格式)
    - [4.6 海光 CSV 具体报告格式](#46-海光-csv-具体报告格式)
  - [5 统一远程证明校验规则抽象](#5-统一远程证明校验规则抽象)
  - [6 中心化的远程证明代理验证服务](#6-中心化的远程证明代理验证服务)
    - [6.1 统一验证服务的 TEE 节点注册流程](#61-统一验证服务的-tee-节点注册流程)
    - [6.2 统一证明服务的 TEE 节点远程认证流程](#62-统一证明服务的-tee-节点远程认证流程)
    - [6.3 统一证明服务的报告格式](#63-统一证明服务的报告格式)
    - [6.4 统一证明服务的接口参考](#64-统一证明服务的接口参考)
  - [7 基于远程证明的安全通道建立流程](#7-基于远程证明的安全通道建立流程)
    - [7.1 基于公钥的安全通道建立流程](#71-基于公钥的安全通道建立流程)
    - [7.2 基于密钥协商的安全通道建立流程](#72-基于密钥协商的安全通道建立流程)
    - [7.3 结合远程证明和 TLS 流程的安全通道建立流程](#73-结合远程证明和-tls-流程的安全通道建立流程)
  - [8 TEE 应用数据统一封装格式](#8-tee-应用数据统一封装格式)
  - [9 TEE 应用和系统层面互联互通要求](#9-tee-应用和系统层面互联互通要求)
    - [9.1 使用安全算法](#91-使用安全算法)
    - [9.2 利用远程证明增强安全](#92-利用远程证明增强安全)
    - [9.3 保证系统安全](#93-保证系统安全)
    - [9.4 利用安全运维辅助](#94-利用安全运维辅助)


## 1 整体框架

TEE 技术本身涉及硬件体系结构、密码学、数据安全保护等多领域知识结合，相对比较复杂。但是大部分复杂度都在 TEE 方案本身实现层面，TEE 可信应用开发者和用户可以感知的主要是编程方式的变化和远程证明流程。

远程证明是 TEE 技术方案中建立可信的最重要手段。相对可信硬件的不可见，远程证明基本上是 TEE 技术中唯一让用户可以感受到可信，让可信可见的方式。也只有通过远程证明解决了信任的问题之后，数据提供方才能安全地把敏感数据交给可信的程序来处理，才能确保程序是按照期待的逻辑处理数据。 所以要解决异构 TEE 互联互通问题，最核心的就是要解决异构 TEE 远程证明流程兼容问题，以及如何基于远程证明实现数据安全流通问题。 当然 TEE 技术最终会用于可信应用和可信系统设计，TEE 互联互通也离不开整体的互联互联考虑和安全考虑。

围绕异构 TEE 远程证明流程和基于 TEE 的应用系统设计，本规范文档包含如下主要内容：

- 异构 TEE 远程证明流程互联互通
- 统一的安全信道建立和密钥协商流程
- 统一的 TEE 应用数据封装格式
- TEE 应用系统设计安全规范

对应异构 TEE 互联互通整体架构模型如下：

```
.---------------------------------------------------.
应用  | .----------------------.      .------------------. |
互联  | | 应用管理流程以及服务规范 |      |    统一数据格式    | |
互通  | '----------------------'      '------------------' |
      '---------------------------------------------------'

      .---------------------------------------------------.
互联  | .-------------------.      .---------------------. |
互通  | |    安全信道构建     |      |      密钥协商协议     | |
信道  | '-------------------'      '---------------------' |
      '---------------------------------------------------'

      .---------------------------------------------------.
统一  | .------------.    .------------.    .------------. |
远程  | | 统一报告接口 |    | 统一报告格式 |    | 统一校验规则 | |
证明  | '------------'    '------------'    '------------' |
      '---------------------------------------------------'

      .---------------------------------------------------.
可信  | .-------------------.   .--------------.           |
执行  | |     SGX1/SGX2     |   | HyperEnclave |           |
环境  | '-------------------'   '--------------'           |
具体  | .-------------------.   .-----.                    |
实现  | | Kunpeng TrustZone |   | CSV | 已验证的代表性TEE方案 |
方案  | '-------------------'   '-----'    待扩展和更新...   |
      '---------------------------------------------------'

      .---------------------------------------------------.
异构  | .-----------------.     .----------------.         |
体系  | |       X86       |     |      ARM       |    ...  |
结构  | '-----------------'     '----------------'         |
      '---------------------------------------------------'

              图1 : TEE系统互联互通分层模型
```

其中整体架构模型各层级说明如下：

- 异构体系结构：不同的 CPU 硬件架构体系基础，是 TEE 实现的基础。
- 可信执行环境：基于不同种类 TEE 技术方案选取的代表性 TEE 具体实现方案。
- 统一远程证明：屏蔽不同 TEE 方案的的远程证明细节，为互联互通提供基础
- 互联互通信道：基于统一远程证明，完全独立于不同 TEE 实现方案的安全信道建立过程
- 应用互联互通：可信应用和系统层面互联互通相关流程和安全规范。

其中应用管理流程以及服务规范可参考管理层接口文档、传输层接口文档。

**专有名词汇总：**这里汇总本规范文档中已经出现或者即将出现的专有名字或者缩写词，方便后续阅读和随时查看。

| 专有名词               | 含义                                                              |
| ---------------------- | ----------------------------------------------------------------- |
| TEE                    | 可信执行环境(Trusted Execution Environment)                       |
| REE                    | 富执行环境(Rich Execution Environment)                            |
| TA                     | 可信应用（Trusted Application）                                   |
| RA                     | 远程证明（Remote Attestation）                                    |
| KMS                    | 秘钥管理服务（Key Management Service）                            |
| SGX                    | 软件保护扩展（Software Guard Extensions），Intel 的 TEE 方案      |
| HyperEnclave           | 蚂蚁自主研发的不依赖特定 CPU 的 TEE 技术方案                      |
| TrustZone              | ARM CPU 上的 TEE 技术，代表方案有华为鲲鹏等                       |
| CSV                    | 中科海光自主研发的安全虚拟化技术（China Security Virtualization） |
| RATS                   | IETF 提出的远程证明规范（Remote Attestation Procedures）          |
| UAR                    | 统一的远程证明报告格式（Unified Attestation Report）              |
| UAI                    | 统一的远程证明报告接口（Unified Attestation Interfaces）          |
| UAP                    | 统一的远程证明报告校验规则（Unified Attestation Policy）          |
| UAS                    | 统一的远程证明代理校验服务（Unified Attestation Service）         |
| Passport Model         | 护照模式，IEFT RATS 远程证明规范里面定义的一种远程证明流程模型    |
| Background Check Model | 背调模式，IEFT RATS 远程证明规范里面定义的一种远程证明流程模型    |
| SGX1                   | TEE platform 的一种：Intel SGX1 的缩写                            |
| SGX2                   | TEE platform 的一种：Intel SGX2 的缩写                            |
| HYEN                   | TEE platform 的一种：AntGroup HyperEnclave 的缩写                 |
| HWKP                   | TEE platform 的一种：Huawei Kunpeng 的缩写                        |
| HCSV                   | TEE platform 的一种：Hygon CSV 的缩写                             |

## 2 TEE 远程证明流程抽象模型

为了屏蔽不同 TEE 方案中远程证明流程实现差异，我们需要对远程证明流程中相关要素做统一的抽象，其中包括：

- UAR：统一的远程证明报告格式（Unified Attestation Report）是对各种 TEE 方案中不同 RA Report 格式的统一抽象封装。
- UAI：统一的远程证明报告接口（Unified Attestation Interfaces）主要提供和 UAR 相关的两个接口: 报告生成接口和报告校验接口。
- UAP：统一的远程证明规则（Unified Attestation Policy）主要包含用户如何对 TEE 平台和应用做校验的规则集合，这些规则项都是所有 TEE 平台和应用属性的统一抽象。

```
.----------------------------.
        .---->| Unified Attestation Report +----.
        |     '----------------------------'    |
        | Unified Attestation                   | Unified Attestation
        | Report Generation                     | Report Verification
        |                                       v
.-------+-------.                       .--------------.
| TEE Platforms |                       |   Verifier   |
'-------+-------'                       '--------------'
        |                                       ^
        |                                       |
        |     .----------------------------.    |
        '---->| Unified Attestation Policy +----'
              '----------------------------'

                 图2 : Unified Attestation Model
```

因为 TEE 对用户可见的主要差异之一就是不同的远程证明流程和报告格式，而远程证明流程我们可以简单抽象为如何生产和校验报告。 所以这一节主要描述对不同 TEE 方案的远程证明相关接口和数据结构规范化抽象。

## 3 统一远程证明报告接口抽象

为了兼容更多其他编程语言，统一远程证明报告接口（UAI）涉及的 API 封装都使用 C-ABI 语法定义。

### 3.1 报告生成接口

```c
/// @brief C API for unified attestation report generation
/// @param tee_identity: The identity of TEE or TA instance
/// @param report_type: Type of report, "BackgroundCheck"|"Passport"|"Uas"
/// @param report_hex_nonce: Provide freshness if necessary.
///                          It's hex string less than 64 Bytes.
/// @param report_params_buf: The TEE special report generation parameters buffer.
/// @param report_params_len: The length of TEE special report generation parameters.
/// @param report_josn_buf: The output serialized JSON string of AttestationReport.
/// @param report_josn_len: The maximal JSON report buffer size as input,
///                         and the real JSON report string size as output.
///
/// @return 0 means success or other error code
///
extern int UnifiedAttestationGenerateReport(const char* tee_identity,
                                            const char* report_type,
                                            const char* report_hex_nonce,
                                            const char* report_params_buf,
                                            const unsigned int report_params_len,
                                            char* report_json_buf,
                                            unsigned int* report_json_len);
```

tee_identity 为了兼容不同的 TEE 平台，标识不同的 TA 或者 TEE 实例，使用不定长的带结束符的 C 风格字符串。
比如：

- SGX 和 HyperEnclave 的 enclave ID 为 unsigned long long 类型， 可以简单整数和字符串互转。
- 华为鲲鹏的 TA identity 是 16 Bytes 的 UUID，可以简单的使用 HEX String 格式转换

report_type 说明：

| 可选报告格式      | 对应数据格式                                                         |
| ----------------- | -------------------------------------------------------------------- |
| "BackgroundCheck" | 对应 RATS 规范中背调模式，只包含 quote                               |
| "Passport"        | 对应 RATS 规范中护照模式，包含所有校验相关信息，不需要再访问其他服务 |
| "Uas"             | 通过中心化代理校验服务之后的报告格式，算是一种变相的护照模式         |

report_params 需要不同的 TEE 实现方案自定义，为了最少化应用程序调用的修改，建议参考以下通用参数定义方案：

```json
// JSON string of UnifiedAttestationReportParams
// 没有把tee_identity等放入这里， 为了通常情况下避免提供JSON序列化的parameters
{
    "str_report_identity": "...",  // The identity string for report instance
                                   // which is cached inside TEE. It's optional
                                   // and usually used in Asynchronous processes.
    "hex_user_data": "...",        // Max to 64Bytes hex string
    "json_nested_report": "...",   // The JSON serialized string of UnifiedAttestationNestedReports
    "hex_spid": "...",             // SPID for SGX1 only
}
```

不同平台的的额外 Parameter 支持情况

| 校验属性名称  | SGX1 | SGX2 | HYEN | HWKP | HCSV |
| ------------- | ---- | ---- | ---- | ---- | ---- |
| hex_user_data | Y    | Y    | Y    | Y    | Y    |
| hex_spid      | Y    | -    | -    | -    | -    |

- 不同值含义
  - Y: 支持
  - -: 不支持

### 3.2 报告校验接口

```c
/// @brief C API for unified attestation report verification
///
/// @param report_json_str: The serialized JSON string of UnifiedAttestationReport.
/// @param report_json_len: The length of serialized JSON string of UnifiedAttestationReport.
/// @param policy_json_str: The serialized JSON string for UnifiedAttestationPolicy.
/// @param policy_json_len: The length of serialized JSON string for UnifiedAttestationPolicy.
///
/// @return 0 means success or other error code
///
int UnifiedAttestationVerifyReport(const char* report_json_str,
                                   const unsigned int report_json_len,
                                   const char* policy_json_str,
                                   const unsigned int policy_json_len);
```

## 4 统一远程证明报告格式抽象

统一的远程证明报告格式是为了屏蔽不同 TEE 方案中报告格式的差异，方便统一远程证明接口兼容不同的 TEE 平台。

考虑到不同 TEE 系统中不同编程语言的兼容性，使用 JSON 格式作为统一远程证明报告格式，方便各种应用之间数据交互。具体实现也可以考虑利用 protobuf 定义数据格式，可以方便和 JSON 格式之间互转。

对于具体的 JSON 数据项键名，采用统一命名规则： 数据值格式前缀_键名称。数据值格式前缀含义如下：

| 前缀   | 对应数据值格式                       |
| ------ | ------------------------------------ |
| str    | Normal string                        |
| hex    | HEX string, using capital letter A-F |
| b64    | Base64 encoded                       |
| pem    | PEM string for key or certificate    |
| json   | JSON string                          |
| int    | int                                  |
| int64  | int64                                |
| uint   | uint                                 |
| uint64 | uint64                               |
| bool   | "false" or "true" as string format   |
| bin    | binary data                          |

### 4.1 统一远程证明报告格式

统一远程证明报告格式（UAR）如下：

```json
//UnifiedAttestationReport
{
    // For compatibility and udpate later, current version is "1.0"
    "str_report_version": "1.0",
    "str_report_type":"...",
    "str_tee_platform":"...",
    "json_report":"...",
    // JSON serialized UnifiedAttestationNestedReports
    "json_nested_reports": "..."
}

// UnifiedAttestationNestedReports
{
    // The JSON serialized string of UnifiedAttestationNestedResults
    "json_nested_results" : "...",
    // The signature of json_nested_results
    "b64_nested_signature": "..."
}

// UnifiedAttestationNestedResults
{
    "nested_report_results": [
        // All UnifiedAttestationAttributes，经过本地校验之后的次级TEE信息汇总
        { ... },
        { ... }
    ]
}
```

为了能正确解释具体 TEE 平台的报告，下面列举常用 TEE 平台远程证明报告具体数据结构。

### 4.2 SGX1 具体报告格式

对于 SGX1， "str_platform"="SGX_EPID", "json_report"为下面 IAS 返回信息集合的 JSON 序列化字符串。

```json
// 背调模式时仅使用b64_quote
// Sgx1Report
{
    "b64_quote":"...",
}

// 护照模式时仅使用IAS格式report
// IasReport
{
    "b64_signature":"...",
    "str_signing_cert":"...",
    "str_advisory_url":"...",
    "str_advisory_ids":"",
    "str_response_body":""
}
```

其中 b64_quote 是 Intel SGX SDK 中 sgx_quote_t 结构体二进制数据的 Base64 编码；
b64_quote_body 是 Intel SGX SDK 中 sgx_report_body_t 结构体的二进制数据的 Base64 编码。

参考 Intel 官方文档：[Attestation Service for Intel(R) Software Guard Extensions: API Documentation](https://api.trustedservices.intel.com/documents/sgx-attestation-api-spec.pdf)

### 4.3 SGX2 具体报告格式

对于 SGX2， "str_platform"="SGX_DCAP", "json_report"为下面格式的 JSON 序列化字符串。

```json
// DcapReport
{
    // 背调模式仅使用b64_quote
    "b64_quote":"...",
    // 护照模式需要额外提供PCCS相关信息
    // JSON serialized string of SgxQlQveCollateral
    "json_collateral": "..."
}

// SgxQlQveCollateral
{
    "int64_version":"...",
    "pem_pck_crl_issuer_chain":"...",
    "str_root_ca_crl":"...",
    "str_pck_crl":"...",
    "pem_tcb_info_issuer_chain":"...",
    "str_tcb_info":"...",
    "pem_qe_identity_issuer_chain":"...",
    "str_qe_identity":"..."
}
```

其中 b64_quote 是 intel SGX_SDK 中 sgx_quote3_t 结构体二进制数据的 Base64 编码，json_verification_collateral 是对 PCCS 服务请求返回的数据封装 JSON 序列化。json_verification_collateral 只是在 passport 类型的报告中提供，避免 Verifier 侧连接还需 PCCS 服务器。

### 4.4 HyperEnclave 具体报告格式

对于 HyperEnclave， "str_platform"="HyperEnclave", "json_report"为下面格式的 JSON 序列化字符串。

```json
// HyperenclaveReport
{
    "b64_quote":"..."
}
```

其中 b64_quote 是 intel SGX_SDK 中 sgx_quote_t 结构体二进制数据的 Base64 编码。

### 4.5 华为鲲鹏具体报告格式

对应华为鲲鹏， "str_platform"="Kunpeng", "json_report"为下面格式的 JSON 序列化字符串。

```json
// KunpengReport
{
    "b64_quote":"...",
    "int64_version": 1   //为了标识不同的report版本
}
```

其中 b64_quote 是对华为鲲鹏格式报告 TA_report 数据结构的 Base64 编码字符串。 (TODO: 待确定)

```c
typedef struct __attribute__((__packed__)) report_response
{
    uint32_t version;
    uint64_t ts;
    // 对应Attribute: hex_nonce
    uint8_t nonce[NONCE_SIZE];
    // 对应Attribute: str_tee_identity
    // 字符串格式：C29D01B0-CD13-405A-99F9-06343DFBE691
    TEE_UUID uuid;
    uint32_t scenario;
    uint32_t param_count;
    struct ra_params params[0];
    /* following buffer data:
    // 对应Attribute: hex_ta_measurement
     * (1)ta_img_hash []
    // 对应Attribute: hex_ta_dyn_measurement
     * (2)ta_mem_hash []
     * (3)reserverd []
     * (4)sign_ak []
     * (5)ak_cert []
     */
} kunpeng_report;
```

### 4.6 海光 CSV 具体报告格式

对应海光 CSV， "str_platform"="CSV", "json_report"为下面格式的 JSON 序列化字符串。

```json
// HygonCsvReport
{
    "b64_quote":"...",
    // JSON serialized string of HygonCertChain
    "json_cert_chain": "...",
    // Chip ID for getting cert
    "str_chip_id": "..."
}

// HygonCertChain
{
    // The Base64 string of hygon_root_cert_t
    "b64_hsk_cert":"...",
    // The Base64 string of csv_cert_t
    "b64_cek_cert":"..."
}
```

其中 b64_quote 是对 CSV 报告 csv_attestation_report 数据结构的 Base64 编码字符串。

```c
typedef struct csv_report_s {
    // 对应Attribute: hex_hash_or_pem_pubkey
    hash_block_t user_pubkey_digest;
    // 对应Attribute: hex_prod_id
    uint8_t vm_id[CSV_VM_ID_SIZE];
    // 对应Attribute: hex_platform_sw_version
    uint8_t vm_version[CSV_VM_VERSION_SIZE];
    // 对应Attribute: hex_user_data
    uint8_t user_data[CSV_ATTESTATION_USER_DATA_SIZE];
    // 对应Attribute: hex_nonce
    uint8_t mnonce[CSV_ATTESTATION_MNONCE_SIZE];
    // 对应Attribute: hex_boot_measurement
    hash_block_t measure;
    // 对应Attribute: hex_secure_flags
    uint32_t policy;
    uint32_t sig_usage;
    uint32_t sig_algo;
    uint32_t anonce;
    union {
        uint8_t sig1[72 * 2];
        struct {
            uint8_t r[72];
            uint8_t s[72];
        } ecc_sig1;
    };
    uint8_t pek_cert[HYGON_CSV_CERT_SIZE];
    uint8_t chip_id[CSV_ATTESTATION_CHIP_SN_SIZE];
    uint8_t reserved1[32];
    hash_block_t hmac;
    uint8_t reserved2[1548]; // Padding to a page size
} csv_report_t;
```

注意： 海光报告中上述内容 Attribute 项都被 anonce 异或过，要获取真实值需要再次和 anonce 异或。

## 5 统一远程证明校验规则抽象

校验规则和统一抽象的可信应用程序可以被远程证明校验的相关属性集合对应，校验方可以根据平台选择对应的校验属性。
属性集合是所有 TEE 平台定义的可信应用程序属性的合集。

```json
// UnifiedAttestationAttributes
{
    "str_tee_platform":"...",           // TEE平台标识字符串, 对应UAR中str_platform字段
    "hex_platform_hw_version":"...",    // TEE平台硬件关联版本号
    "hex_platform_sw_version":"...",    // TEE平台软件关联版本号
    "hex_secure_flags":"...",           // TEE平台或者可信实例的安全属性标志位
    "hex_platform_measurement": "...",  // 硬件平台相关组件度量值
    "hex_boot_measurement": "...",      // 启动阶段相关组件度量值
    "str_tee_identity": "...",          // TEE实例或者TA实例的标识符，和生成报告时一致
    "hex_ta_measurement":"...",         // TA的静态度量值
    "hex_ta_dyn_measurement":"...",     // TA的动态度量值
    "hex_signer":"...",                 // TA的签名信息
    "hex_prod_id":"...",                // TA的产品编号
    "str_min_isvsvn":"...",             // TA的软件版本
    "bool_debug_disabled":"...",        // TA是否关闭了debug模式
    "hex_user_data":"...",              // 用户自定义数据
    "hex_hash_or_pem_pubkey": "...",    // 报告中绑定的用户公钥或者其HASH，公钥用于业务数据加密
    "hex_nonce":"...",                  // user_data之外，独立的保证freshness的随机值
    "hex_spid":"..."                    // 第三方ServiceProvider请求标识, 比如SGX1中使用
}
```

> 注意：

- 用作 UnifiedAttestationAttribues 时，hex_hash_or_pem_pubkey 里面存放报告里面解析出来的公钥 HASH hex string 值。
- 用作 UnifiedAttestationPolicy 时，hex_hash_or_pem_pubkey 里面存放的是 pem 格式的完整公钥或者是 HASH hex string 值。
- hex_secure_flags 统一成 hex string 格式而不是 unsigned long 等类型，是为了兼容不同长度，确保 json 中字符串格式形态。

根据 UnifiedAttestationAttributes 我们可以指定对应的校验规则(UAP), 对应格式如下：

```json
// UnifiedAttestationPolicy
{
    // 假定一个公钥和一份报告绑定，可以在这里统一指定公钥。
    // 或者在UnifiedAttestationAttributes里面精确指定每个公钥HASH值
    // 这里的公钥和UnifiedAttestationAttributes里面公钥hash都会被用于校验报告中实际公钥hash
    // 如果报告中存在submodule，那么一定需要在这里指定公钥用于校验
    "pem_public_Key": "...",
    // 主TA的所有可能校验规则，比如多个版本，多个signer都认可
    "main_attributes": [
        {...}, // UnifiedAttestationAttributes
        {...}
    ],
    // multi nested submodules, and each submodule
    // support multi UnifiedAttestationAttributes
    "nested_policies": [
        {
            "sub_attributes": [
                {...}, // UnifiedAttestationAttributes
                {...}
            ]
        },
        { ... } // next submodule
    ]
}
```

不同 TEE 方案支持的校验属性情况如下：

| 校验属性名称            | SGX1 | SGX2 | HYEN | HWKP | HCSV |
| ----------------------- | ---- | ---- | ---- | ---- | ---- |
| str_tee_platform        | Y    | Y    | Y    | Y    | Y    |
| hex_platform_hw_version | Y    | Y    | Y    | -    | Y    |
| hex_platform_sw_version | Y    | Y    | Y    | Y    | Y    |
| hex_secure_flags        | Y    | Y    | Y    | -    | Y    |
| hex_platform_measurment | -    | -    | -    | Y    | -    |
| hex_boot_measurment     | -    | -    | -    | -    | Y    |
| hex_ta_measurement      | Y    | Y    | Y    | Y    | -    |
| hex_ta_dyn_measurement  | -    | -    | -    | Y    | -    |
| hex_signer              | Y    | Y    | Y    | -    | -    |
| hex_prod_id             | Y    | Y    | Y    | -    | -    |
| str_min_isvsvn          | Y    | Y    | Y    | -    | Y    |
| hex_user_data           | Y    | Y    | Y    | Y    | Y    |
| hex_hash_or_pem_pubkey  | Y    | Y    | Y    | Y    | Y    |
| hex_spid                | Y    | -    | -    | -    | -    |
| hex_nonce               | -    | -    | Y    | Y    | Y    |
| bool_debug_disabled     | Y    | Y    | Y    | -    | -    |

- 不同值含义
  - Y: 支持
  - -: 不支持

## 6 中心化的远程证明代理验证服务

由于需要不同的 TEE 之间相互验证远程证明报告，涉及到不同 TEE 的验证机制。如果不改动系统架构，那么各方的 TEE 应用方案中都要同时集成不同 TEE 方案的验证逻辑。若系统需要新增一类 TEE 节点，那么所有互联互通 TEE 节点都需要升级来支持新的 TEE 远程验证逻辑。一方面这会造成互验证的工程复杂度提高，另一方面也不利于系统后期维护。

为了解决上述问题，可独立实现出一个中心化的 TEE 远程证明统一代理验证服务（Unified Attestion Service，以下简称 UAS 或者统一验证服务）。由这个服务收敛所有远程验证差异化逻辑，其他 TEE 端借助证明服务完成与对端的远程验证。使得各个 TEE 端不需要特别地兼容异构 TEE 的认证逻辑。

统一证明服务本身也需要基于 TEE 实现，以此保证其自身验证逻辑的正确性。而各个 TEE 端在交互通信前，需要向对端发起远程验证请求获取统一证明报告发送给统一证明服务。远程验证由统一证明服务代理完成，验证结果由统一证明服务进行背书确认，并且也封装为 UAR 格式，方便 TEE 端做其他额外校验。

通过引入基于中心化的证明服务，可以将 N（N 个节点）x N（N 套远程验证机制）的工程复杂度压缩到 N（N 个节点）x 1（1 套远程验证机制）。

### 6.1 统一验证服务的 TEE 节点注册流程

统一证明服务的 TEE 节点注册流程是为了实现 TEE 节点向 UAS 注册，获取访问凭证。参考过程如下：

**参考流程一**：

- TEE 节点生成表征自己身份的一组公私钥对：ak.pub/ak.priv
- TEE 节点将自己必要的元信息与 ak.pub 发送给 UAS
- UAS 返回自己的根证书以及签发的 ak.crt 给 TEE 节点（为了保证 ak.crt 安全，UAS 作为第二级 CA，由第三方 CA 对 UAS 颁发中间证书）

**参考流程二**：

- TEE 节点提前获取用于验证 UAS 签名的公钥，内置于可信代码中。（UAS 签名公私钥对可以通过安全 KMS 保管）
- TEE 节点开发者或者挑战者都可以通过 UAS 管理界面注册元信息，获取访问凭证 AccessKey（类似 Intel IAS 做法）
- 后续 TEE 节点或者挑战者都可以通过 AccessKey+UAR 请求 UAS 提供的代理验证服务

### 6.2 统一证明服务的 TEE 节点远程认证流程

引入中心化的统一证明服务的 TEE 节点远程认证流程：

a)、护照模式报告转换为 UAS 格式报告

```
.-------.                 .--------------.                   .-----.
| 挑战者 |                 | TEE Attester |                   | UAS |
'---+---'                 '-------+------'                   '--+--'
    | 1) 生成随机的Nonce值          |                             |
    | 请求护照模式远程证明报告        |                             |
    +---------------------------->|                             |
    |                             | 2) TEE节点生成本地            |
    |                             | 护照模式报告                  |
    |                             |                             |
    |                             | 3) 发送统一验证服务验证请求     |
    |                             | (UAR、Nonce和访问凭证)        |
    |                             +---------------------------->|
    |                             |                             |
    |                             |               4) 验证访问凭证 |
    |                             |  根据TEE平台类型调用不同验证逻辑 |
    |                             |   (中间可能涉及对第三方服务请求) +-->
    |                             |  使用签名密钥对Nonce和校验结果  |
    |                             |     签名，并返回UAS统一证明报告 |
    |                             |<----------------------------+
    |                             |                             |
    |                             | TEE节点校验UAS签名(可选)       |
    |<----------------------------+ 5) TEE节点转发UAS格式UAR      |
    |                             |                             |
    | 6) 挑战者校验UAS签名信息       |                             |
    | 然后校验Nonce值               |                             |
    | 选择性校验其他报告内信息        |                             |
    | 完成认证流程                  |                             |
    |                             |                             |

                图3 : 护照模式报告转换为UAS格式报告流程
```

a)、背调模式报告转换为 UAS 格式报告

```
.-------.                     .-------.                 .--------------.
|  UAS  |                     | 挑战者 |                 | TEE Attester |
'---+---'                     '---+---'                 '-------+------'
    |                             | 1) 生成随机的Nonce值          |
    |                             | 请求护照模式远程证明报告        |
    |                             +---------------------------->|
    |                             |                             |
    |                             |            2) TEE节点生成本地 |
    |                             |             背调模式报告并返回 |
    |                             |<----------------------------+
    |     3) 发送统一验证服务验证请求 |                             |
    |        (UAR、Nonce和访问凭证) |                             |
    |<----------------------------+                             |
    |                             |                             |
    | 4) 验证访问凭证               |                             |
    | 根据TEE平台类型调用不同验证逻辑  |                             |
 <--+ (中间可能涉及对第三方服务请求)   |                             |
    | 使用签名密钥对Nonce和校验结果   |                             |
    | 签名，并返回UAS统一证明报告     |                             |
    +---------------------------->|                             |
    |                             |                             |
    |                             | 6) 挑战者校验UAS签名信息       |
    |                             | 然后校验Nonce值               |
    |                             | 选择性校验其他报告内信息        |
    |                             | 完成认证流程                  |
    |                             |                             |

                  图4 : 背调模式报告转换为UAS格式报告流程
```

### 6.3 统一证明服务的报告格式

统一验证服务的返回报告格式也是 UnifiedAttestationReport 格式。
其中"str_platform"="Uas", "json_report"为下面格式的 JSON 序列化字符串。

```protobuf
message UasAttestionResult {
    optional int64 int64_result_code = 1;
    optional string str_tee_platform = 2;
    optional string hex_nonce = 3;
    optional string b64_quote = 4;
}

message UasReport {
    // The JSON serialized UasAttestionResult
    optional string str_uas_result = 1;
      // the UAS signature of str_uas_result
    optional string b64_signature = 2;
}
```

### 6.4 统一证明服务的接口参考

| URL           | POST /v1/interconn/tee/uas/verify                                                                                                                   |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Request Body  | {"biz_id": "your biz id","access_key": "access key","access_secret: "other access secret","nonce": "something as nonce","report": "json input UAR"} |
| Response Body | {"result_code": "0","result_msg": "success-or-other-msg","attestation_result": "json output UAR with UasReport"}                                    |

Request 和 Response Body 中的参数说明如下：

| Parameter          | Description                                 |
| ------------------ | ------------------------------------------- |
| biz_id             | 业务 ID（可选）                             |
| access_key         | 访问凭证密钥                                |
| access_secret      | 其他可能使用的访问凭证相关敏感信息          |
| nonce              | 防止重放攻击的新鲜值                        |
| report             | Json 序列化的 Unified Attestation Report    |
| result_code        | UAS 服务返回的验证请求状态码                |
| result_msg         | UAS 服务返回的验证请求消息                  |
| attestation_result | JSON 序列化的保含 UasReport 的 UAS 类型 UAR |

## 7 基于远程证明的安全通道建立流程

TEE 互联互通的核心就是基于远程证明建立安全通道，发起方将敏感数据已约定好的格式传输到目标 TEE 环境。TEE 平台互联互通安全通道模型可以分为：

- **单向 TEE 互联互通模型**：非 TEE 环境把数据加密传输到 TEE 环境，可能面临不同的 TEE 环境。
- **双向 TEE 互联互通模型**：两个 TEE 环境之间互相传输加密数据，两个 TEE 环境可能是同构或者异构的。双向远程证明不只是简单地把两个单向的相互结合，同时能够利用 TEE 特性担保发起方的身份和保证数据的全流程安全。

```
(Optional Unified Data Format)
.------------.      .--------------------------.      .-------------.
|            |     /       Secure Channel       \     |             |
|    REE     +=====           based on           ====>|     TEE     |
| Platform   |     \ Unified Attestation Report /     |  Platforms  |
'------------'      '--------------------------'      '-------------'

                    图5: 单向TEE互联互通模型


                   (Optional Unified Data Format)
.------------.      .--------------------------.      .------------.
|            |     /       Secure Channel       \     |            |
|     TEE    +<====           based on           ====>+     TEE    |
| Platform A |     \ Unified Attestation Report /     | Platform B |
'------------'      '--------------------------'      '------------'

                    图6 : 双向TEE互联互通模型
```

安全通道建立过程基于远程证明流程和秘钥协商协议。

### 7.1 基于公钥的安全通道建立流程

基于公钥的安全通道建立过程只需要安全地共享 TEE 内部公钥，便可以通过公钥加密数据，TEE 内部私钥解密数据，从而形成逻辑意义上的安全通道。

具体过程如下：

- 生成 TEE 本地统一证明报告，报告内置 TEE 内部公钥 HASH 值
- 数据方获取报告和 TEE 公钥，校验并比对公钥 HASH，一致则信任该公钥
- 数据方通过公钥加密数据发送到 TEE 内
- TEE 内部用私钥解密数据

```protobuf
/// Unified attestation report with public key authentication
message UnifiedAttestationAuthReport {
    UnifiedAttestationReport report = 1;
    string pem_public_key = 2;
}
```

公钥 HASH 在不同的平台按照如下方式内置：

- 对于 SGX1、SGX2、HyperEnclave 平台，公钥 HASH 置于 64Byptes 的 report_data 的高 32Bytes，低 32Bytes 保存其他 user-data。
- 对于 CSV 平台，公钥 HASH 置于 64Byptes 的 user_data 的高 32Bytes，低 32Bytes 保存其他 user-data。
- 对于鲲鹏，（TODO： 没有看到存放 user-data 的字段）

### 7.2 基于密钥协商的安全通道建立流程

通过远程证明报告担保密钥协商过程中间交互数据，在协商密钥的同时完成基于远程证明报告的身份和可信确认。
详细流程可以参考 Intel SGXSDK [远程证明 sample](https://github.com/intel/linux-sgx/tree/master/SampleCode/RemoteAttestation)

### 7.3 结合远程证明和 TLS 流程的安全通道建立流程

远程证明和 TLS 结合流程参考如下：

- 把远程证明报告作为 TLS 证书的 extension 扩展，在校验证书的时候通过注册的回调函数实现报告校验，结合 RA 和 TLS 流程
- 通过可信的代理 CA 组件或者服务校验远程证明报告，然后签发 TLS 通信证书
- 建立普通的 TLS 通道，通道内通过上述协商密钥或者公钥二次加密应用数据

## 8 TEE 应用数据统一封装格式

TEE 应用数据统一封装格式可以帮助可信应用更好的交换和传输数据。考虑应用场景的多样性和复杂性，这里仅提出一些参考意见。

EE 应用数据封装应该包含数据本身、对应元数据、以及可选的用户数据传输握手协议的相关信息（如果不是基于其他类似 TLS 等外部安全通道。）

```json
{
    "payload": {
        "str_cipher_mode":"...",
        "json_data":"..."
    },
    "json_handshake": {
        "json_handshake":"...",
        "b64_signature":"...",
        "auth_report":{
            "attestation_report":{
                ...
            },
            "pem_public_key":"..."
        }
    }
}
```

json_data 可以是明文或者密文，如果是明文，对应如下格式 JSON 序列化字符串：

```json
// DataPackage
{
    "raw_data":{
        ...
    },
    "meta_data":{
        ...
    },
    "data_policy":{
        ...
    }
}
```

## 9 TEE 应用和系统层面互联互通要求

为了满足基于 TEE 实现的可信应用乃至计算系统之间互联互通的基本安全，需要可信应用程序或者整个计算系统的实现满足一定的安全和互联互通要求。

### 9.1 使用安全算法

TEE 应用中应该使用业界共识的安全的密码学算法。

**加密和解密算法**

| 密码学算法 | 国际算法     | 国密算法 |
| ---------- | ------------ | -------- |
| 对称密钥   | AESGCM-256   | SM4      |
| 非对称密钥 | RSA 4096+bit | SM2      |
| 哈希算法   | SHA256       | SM3      |

**签名和校验算法**

| 密码学算法 | 国际算法     | 国密算法 |
| ---------- | ------------ | -------- |
| 非对称密钥 | RSA 4096+bit | SM2      |

**哈希算法**

| 密码学算法 | 国际算法 | 国密算法 |
| ---------- | -------- | -------- |
| 哈希算法   | SHA256   | SM3      |

**数字信封**

| 密码学算法 | 国际算法                  | 国密算法  |
| ---------- | ------------------------- | --------- |
| 数字信封   | AESGCM-256 + RSA 4096+bit | SM4 + SM3 |

**数据密封**

TEE 方案提供 seal、unseal 接口，可以用作持久化保存私有数据，sealed 的数据只能在同一个 CPU 内 unseal。

注意：SGX 方案提供 MRENCLAVE 和 MRSIGNER 两种 seal/unseal 机制，具有不同的数据安全强度，需要谨慎选择。

- MRENCLAVE 模式中，seal/unseal 使用的硬件密钥在派生过程中包含可信应用度量值，只有当前版本可以解密数据，应用升级之后 sealed 数据无法 unseal。
- MRSIGNER 模式中，seal/unseal 使用的硬件密钥在派生过程中不包含可信应用度量值，只要是相同密钥签名，应用升级之后 sealed 数据依然可以 unseal。

### 9.2 利用远程证明增强安全

建议利用远程证明流程增强系统安全。

- 通过远程证明校验之后，才能信任运行在 TEE 中的可信应用程序计算逻辑。
- 结合远程证明机制鉴别可信应用程序身份之后，才能授权操作或者安全通信。

### 9.3 保证系统安全

【可选】利用可信启动或者安全启动流程保证系统的基础可信，利用已证明的可信内核和可信软件组合需要的业务能力。

### 9.4 利用安全运维辅助

【可选】利用安全配置，安全审计、安全运维保证系统全流程和生命周期安全。
