# r2c1 核心逻辑功能库
# 2015.6.16 create by David.Yi
#   增加 def do_show, 提供show 命令的解析，
#   解析使用配置文件r2c1.conf 动态生成r2c1对象
# 2015.6.20 edit log属性相关移到r2对象中, r2自己开始采用r2_log独立log文件
# 2015.7.30 独立 解析命令行的参数 函数 def phrase_opts()
# 2015.9.2 格式整理
# 2015.9.6 r2_main.py --> r2c1_main.py
# 2015.9.13 extra rules 命令参数的扩展规则解析
# 2015.9.25 开始引入 r2_const.py 常量统一
# 2015.10.17 引入 tokenize.py 加入参数是否符合数字表达式判断
# 2015.11.22 12.1 #12046 #12047 #12048 #12049 优化增强 check_value()，支持money类数值参数
# 2015.12.18 #12085 将整个文件修改为类模式，供其他调用
# 2015.12.19 #12088 R2中的方法除了phrase_cmd() 都修改为保护方法
# 2015.12.19 #12089 使用公共函数fpytools 中的 FpyCache class方式进行cf 读取缓存
# 2015.12.27 edit by david.yi #12091 替换字符串+ 为 join 方法
# 2016.2.27 edit 修改 import 方式, v1.0.2 #12100
# 2016.3.4 edit #12102 所有opt相关变量增加opt 标示
# 2016.3.31 edit #12098 lib fish_base 修改为标准 python 包 import 方式
# 2016.4.1 move the project to github
# 2016.4.3 edit python package fish_base usage, FpyCache to FishCache, get_cache to get_cf_cachet
# 2016.4.3 ready for upload to Pypi


import configparser  # 配置文件读写
import getopt  # 命令行参数处理
import json
import logging
import logging.config
import os
import re

import fish_base
from fish_base import FishCache
from .r2c1_const import *  # r2c1 私有常量

from r2c1 import r2_tokenize


