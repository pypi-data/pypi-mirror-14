# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
class CfAccountQueryRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'CF', '2015-11-27', 'CfAccountQuery')
		self.set_protocol_type('https');

	def get_AppKey(self):
		return self.get_query_params().get('AppKey')

	def set_AppKey(self,AppKey):
		self.add_query_param('AppKey',AppKey)

	def get_SceneId(self):
		return self.get_query_params().get('SceneId')

	def set_SceneId(self,SceneId):
		self.add_query_param('SceneId',SceneId)

	def get_Ip(self):
		return self.get_query_params().get('Ip')

	def set_Ip(self,Ip):
		self.add_query_param('Ip',Ip)

	def get_PhoneNumber(self):
		return self.get_query_params().get('PhoneNumber')

	def set_PhoneNumber(self,PhoneNumber):
		self.add_query_param('PhoneNumber',PhoneNumber)

	def get_Trans(self):
		return self.get_query_params().get('Trans')

	def set_Trans(self,Trans):
		self.add_query_param('Trans',Trans)

	def get_CFTimestamp(self):
		return self.get_query_params().get('CFTimestamp')

	def set_CFTimestamp(self,CFTimestamp):
		self.add_query_param('CFTimestamp',CFTimestamp)

	def get_AppToken(self):
		return self.get_query_params().get('AppToken')

	def set_AppToken(self,AppToken):
		self.add_query_param('AppToken',AppToken)