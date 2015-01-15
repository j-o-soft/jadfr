from apps.userfeeds.managers import CallbackManager
from django.db.models import Model
from django.test import TestCase
from mock import Mock, patch


class TestCallbackManager(TestCase):

    def setUp(self):

        class M(Model):
            objects = CallbackManager()
        self.M = M

    def test_callback_manager(self):
        """
        Tests that the manager retuns the expected value and the callback function is called for each item

        todo: for unknown reasons this test fails if it's split into different methods
        """

        # test get if callback is passed to the manager
        callback = Mock()
        return_val = 'return'
        with patch('apps.userfeeds.managers.QuerySet.get', return_value=return_val) as base_path:
            assert return_val == self.M.objects(callback).all().get()
        callback.assert_called_once_with(return_val)
        callback.reset_mock()
        # test the iterator if callback is passed to the manager
        return_val = ['rval1', 'rval2']
        with patch('apps.userfeeds.managers.QuerySet.iterator', return_value=return_val) as base_path:
            qs = self.M.objects(callback).all()
            for item in qs:
                pass
        assert map(lambda x, y: x, callback.call_args_list, return_val)
        assert return_val == list(qs)
        # test the iterator if callback is passed to the queryset
        callback.reset_mock()
        return_val = ['rval1', 'rval2']
        with patch('apps.userfeeds.managers.QuerySet.iterator', return_value=return_val) as base_path:
            qs = self.M.objects.all()(callback).all()
            for item in qs:
                pass
        assert map(lambda x, y: x, callback.call_args_list, return_val)
        assert return_val == list(qs)
        # test get if callback is passed to the queryset
        callback.reset_mock()
        callback = Mock()
        return_val = 'return'
        with patch('apps.userfeeds.managers.QuerySet.get', return_value=return_val) as base_path:
            assert return_val == self.M.objects.all()(callback).get()
        callback.assert_called_once_with(return_val)
