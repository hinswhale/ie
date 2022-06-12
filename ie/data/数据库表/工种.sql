/*
 Navicat Premium Data Transfer

 Source Server         : 测试服务器
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : 172.16.1.201:3306
 Source Schema         : happy_worker

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 13/05/2022 13:15:17
*/


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hpwk_worker_profession_show
-- ----------------------------
use wx;
DROP TABLE IF EXISTS `hpwk_worker_profession_show`;
CREATE TABLE `hpwk_worker_profession_show`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '序号',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Name',
  `code` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Code',
  `parent_code` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '0' COMMENT '父节点',
  `source_num` int(3) NULL DEFAULT NULL COMMENT '显示顺序',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 129 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hpwk_worker_profession_show
-- ----------------------------
INSERT INTO `hpwk_worker_profession_show` VALUES (13, '建筑管理/九大员', '10', '0', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (14, '材料员', '104', '10', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (15, '施工员/工长', '101', '10', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (16, '质量员/检测员/检验员', '102', '10', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (17, '安全员', '103', '10', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (18, '实验员', '105', '10', 12);
INSERT INTO `hpwk_worker_profession_show` VALUES (19, '技术员/放线', '106', '10', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (20, '资料员/内业', '107', '10', 7);
INSERT INTO `hpwk_worker_profession_show` VALUES (21, '预算/造价', '108', '10', 8);
INSERT INTO `hpwk_worker_profession_show` VALUES (22, '测量/测绘', '109', '10', 9);
INSERT INTO `hpwk_worker_profession_show` VALUES (23, '监理', '1010', '10', 10);
INSERT INTO `hpwk_worker_profession_show` VALUES (24, '设计师/竣工图', '1011', '10', 11);
INSERT INTO `hpwk_worker_profession_show` VALUES (25, '实习生', '1012', '10', 16);
INSERT INTO `hpwk_worker_profession_show` VALUES (26, '项目经理/工程师/建造师', '1013', '10', 13);
INSERT INTO `hpwk_worker_profession_show` VALUES (27, '库管员', '1014', '10', 14);
INSERT INTO `hpwk_worker_profession_show` VALUES (28, '招投标人员', '1015', '10', 15);
INSERT INTO `hpwk_worker_profession_show` VALUES (29, '全部', '1016', '10', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (30, '建筑/装饰工程', '11', '0', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (31, '市政/园林/亮化', '12', '0', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (32, '绿化/园林/景观设计', '1201', '12', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (33, '古建筑', '1202', '12', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (34, '市政/管网', '1203', '12', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (35, '亮化/市政照明', '1204', '12', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (36, '污水处理', '1205', '12', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (37, '道路/桥梁/隧道', '13', '0', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (38, '道路/公路/铁路', '1301', '13', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (39, '桥梁', '1302', '13', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (40, '隧道/涵洞', '1303', '13', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (41, '壮工/零工', '1305', '13', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (42, '防护工程', '14', '0', 7);
INSERT INTO `hpwk_worker_profession_show` VALUES (43, '防水', '1401', '14', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (44, '护坡/边坡', '1402', '14', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (45, '安防/监控', '1403', '14', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (46, '加固', '1404', '14', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (47, '爆破', '1304', '13', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (48, '桩基/加固/土石方', '15', '0', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (49, '挖桩/打桩/破桩', '1502', '15', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (50, '地基处理', '1504', '15', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (51, '土石方', '1503', '15', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (52, '灌注桩钢筋工', '1505', '15', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (53, '加固/防护', '1506', '15', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (54, '全部', '1501', '15', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (55, '全部', '1405', '14', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (56, '全部', '1306', '13', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (57, '全部', '1206', '12', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (58, '机械工/司机/维修', '16', '0', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (59, '全部', '1601', '16', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (60, '电梯/升降机司机/安装/维修', '1602', '16', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (61, '塔吊/吊车司机/信号工/维修', '1603', '16', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (62, '挖机/钩机/维修', '1604', '16', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (63, '推土机司机', '1605', '16', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (64, '压路机/摊铺机', '1606', '16', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (65, '货车/运输车/渣土车/挂车司机', '1607', '16', 7);
INSERT INTO `hpwk_worker_profession_show` VALUES (66, '铲车/装载机', '1608', '16', 8);
INSERT INTO `hpwk_worker_profession_show` VALUES (67, '搅拌罐车/泵车司机/搅拌站', '1609', '16', 9);
INSERT INTO `hpwk_worker_profession_show` VALUES (68, '打桩机/架桥机', '1610', '16', 10);
INSERT INTO `hpwk_worker_profession_show` VALUES (69, '叉车工', '1611', '16', 11);
INSERT INTO `hpwk_worker_profession_show` VALUES (70, '吊篮安拆工/维修工', '1612', '16', 12);
INSERT INTO `hpwk_worker_profession_show` VALUES (71, '其他司机', '1613', '16', 13);
INSERT INTO `hpwk_worker_profession_show` VALUES (72, '物流运输', '20', '0', 10);
INSERT INTO `hpwk_worker_profession_show` VALUES (73, '全部', '2001', '20', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (74, '搬运工/装卸工', '2002', '20', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (75, '物流货运司机', '2003', '20', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (76, '押运员', '2004', '20', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (77, '工厂招工', '17', '0', 9);
INSERT INTO `hpwk_worker_profession_show` VALUES (78, '全部', '1701', '17', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (79, '普工', '1702', '17', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (80, '打磨工', '1703', '17', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (81, '搬运工', '1704', '17', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (82, '焊工', '1705', '17', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (83, '电工', '1706', '17', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (84, '叉车工', '1707', '17', 7);
INSERT INTO `hpwk_worker_profession_show` VALUES (85, '喷漆工', '1708', '17', 8);
INSERT INTO `hpwk_worker_profession_show` VALUES (86, '缝纫工', '1709', '17', 9);
INSERT INTO `hpwk_worker_profession_show` VALUES (87, '汽车维修工', '1710', '17', 10);
INSERT INTO `hpwk_worker_profession_show` VALUES (88, '包装工', '1711', '17', 11);
INSERT INTO `hpwk_worker_profession_show` VALUES (89, '钳工', '1712', '17', 12);
INSERT INTO `hpwk_worker_profession_show` VALUES (90, '品检工', '1713', '17', 13);
INSERT INTO `hpwk_worker_profession_show` VALUES (91, '冲压工', '1714', '17', 14);
INSERT INTO `hpwk_worker_profession_show` VALUES (92, '装配工', '1715', '17', 15);
INSERT INTO `hpwk_worker_profession_show` VALUES (93, '车工', '1716', '17', 16);
INSERT INTO `hpwk_worker_profession_show` VALUES (94, '操作工', '1717', '17', 17);
INSERT INTO `hpwk_worker_profession_show` VALUES (95, '组装工', '1718', '17', 18);
INSERT INTO `hpwk_worker_profession_show` VALUES (96, '学徒工', '1719', '17', 19);
INSERT INTO `hpwk_worker_profession_show` VALUES (97, '其他工厂', '1720', '17', 20);
INSERT INTO `hpwk_worker_profession_show` VALUES (98, '服务业', '18', '0', 11);
INSERT INTO `hpwk_worker_profession_show` VALUES (99, '全部', '1801', '18', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (100, '临时工/兼职/其他', '1810', '18', 10);
INSERT INTO `hpwk_worker_profession_show` VALUES (101, '快递员/快递分拣', '1802', '18', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (102, '外卖骑手', '1803', '18', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (103, '物业/保安/保洁/内勤', '1804', '18', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (104, '服务员/洗碗工/配菜', '1805', '18', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (105, '销售/导购/理货/营业员/店长', '1806', '18', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (106, '厨师/中餐/西餐/面点/烧烤', '1807', '18', 7);
INSERT INTO `hpwk_worker_profession_show` VALUES (107, '美容/美发', '1808', '18', 8);
INSERT INTO `hpwk_worker_profession_show` VALUES (108, '客服/售后', '1809', '18', 9);
INSERT INTO `hpwk_worker_profession_show` VALUES (109, '全部', '1101', '11', 1);
INSERT INTO `hpwk_worker_profession_show` VALUES (110, '建筑木工/铝模/拆模/二次结构', '1102', '11', 2);
INSERT INTO `hpwk_worker_profession_show` VALUES (111, '装修木工/家具/吊顶/地板', '1103', '11', 3);
INSERT INTO `hpwk_worker_profession_show` VALUES (112, '焊工/铆工/钣金/钳工', '1104', '11', 4);
INSERT INTO `hpwk_worker_profession_show` VALUES (113, '水电工/电工', '1105', '11', 5);
INSERT INTO `hpwk_worker_profession_show` VALUES (114, '弱电/消防/水暖/开槽/通风', '1106', '11', 6);
INSERT INTO `hpwk_worker_profession_show` VALUES (115, '钢筋工/绑扎/翻样/后台', '1107', '11', 7);
INSERT INTO `hpwk_worker_profession_show` VALUES (116, '架子工/爬架/拆架', '1108', '11', 8);
INSERT INTO `hpwk_worker_profession_show` VALUES (117, '混凝土/打爆模/拉毛挂网', '1109', '11', 9);
INSERT INTO `hpwk_worker_profession_show` VALUES (118, '瓦工/泥工/抹灰/砌砖/贴砖/美缝', '1110', '11', 10);
INSERT INTO `hpwk_worker_profession_show` VALUES (119, '油漆/涂料/腻子/大白/喷漆', '1111', '11', 11);
INSERT INTO `hpwk_worker_profession_show` VALUES (120, '小工/杂工/拆除工/打磨/学徒', '1112', '11', 12);
INSERT INTO `hpwk_worker_profession_show` VALUES (121, '幕墙/门窗/干挂/塞缝/打胶', '1113', '11', 13);
INSERT INTO `hpwk_worker_profession_show` VALUES (122, '外墙/吊篮/保温/高空作业', '1114', '11', 14);
INSERT INTO `hpwk_worker_profession_show` VALUES (123, '地坪/自流平/固化', '1115', '11', 15);
INSERT INTO `hpwk_worker_profession_show` VALUES (124, '空调/管道/通风/管网', '1116', '11', 16);
INSERT INTO `hpwk_worker_profession_show` VALUES (125, '钢结构/打板/不锈钢/抗震支架', '1117', '11', 17);
INSERT INTO `hpwk_worker_profession_show` VALUES (126, '钻工/炮工/矿工/喷浆手/爆破', '1118', '11', 18);
INSERT INTO `hpwk_worker_profession_show` VALUES (127, '综合承包', '19', '0', 8);
INSERT INTO `hpwk_worker_profession_show` VALUES (128, '综合承包', '1901', '19', 1);

SET FOREIGN_KEY_CHECKS = 1;
