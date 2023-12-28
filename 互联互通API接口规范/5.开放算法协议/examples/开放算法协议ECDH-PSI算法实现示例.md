目前已经针对ECDH-PSI协议部分，隐语社区进行了开源实现，相关实现代码见：
- 握手协议： https://github.com/secretflow/interconnection-impl/blob/main/ic_impl/algo/psi/v2/psi_handler_v2.cc
- 算法实际运行：https://github.com/secretflow/psi/blob/main/psi/psi/core/ecdh_psi.cc

该实现结果已与洞见，华控，工商银行等公司等完成联调互通的实践。