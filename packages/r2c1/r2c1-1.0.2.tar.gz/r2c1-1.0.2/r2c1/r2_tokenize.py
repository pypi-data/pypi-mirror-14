# 2015.10.15 edit by david.yi, 从网络上学习
# 2015.10.17 almost finish
# 2015.12 持续优化

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

Alpha, Integer, LP, RP, LB, RB, Hyphen, Semicolon, EOF, ErrToken \
    = \
    'Alpha', 'Integer', 'LP', 'RP', 'LB', 'RB', 'Hyphen', 'Semicolon', 'EOF', 'ErrToken'

Token_List = ['(', ')', '[', ']', '-', ';']
Token_Name = ['LP', 'RP', 'LB', 'RB', 'Hyphen', 'Semicolon']

Alpha_List = ['ELSE', 'NINF', 'PINF']


# 自定义异常
# 2015.10.17
class TokenError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


class Token(object):
    def __init__(self, token_type, value):
        # token type: Integer, PLUS, MINUS, or EOF
        self.token_type = token_type
        # token value: non-negative integer value, '+', '-', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(Integer, 3)
            Token(PLUS, '+')
        """
        return 'Token({token_type}, {value})'.format(
            token_type=self.token_type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


# 实现tokenize过程的class
# edit 2015.11.12
class Tokenize(object):
    def __init__(self, text):
        # client string input, e.g. "3 + 5", "12 - 5 + 3", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    ##########################################################
    # Lexer code                                             #
    ##########################################################

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multi digit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    # 2015.10.16. 判断处理表达式中的字符串
    def alpha(self):
        """Return a (multi) Alpha consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    @property
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            temp_char = self.current_char

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(Integer, self.integer())

            if self.current_char.isalpha():
                return Token(Alpha, self.alpha())

            # 判断各类 token 符号
            if self.current_char in Token_List:
                self.advance()
                token_pos = Token_List.index(temp_char)
                return Token(Token_Name[token_pos], temp_char)

            # 返回解析错误
            return Token(ErrToken, self.current_char)

            # 触发token异常
            # raise TokenError('tokenize token error')

        return Token(EOF, None)


# 输入： 字符串
# 输出：是否解析正确或者错误，解析后的list，解析信息主要用在错误信息
# 2015.10.17
def get_token(s):
    tokens = Tokenize(s)

    m = None  # 标志，循环控制
    l = []  # 存储结果列表
    token_err_mark = False  # 记录tokenize 错误
    info = ''  # 记录token解析信息

    while m != EOF:
        try:
            # 获得 token
            t1 = tokens.get_next_token
            l.append(t1)  # token追加到list
            m = t1.token_type  # token 的类型

            # 如果 token 类型是token解析错误
            if m == ErrToken:
                token_err_mark = True
                info = t1.value
                break
        except TokenError:
            token_err_mark = True
            break

    # 返回结果
    if not token_err_mark:
        return True, l, info
    else:
        return False, l, info


# token表达式基础规则1，判断token_list指定位置是否存在指定字符列表
# 输入参数：token_list：通过解析的token列表 token_index：需要判断的位置
# 输出：True 匹配规则  False 不匹配规则
# token_match_list: 需要检查匹配的token列表
# 2015.10.20. 11.8.
def exp_rule_01(token_list, token_index, token_match_list):

    if token_list[token_index].value in token_match_list:
        return True
    else:
        return False


# token表达式基础规则2，判断token_list指定位置是否存在指定类型
# 输入参数：token_list：通过解析的token列表 token_pos：需要判断的位置
# 输出：True 匹配规则  False 不匹配规则
# 2015.11.13
def exp_rule_02(token_list, token_pos, token_type):

    if token_list[token_pos].token_type == token_type:
        return True
    else:
        return False


# token表达式基础规则3，计算 token_list 中元素个数
# 输入参数：token_list：通过解析的token列表
# 输出：数量
# create 2015.11.29
def exp_rule_03(token_list):
    return len(token_list)


