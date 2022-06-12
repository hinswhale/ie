"""
找工作：
---工种根据提供的工种列表（见后台）匹配对应关键词，对应到多个关键词的，填写多个工种；
---地址根据提供的地址库信息（见后台），匹配到哪一级地址，自动填写直到最高级地址；
---薪酬根据数据内容获取，含多种薪资单位的，获取优先级日薪>月薪>时薪，获取不到则为面议，日薪区间50-1999；月薪区间2000-29999；时薪区间1-100，区间外为面议；
---联系人有姓名则匹配姓名，没有匹配如下关键词：X工，X师傅，X经理，X总，X老板，X先生，X女士，X小姐，X为姓，匹配不到任何信息默认为先生；
---联系电话根据运营商号段表（待提供）匹配，多个号码录入首个，消息中无号码的若微信用户名中包含则录入微信用户名中号码，若无法获取则整条找工作信息不录入；
---用工需求录入社群用户发布的完整消息，并删除所有联系方式；
---必填项不完整的不录入（区、详细地址、薪酬为非必填项）
"""

from ie.units import staff, worktype, contact, phone_unit
from ie.units import gender, address


# 待确认找工数据表
def extract(content):
    nickname = contact.search(content)  # 联系人
    gender_ = gender.search(content)  # 性别
    mobiles = phone_unit.search(content)  # 手机号
    work_type1 = worktype.search(content)  # 工种 多个
    city = address.search(content)  # 期望城市
    print(city)
    expected_city_name = city.get('province') + city.get('city')
    pep_composition = staff.search(content)
    introduction = content
    for mobile in mobiles:
        introduction = introduction.replace(mobile, '')

    mobile = ' '.join(mobiles)

    num = None
    compose = ''
    for i in pep_composition:
        num = i.get('num')
        compose = i.get('compose')
    return {
        'data_info': content,
        'nickname': nickname,
        'gender': gender_,
        'mobile': mobile,
        'work_type1': work_type1,
        'expected_city_name': expected_city_name,
        'pep_num': num,
        'pep_composition': compose,
        'self_introduction': introduction
    }
