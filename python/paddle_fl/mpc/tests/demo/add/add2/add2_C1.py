# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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

import unittest
from multiprocessing import Manager
import numpy as np
import paddle.fluid as fluid
import paddle_fl.mpc as pfl_mpc
import test_op_base
from paddle_fl.mpc.data_utils.data_utils import get_datautils

aby3 = get_datautils('aby3')

class TestOpAdd2_C1(test_op_base.TestOpBase):

    def add2_C1(self, **kwargs):

        role = 1
        num = 100
        d_1 = np.load('data_C1_P0.npy',allow_pickle=True)
        d_2 = np.load('data_C1_P1.npy',allow_pickle=True)
        pfl_mpc.init("aby3", role, "localhost", self.server, int(self.port))
        x = pfl_mpc.data(name='x', shape=[num], dtype='int64')
        y = pfl_mpc.data(name='y', shape=[num], dtype='int64')
        # math_add = x + y
        math_add = pfl_mpc.layers.elementwise_add(x, y, axis=1)
        exe = fluid.Executor(place=fluid.CPUPlace())
        results = exe.run(feed={'x': d_1, 'y': d_2}, fetch_list=[math_add])
        np.save('result_C1.npy', results[0])

    def test_add2_C1(self):
        ret = self.multi_party_run1(target=self.add2_C1)

if __name__ == '__main__':
    unittest.main()