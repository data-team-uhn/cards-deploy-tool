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


tinyproxy -c /tinyproxy.conf

[ -z $UNIX_WEBSOCKET_LISTEN ] && {
  echo "Listening for WebSocket connections on TCP port";
  websocat --binary ws-l:0.0.0.0:8889 tcp:127.0.0.1:8888;
}

[ -z $UNIX_WEBSOCKET_LISTEN ] || {
  echo "Listening for WebSocket connections on UNIX domain socket"
  websocat --binary l-ws-unix:${UNIX_WEBSOCKET_LISTEN} tcp:127.0.0.1:8888;
}
