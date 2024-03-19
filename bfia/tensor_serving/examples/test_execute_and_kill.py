import asyncio
from tscli import AsyncTensorClient, secure_operate_pb2, packer
import define_parties


async def vds_role_0_and_kill():
    arr = [1, 2, 3, 4]
    dtype = "int32"
    shape = [len(arr)]

    req = secure_operate_pb2.ExecuteRequest(
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

    client = AsyncTensorClient(define_parties.servring_addr0)
    resp = await client.execute(req)

    assert(resp.code == 0)

    kill_resp = await client.kill(secure_operate_pb2.TaskTabRequest(taskId="a", subTaskId="b", localPartyId=define_parties.role0))
    print(kill_resp)


async def main():
    await vds_role_0_and_kill()


if __name__ == "__main__":
    asyncio.run(main())
    pass
