from vmupdate.cli import main, _parse_args, _unhandled_exception_handler

from tests.case import TestCase
from tests.context import mock


class CliTestCase(TestCase):
    @mock.patch('vmupdate.cli.update_all_vms', autospec=True)
    @mock.patch('vmupdate.cli._parse_args', autospec=True)
    def test_main(self, mock_parse_args, mock_update_all_vms):
        mock_parse_args.return_value = _parse_args([])

        mock_update_all_vms.return_value = 0

        main()

        mock_update_all_vms.assert_called_once_with()

    def test_unhandled_exception_handler(self):
        _unhandled_exception_handler(None, Exception(), None)
