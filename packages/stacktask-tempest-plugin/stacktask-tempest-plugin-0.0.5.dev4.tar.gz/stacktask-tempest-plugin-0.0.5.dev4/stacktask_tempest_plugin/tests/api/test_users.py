from stacktask_tempest_plugin.tests import base
from tempest import test


class StacktaskProjectAdminTestUsers(base.BaseStacktaskTest):
    credential_roles = ['project_admin']

    @classmethod
    def resource_setup(cls):
        super(StacktaskProjectAdminTestUsers, cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        super(StacktaskProjectAdminTestUsers, cls).resource_cleanup()

    @test.idempotent_id('90fd103c-e071-11e5-893b-74d4358b0331')
    def test_get_users(self):
        users = self.stacktask_client.user_list()
        self.assertIsInstance(users, dict)
