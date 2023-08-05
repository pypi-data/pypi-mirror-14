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
class CfAccountFeedbackRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'CF', '2015-11-27', 'CfAccountFeedback')
		self.set_protocol_type('https');

	def get_AppKey(self):
		return self.get_query_params().get('AppKey')

	def set_AppKey(self,AppKey):
		self.add_query_param('AppKey',AppKey)

	def get_EventId(self):
		return self.get_query_params().get('EventId')

	def set_EventId(self,EventId):
		self.add_query_param('EventId',EventId)

	def get_UserFeedback(self):
		return self.get_query_params().get('UserFeedback')

	def set_UserFeedback(self,UserFeedback):
		self.add_query_param('UserFeedback',UserFeedback)

	def get_CustomerDecision(self):
		return self.get_query_params().get('CustomerDecision')

	def set_CustomerDecision(self,CustomerDecision):
		self.add_query_param('CustomerDecision',CustomerDecision)

	def get_AliDecision(self):
		return self.get_query_params().get('AliDecision')

	def set_AliDecision(self,AliDecision):
		self.add_query_param('AliDecision',AliDecision)

	def get_DenyReason(self):
		return self.get_query_params().get('DenyReason')

	def set_DenyReason(self,DenyReason):
		self.add_query_param('DenyReason',DenyReason)

	def get_CFTimestamp(self):
		return self.get_query_params().get('CFTimestamp')

	def set_CFTimestamp(self,CFTimestamp):
		self.add_query_param('CFTimestamp',CFTimestamp)

	def get_AppToken(self):
		return self.get_query_params().get('AppToken')

	def set_AppToken(self,AppToken):
		self.add_query_param('AppToken',AppToken)