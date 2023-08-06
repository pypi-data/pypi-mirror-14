# r2 用到常量文件
# 2015.9.25 create by David.Yi
# 2015.9.28 增加  r2_command 列表
# 2016.3.21 修改 r2c1 版本号

r2_info = {'R2C1_LOG_CONFIG_FILE_NOT_EXISTS': 'r2c1 log config file not exists',
           'R2C1_CONFIG_FILE_NOT_EXISTS': 'r2c1 config file not exists',
           'ARGS_ILLEGAL': 'args {info_args} is illegal',
           'NEED_OPTION_NOT_IN_COMMAND': 'need options not in command',
           'COMMAND_NOT_EXISTS': 'command {info_cmd} doesnt exists',
           'COMMAND_OPTION_ERROR': 'command {info_cmd} option error',
           'COMMAND_OPTIONS_ERROR': 'command options error',
           'OPTION_KEY_VALUE_NOT_IN_LIST': 'option key {info_key} value {info_value} error, not in list',
           'OPTION_KEY_VALUE_EXPRESSION_ERROR': 'option key {info_key} value {info_value} error, expression error',
           'EXTRA_RULE_OK': 'extra rule ok',
           'EXTRA_RULE_ERROR': 'extra rule {info_erule} error',
           'OPTION_VALUE_EXPRESSION_INVALID_SYMBOL': 'option expression invalid symbol: {info_symbol}'}

r2_command = ['get', 'show', 'quit']

r2c1_version = '1.0.2'
r2c1_date = '2016-4-3'
r2c1_tag = ''
