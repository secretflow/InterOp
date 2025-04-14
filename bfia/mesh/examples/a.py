#
# Copyright 2023 The BFIA Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import mesh
from mesh import Mesh, log, ServiceLoader, Transport, Routable
from mesh.prsim import Metadata


def main():
    mesh.start()
    transport = Routable.of(ServiceLoader.load(Transport).get("mesh"))
    session = transport.with_address("127.0.0.1:7304").local().open('session_id', {
        Metadata.MESH_TOKEN.key(): 'TOKEN',
        Metadata.MESH_TRACE_ID.key(): Mesh.context().get_trace_id(),
        Metadata.MESH_TARGET_NODE_ID.key(): 'LX0000011000050',
    })
    for index in range(100):
        i0405 = f"04-05包{index}"
        log.info(f":{i0405}")
        session.push(i0405.encode('utf-8'), {})
        i0504 = session.pop()
        log.info(f":{i0504}")
    session.release(0)
    mesh.stop()


if __name__ == "__main__":
    main()
