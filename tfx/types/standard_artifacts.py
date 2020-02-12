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
"""A set of standard TFX Artifact types.

Note: the artifact definitions here are expected to change.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Text
import tensorflow as tf

from tfx.types.artifact import Artifact
from tfx.types.artifact import Property
from tfx.types.artifact import PropertyType

# Span for an artifact.
SPAN_PROPERTY = Property(type=PropertyType.INT)
# Comma separated of splits for an artifact. Empty string means artifact
# has no split.
SPLIT_NAMES_PROPERTY = Property(type=PropertyType.STRING)
# Value for a string-typed artifact.
STRING_VALUE_PROPERTY = Property(type=PropertyType.STRING)


class Examples(Artifact):
  TYPE_NAME = 'Examples'
  PROPERTIES = {
      'span': SPAN_PROPERTY,
      'split_names': SPLIT_NAMES_PROPERTY,
  }


class ExampleAnomalies(Artifact):
  TYPE_NAME = 'ExampleAnomalies'
  PROPERTIES = {
      'span': SPAN_PROPERTY,
  }


class ExampleStatistics(Artifact):
  TYPE_NAME = 'ExampleStatistics'
  PROPERTIES = {
      'span': SPAN_PROPERTY,
      'split_names': SPLIT_NAMES_PROPERTY,
  }


class ExternalArtifact(Artifact):
  TYPE_NAME = 'ExternalArtifact'


class InferenceResult(Artifact):
  TYPE_NAME = 'InferenceResult'


class InfraBlessing(Artifact):
  TYPE_NAME = 'InfraBlessing'


class Model(Artifact):
  TYPE_NAME = 'Model'


class ModelBlessing(Artifact):
  TYPE_NAME = 'ModelBlessing'


class ModelEvaluation(Artifact):
  TYPE_NAME = 'ModelEvaluation'


class PushedModel(Artifact):
  TYPE_NAME = 'PushedModel'


class Schema(Artifact):
  TYPE_NAME = 'Schema'


# DO NOT SUBMIT: Pending implementation of SerializableArtifact.
class StringType(Artifact):
  """String-typed artifact."""
  TYPE_NAME = 'StringType'
  PROPERTIES = {
      'value': STRING_VALUE_PROPERTY,
  }

  def read(self) -> Text:
    return tf.io.gfile.GFile(self.uri, 'rb').read()

  def write(self, value: Text):
    tf.io.gfile.GFile(self.uri, 'wb').write(value)


class TransformGraph(Artifact):
  TYPE_NAME = 'TransformGraph'


# Still WIP and subject to change.
class HyperParameters(Artifact):
  TYPE_NAME = 'HyperParameters'
