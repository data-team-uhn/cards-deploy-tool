#!/bin/sh

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

[ -z $CARDS_MOCK_SERVER_WEBSOCKET_URL ] && {
  echo "ERROR: CARDS_MOCK_SERVER_WEBSOCKET_URL environment variable has not been set";
  exit 1;
}

BASIC_AUTH_PARAM=""
[ -z $AUTH ] || {
  BASIC_AUTH_PARAM="--basic-auth $AUTH";
};

echo "Starting websocat to proxy local web browser to mock CARDS environment..."
websocat $BASIC_AUTH_PARAM --binary tcp-l:0.0.0.0:8888 ${CARDS_MOCK_SERVER_WEBSOCKET_URL}