# r2 对象，保存一条r2命令需要的相关的信息
# 2015.7.25 add rf
# 2015.7.26 add pattern
# 2015.12.9 add token 相关
# 2015.12.17 #12085 class化
class R2(object):
    # edit 2015.9.5.
    # r2c1 对象，和r2命令的参数对应的对象，和json对象对应
    class R2C1(object):
        pass

    r2c1_class = R2C1()  # r2c1 class

    r2_cache = FishCache()  # 申明conf 文件使用的cache

    # 定义类内部变量

    json_path = ''
    conf_path = ''

    r2c1_conf_long_filename = ''

    setattr_list = []

    cf_args = ''
    cf_short_opt = ''
    cf_long_opt = []

    cf = configparser.ConfigParser()  # 配置文件
    cf_opt_section = []  # 配置文件section列表

    r2c1_info_list = []  # 记录处理过程中的信息列表

    pattern = False
    pattern_name = ''

    cmd0 = ''  # 用户输入的命令，eg. get
    cmd1 = ''  # 用户输入的命令后面的参数

    args0_list = ''  # 用户输入的参数列表
    opt0_list = []  # 用户输入的选项列表

    opt = ''  # 选项的key,eg. business
    opt0 = ''  # 选项的key原来值，eg. -b
    cur_opt_value = ''

    token_mark = False

    glist_count = 0  # group 处理用
    glist = []

    support_cmd = []  # 支持命令

    # r2_cache = {}  # 定义缓存

    # 版本和日期修改为从 consts 文件中读取
    def __init__(self):

        self.ver = r2c1_version
        self.date = r2c1_date
        self.tag = r2c1_tag

    # my_init()
    # r2 初始化,定义所有属性
    # 2015.7.7 7.11 7.25 edit by david.yi
    # 2015.7.27 增加json path, conf path
    # 2015.8.30 调整 log 文件的路径统一到 conf 目录  edit by david.yi
    # 2015.9.25 删除 init_r2c1_str()  函数，常量统一引用 r2_const.py
    # 2015.12.15 #12082 conf文件使用参数方式调入
    # 2015.12.17 #12085 class化
    # 2016.2.28 #13001 获得路径方法修改
    @staticmethod
    def my_init(conf_name):

        logging.info('new import r2_main.py ok')

        # 2016.2.28
        cur_dir = os.path.split(os.path.realpath(__file__))[0]

        # json 文件存放路径
        R2.json_path = os.path.join(cur_dir, 'json')

        # conf 文件存放路径
        R2.conf_path = os.path.join(cur_dir, 'conf')

        # 拼接获得完整r2c1 conf 文件名，包含路径
        # #12082 conf文件使用参数传入
        R2.r2c1_conf_long_filename = os.path.join(R2.conf_path, conf_name)
        # #12083 conf文件如果不存在，返回错误信息
        if not os.path.isfile(R2.r2c1_conf_long_filename):
            s = (r2_info['R2C1_CONFIG_FILE_NOT_EXISTS'])
            R2.r2c1_info_list.append(s)
            return False, R2.r2c1_info_list, None

        # log 记录 r2_main开始
        logging.info('import r2_main.py ok')

        logging.info(' '.join(['json path:', 'R2.json_path', 'conf path:', 'R2.conf_path']))

        # 检查value标志是否合法属性，初始化为False
        R2.check_value_mark = False

        # cf: 准备读取r2c1配置文件，其中包括 -b=business 这样的转换预定义
        # 读入配置文件
        R2.cf.read(R2.r2c1_conf_long_filename)

        # #12073 从配置文件中 读取 group 内容
        # 有多少group rule 记录到glist_count
        R2.glist_count = int(R2.cf['re_group']['group_rule_count'])

        # 根据group rule数量循环判断
        for i in range(R2.glist_count):
            # 从 conf 文件中读取真实的规则
            R2.glist.append(R2.cf['re_group'][''.join(['re_', str(i)])])

        # #12084 读入r2c1 支持的命令
        R2.support_cmd = R2.cf['r2c1_cmd']['support_cmd'].split(',')

        return True

    # phrase_cmd()
    # 执行r2命令的c1过程，解析传入的命令参数，返回结果，json解析结果或者错误信息
    # 输入: cmd0: 命令 cmd1: 选项参数值，
    # 输出:  返回值1：参数检验是否正确，true/false
    #       返回值2：如果为true，返回参数解析的json串；如果为false，返回相信错误信息
    #
    # 2015.6.16 create and edit by david.yi
    # 2015.7.4 7.6 优化
    # 2015.7.10 7.11 7.13 7.15 参数匹配规则
    # 2015.7.28 show --> phrase  命令标准化，准备增加更多命令
    # 2015.7.30 修改细节，加入错误判断，增加判断必须输入选项
    # 2015.9.4 修改返回参数，修改为返回成功标志、结果和错误信息三个参数
    # 2015.9.14 增加判断扩展规则功能，调用 check_extra_rule()
    # 2015.9.20 写对象属性时候，考虑日期范围类型，比如2014-2015
    # 2015.12.6 代码优化，常用变量写入到对象，便于全局调用
    # 2015.12.8 #12070 如果标准检查已经有错误，则扩展规则检查不需要，优化性能
    # 2015.12.13 #12080 增加判断cmd不在预设命令的判断
    # 2016.2.13 #12092 日志记录cmd0和cmd1参数，修正原来日志错误
    # 2016.3.5 v1.0.2 开始处理 args 设计 #12103 #12104 #12105
    def phrase_cmd(self, cmd0, cmd1):

        # 设置记录检查value错误列表为空
        R2.r2c1_info_list = []

        # 用户输入的命令和后面的参数值等
        R2.cmd0 = cmd0
        R2.cmd1 = cmd1
        logging.info(' '.join(['cmd0: ', R2.cmd0, 'cmd1: ', R2.cmd1]))

        # #12080 检查命令是否在支持命令中
        if not (self._check_cmd(R2.cmd0)):
            # 不支持的命令，返回错误
            s = (r2_info['COMMAND_NOT_EXISTS']).format(info_cmd=R2.cmd0)
            R2.r2c1_info_list.append(s)
            return False, R2.r2c1_info_list, None

        # >>> 处理 conf args 开始
        # 生成解析命令参数需要的conf 文件中的 section 名称 #12103
        temp_args = ''.join([R2.cmd0, '_args'])

        # 从 conf 获得参数 args 的设置
        temp_s = self.r2_cache.get_cf_cache(R2.cf, temp_args, 'args')
        R2.cf_args = temp_s.split(',')
        logging.info(''.join(['cf args: ', temp_s]))

        # <<< 处理 conf args 结束

        # >>> 处理 conf opt 开始
        # 生成解析命令需要的conf文件中的section 名称
        temp_opt = ''.join([R2.cmd0, '_opt'])
        temp_opt_common = ''.join([R2.cmd0, '_opt_common'])
        temp_opt_common2 = ''.join([R2.cmd0, '_opt_common2'])

        # 从 conf 获得短选项，长选项的设置
        R2.cf_short_opt = self.r2_cache.get_cf_cache(R2.cf, temp_opt, 'short_opt')
        # 长参数转换为list
        R2.cf_long_opt = self.r2_cache.get_cf_cache(R2.cf, temp_opt, 'long_opt').split(',')
        logging.info(''.join(['cf_short_opt:', R2.cf_short_opt]))
        logging.info(''.join(['cf_long_opt:', self.r2_cache.get_cf_cache(R2.cf, temp_opt, 'long_opt')]))

        # <<< 处理 conf opt 结束

        # 解析命令行的参数，获得短选项、长选项、开关参数等，调用内部 _phrase_option() 静态方法
        # 解析后的结果会放在 R2.opt0_list 和 R2.args0_list
        if not (self._phrase_option()):
            return False, R2.r2c1_info_list, None

        # >>> 处理 r2 args 开始 #12104

        # 按照用户输入的args 来循环
        args_in_conf = True
        # print(R2.args0_list)
        # print(R2.cf_args)
        for temp_a0 in R2.args0_list:
            # print(temp_a0)
            # 检查是否在 conf 规定的 args 中
            if not(temp_a0 in R2.cf_args):
                args_in_conf = False

        # print(args_in_conf)

        # 有不存在的 args , 返回错误
        if not args_in_conf:
            # 拼接提示错误信息
            R2.r2c1_info_list.append(r2_info['ARGS_ILLEGAL'].format(info_args=''.join(R2.args0_list)))
            return False, R2.r2c1_info_list, None

        # <<< 处理 r2 args 结束

        # 将 opt list转换为 dict类型，便于检索
        R2.opt_dict = dict(R2.opt0_list)

        # 读入配置文件中 common section设置，其中包含所有选项对应，比如 -b=business
        R2.cf_opt_section = R2.cf.options(temp_opt_common)

        # 检查必须输入的选项是否都输入
        need_opt = self.r2_cache.get_cf_cache(R2.cf, temp_opt_common2, 'need')
        need_opt_list = need_opt.split(',')

        need_opt_in_mark = False

        for key in R2.opt_dict:
            if key in need_opt_list:
                need_opt_in_mark = True

        # 如果有需要输入的参数没有输入，返回false，记录错误信息
        if not need_opt_in_mark:
            R2.r2c1_info_list.append(r2_info['OPTION_KEY_VALUE_EXPRESSION_ERROR'])
            return False, R2.r2c1_info_list, None

        # 如果 设置过r2c1 class属性，则需要先清空这些属性
        # r2c1 class实例中的属性是根据用户参数自动设置便于转换为json，所以要判断
        if len(R2.setattr_list) > 0:
            for i in range(len(R2.setattr_list)):
                delattr(self.r2c1_class, R2.setattr_list[i])
            # date 属性是硬加入的，也需要删除
            if hasattr(self.r2c1_class, 'date'):
                delattr(self.r2c1_class, 'date')

        # 设置属性列表为空
        R2.setattr_list = []

        # 写入r2c1 版本、命令等，供后续解析使用
        self.r2c1_class._version = self.ver
        self.r2c1_class._command = R2.cmd0
        self.r2c1_class._tag = self.tag

        # 生成需要检查key的列表,check_opt_list
        check_opt = self.r2_cache.get_cf_cache(R2.cf, temp_opt_common2, 'check')
        check_opt_list = check_opt.split(',')

        # 日志记录
        # r2.log.info('check key list: ' + check_opt)

        # args 内容写入 r2c1 class #12105
        for item in R2.args0_list:
            setattr(self.r2c1_class, item, True)
            R2.setattr_list.append(item)

        # 根据配置文件中的设定，匹配opt_dict中的key-value值，并动态设置为r2c1的属性名称和值
        # eg. [get_common]  -b=business  -f=fields
        for item in R2.cf_opt_section:
            # 如果用户输入的参数key中存在规则中的key
            if item in R2.opt_dict.keys():
                # 日志记录
                # r2.log.info('input key: ' + item)
                # 读取key, value,  r2.cf_opt_section[i] 表示参数，比如 -b
                # r2.key = r2.cf.get(temp_opt_common, item)
                R2.opt = self.r2_cache.get_cf_cache(R2.cf, temp_opt_common, item)

                # value_str 记录value，以字符串形式
                value_str = R2.opt_dict[item]
                # value 记录为列表形式
                value = value_str.split(',')

                # r2.log.info('key: ' + r2.key)
                # r2.log.info('value: ' + value_str)

                R2.opt0 = item

                # 参数在需要检查的列表范围内，则进行参数检查
                if R2.opt0 in check_opt_list:

                    # 检查输入的参数值是否正确
                    for j in range(len(value)):
                        R2.cur_opt_value = value[j]

                        # 检查命令参数，调用 check_value()
                        self._check_value()

                # 将正确的 r2 命令写入 r2c1 class, 这样可以转换为 json 格式
                # 动态设置r2c1 class 实例的属性和值
                setattr(self.r2c1_class, R2.opt, value)
                R2.setattr_list.append(R2.opt)

        # 根据记录 check value的错误列表内容，来判断是否所有参数检查通过，设置标志
        if len(R2.r2c1_info_list) == 0:
            R2.check_value_mark = True
        else:
            R2.check_value_mark = False

        # #12070 对于扩展规则性能优化
        # 检查参数错误
        if not R2.check_value_mark:

            logging.error('command check value error')
            return False, R2.r2c1_info_list, None

        # 检查参数标志为True，通过所有语法检查
        else:

            # 判断是否存在当前命令的扩展规则，类似 [get_extra_rules]
            if R2.cf.has_section(''.join([R2.cmd0, '_extra_rules'])):

                # 日志记录
                logging.info(''.join(['found extra rules:', R2.cmd0]))

                # 如果检查扩展规则返回为 False，说明没有通过检查，调用 check_extra_rule()
                if not (self._check_extra_rule()):
                    # r2c1 直接返回 False 等错误信息
                    return False, R2.r2c1_info_list, None

            # 生成 r2c1 的json string，回写到 r2 对象的json_str属性
            R2.json_str = json.dumps(fish_base.serialize_instance(self.r2c1_class),
                                     sort_keys=True, indent=4)

            logging.info(''.join(['r2c1 json: ', R2.json_str]))

            return True, R2.r2c1_info_list, R2.json_str

            # 测试将R2C1生成的json读入到python
            # j1 = json.loads(r2.json_str)
            # print('json to dict:', j1)
            # print("time", j1["time"])

    # phrase_option()
    # 解析命令行的参数
    # 2015.7.30 create
    @staticmethod
    def _phrase_option():
        try:
            # 解析命令行参数， opt0_list 为各类选项  a参数
            R2.opt0_list, R2.args0_list = getopt.getopt(R2.cmd1.split(), R2.cf_short_opt, R2.cf_long_opt)
            # 打日志，r2 命令选项和参数解析内容
            logging.info(' '.join(['opt list: ', str(R2.opt0_list)]))
            logging.info(' '.join(['args list: ', str(R2.args0_list)]))
            return True

        # 错误处理
        except getopt.GetoptError:

            # 记录错误信息
            s = r2_info['COMMAND_OPTIONS_ERROR']
            R2.r2c1_info_list.append(s)
            # 记录到日志
            logging.warning(s)

            return False

    # check_value() 检查r2c1中输入的命令行参数是否合法
    # 输入：无
    # eg. command='get' key='business' key0='-b' value='sky'
    # 输出：True or False
    # create 2015.7.5 7.11  by david.yi
    # 2015.7.13 测试正则表达式的检测 by david.yi
    # 2015.7.25 日期正则表达式抽象到 r2c1_rule.conf，减少重复设置
    # 2015.7.28 7.30 准备支持多命令，优化
    # 2015.9.3 进行多命令支持同样功能参数设计修改
    # 2015.9.5 去除r2c1_rule.conf调用，日期正则也写到 r2c1.conf 中
    # 2015.9.8 修改完善正则代理功能 #11106
    # 2015.9.20 修改正则规则解析，支持类似 yyyy-yyyy 这样情况 #12006
    # 2015.9.26 修改代码中的逻辑错误
    # 2015.10.17 增加判断value为数字表达式的情况
    # 2015.11.27 #12046 修改正则判断的各类扩展情况
    def _check_value(self):
        # 拼接配置文件中保存参数规则的section项名称
        # eg. 'get_rule_business'
        command_rule_key = ''.join([R2.cmd0, '_rule_', R2.opt])

        # 检查是否存在直接拼接的section名称
        if R2.cf.has_section(command_rule_key):

            # 存在直接命令参数规则的section, 设置到标准rule_key，作为后续操作
            rule_key = command_rule_key
        else:

            # 不存在直接命令rule key的section，则拼接 base rule key作为参考的section
            rule_key = ''.join(['base', '_rule_', R2.opt])

        # 日志记录，rule_key， 可以知道从command rule读取还是 base rule 读取
        # r2.log.info('config find section: ' + rule_key)

        # 读入配置文件中相应section的rule规则，section 的名称如 rule_business
        rule_type = self.r2_cache.get_cf_cache(R2.cf, rule_key, 'rule_type')

        # 如果规则是 list
        if rule_type == 'list':
            # 读取临时 list 内容
            l = self.r2_cache.get_cf_cache(R2.cf, rule_key, 'list')
            # 如果输入的 value 在 list 中
            if R2.cur_opt_value in l:
                return True
            else:
                # 记录错误信息
                s = (r2_info['OPTION_KEY_VALUE_NOT_IN_LIST']).format(info_key=R2.opt0, info_value=R2.cur_opt_value)
                R2.r2c1_info_list.append(s)
                logging.error(s)
                return False

        # 如果规则是 表达式  money expression
        # 如果规则是日期正则re，进行处理
        # 2015.10.17 11.28 12.6
        if rule_type == 'expression' or rule_type == 're_datetime':

            # 设置正则类检查的参数字典
            arg_dict_re = {'rule_type': rule_type, 'rule_key': rule_key}

            # print(arg_dict)

            # 表达式和正则检查，调用 check_value_re()
            if self._check_value_re(**arg_dict_re):
                return True
            else:
                return False

    # check_value_re()
    # 对于正则类规则进行检查，配合 check_value()
    # 2015.11.22 create by david.yi 移植自 check_value() 中原来相关代码
    # 2015.11.27 #12046 正则规则判断扩展
    # 2015.12.6 #12061 支持 expression 的更多判断
    def _check_value_re(self, **arg_dict_re):
        rule_key = arg_dict_re['rule_key']
        rule_type = arg_dict_re['rule_type']

        # print(arg_dict)

        value_separate = ''

        if rule_type == 're_datetime':
            value_separate = '-|\||'
        elif rule_type == 'expression':
            value_separate = '\||'

        # 读取配置文件是否使用正则代理标志，记录到 re_agent
        re_agent = R2.cf.getboolean(rule_key, 're_agent')

        # print(rule_key, re_agent)
        logging.info(' '.join(['re rule and agent:', rule_key, ',', str(re_agent)]))

        # 读取正则规则数量，记录到 rule_count
        rule_count = int(self.r2_cache.get_cf_cache(R2.cf, rule_key, 'rule_count'))

        # 分解 value 到 list 类型，记录到 value_list
        # 对应 2014-2015 这样时间范围，以及 2014|2016 这样
        value_list = re.split(value_separate, R2.cur_opt_value)

        # print('value_list:', value_list)

        # 建立判断扩展规则结果的初始值，之后通过正确次数和要判断的value个数比较
        value_check_count = 0

        # 根据value list进行循环，逐个value进行正则校验
        for value_temp in value_list:

            # print('value:' + value_temp)

            # 循环读取参数规则，准备逐一尝试匹配
            for i in range(rule_count):

                # 读取参数规则, 记录到 value_rule_temp
                # eg. yyyyhx, number
                value_rule_temp = self.r2_cache.get_cf_cache(R2.cf, rule_key, ''.join(['re_', str(i)]))

                # print(value_rule_temp)

                # 如果是使用正则规则代理的话，需要另外读取真正对应的正则内容
                # 也就是把 yyyyhx 这样的表达式翻译成整正的f正则表达式
                if re_agent:
                    # 读取真正的正则表达式, 记录到 rule_real
                    rule_real = self.r2_cache.get_cf_cache(R2.cf, rule_type, value_rule_temp)
                    # print('re_agent true do this ', rule_type)

                # 如果是 money 参数，则不需要翻译正则，需要自己实现
                else:
                    rule_real = value_rule_temp
                    # print('re_agent false do this ', rule_type)

                # 记录日志，记录 value 和 rule
                # s = 're rule: {re_rule} , value: {check_value} '.format(re_rule=rule_real, check_value=value_temp)
                # r2.log.info(s)

                # rule_result_temp = False

                # 检查value是否符合正则, 调用 check_rule()
                rule_result_temp = self._check_rule(rule_type, rule_real, value_temp)

                # 参数符合正则
                if rule_result_temp:
                    # value 检查计数器 +1
                    value_check_count += 1

                    # print('re rule match')
                    break

        # 记录正确的正则匹配数量=元素个数，说明每个分解的value都检查正确，返回True，
        if value_check_count == len(value_list):
            return True

        # 有参数不匹配规则处理
        else:
            # 记录错误信息
            # print('key and value error:', key0, value)
            s = (r2_info['OPTION_KEY_VALUE_EXPRESSION_ERROR']).format(info_key=R2.opt0, info_value=R2.cur_opt_value)
            # print(s)
            R2.r2c1_info_list.append(s)
            logging.info(s)
            return False

    # check_rule()
    # 真正检查参数中的输入value是否符合正则或者表达式等
    # 输入参数： rule_type: 规则类型，rule_real: 真实需要匹配的规则，value: 需要检查的值， key: 参数
    # 返回参数： 符合规则的话，返回 True
    # 2015.11.22 create by david.yi
    # 2015.11.28 edit #12047 修改返回值，不管正则或者以后，统一返回True or False
    # 2015.11.29 edit #12047 针对money value 加入最基本token判断
    # 2015.11.30 edit #12048 针对money value 多个情况进行规则判断
    # 2015.12.1 12.5 edit 加入更多token 规则
    # 2015.12.6 #13003 （n1,n2） n1<n2 判断 exp rule 10
    # 2015.12.6 #12061 expression 的更好支持
    # 2015.12.9 #12071 #13006 expression 判断代码重构，逻辑合理，单元测试通过
    # 2015.12.11 #12073 优化group list 读取文件方式
    @staticmethod
    def _check_rule(rule_type, rule_real, value):
        # print(rule_type, rule_real, value)

        if rule_type == 're_datetime':

            # 调用正则进行判断
            result_temp = re.match(rule_real, value)
            if result_temp is not None:
                return True
            else:
                return False

        elif rule_type == 'expression':

            # print('value:', value)
            # print('rule_real:', rule_real)
            # print(r2.cur_opt_value)

            # 检查是否符合基本表达式校验，通过函数 r2_tokenize.get_token
            token_mark, token_list, token_info = r2_tokenize.get_token(value)

            # 判断是否含有非法字符
            if not token_mark:
                return False

            # 如果是 group 参数 特殊处理
            # 2015.12.6　12.7
            # 2015.12.9 #13006 支持group中单词分组  eg. sh|js
            if R2.opt == 'group':

                # #13005 对于 ELSE 进行特判，是否在最右边
                if value == 'ELSE':
                    if not (R2.cur_opt_value[-4:] == 'ELSE'):
                        return False

                # 符合规则的计数器
                ok_count = 0

                # 根据group rule数量循环判断
                for i in range(R2.glist_count):

                    # 判断是否在token list中包含 group list中的内容
                    if r2_tokenize.exp_rule_11(token_list, (R2.glist[i]).split(',')):
                        ok_count += 1

                # print('ok_count ', ok_count, 'token ', token_list)

                if ok_count >= 1:
                    return True
                else:
                    return False

            token_count = len(token_list)

            # token list 长度 2
            if token_count == 2:
                # token是否一个数字或者单词合法性
                if not r2_tokenize.exp_rule_09(token_list):
                    return False
            elif token_count == 3 or token_count == 4 or token_count == 5:
                return False
            # token list 长度 6 （a-b） 样式
            elif token_count == 6:
                # 检查括号匹配
                if not r2_tokenize.exp_rule_07(token_list):
                    return False
                # 检查 NINF 和  PINF 位置和拼写
                if not r2_tokenize.exp_rule_08(token_list):
                    return False
                # #13003
                # 检查 （n1,n2) n1< n2
                if not r2_tokenize.exp_rule_10(token_list):
                    return False
            # token list 长度大于 6
            else:

                # 检查是否有字母数字混合，如 (1-1s)
                if not r2_tokenize.exp_rule_04(token_list):
                    return False

                # 检查是否有- 大于 1个情况
                if r2_tokenize.exp_rule_06(token_list):
                    return False

            return True

    # check_extra_rule()
    # 检查命令扩展规则 by david.yi
    # 2015.9.13 create
    # 2015.9.15 edit #12003, #12004 增加opt_rule_2，目前支持判断两条规则，
    # 2015.9.24 代码优化
    # 2015.10.29 #12053 修改 result 逻辑
    # 2015.12.6 代码格式优化
    # 2015.12.7 #12063 增加规则4，将两个属性zip成一个属性
    # 2015.12.12 #12076 conf文件读采用缓冲方式
    def _check_extra_rule(self):
        # 建立判断扩展规则结果的初始值，表示没有错误
        err_count = 0

        erule_section = ''.join([R2.cmd0, '_extra_rules'])

        # 获得扩展规则的数量
        erule_count = int(self.r2_cache.get_cf_cache(R2.cf, erule_section, 'erule_count'))

        # 如果扩展规则数量小于1，说明没有规则需要判断，返回 True
        if erule_count < 1:
            return True

        # 根据扩展规则数量进行循环
        for i in range(erule_count):

            # 拼接 erule 的名称
            erule_pre = ''.join(['erule_', str(i), '_'])

            # 初始化 result 结果为 false
            result = False

            # 获得 扩展规则类型
            erule_type = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'type']))

            # 参数规则1
            if erule_type == 'extra_rule_1':

                # 获得需要的参数值
                erule_key = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'key']))
                erule_value = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'value']))
                erule_key1 = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'key1']))

                # print(erule_key)
                # print(erule_value)
                # print(erule_key1)

                # 检查 r2c1 对象中是否存在 extra_key
                if hasattr(self.r2c1_class, erule_key):
                    temp_list = getattr(self.r2c1_class, erule_key)
                    # 判断 value 是否在指定 key 中
                    if erule_value in temp_list:
                        # 判断是否存在指定 key
                        if hasattr(self.r2c1_class, erule_key1):
                            # 存在，返回 True
                            result = True
                        else:
                            result = False
                            err_count += 1
                    else:
                        result = True
                else:
                    result = True

            # 参数规则2
            elif erule_type == 'extra_rule_2':

                # 获得需要的参数值
                erule_key = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'key']))
                erule_value = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'value']))

                # 检查 r2c1 对象中是否存在 extra_key
                if hasattr(self.r2c1_class, erule_key):
                    temp_list = getattr(self.r2c1_class, erule_key)
                    # 判断 value 是否在指定 key 中
                    if erule_value in temp_list:
                        # 判断value的list元素是否等于1，是的话，说明指定value
                        if len(temp_list) == 1:
                            # 存在，返回 True
                            result = True
                        else:
                            # 不存在，返回 False
                            result = False
                            err_count += 1
                    else:
                        result = True
                else:
                    result = True

            # 参数规则3
            elif erule_type == 'extra_rule_3':

                # 获得需要的参数值
                erule_key = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'key']))
                erule_key1 = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'key1']))

                # 检查 r2c1 对象中是否存在 extra_key
                if hasattr(self.r2c1_class, erule_key):

                    # print('has opt key ', erule_key)

                    if hasattr(self.r2c1_class, erule_key1):
                        # 存在，返回 True
                        result = True
                    else:
                        # 不存在，返回 False
                        result = False
                        err_count += 1
                else:
                    result = True

            # 参数规则4
            # 2015.12.7 #12063
            elif erule_type == 'extra_rule_4':

                # 获得需要的参数值
                erule_key = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre, 'key']))
                erule_key1 = self.r2_cache.get_cf_cache(R2.cf, erule_section, ''.join([erule_pre + 'key1']))

                # 合并属性
                # eg. get -buser --user=p2p --date_kind=open,acct --date=2014,2015
                # get -buser --user=p2p --money_kind=save --money=2000
                # 2015.12.7 edit
                if hasattr(self.r2c1_class, erule_key) and hasattr(self.r2c1_class, erule_key1):
                    temp_dict = dict(zip(getattr(self.r2c1_class, erule_key), getattr(self.r2c1_class, erule_key1)))
                    setattr(self.r2c1_class, erule_key1, temp_dict)

                result = True

            # 扩展规则正确处理
            if result:
                pass
                # 日志记录
                # s = 'extra rule:' + erule_type + ';' + r2_info['EXTRA_RULE_OK']
                # logging.info(s)
            else:
                # 记录错误信息
                s = r2_info['EXTRA_RULE_ERROR'].format(info_erule=erule_type)
                # 记录到错误信息列表
                R2.r2c1_info_list.append(s)
                # 日志记录错误信息
                logging.info(s)

        # 根据错误数量，返回结果
        if err_count == 0:
            return True
        else:
            return False

    # get_cf_cache()
    # conf 读取缓存机制
    # 输入
    # 2015.12.12 create #12076
    # @staticmethod
    # def get_cf_cache(cf, section, key):
    # 
    #     # 生成 key，用于 dict
    #     temp_opt = section + '_' + key
    # 
    #     if not (temp_opt in R2.cache):
    #         R2.cache[temp_opt] = cf[section][key]
    # 
    #     return R2.cache[temp_opt]

    # check_cmd()
    # 检查命令是否在r2支持命令列表中
    # 2015.9.28. create and edit by david.yi
    # 2015.12.19 #12084 修改判断cmd的列表，从conf文件读出
    @staticmethod
    def _check_cmd(cmd):
        if cmd in R2.support_cmd:
            return True
        else:
            return False


# 生成 r2 命令的 md5  by david.yi
# 输入: cmd: r2 命令
# 输出: md5 e.g. 7c54c88c6e2f1cf32fb2bbd4a8e4bd9f
# 2016.3.9 create #12107
def cal_r2cmd_md5(cmd):

    temp_list = cmd.split(' ')
    temp_list.sort()
    temp_s = ''.join(temp_list)
    temp_md5 = fish_base.get_md5(temp_s)

    return temp_md5

# test case
# 基本测试get命令：  get -buser --user=p2p
# get -buser --user=p2p --money=1000
# get -buser --user=p2p --money=(0-10000)
