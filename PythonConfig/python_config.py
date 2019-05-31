# coding=utf-8
import collections
import configparser
import os.path
HOME_DIR = os.path.dirname(__file__)
"""
[mysql]    --> node 
host = 'localhost'  --> attr = value
port = 8080
ehco = True
"""

class BaseConfigParser(configparser.ConfigParser):
    """
    configParse for user
    """

    def __init__(self):
        """
        use no order dict to storge ini file
        """
        configparser.ConfigParser.__init__(self, dict_type=collections.OrderedDict)

    def __str__(self):
        """
        stdout
        """
        return json.dumps(self._sections, indent=2)

    def __eq__(self, other):
        """
        compare two sections
        """
        return self._sections == other._sections

    def optionxform(self, optionstr):
        """
        rewrite optionxform
        """
        return optionstr

    def read(self, filenames, encoding=None):
        if os.path.exists(filenames):
            if encoding is None:
                encoding = 'UTF-8'
            super().read(filenames=filenames, encoding=encoding)
        else:
            print('The file:{} is not exist.'.format(filenames))

    def set(self, section, option, value=None):
        if value is None:
            print('The value is not allowed None')
        else:
            super().set(section=section, option=option, value=value)


def parse_config(node, attr, path=None):
    """
    :param node: node to read
    :param attr: attribute in node
    :param path: file path
    :return: attribute value
    """
    conf = BaseConfigParser()
    if path:
        conf_path = path
    else:
        conf_path = os.path.join(HOME_DIR, 'config.ini')
    conf.read(conf_path)
    try:
        str_val = conf.get(node, attr)
    except Exception as e:
        print(e)
        str_val = None
    return str_val

if __name__ == "__main__":
    # print(os.path.abspath(__file__)) #绝对路径
    # print(os.path.dirname(__file__)) #文件所在目录
    # print("cur path:",HOME_DIR)
    config = parse_config('mysql','port')
    print(config)