# token表达式基础规则4，判断 token_list 中是否有 Integer 和 APLHA 相邻，视其为错误
# create 2015.12.5.
def exp_rule_04(token_list):

    # 判断是否是一个单词
    if not(exp_rule_09(token_list)):

        for index in range(len(token_list)):

            # 如果 token 是  Integer 且  不在第一个
            if (token_list[index].token_type == Integer) and not (index == 0):

                # 如果相邻 Alpha
                if token_list[index - 1].token_type == Alpha or token_list[index + 1].token_type == Alpha:
                    return False

    return True


# token表达式基础规则5，判断 token_list 某个符号的限制数量，
# create 2015.12.5.
def exp_rule_05(token_list, char, char_limit):

    counter = 0

    for i in range(len(token_list)):

        if token_list[i].token_type == RP or token_list[i].token_type == RB:

            counter = 0

        if token_list[i].value == char:

            counter += 1

        if counter == char_limit:

            return True

    return False


# token表达式基础规则6，判断 token_list 某个符号的数量，如果大于1个，则为False
# create 2015.12.5.
def exp_rule_06(token_list):

    if exp_rule_05(token_list, '-', 2):
        return True


# 表达式规则7，检查括号匹配情况
# 2015.11.8 11.11 11.30 12.4
def exp_rule_07(token_list):
    # 如果token list 只有两个token，不需要判断括号，跳出
    if exp_rule_03(token_list) == 2:
        return True

    # 如果是 [a]，则返回False，不符合
    if exp_rule_03(token_list) == 4:
        if exp_rule_02(token_list, 1, Alpha):
            return False

    # 判断左边括号
    if not (exp_rule_01(token_list, 0, ['[', '('])):
        return False

    # 判断右边括号
    # -1 为 EOF 标记，-2 为最右边token位置
    if not (exp_rule_01(token_list, -2, [']', ')'])):
        return False

    # 左边右边判断都没有跳出，说明符合规则，返回 True
    return True


# 表达式规则8，判断 NINF，PINF 拼写是否正确，以及位置是否正确，分别表示无穷小，无穷大
# 2015.11.12 11.13 12.1 12.4
# 2015.12.2 需要判断如果左边和右边不是字符的话，不参加判断
# 2015.12.6 #13004 NINF 和 PINF 只能用在开区间 ()
# 2015.12.7 修订，针对 (js;zj) 类情况算正确
def exp_rule_08(token_list):
    # 如果token 数量是6个，也就是 [n0,n1] 这样
    if exp_rule_03(token_list) == 6:

        # 如果两个都是alpha，且不是NINF和PINF，返回True
        if exp_rule_02(token_list, 1, Alpha) and exp_rule_02(token_list, -3, Alpha):
            if (not exp_rule_01(token_list, 1, ['NINF'])) and (not exp_rule_01(token_list, -3, ['NINF'])):
                if (not exp_rule_01(token_list, 1, ['PINF'])) and (not exp_rule_01(token_list, -3, ['PINF'])):
                    return True

        # 判断左边NINF
        # 如果左边token是字符，判断是否为left的NINF
        if exp_rule_02(token_list, 1, Alpha):
            if not exp_rule_01(token_list, 1, ['NINF']):
                return False
            # 检查括号
            if not exp_rule_02(token_list, 0, LP):
                return False

        # 判断右边PINF
        # 如果右边token是字符，判断是否为right的PINF
        if exp_rule_02(token_list, -3, Alpha):
            if not exp_rule_01(token_list, -3, ['PINF']):
                return False
            # 检查括号
            if not exp_rule_02(token_list, -2, RP):
                return False

    return True


