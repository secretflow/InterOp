

import asyncio
import argparse
import threading
from tscli import AsyncTensorClient, secure_operate_pb2, packer
import define_parties
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--role", type=int, default=-1, choices=[-1, 0, 1],
                    help="role, defalut value is -1, mean run all role")

args = parser.parse_args()
print("args=", args)


def vds_role0_req():
    arr = [1, 2, 3, 4]
    dtype = "int32"
    shape = [len(arr)]
    return secure_operate_pb2.ExecuteRequest(
        taskId="a",
        subTaskId="b",
        asyncMode=True,
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
        taskId="a",
        subTaskId="b",
        asyncMode=True,
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


async def vds_role_0_and_query():
    req = vds_role0_req()
    client = AsyncTensorClient(define_parties.servring_addr0)
    resp = await client.execute(req)
    assert(resp.code == 0)

    await asyncio.sleep(3)

    resp = await client.query(secure_operate_pb2.TaskTabRequest(
        taskId="a", subTaskId="b", localPartyId=define_parties.role0))

    result = resp.result[0]
    val = packer.unpack_from_bytes(
        result.directValue, result.dataValueTag.dtype)
    #print("resp = ", resp)
    print("val=", val)


async def vds_role_1_and_query():
    req = vds_role1_req()
    client = AsyncTensorClient(define_parties.servring_addr1)
    resp = await client.execute(req)
    assert(resp.code == 0)

    await asyncio.sleep(3)

    resp = await client.query(secure_operate_pb2.TaskTabRequest(
        taskId="a", subTaskId="b", localPartyId=define_parties.role1))

    result = resp.result[0]
    val = packer.unpack_from_bytes(
        result.directValue, result.dataValueTag.dtype)
    #print("resp = ", resp)
    print("val=", val)


async def main():
    if args.role == -1:
        return await asyncio.gather(
            vds_role_0_and_query(),
            vds_role_1_and_query()
        )

    if args.role == 0:
        return await vds_role_0_and_query()

    if args.role == 1:
        return await vds_role_1_and_query()

    assert(False)


if __name__ == "__main__":
    asyncio.run(main())
    pass
