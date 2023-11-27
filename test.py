#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing,
  software distributed under the License is distributed on an
  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  KIND, either express or implied.  See the License for the
  specific language governing permissions and limitations
  under the License.
"""

import os
import sys
import json
import yaml
import requests
import termcolor

EXEC_TYPE_FUNCTIONS = {}

def runShell(stepExec):
  # Runs the given command and throws an error if the command returns a non-zero exit status
  cmd = stepExec['code']
  assert os.system(cmd) == 0
EXEC_TYPE_FUNCTIONS['shell'] = runShell

def httpResponse(stepExec):
  # Makes a HTTP request to the specified URL
  # Asserts that:
  #   - The HTTP response code is the expected one
  #   - The response contains certain lines
  #   - The response does not contain certain lines
  httpMethod = stepExec['httpMethod']
  url = stepExec['url']
  expectedStatusCode = stepExec['responseCode']
  expectedContainsLines = stepExec['responseContains']
  expectedOmittedLines = stepExec['responseContainsNot']
  resp = requests.request(httpMethod, url)
  assert expectedStatusCode == resp.status_code
  responseLines = [line.lstrip().rstrip() for line in resp.text.split('\n')]
  for line in expectedContainsLines:
    assert line in responseLines
  for line in expectedOmittedLines:
    assert line not in responseLines
EXEC_TYPE_FUNCTIONS['httpResponse'] = httpResponse

def checkDockerComposeYAML(stepExec):
  yamlPath = stepExec['yamlPath']
  comparator = stepExec['comparator']
  assert comparator in ['==', 'exists', 'existsNot', 'contains', 'containsNot', 'keysetEquals']
  with open('docker-compose.yml', 'r') as f_yaml:
    yaml_obj = yaml.load(f_yaml)
  resolvedEntity = yaml_obj
  entityExists = True
  try:
    for node in yamlPath:
      resolvedEntity = resolvedEntity[node]
  except KeyError as e:
    entityExists = False
  except IndexError as e:
    entityExists = False
  if comparator == '==':
    assert entityExists
    assert stepExec['expectedValue'] == resolvedEntity
  elif comparator == 'exists':
    assert entityExists
  elif comparator == 'existsNot':
    assert not entityExists
  elif comparator == 'contains':
    assert entityExists
    assert stepExec['expectedValue'] in resolvedEntity
  elif comparator == 'containsNot':
    assert entityExists
    assert stepExec['expectedValue'] not in resolvedEntity
  elif comparator == 'keysetEquals':
    assert set(stepExec['expectedValue']) == set(resolvedEntity.keys())
EXEC_TYPE_FUNCTIONS['checkDockerComposeYAML'] = checkDockerComposeYAML

def doExec(stepExec):
  execType = stepExec['type']
  EXEC_TYPE_FUNCTIONS[execType](stepExec)

def runStep(step):
  stepName = step['name']
  stepExec = step['exec']
  print(termcolor.colored("Running {}".format(stepName), "cyan"))
  try:
    doExec(stepExec)
  except AssertionError as e:
    print(termcolor.colored("Failed at step {}".format(stepName), "red"))
    raise e
  print(termcolor.colored("{} --> OK".format(stepName), "green"))

def runTestWorkflow(testWorkflow):
  for step in testWorkflow:
    runStep(step)


TEST_WORKFLOW_FILE = sys.argv[1]
with open(TEST_WORKFLOW_FILE) as f_test_workflow:
  runTestWorkflow(json.load(f_test_workflow))
