from phonenumbers import PhoneNumberMatcher


def search(content):
    """todo 区号"""
    res = set()
    for match in PhoneNumberMatcher(content, 'CN'):
        p = str(match.number.national_number)
        res.add(p)
    return res


if __name__ == '__main__':
    content = '明天找活，我有五个内外架师傅，有需要帮忙的联系方式'
    r = search(content)
    print(r)
