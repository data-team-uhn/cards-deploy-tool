#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import docker
import shutil
import tarfile

class fileobjFromIterator:
  def __init__(self, iterator):
    self.iterator = iterator
    self.buffer = bytes()
    self.tell_position = 0

  def read(self, size=-1):
    if (size == None) or (size < 0):
      while True:
        try:
          self.buffer += self.iterator.__next__()
        except StopIteration:
          break
      self.tell_position += len(self.buffer)
      return self.buffer

    if len(self.buffer) >= size:
      ret = self.buffer[0:size]
      self.buffer = self.buffer[size:]
      self.tell_position += len(ret)
      return ret
    else:
      while len(self.buffer) < size:
        try:
          self.buffer += self.iterator.__next__()
        except StopIteration:
          break
      ret = self.buffer[0:size]
      self.buffer = self.buffer[size:]
      self.tell_position += len(ret)
      return ret

  def tell(self):
    return self.tell_position

  def seek(self, pos):
    if pos < self.tell():
      raise Exception("Backwards seeking not supported!")
    while self.tell() < pos:
      self.read(pos - self.tell())

def copyFileFromDockerImage(imageName, srcPath, dstPath):
  docker_client = docker.from_env()
  stopped_cards_container = docker_client.containers.create(imageName)
  bits, stat = stopped_cards_container.get_archive(srcPath)
  tar_stream = fileobjFromIterator(bits)
  tf = tarfile.open(fileobj=tar_stream, mode='r|')
  for contained_file in tf:
    with open(dstPath, 'wb') as f_save:
      shutil.copyfileobj(tf.extractfile(contained_file), f_save)
  stopped_cards_container.remove()
