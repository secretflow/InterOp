

import asyncio
import argparse
import threading
from tscli import TensorClient, AsyncTensorClient, secure_operate_pb2, packer
import define_parties
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--role", type=int, default=-1, choices=[-1, 0, 1],
                    help="role, defalut value is -1, mean run all role")
parser.add_argument("-s", "--sync", type=int, default=1, choices=[0, 1],
                    help="async, defalut value is 1, mean use TensorClient, otherwise use AsyncTensorClient")

args = parser.parse_args()
print("args=", args)


def vds_role0_req():
    arr = [1, 2, 3, 4]
    dtype = "int32"
    shape = [len(arr)]
    return secure_operate_pb2.ExecuteRequest(
        taskId="a1",
        subTaskId="b1",
        asyncMode=False,
        timeout=0,
        mpcProtocol=secure_operate_pb2.MpcProtocol(
            protocolCode="ss",
            providerCode="lanxiang",
            version="0.0.1",
            param={
                    "aaa": "bbb"
            }
        ),
        expression="vds",
        parties=[
            define_parties.role0,
            define_parties.role1
        ],
        localPartyId=define_parties.role0,
        resultParties=[
            define_parties.role0,
            define_parties.role1
        ],
        inputs=[
            secure_operate_pb2.DataValue(
                dataValueTag=secure_operate_pb2.DataValueTag(
                    type="direct",
                    name="x",
                    dtype=dtype,
                    shape=shape
                ),
                directValue=packer.pack_to_bytes(arr, dtype)
            )
        ],
        outputMethod=[secure_operate_pb2.DataValueTag(
            type="direct"
        )],
    )


def vds_role1_req():
    arr = [5, 6, 7, 8]
    dtype = "int32"
    shape = [len(arr)]

    return secure_operate_pb2.ExecuteRequest(
        taskId="a1",
        subTaskId="b1",
        asyncMode=False,
        timeout=0,
        mpcProtocol=secure_operate_pb2.MpcProtocol(
            protocolCode="ss",
            providerCode="lanxiang",
            version="0.0.1",
            param={
                    "aaa": "bbb"
            }
        ),
        expression="vds",
        parties=[
            define_parties.role0,
            define_parties.role1
        ],
        localPartyId=define_parties.role1,
        resultParties=[
            define_parties.role0,
            define_parties.role1
        ],
        inputs=[
            secure_operate_pb2.DataValue(
                dataValueTag=secure_operate_pb2.DataValueTag(
                    type="direct",
                    name="y",
                    dtype=dtype,
                    shape=shape
                ),
                directValue=packer.pack_to_bytes(arr, dtype)
            )
        ],
        outputMethod=[secure_operate_pb2.DataValueTag(
            type="direct"
        )],
    )


def vds_role0():
    client = TensorClient(define_parties.servring_addr0)
    req = vds_role0_req()
    resp = client.execute(req)

    if resp.code == 0:
        val = resp.result[0]
        # 非direct类型，需要外层从存储引擎中取出数据，再调用unpack_from_bytes
        ret = packer.unpack_from_bytes(
            val.directValue, val.dataValueTag.dtype)
        print(ret)
    else:
        print("error code:", resp.code, ",msg:", resp.msg)


def vds_role1():
    client = TensorClient(define_parties.servring_addr1)
    req = vds_role1_req()
    resp = client.execute(req)

    if resp.code == 0:
        val = resp.result[0]
        # 非direct类型，需要外层从存储引擎中取出数据，再调用unpack_from_bytes
        ret = packer.unpack_from_bytes(
            val.directValue, val.dataValueTag.dtype)
        print(ret)
    else:
        print("error code:", resp.code, ",msg:", resp.msg)


def sync_main():
    if args.role == -1:
        t1 = threading.Thread(target=vds_role0)
        t2 = threading.Thread(target=vds_role1)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    elif args.role == 0:
        vds_role0()
    elif args.role == 1:
        vds_role1()
    else:
        assert(False)


async def vds_role_0_async():
    req = vds_role0_req()
    client = AsyncTensorClient(define_parties.servring_addr0)
    resp = await client.execute(req)
    result = resp.result[0]
    val = packer.unpack_from_bytes(
        result.directValue, result.dataValueTag.dtype)
    #print("resp = ", resp)
    print("val=", val)


async def vds_role_1_async():
    req = vds_role1_req()
    client = AsyncTensorClient(define_parties.servring_addr1)
    resp = await client.execute(req)
    result = resp.result[0]
    val = packer.unpack_from_bytes(
        result.directValue, result.dataValueTag.dtype)
    #print("resp = ", resp)
    print("val=", val)


async def async_main():
    if args.role == -1:
        return await asyncio.gather(
            vds_role_0_async(),
            vds_role_1_async()
        )

    if args.role == 0:
        return await vds_role_0_async()

    if args.role == 1:
        return await vds_role_1_async()

    assert(False)


if __name__ == "__main__":
    if args.sync == 1:
        sync_main()
    else:
        import asyncio
        asyncio.run(async_main())