# 判断token list是否只是一个数字或者单词，eg  money=1000； ELSE
# 2015.11.30 create
# 2015.12.6 edit, #12060, 支持单词判断
# 2015.12.7 edit
# 2015.12.15 edit from LiuQuan's comment
def exp_rule_09(token_list):

    # 如果是单一整数，返回 True
    if exp_rule_02(token_list, 0, Integer):
        return True
    # 如果是单一单词，判断是否在默认单词列表中
    if exp_rule_02(token_list, 0, Alpha):
        if token_list[0].value in Alpha_List:
            return True

    return False


# token表达式基础规则10，判断 token_list 如果 (n1-n2)情况，n1 < n2
# create 2015.12.6.
def exp_rule_10(token_list):

    # 判断位置  (n1,n2) n1和n2都是INTEGER，才判断
    if exp_rule_02(token_list, 1, Integer) and exp_rule_02(token_list, -3, Integer):
        if token_list[1].value < token_list[-3].value:
            return True
        else:
            return False

    return True


# token表达式基础规则11，判断 token_list 中是否 value 都在传入的 list 中
# create 2015.12.6
# edit 2015.12.9 修改list匹配，考虑NINF，PINF等保留字情况
def exp_rule_11(token_list, value_list):

    value_list.extend(Alpha_List)

    if exp_rule_03(token_list) > 2:

        for item in token_list:
            if item.token_type == Alpha:
                if not (item.value in value_list):
                    return False

    return True


# token表达式基础规则12，判断 token_list 中是否 (1-100) (NINF-1000) (1-PINF) 样式
# create 2015.12.7.
def exp_rule_12(token_list):

    if exp_rule_02(token_list, 1, Integer) or exp_rule_02(token_list, -3, Integer):
        return True


# 可以理解为如何使用 get_token 函数
# 2015.10 2015.11
def main():
    token_mark, token_list, token_info = get_token('(1-1s)')
    if token_mark:
        print('token ok')
        print(token_list)
    else:
        print('token error')
        print(token_info)

    print('token list:', get_token('[0-24]')[1])
    print('token list:', get_token('ELSE')[1])
    print('token list:', get_token('(sh;js)')[1])
    print('token count:', exp_rule_03(get_token('1000')[1]))

    # 检查 括号 输入是否正确
    if exp_rule_07(get_token('(1000,3000)')[1]):
        print('match rule 1 ')
    else:
        print('not match rule 1 ')

    # 检查 NINF 输入是否正确
    # 实际使用的时候，需要先判断左边token是否为Alpha，是的话，再判断是否为NINF
    if exp_rule_08(get_token('(NINF-3000)')[1]):
        print('match rule 2 ')
    else:
        print('not match rule 2 ')

    if exp_rule_08(get_token('(0-PINF)')[1]):
        print('match rule 2 ')
    else:
        print('not match rule 2 ')

    if exp_rule_08(get_token('(100-1000)')[1]):
        print('two integer, rule 2 ')
    else:
        print('should two integer, but sth error')

    if exp_rule_09(get_token('(3000-1000)')[1]):
        print('only integer or more tokens')
    else:
        print('not only integer')

    # test rule 04
    if not(exp_rule_04(get_token('(1-1s)')[1])):
        print('1s is false')
    else:
        print('1s check wrong')

    # test rule 06
    if exp_rule_06(get_token('(1-1s)(1-23)')[1]):
        print('more than one Hyphen')
    else:
        print('only one Hyphen')

    # test rule 10
    if exp_rule_10(get_token('(10-100)')[1]):
        print('rule 10, n1 < n2')
    else:
        print('rule 10, sth wrong')

    # test rule 11
    if exp_rule_11(get_token('(sh;zj)')[1], ['sh', 'zj', 'js']):
        print('rule 11-1, token in list')
    else:
        print('rule 11-1, sth wrong')

    if exp_rule_11(get_token('(sh;zq)')[1], ['sh', 'zj', 'js']):
        print('rule 11-2, token not in list')
    else:
        print('rule 11-2, sth wrong')


# main
if __name__ == '__main__':
    main()
