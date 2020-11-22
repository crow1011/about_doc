import unittest
import requests
import yaml
import sys


class ColorPrint:

    @staticmethod
    def print_fail(message, end='\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end='\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end='\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end='\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end='\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)


class ConfTest(unittest.TestCase, ColorPrint):
    def setUp(self):
        with open('conf/conf.yaml') as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

    def test_conf(self):
        print('\n')
        self.print_bold('---------------------------')
        self.print_bold('Case: check conf fields')
        self.print_bold('---------------------------')

    def test_query_interval(self):
        self.print_info('Checking query_interval type is int, is not empty and is bigger than 59')
        self.assertEqual(type(self.conf['query_interval']), int)
        self.assertEqual(self.conf['query_interval'] > 59, True)
        self.print_pass('Done')

    def test_users_url(self):
        self.print_info('Checking users_url type is string and is not empty')
        self.assertEqual(type(self.conf['users_url']), str)
        self.assertEqual(len(self.conf['users_url']) > 0, True)
        self.print_pass('Done')
        self.print_info('Checking user_url return status.code 200')
        status_code = requests.get(self.conf['users_url']).status_code
        self.assertEqual(200, status_code)
        self.print_pass('Done')

    def test_todos_url(self):
        self.print_info('Checking todos_url type is string and is not empty')
        self.assertEqual(type(self.conf['todos_url']), str)
        self.assertEqual(len(self.conf['todos_url']) > 0, True)
        self.print_pass('Done')
        self.print_info('Checking todos_url return status.code 200')
        status_code = requests.get(self.conf['todos_url']).status_code
        self.assertEqual(200, status_code)
        self.print_pass('Done')

    def test_title_max_len(self):
        self.print_info('Checking title_max_len type is int, is not empty and is bigger than 0')
        self.assertEqual(type(self.conf['title_max_len']), int)
        self.assertEqual(self.conf['title_max_len'] > 0, True)
        self.print_pass('Done')

    def test_file_dir(self):
        self.print_info('Checking file_dir type is string and is not empty')
        self.assertEqual(type(self.conf['file_dir']), str)
        self.assertEqual(len(self.conf['file_dir']) > 0, True)
        self.print_pass('Done')

    def test_conf_logger(self):
        self.print_info('Checking logger->log_level type is string and is not empty ""')
        self.assertEqual(type(self.conf['logger']['log_level']), str)
        self.assertNotEqual(len(self.conf['logger']['log_level']), 0)
        self.print_pass('Done')

        self.print_info('Checking logger->log_file type is string and is not empty ""')
        self.assertEqual(type(self.conf['logger']['log_file']), str)
        self.assertNotEqual(len(self.conf['logger']['log_file']), 0)
        self.print_pass('Done')

        self.print_info('Checking logger->log_dir type is string and is not empty ""')
        self.assertEqual(type(self.conf['logger']['log_dir']), str)
        self.assertNotEqual(len(self.conf['logger']['log_dir']), 0)
        self.print_pass('Done')
