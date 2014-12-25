from django_behave.runner import DjangoBehaveTestCase, DjangoBehaveTestSuiteRunner


class FirefoxTestCase(DjangoBehaveTestCase):
    def get_browser(self):
        return self.webdriver.Firefox()


class FirefoxeRunner(DjangoBehaveTestSuiteRunner):
    def make_bdd_test_suite(self, features_dir):
        return FirefoxTestCase(features_dir=features_dir)
