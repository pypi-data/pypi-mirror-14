# Copyright 2015 Google Inc. All rights reserved.
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

import unittest2


class TestSubscription(unittest2.TestCase):
    PROJECT = 'PROJECT'
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
    SUB_NAME = 'sub_name'
    SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
    DEADLINE = 42
    ENDPOINT = 'https://api.example.com/push'

    def _getTargetClass(self):
        from gcloud.pubsub.subscription import Subscription
        return Subscription

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        client = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, None)
        self.assertEqual(subscription.push_endpoint, None)

    def test_ctor_explicit(self):
        client = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     self.DEADLINE, self.ENDPOINT)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_ctor_w_client_wo_topic(self):
        client = _Client(project=self.PROJECT)
        subscription = self._makeOne(self.SUB_NAME, client=client)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is None)

    def test_ctor_w_both_topic_and_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        with self.assertRaises(TypeError):
            self._makeOne(self.SUB_NAME, topic, client=client2)

    def test_ctor_w_neither_topic_nor_client(self):
        with self.assertRaises(TypeError):
            self._makeOne(self.SUB_NAME)

    def test_from_api_repr_no_topics(self):
        from gcloud.pubsub.topic import Topic
        resource = {'topic': self.TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        klass = self._getTargetClass()
        client = _Client(project=self.PROJECT)
        subscription = klass.from_api_repr(resource, client)
        self.assertEqual(subscription.name, self.SUB_NAME)
        topic = subscription.topic
        self.assertTrue(isinstance(topic, Topic))
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.project, self.PROJECT)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_from_api_repr_w_deleted_topic(self):
        klass = self._getTargetClass()
        resource = {'topic': klass._DELETED_TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        klass = self._getTargetClass()
        client = _Client(project=self.PROJECT)
        subscription = klass.from_api_repr(resource, client)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is None)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_from_api_repr_w_topics_no_topic_match(self):
        from gcloud.pubsub.topic import Topic
        resource = {'topic': self.TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        topics = {}
        klass = self._getTargetClass()
        client = _Client(project=self.PROJECT)
        subscription = klass.from_api_repr(resource, client, topics=topics)
        self.assertEqual(subscription.name, self.SUB_NAME)
        topic = subscription.topic
        self.assertTrue(isinstance(topic, Topic))
        self.assertTrue(topic is topics[self.TOPIC_PATH])
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.project, self.PROJECT)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_from_api_repr_w_topics_w_topic_match(self):
        resource = {'topic': self.TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        client = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client)
        topics = {self.TOPIC_PATH: topic}
        klass = self._getTargetClass()
        subscription = klass.from_api_repr(resource, client, topics=topics)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_create_pull_wo_ack_deadline_w_bound_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        BODY = {'topic': self.TOPIC_PATH}
        conn = _Connection({'name': self.SUB_PATH})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.create()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], BODY)

    def test_create_push_w_ack_deadline_w_alternate_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        BODY = {'topic': self.TOPIC_PATH,
                'ackDeadlineSeconds': self.DEADLINE,
                'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        conn1 = _Connection({'name': self.SUB_PATH})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({'name': self.SUB_PATH})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     self.DEADLINE, self.ENDPOINT)
        subscription.create(client=client2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], BODY)

    def test_exists_miss_w_bound_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        self.assertFalse(subscription.exists())
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req.get('query_params'), None)

    def test_exists_hit_w_alternate_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        conn1 = _Connection({'name': self.SUB_PATH, 'topic': self.TOPIC_PATH})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({'name': self.SUB_PATH, 'topic': self.TOPIC_PATH})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)
        self.assertTrue(subscription.exists(client=client2))
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req.get('query_params'), None)

    def test_reload_w_bound_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        conn = _Connection({'name': self.SUB_PATH,
                            'topic': self.TOPIC_PATH,
                            'ackDeadlineSeconds': self.DEADLINE,
                            'pushConfig': {'pushEndpoint': self.ENDPOINT}})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.reload()
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)

    def test_reload_w_alternate_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({'name': self.SUB_PATH,
                             'topic': self.TOPIC_PATH,
                             'ackDeadlineSeconds': self.DEADLINE,
                             'pushConfig': {'pushEndpoint': self.ENDPOINT}})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.reload(client=client2)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)

    def test_modify_push_config_w_endpoint_w_bound_client(self):
        PATH = '/%s:modifyPushConfig' % (self.SUB_PATH,)
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.modify_push_configuration(push_endpoint=self.ENDPOINT)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'],
                         {'pushConfig': {'pushEndpoint': self.ENDPOINT}})

    def test_modify_push_config_wo_endpoint_w_alternate_client(self):
        PATH = '/%s:modifyPushConfig' % (self.SUB_PATH,)
        conn1 = _Connection({})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     push_endpoint=self.ENDPOINT)
        subscription.modify_push_configuration(push_endpoint=None,
                                               client=client2)
        self.assertEqual(subscription.push_endpoint, None)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], {'pushConfig': {}})

    def test_pull_wo_return_immediately_max_messages_w_bound_client(self):
        import base64
        from gcloud.pubsub.message import Message
        PATH = '/%s:pull' % (self.SUB_PATH,)
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
        MESSAGE = {'messageId': MSG_ID, 'data': B64}
        REC_MESSAGE = {'ackId': ACK_ID, 'message': MESSAGE}
        conn = _Connection({'receivedMessages': [REC_MESSAGE]})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        pulled = subscription.pull()
        self.assertEqual(len(pulled), 1)
        ack_id, message = pulled[0]
        self.assertEqual(ack_id, ACK_ID)
        self.assertTrue(isinstance(message, Message))
        self.assertEqual(message.data, PAYLOAD)
        self.assertEqual(message.message_id, MSG_ID)
        self.assertEqual(message.attributes, {})
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'],
                         {'returnImmediately': False, 'maxMessages': 1})

    def test_pull_w_return_immediately_w_max_messages_w_alt_client(self):
        import base64
        from gcloud.pubsub.message import Message
        PATH = '/%s:pull' % (self.SUB_PATH,)
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
        MESSAGE = {'messageId': MSG_ID, 'data': B64, 'attributes': {'a': 'b'}}
        REC_MESSAGE = {'ackId': ACK_ID, 'message': MESSAGE}
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({'receivedMessages': [REC_MESSAGE]})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)
        pulled = subscription.pull(return_immediately=True, max_messages=3,
                                   client=client2)
        self.assertEqual(len(pulled), 1)
        ack_id, message = pulled[0]
        self.assertEqual(ack_id, ACK_ID)
        self.assertTrue(isinstance(message, Message))
        self.assertEqual(message.data, PAYLOAD)
        self.assertEqual(message.message_id, MSG_ID)
        self.assertEqual(message.attributes, {'a': 'b'})
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'],
                         {'returnImmediately': True, 'maxMessages': 3})

    def test_pull_wo_receivedMessages(self):
        PATH = '/%s:pull' % (self.SUB_PATH,)
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        pulled = subscription.pull(return_immediately=False)
        self.assertEqual(len(pulled), 0)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'],
                         {'returnImmediately': False, 'maxMessages': 1})

    def test_acknowledge_w_bound_client(self):
        PATH = '/%s:acknowledge' % (self.SUB_PATH,)
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.acknowledge([ACK_ID1, ACK_ID2])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], {'ackIds': [ACK_ID1, ACK_ID2]})

    def test_acknowledge_w_alternate_client(self):
        PATH = '/%s:acknowledge' % (self.SUB_PATH,)
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        conn1 = _Connection({})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.acknowledge([ACK_ID1, ACK_ID2], client=client2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], {'ackIds': [ACK_ID1, ACK_ID2]})

    def test_modify_ack_deadline_w_bound_client(self):
        PATH = '/%s:modifyAckDeadline' % (self.SUB_PATH,)
        ACK_ID = 'DEADBEEF'
        SENT = {'ackIds': [ACK_ID], 'ackDeadlineSeconds': self.DEADLINE}
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.modify_ack_deadline(ACK_ID, self.DEADLINE)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], SENT)

    def test_modify_ack_deadline_w_alternate_client(self):
        PATH = '/%s:modifyAckDeadline' % (self.SUB_PATH,)
        ACK_ID = 'DEADBEEF'
        SENT = {'ackIds': [ACK_ID], 'ackDeadlineSeconds': self.DEADLINE}
        conn1 = _Connection({})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.modify_ack_deadline(ACK_ID, self.DEADLINE, client=client2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], SENT)

    def test_delete_w_bound_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.delete()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], PATH)

    def test_delete_w_alternate_client(self):
        PATH = '/%s' % (self.SUB_PATH,)
        conn1 = _Connection({})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)
        subscription.delete(client=client2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], PATH)

    def test_get_iam_policy_w_bound_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        OWNER1 = 'user:phred@example.com'
        OWNER2 = 'group:cloud-logs@google.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        POLICY = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            ],
        }
        PATH = '/%s:getIamPolicy' % (self.SUB_PATH,)

        conn = _Connection(POLICY)
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        policy = subscription.get_iam_policy()

        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(sorted(policy.owners), [OWNER2, OWNER1])
        self.assertEqual(sorted(policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(policy.viewers), [VIEWER1, VIEWER2])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)

    def test_get_iam_policy_w_alternate_client(self):
        POLICY = {
            'etag': 'ACAB',
        }
        PATH = '/%s:getIamPolicy' % (self.SUB_PATH,)

        conn1 = _Connection()
        conn2 = _Connection(POLICY)
        client1 = _Client(project=self.PROJECT, connection=conn1)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        policy = subscription.get_iam_policy(client=client2)

        self.assertEqual(policy.etag, 'ACAB')
        self.assertEqual(policy.version, None)
        self.assertEqual(sorted(policy.owners), [])
        self.assertEqual(sorted(policy.editors), [])
        self.assertEqual(sorted(policy.viewers), [])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], PATH)

    def test_set_iam_policy_w_bound_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        from gcloud.pubsub.iam import Policy
        OWNER1 = 'group:cloud-logs@google.com'
        OWNER2 = 'user:phred@example.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        POLICY = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            ],
        }
        RESPONSE = POLICY.copy()
        RESPONSE['etag'] = 'ABACABAF'
        RESPONSE['version'] = 18
        PATH = '/%s:setIamPolicy' % (self.SUB_PATH,)

        conn = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        policy = Policy('DEADBEEF', 17)
        policy.owners.add(OWNER1)
        policy.owners.add(OWNER2)
        policy.editors.add(EDITOR1)
        policy.editors.add(EDITOR2)
        policy.viewers.add(VIEWER1)
        policy.viewers.add(VIEWER2)

        new_policy = subscription.set_iam_policy(policy)

        self.assertEqual(new_policy.etag, 'ABACABAF')
        self.assertEqual(new_policy.version, 18)
        self.assertEqual(sorted(new_policy.owners), [OWNER1, OWNER2])
        self.assertEqual(sorted(new_policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(new_policy.viewers), [VIEWER1, VIEWER2])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], {'policy': POLICY})

    def test_set_iam_policy_w_alternate_client(self):
        from gcloud.pubsub.iam import Policy
        RESPONSE = {'etag': 'ACAB'}
        PATH = '/%s:setIamPolicy' % (self.SUB_PATH,)

        conn1 = _Connection()
        conn2 = _Connection(RESPONSE)
        client1 = _Client(project=self.PROJECT, connection=conn1)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        policy = Policy()
        new_policy = subscription.set_iam_policy(policy, client=client2)

        self.assertEqual(new_policy.etag, 'ACAB')
        self.assertEqual(new_policy.version, None)
        self.assertEqual(sorted(new_policy.owners), [])
        self.assertEqual(sorted(new_policy.editors), [])
        self.assertEqual(sorted(new_policy.viewers), [])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], {'policy': {}})

    def test_check_iam_permissions_w_bound_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        PATH = '/%s:testIamPermissions' % (self.SUB_PATH,)
        REQUESTED = {
            'permissions': ROLES,
        }
        RESPONSE = {
            'permissions': ROLES[:-1],
        }
        conn = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=conn)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        allowed = subscription.check_iam_permissions(ROLES)

        self.assertEqual(allowed, ROLES[:-1])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], REQUESTED)

    def test_check_iam_permissions_w_alternate_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        PATH = '/%s:testIamPermissions' % (self.SUB_PATH,)
        REQUESTED = {
            'permissions': ROLES,
        }
        RESPONSE = {}
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESPONSE)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        allowed = subscription.check_iam_permissions(ROLES, client=client2)

        self.assertEqual(len(allowed), 0)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], PATH)
        self.assertEqual(req['data'], REQUESTED)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response


class _Topic(object):

    def __init__(self, name, client):
        self.name = name
        self._client = client
        self.project = client.project
        self.full_name = 'projects/%s/topics/%s' % (client.project, name)
        self.path = '/projects/%s/topics/%s' % (client.project, name)


class _Client(object):

    def __init__(self, project, connection=None):
        self.project = project
        self.connection = connection

    def topic(self, name, timestamp_messages=False):
        from gcloud.pubsub.topic import Topic
        return Topic(name, client=self, timestamp_messages=timestamp_messages)
