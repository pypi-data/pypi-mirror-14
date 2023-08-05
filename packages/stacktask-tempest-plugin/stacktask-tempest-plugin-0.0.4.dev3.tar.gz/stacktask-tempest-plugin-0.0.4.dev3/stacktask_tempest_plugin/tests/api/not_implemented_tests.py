
    @test.idempotent_id('3bebb5d2-e137-11e5-b4ac-74d4358b0331')
    @skip()
    def test_update_roles_add(self):
        # TODO: setup - create keystone user with _member_ role only
        ks_user = {
            'id': 2,
            'project_id': 1
        }
        u_roles = ['_member_']
        self.assert_user_roles(ks_user['project_id'], ks_user['id'], u_roles)

        # grant them the project_mod role via stacktask
        u_roles.append('project_mod')
        self.stacktask_client.user_roles_add(
            ks_user['id'],
            ["project_mod"]
        )

        # check roles for this user
        self.assert_user_roles(ks_user['project_id'], ks_user['id'], u_roles)

    @test.idempotent_id('48fa7f74-e137-11e5-acd2-74d4358b0331')
    @skip('NYI')
    def test_update_roles_remove(self):
        pass

    @test.idempotent_id('6ece7a5c-e137-11e5-8c90-74d4358b0331')
    def test_user_revoke(self):
        pass

    @test.idempotent_id('6ef956c8-e137-11e5-8151-74d4358b0331')
    def test_user_password_reset(self):
        pass

    @test.idempotent_id('6f1cc7fc-e137-11e5-bfd4-74d4358b0331')
    def test_user_cancel_invite(self):
        pass
