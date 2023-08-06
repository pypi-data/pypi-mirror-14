# test_r2_main 单元测试
# 2015.7.11 create by David.Yi
# 2015.7.15 针对phrase_cmd 返回两个参数情况处理，对于返回false的取第一个返回值
# 2015.7.28 针对多命令支持的修改
# 2015.9.26 所有针对 show 的命令修改为针对 get 命令
# 2015.10. 对于 tokenize 也加入单元测试中
# 2015.10.31. 删除 class CheckValueTestCase(unittest.TestCase), test case已经可以覆盖，不再需要
# 2015.12.10 #12072 修改 date_kind user_kind money_kind group_kind 为 xkind，money到m，group到g
# 2015.12.18 #12085 调增为class调用方式R2
# 2016.3.5 v1.0.2 #12106 增加 args 的测试

import logging
import logging.config
import unittest
import os

import r2c1.r2_tokenize as r2t

from r2c1.r2c1_main import R2


# create 2015.7.13 by David.Yi
# edit 2015.7.28 7.31
# edit 2015.9.12 增加测试案例 #12001 #12002
# edit 2015.9.14 增加extra tools opt_rule_1 测试  #12003
# 测试 r2_main 中的 function phrase_cmd
class R2C1DoPhraseTestCase(unittest.TestCase):
    def setUp(self):
        print("test start: phrase_cmd")

    def tearDown(self):
        print("test stop: phrase_cmd")

    # bad command
    def test_cmd(self):
        self.assertFalse(r2.phrase_cmd('set', '-bsky')[0], 'test')

    # test business
    def test_phrase_cmd_business(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p')[0], 'test')
        # self.assertTrue(r2.phrase_cmd('get', '-b pos'), 'test')
        # self.assertTrue(r2.phrase_cmd('get', '-b p2p,pos'), 'test')
        self.assertFalse(r2.phrase_cmd('get', '-b p3p')[0], 'test')

    # 2015.10.28. edit
    # test region
    def test_phrase_cmd_region(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --region=w')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --region=n,s')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --region=e,w,n,s')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --region=h,c')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --region=e,w,g,s')[0], 'test')

    # test prov
    def test_phrase_cmd_prov(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --prov=sh')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --prov=sh,gd')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --region=tt')[0], 'test')

    # test multi key values
    def test_phrase_cmd_m01(self):
        self.assertTrue(r2.phrase_cmd('get', '-b p2p --dkind=open --date=2015')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-b p2p --dkind=open --date=2015,2015q1')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-b p2p --dkind=open --date=2013,2013q2 --region=w')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-b p2p --dkind=open --date=2014q3,2014q4 --region=n --prov=sh')[0],
                        'test')

    # test patten
    def test_phrase_cmd_patten(self):
        self.assertTrue(r2.phrase_cmd('get', '-b p2p -p sky01')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-b p2p -p sky02'[0]), 'test')
        self.assertTrue(r2.phrase_cmd('get', '-b p2p -p sky03')[0], 'test')

    # test --dkind option
    # 2015.9.21 create
    def test_phrase_cmd_date_kind(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=due  --date=2014')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=acct --date=2014')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=acct,open --date=2014')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=big --date=2014')[0], 'test')

    # test date
    # 2015.9.20 create
    # 2015.9.20 add test case
    # 2015.9.21 change open_date to date
    # 2015.9.26 增加 date 中错误 test case
    # 2015.10.30 增加多日期 test case
    def test_phrase_cmd_date(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=2014')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=2014-2015'), 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=2013-2014|2015')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=2013h1')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=2013h1-2013h2')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=2011q2')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=2011q2-2011q4')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=201108')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=201511')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=201507-201509')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=20160228')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=20120229')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=20151231')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open --date=20151001-20151130')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --dkind=open,due --date=20151001-20151130,2014')[0], 'test')

        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=open --date=1910')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=open --date=2013h3')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=open --date=2011q6')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=open --date=20151')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=open --date=2014-201')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=open --date=2013-2014|203')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --dkind=open,due --date=20151001-20151130,201a')[0], 'test')

    # test webstatus
    def test_phrase_cmd_webstatus(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --web_status=c')[0], 'test')

    # test --user option
    # 2015.9.12 create
    def test_phrase_cmd_user(self):
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=tty1')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=tty2')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p,tty1')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p3p')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p,tty3')[0], 'tty3 is not in value')

    # test extra tools extra_rule_1
    # 2015.9.14 create
    # 2015.9.15 add erule extra_value_2
    # 2015.10.29 add erule extra_value_3 #12053
    def test_phrase_cmd_erule_extra_rule_1(self):
        # opt_value_1
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --user=tty1')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-buser')[0], 'test')

        # opt_value_2
        self.assertTrue(r2.phrase_cmd('get', '-bsky,p2p')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-buser,sky')[0], 'test')

        # opt_value_3
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --dkind=open --date=20150703-20150803')[0],
                        'test')
        # has date, miss dkind
        self.assertFalse(r2.phrase_cmd('get', '-fusr_num,sex -buser --user=p2p --date=20150703-20150803')[0], 'test')
        # has dkind, miss date_open
        self.assertFalse(r2.phrase_cmd('get', '-fusr_num,sex -buser --user=p2p --dkind=open')[0], 'test')

    # test --period option
    # 2015.9.16 create
    def test_phrase_cmd_period(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --period=d')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --period=w')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --period=m')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --period=q')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --period=h')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --period=y')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --period=d,w')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --period=s')[0], 'test')

    # test --sex option
    # 2015.9.17 create
    def test_phrase_cmd_sex(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --sex=m')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --sex=f')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --sex=m,f')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --sex=s')[0], 'test')

    # test --ukind option
    # 2015.10.28 create
    def test_phrase_cmd_user_kind(self):
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --ukind=b')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --ukind=c')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --ukind=b,c')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p --ukind=e')[0], 'test')

    # test --mkind option
    # 2015.9.26 create
    def test_phrase_cmd_money_kind(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m1000')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=cash -m1000')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=bid -m1000')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=borr -m1000')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save,cash -m1000')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '--mkind=this')[0], 'test')

    # test -m range option
    # 2015.12.1 12.5 edit, add more test case
    # 2015.11.28 create
    def test_phrase_cmd_money(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m1000')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m1000,2000')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m1000,2000,3000')[0], 'test')

        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-1000),(2000-4000)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-1000),(2000-4000),'
                                             '(4000-6000)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-1000],(2000-4000]')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-1000),[2000-4000]')[0], 'test')

        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m1abc')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-1000}')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(10sd-1000}')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(a)')[0], 'test')

        # begin from 2015.12.5 more test case
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(1-1s]')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -mABC')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(1-100-1000]')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(1---1000]')[0], 'test')

        # exp rule 8
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m[NINF-PINF)')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-PINF]')[0], 'test')

        # exp rule 10
        self.assertTrue(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-1000)')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky --mkind=save -m(100-10)')[0], 'test')

    # test --gkind option
    # 2015.12.2 create
    def test_phrase_cmd_group_kind(self):
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age '
                                             '-g[0-24]|[25-30]')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age,prov '
                                             '-g[0-24]|[25-30]')[0], 'test')

        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age,city '
                                              '-g[0-24]|[25-30]')[0], 'test')

    # test --group option
    # 2015.12.2 create
    # 2015.12.6. 12.7 edit, add more test case
    def test_phrase_cmd_group(self):
        # group age
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age '
                                             '-g[0-24]|[25-30]|[30-PINF)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age '
                                             '-g[0-24]|[25-30]|[30-PINF)|ELSE')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age,prov '
                                             '-g[0-24]|[25-30],[40-50]')[0], 'test')

        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age -g1|2|3')[0], 'test')

        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p --gkind=age '
                                              '-g[0-ABC]|[25-30]')[0], 'test')
        # self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -gA|2|3')[0], 'test')

        # gkind 省份
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -g(sh;js;zj)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -g(sh;js;zj)|(fj;gd)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -g(sh;js;zj)|(fj;gd)|ELSE')[0],
                        'test')

        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -gsh|fj')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -gsh|ELSE')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -gsh|(gd;bj)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -ge|w|n')[0], 'test')

        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -gsh|ELSE|js')[0], 'test')

        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=region -g(e;w;n)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=region -g(e;w)|(n;s)')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=region -g(e;w;s)|(n;s)|ELSE')[0],
                        'test')

        self.assertTrue(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov,region'
                                             ' -g(sh;js;zj),(e;w)|(n;s)')[0], 'test')

        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p --gkind=prov -g(sh;jq;zj)')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-buser --user=p2p --gkind=region -g(e;w;q)')[0], 'test')

    # test args, cmd: get  args: download, test
    # 2016.3.5 create
    def test_phrase_args(self):
        self.assertTrue(r2.phrase_cmd('get', '-bsky download')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky download test')[0], 'test')
        self.assertTrue(r2.phrase_cmd('get', '-bsky')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky down')[0], 'test')
        self.assertFalse(r2.phrase_cmd('get', '-bsky download test2')[0], 'test')


# create 2015.10.17 by David.Yi
# 2015.10.21 edit 加入 exp_rule_01 测试
# 2015.11.13 edit 加入 exp_rule_02, exp_rule_07,02 测试
# 测试 tokenize.py 中的 get_token(), 对于表达式的token化测试
# 测试基于 token 的各类检查，便于r2c1中对于表达式进行检查
class R2C1TokenizeTestCase(unittest.TestCase):
    def setUp(self):
        print("test start: tokenize")

    def tearDown(self):
        print("test stop: tokenize")

    # test number expression
    def test_tokenize_number_expression(self):
        self.assertTrue(r2t.get_token('(1000-2000)')[0], 'test')
        self.assertTrue(r2t.get_token('(0-2000)')[0], 'test')
        self.assertTrue(r2t.get_token('[1000-PINF)')[0], 'test')
        self.assertTrue(r2t.get_token('[1000-20000]')[0], 'test')
        self.assertFalse(r2t.get_token('[+1000-20000]')[0], 'test')

    # 测试 token基础表达式 01 , exp_rule_01
    def test_tokenize_exp_rule_01(self):
        self.assertTrue(r2t.exp_rule_01(r2t.get_token('(1000-3000)')[1], 0, ['[', '(']), 'test')
        self.assertFalse(r2t.exp_rule_01(r2t.get_token('(1000-3000)')[1], 0, ['+', '-']), 'test')

    # 2015.11.13
    # 测试 token基础表达式 02 , exp_rule_02
    def test_tokenize_exp_rule_02(self):
        self.assertTrue(r2t.exp_rule_02(r2t.get_token('(1000-3000)')[1], 1, r2t.Integer))
        self.assertTrue(r2t.exp_rule_02(r2t.get_token('(NINF-3000)')[1], 1, r2t.Alpha))

    # 2015.11.13
    # 测试 token 表达式 01 , exp_rule_07, 检查左右括号 () []
    def test_tokenize_exp_rule_07(self):
        self.assertTrue(r2t.exp_rule_07(r2t.get_token('(1000-3000)')[1]))
        self.assertFalse(r2t.exp_rule_07(r2t.get_token('1000-3000)')[1]))

    # 2015.11.13
    # 测试 token 表达式 02 , exp_rule_08, 检查 NINF PINF
    def test_tokenize_exp_rule_08(self):
        self.assertTrue(r2t.exp_rule_08(r2t.get_token('(NINF-3000)')[1]))
        self.assertTrue(r2t.exp_rule_08(r2t.get_token('(0-PINF)')[1]))

        self.assertFalse(r2t.exp_rule_08(r2t.get_token('(NRR-3000)')[1]))
        self.assertFalse(r2t.exp_rule_08(r2t.get_token('(0-PI)')[1]))


# main
# 2016.3.29 edit for logger
if __name__ == '__main__':

    logging.basicConfig(filename='log/r2_test.log', level=logging.INFO)

    logging.info('test start')

    r2 = R2()

    # 2016.4.4 #1
    cur_dir = os.path.split(os.path.realpath(__file__))[0]
    conf_filename = os.path.join(cur_dir, 'r2c1.conf')
    # print(conf_filename)

    r2.my_init(conf_filename)
    unittest.main()
