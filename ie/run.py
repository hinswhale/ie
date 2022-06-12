import logging
import os
import traceback

import pandas as pd
from units import salary
from settings import data_root
from utils.tools import clean_text

pattern = f'\d+(元|块)?(?P<unit>一小?(月|天|时))'
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.ERROR)
handler = logging.FileHandler('../log/error.log')
logger.addHandler(handler)


def read_data(file_path):
    path = os.path.join(data_root, file_path)
    print(path)
    try:
        df = pd.read_excel(path)
    except:
        df = pd.read_csv(path)
    return df


def run_worker():
    path = '自动摘录样本&相关词表/【样本】-招工-平台抓取.xlsx'
    # path = '自动摘录样本&相关词表/【样本】-招工-人工采集(含字段抽取).xlsx'
    # 招工数据表
    from core.search_worker import extract
    from core.extract import propress_text
    df = read_data(path)
    records = df.to_dict('records')

    l = []
    for i, record in enumerate(records):
        content = record['用工需求']
        print(content)
        content = propress_text(content)
        res = extract(content)
        print(res)
        l.append(res)
    df = pd.DataFrame(l)
    df.to_csv(data_root + 'run_worker.csv')
    return l


def run_job():
    path = '自动摘录样本&相关词表/【样本】-工人-平台抓取.xlsx'
    path = '自动摘录样本&相关词表/【样本】-工人-人工采集(含字段抽取).xlsx'
    # # 找工作
    from core.search_job import extract
    from core.extract import propress_text
    df = read_data(path)
    records = df.to_dict('records')
    key = '自我介绍'  # 招工详情

    l = []
    for i, record in enumerate(records):
        content = record[key]
        if pd.isnull(content):
            continue

        print(content)
        content = propress_text(content)
        if pd.isnull(content):
            continue
        res = extract(content)
        # ad = address.search(content)
        print(res)
        # print(record['详细地址'])
        print('########' * 30)
        l.append(res)
    df = pd.DataFrame(l)
    df.to_csv(data_root + 'run_job.csv')
    return l


def run_job_1():
    path = '自动摘录样本&相关词表/【样本】-工人-平台抓取.xlsx'
    path = '自动摘录样本&相关词表/【样本】-工人-人工采集(含字段抽取).xlsx'
    # # 找工作
    from core.search_job import extract
    from core.extract import propress_text
    df = read_data(path)
    records = df.to_dict('records')
    key = '自我介绍'  # 招工详情

    l = []
    for i, record in enumerate(records):
        content = record[key]
        content = '找活!平顶山,叶县,襄县附近!专业架子工突击队!平顶山附近方园百里都可以去!包工优先,欢迎与各位合作共赢!电话微信同号!'
        if pd.isnull(content):
            continue

        r = {}
        content = propress_text(content)
        if pd.isnull(content):
            continue
        print(content)
        print(record['期望工作地点（市）名称'])
        print('\n')
        try:
            res = extract(content)
            print(res)
            r['pep_num'] = res['pep_num']
            r['pep_composition'] = res['pep_composition']
            r['city_name'] = res['expected_city_name']
            r['nickname'] = res['nickname']
        except Exception as e:
            logger.error(e)
            logger.error(f'content: {content},e: {traceback.format_exc()}')
        # r['自我介绍'] = record['自我介绍']
        # r['人数'] = record['人数']
        # r['人员构成'] = record['人员构成']
        # r['城市'] = record['期望工作地点（市）名称']
        # r['昵称'] = record['昵称']
        break
        print('########' * 30)
        l.append(r)
    # df = pd.DataFrame(l)
    # df.to_csv(data_root + 'run_job.csv')
    return l


if __name__ == '__main__':
    run_job_1()

#
# 徐州铜山区小别墅钢木化，木工带材料，大清包找有实力的老板
# 专业承接：家装 木工，水电，厂房办公楼轻钢龙骨隔断，吊顶，开关插座，灯具洁具，壁纸，硅藻泥，有需要的联系
# 找活,,,外架搭拆,明天用人的老板提前联系了,找我,人员充足,周口,西华,商水,项城,郸城,许昌,漯河,淮阳,沈丘,扶沟,太康,方圆百里都可以去,人员年轻,干活实在,专业队伍,我专业你需要,拿起电话合作就开始了,专业架子工团队,主干,外架,内架,爬架,满堂架,人员年轻,火力强大,干活生猛,专业为各位老板排忧解难微信同号
# 广东省,江西省
 # 京津冀。雄安新区,保定地区,用人老板请联系诚信架子工突击队人员充足,钢挑架。爬架,吊架,接受您来随时骚扰,电话人员齐全,带有核酸,诚信架子工突击队,价格公道,绝对不高,找活
# dizhi
# 人找活：装修水电工2－4人，需要的联系王工
# 专业水电团队、专业工装水电团队、施工经验丰富（办公楼、商铺、饭店、学校，银行、商场、桥架安装、T接、配电柜压线、住宅楼穿线上面板）、工具齐全、可随时上人、施工保证质量、有需要的联系、服务于京津冀以及周边、介绍活的给提成、谢谢
# 江苏盐城水电安装团队，以强电为主，后期安装，桥架，配管，穿线，放电缆，压箱子，上面板 有二十多人有需要的老板联系：
# 雄安新区有十几个钢筋工，几个力工，七八个木工找活，要求下班结账，联系电话同微信。
# 本人专业内墙抹灰长期在碧桂园干有需要的老板可以联系我限广西微信同号
# 找珠三角套房工区墙地砖活 周

# 接钢筋翻样，钢筋算量，模板算量，月薪，包平米基础住现场，排布图，料单清晰易懂。有翻样外包的老板，翻样忙不过来的，价格从优。期待与您的合作，微信，手机同号，

# 现在有一车钢筋工人在济宁有用人的老板或伙伴请联系我
# 专业油工找活工装，别墅，厂房，油工全活，工具齐全。微信同步 都是年轻人干活麻利
# 明天还有，钢筋工一车有用的联系我
# 明天还有一车钢筋好手用人的老板请联系
# 明天下来1车钢筋熟手用人说话
# 【工人找活】勤劳能干，诚实靠谱。在北京承接新～旧楼外墙保温，弹涂，涂料，真石漆，颗粒找平，随时上岗，需要施工人员的老板来电非诚勿扰
# 北京现在本人还剩40多个专业干外墙岩棉，外墙旧楼，新旧，吊篮，架子都可以，岩棉，挤塑板都行，有活的老板联系我随时可以上人，都在北京14天了，都有48小时核酸.
# 明天四五个人到十人找活。包工优先。都是老手。要求日结。
# 明天两焊工找活，找活，电焊二氧氩弧焊，工具齐全带证带车，包工天工都行
# "人找活：装修水电工2－4人，需要的联系王工
# 微信同步"
# 找活，找活？山东境内 专业拆木模，模壳，高低楼都可以，，拆内架，人年轻能干，价格合理，可包可点，要求钱快，欢迎各位老板来电：田
