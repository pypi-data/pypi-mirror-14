from tests import *
from global_identity.global_identity import GlobalIdentity


class TestExample(unittest.TestCase):

    def setUp(self):
        self.global_identity_server = 'https://private-anon-741e5c3d6-globalidentity.apiary-mock.com'

    def test_authentication_user(self):
        gi = GlobalIdentity(
            '00000000-0000-0000-0000-000000000000',
            self.global_identity_server)

        response = gi.authenticate_user(
            'account@email.com', 'account password')
        self.assertTrue(response['Success'])

    def test_validate_token(self):
        gi = GlobalIdentity(
            '6f3ef834-446f-48d7-9cfb-5a85a8a2576a',
            self.global_identity_server)

        response = gi.validate_token('token')
        self.assertTrue(response['Success'])

    def test_authenticate_application(self):
        gi = GlobalIdentity(
            '6f3ef834-446f-48d7-9cfb-5a85a8a2576a',
            self.global_identity_server)

        response = gi.validate_application(
            '2d8299ce-ae50-4c77-bf69-c436ed7650a7',
            'testsampleencoded',
            'sample string', encrypt=False)
        self.assertTrue(response['Success'])

        response = gi.validate_application(
            '2d8299ce-ae50-4c77-bf69-c436ed7650a7',
            '3409DC43229EC9A23F429772C85A0391FD6B15BAAC1FC86F75CED63A23686C69\
D0F2F79A2CCF9F20C46642B522E1B3FAC71F7807F685A0BA47E7F8FDFC3DA6D5',
            'sample string', encrypt=False)
        self.assertTrue(response['Success'])

    def test_is_user_in_role(self):
        gi = GlobalIdentity(
            '"6f3ef834-446f-48d7-9cfb-5a85a8a2576a',
            self.global_identity_server)
        response = gi.is_user_in_role(
            '078d59eb-ae2c-46c2-a995-b8b5c21fcde8', 'User')
        self.assertTrue(response['Success'])
