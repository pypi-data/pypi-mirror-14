from mock import patch

from .util import V1TestCase


class TestTokenCommand(V1TestCase):
    get_workitem = patch('helga_versionone.get_workitem')
    get_user = patch('helga_versionone.get_user')

    def test_step1(self):
        auth_info = {}
        self.db.v1_oauth.find_one.return_value = auth_info

        return self._test_command(
            'token',
            'In V1 go to your Applications and generate a Personal Access Token'
            'then do "!v1 token <code>" with the generated code',
            to_nick=True
        )
    def test_no_token(self):
        auth_info = {}
        self.db.v1_oauth.find_one.return_value = auth_info

        return self._test_command(
            'token forget',
            'Token was already gone',
            to_nick=True
        )

    def test_forget_works(self):
        auth_info = {'api_token': 'delete me'}
        self.db.v1_oauth.find_one.return_value = auth_info

        d = self._test_command(
            'token forget',
            to_nick=True
        )

        def check(res):
            self.assertEqual(auth_info, {})
            self.assertAck()

        d.addCallback(check)
        return d

    def test_set_token(self):
        # If the return were False, a new dict gets created
        auth_info = {'notfalse': True}
        self.db.v1_oauth.find_one.return_value = auth_info

        d = self._test_command(
            'token newvalue',
            to_nick=True
        )

        def check(res):
            self.assertEqual(auth_info, {'api_token': 'newvalue', 'notfalse': True})
            self.assertAck()

        d.addCallback(check)
        return d
