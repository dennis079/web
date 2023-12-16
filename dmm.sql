SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for dm_orders
-- ----------------------------
DROP TABLE IF EXISTS `dm_orders`;
CREATE TABLE `dm_orders` (
  `oid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `olabel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Order custom name, used for order management, not used for now',
  `oname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ts_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `odirect` int(11) DEFAULT NULL COMMENT 'Position opening direction, 0-buy open, 1-sell open, 2-sell close to buy, 3-buy close and sell',
  `amount` float DEFAULT NULL COMMENT 'Lot is the unit, 1 lot = 100 shares, 1 lot = 1 contract unit, decimals are not allowed, but they can be decimals',
  `price` float(10,3) DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  `ostatus` int(11) DEFAULT NULL COMMENT 'Order status: 0-new order, 1-submitting, 2-completed, 3-completed, -5-to be cancelled, -1-cancelled, -2-invalid, -3-timed out, -4 invalid order',
  `dealamount` float DEFAULT NULL COMMENT 'Actual transaction quantity',
  `dealprice` float(10,3) DEFAULT NULL COMMENT 'Actual transaction price',
  `dealtime` datetime DEFAULT NULL COMMENT 'Actual transaction time ',
  `nownum` float DEFAULT NULL COMMENT 'The number of positions held after the order is filled',
  `costprice` float DEFAULT NULL COMMENT 'The average cost of the same direction after the order is completed',
  `lastnum` float DEFAULT NULL,
  `lastcost` float(10,3) DEFAULT NULL,
  `testid` int(11) DEFAULT '0' COMMENT 'The backtest number, which identifies all the order lists corresponding to the backtest, the default is 0 - the actual order list corresponding to the pid',
  `sparam` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nparam` int(11) DEFAULT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=256 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of dm_orders
-- ----------------------------
INSERT INTO `dm_orders` VALUES ('252', '0', '', 'kswh', '002425.SZ', '0', '8000', '6.990', '2021-08-31 10:35:00', '2', '8000', '6.990', '2021-08-31 10:35:00', '8000', '6.99', '8000', '6.990', '0', '', '0');
INSERT INTO `dm_orders` VALUES ('253', '0', '', 'bysk', '688181.SH', '0', '700', '49.050', '2021-09-01 10:30:00', '2', '700', '49.050', '2021-09-01 10:30:00', '700', '49.05', '700', '49.050', '0', '', '0');
INSERT INTO `dm_orders` VALUES ('254', '0', '', 'nsjt', '603700.SH', '0', '6000', '18.970', '2021-09-02 09:25:00', '2', '6000', '18.970', '2021-09-02 09:25:00', '6000', '18.97', '6000', '18.970', '0', '', '0');
INSERT INTO `dm_orders` VALUES ('255', '0', '', 'kswh', '002425.SZ', '3', '7000', '8.090', '2021-09-07 09:35:00', '2', '7000', '8.090', '2021-09-07 09:35:00', '7000', '8.09', '7000', '8.090', '0', '', '0');

-- ----------------------------
-- Table structure for dusers
-- ----------------------------
DROP TABLE IF EXISTS `dusers`;
CREATE TABLE `dusers` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(50) DEFAULT NULL,
  `utype` int(11) DEFAULT NULL COMMENT '0-admin，1-customer，2-VIP_customer',
  `urefer` int(11) DEFAULT NULL,
  `upoint` int(11) DEFAULT NULL,
  `sparam` varchar(255) DEFAULT NULL,
  `nparam` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of dusers
-- ----------------------------
INSERT INTO `dusers` VALUES ('1', 'Admin', '0', '0', '0', '', '0');
INSERT INTO `dusers` VALUES ('2', 'Guest', '1', '0', '0', '', '0');
INSERT INTO `dusers` VALUES ('3', 'Tester', '1', '0', '0', '', '0');
