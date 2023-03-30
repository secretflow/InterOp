# 通信套件(mesh)

将算子以服务化的形式，将算子与算法进行分离，通过定义出良好的算子服务接口，实现算子的解耦。通过算子服务化的形式，可独立实现算子服务的硬件平台、操作系统和编程语言，解决隐私计算技术融合的核心难题。在底层的多方安全计算技术与其它技术之间，划分出一道明确的边界，可以有效解决技术融合过程中的问题，能够有效提高技术创新产能、降低技术融合门槛、在多种技术路线之间构建一个可以融合的方案，并能够有望在不同的隐私计算科技公司之间构建一个通用的边界，实现隐私计算互联互通方案。


## api定义
算子服务化对外同时提供grpc和restful样式接口
- restful接口定义见[api/secure_operate.swagger.json](api/secure_operate.swagger.json)
- grpc接口定义见[api/secure_operate.proto](api/secure_operate.proto)

## 调用示例
- 参见[examples](examples)目录
