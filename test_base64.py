# coding=utf-8
'''
原理：
Base64编码表由64个字符组成，编码后的字符由表中字符组合而成，流程如下：
1. base64的编码都是按字符串长度，以每3个8bit的字符为一组。
2. 然后针对每组，首先获取每个字符的ASCII编码。
3. 然后将ASCII编码转换成8bit的二进制，得到一组3*8=24bit的字节。
4. 然后再将这24bit划分为4个6bit的字节，并在每个6bit的字节前面都填两个高位0，得到4个8bit的字节。
5. 然后将这4个8bit的字节转换成10进制，对照Base64编码表，得到对应编码后的字符。
注：
• 由于要求被编码字符是8bit，所以须在ASCII编码范围内，\u0000-\u00ff，中文就不行。
• 由于2^6=64，而以1个6bit为一个单元，因此一定能在0~63的编码表中找到对应的编码！
举例如下：
（一）字符长度为能被3整除时：比如“Tom”：
                T           o         m
ASCII：        84         111       109
8bit字节：01010100    01101111  01101101
6bit字节：  010101      000110    111101     101101
十进制：        21           6        61         45
对应编码：       V           G         9          t
（二）字符串长度不能被3整除时，比如“Lucy”：
                L           u         c          y
ASCII：        76         117        99        121
8bit字节：01001100    01110101  01100011   01111001   00000000    00000000
6bit字节：  010011      000111    010101     100011     011110      010000      000000      000000
十进制：        19           7        21         35         30          16         异常        异常
对应编码：       T           H         V          j          e           Q           =           =
由于Lucy只有4个字母，所以按3个一组的话，第二组还有两个空位，所以需要用0来补齐。这里就需要注意，因为是需要补齐而出现的0，
所以转化成十进制的时候就不能按常规用base64编码表来对应，所以不是a， 可以理解成为一种特殊的“异常”，编码应该对应“=”。
如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节怎么办？Base64用\x00字节在末尾补足后，
再在编码的末尾加上1个或2个=号（最多2个=号，理解？），表示补了多少字节，解码的时候，会自动去掉。
所以，Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加33%，好处是编码后的文本数据可以在邮件正文、网页等直接显示。
'''
import base64

print base64.b64encode('binary\x00string')
print base64.b64decode('YmluYXJ5AHN0cmluZw==')
print base64.b64encode('i\xb7\x1d\xfb\xef\xff')
print base64.urlsafe_b64encode('i\xb7\x1d\xfb\xef\xff')
print base64.urlsafe_b64decode('abcd--__')
print base64.b64decode('YWJjZA==')

def safe_b64decode(instr):
    left = len(instr) % 4
    if left != 0:
        add = 4 - left
        return base64.b64decode(instr + '=' * add)
    else:
        return base64.b64decode(instr)

print safe_b64decode('YWJjZA')