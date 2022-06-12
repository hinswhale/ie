"""
找工人：
---昵称、联系方式、工种同找工作；
---性别获取不到则默认为男；
---期望工作地仅限省、市，若仅获取到区，则根据地址库自动填入市的信息；
---人员构成分为班组和个人，若获取不到班组则默认为个人；
---人数在人员构成为班组时填写，获取到不填写；
---自我介绍录入社群用户发布的完整消息，并删除所有联系方式；
---必填项不完整的不录入（工种code2、工种code3、人数为非必填项）
"""
from ie.units import worktype, contact, phone_unit, salary
from ie.units import address


# 待确认招工数据表
def extract(content):
    work_type = worktype.search(content)  # 工种
    ad = address.search(content)  # 省/市/区/详细地址
    salary_ = salary.search(content)

    # 薪酬及单位
    try:
        contact_ = contact.search(content)  # 联系人
    except:
        contact_ = ''
    mobiles = phone_unit.search(content)  # 手机号

    job_details = content
    for mobile in mobiles:
        job_details = job_details.replace(mobile, '')
    try:
        return {
            'work_type': work_type,
            'province': ad.get('province'),
            'city': ad.get('city'),
            'district': ad.get('county'),
            'address': ad.get('address'),
            'pay': salary_.get('salary'),
            'pay_type': salary_.get('unit'),
            'contacts_pep': contact_,
            'contacts_tel': ' '.join(mobiles),
            'job_details': job_details,
            'data_info': content,
        }
    except Exception as e:
        print(e)
        return {}
