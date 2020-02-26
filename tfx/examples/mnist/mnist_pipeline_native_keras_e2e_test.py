# Lint as: python2, python3
# Copyright 2019 Google LLC. All Rights Reserved.
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
"""E2E Tests for tfx.examples.mnist.mnist_pipeline_native_keras."""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from typing import Text

import tensorflow as tf

from tfx.examples.mnist import mnist_pipeline_native_keras
from tfx.orchestration import metadata
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner


class MNISTPipelineNativeKerasEndToEndTest(tf.test.TestCase):

  def setUp(self):
    super(MNISTPipelineNativeKerasEndToEndTest, self).setUp()
    self._test_dir = os.path.join(
        os.environ.get('TEST_UNDECLARED_OUTPUTS_DIR', self.get_temp_dir()),
        self._testMethodName)

    self._pipeline_name = 'keras_test'
    self._data_root = os.path.join(
        os.path.dirname(__file__), 'data-mnist-small')
    self._module_file = os.path.join(
        os.path.dirname(__file__), 'mnist_utils_native_keras.py')
    self._pipeline_root = os.path.join(self._test_dir, 'tfx', 'pipelines',
                                       self._pipeline_name)
    self._metadata_path = os.path.join(self._test_dir, 'tfx', 'metadata',
                                       self._pipeline_name, 'metadata.db')

  def assertExecutedOnce(self, component: Text) -> None:
    """Check the component is executed exactly once."""
    component_path = os.path.join(self._pipeline_root, component)
    self.assertTrue(tf.io.gfile.exists(component_path))
    outputs = tf.io.gfile.listdir(component_path)
    for output in outputs:
      execution = tf.io.gfile.listdir(os.path.join(component_path, output))
      self.assertEqual(1, len(execution))

  def assertPipelineExecution(self) -> None:
    self.assertExecutedOnce('ImportExampleGen')
    self.assertExecutedOnce('Evaluator')
    self.assertExecutedOnce('ExampleValidator')
    self.assertExecutedOnce('SchemaGen')
    self.assertExecutedOnce('StatisticsGen')
    self.assertExecutedOnce('Trainer')
    self.assertExecutedOnce('Transform')

  def testMNISTPipelineNativeKeras(self):
    BeamDagRunner().run(
        mnist_pipeline_native_keras._create_pipeline(
            pipeline_name=self._pipeline_name,
            data_root=self._data_root,
            module_file=self._module_file,
            pipeline_root=self._pipeline_root,
            metadata_path=self._metadata_path))

    self.assertTrue(tf.io.gfile.exists(self._metadata_path))
    metadata_config = metadata.sqlite_metadata_connection_config(
        self._metadata_path)
    with metadata.Metadata(metadata_config) as m:
      artifact_count = len(m.store.get_artifacts())
      execution_count = len(m.store.get_executions())
      self.assertGreaterEqual(artifact_count, execution_count)
      self.assertEqual(7, execution_count)

    self.assertPipelineExecution()


if __name__ == '__main__':
  tf.compat.v1.enable_v2_behavior()
  tf.test.main()
