import threading
from tscli import TensorClient, secure_operate_pb2, packer
import define_parties
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--role", type=int, default=-1, choices=[-1, 0, 1],
                    help="role, defalut value is -1, mean run all role")

args = parser.parse_args()
print("args=", args)

def mvm_role_0():
    arr = [1, 2, 3, 4]
    dtype = "int32"
    shape = [4]


    req = secure_operate_pb2.ExecuteRequest(
        taskId="a",
        subTaskId="b",
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
        expression="mvm",
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
    client = TensorClient(define_parties.servring_addr0)

    resp = client.execute(req)
    result = resp.result[0]
    val = packer.unpack_from_bytes(
        result.directValue, result.dataValueTag.dtype)
    #print("resp = ", resp)
    print("val=", val)


def mvm_role_1():
    arr = [5, 6, 7, 8, 1, 2, 3, 4]
    dtype = "int32"
    shape = [4, 2]

    req = secure_operate_pb2.ExecuteRequest(
        taskId="a",
        subTaskId="b",
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
        expression="mvm",
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
                    name="Y",
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
    client = TensorClient(define_parties.servring_addr1)

    resp = client.execute(req)
    result = resp.result[0]
    val = packer.unpack_from_bytes(
        result.directValue, result.dataValueTag.dtype)
    #print("resp = ", resp)
    print("val=", val)


def main():
    if args.role == -1:
        t1 = threading.Thread(target=mvm_role_0)
        t2 = threading.Thread(target=mvm_role_1)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    elif args.role == 0:
        mvm_role_0()
    elif args.role == 1:
        mvm_role_1()
    else:
        assert(False)


if __name__ == "__main__":
    main()

