/*
 Navicat Premium Data Transfer

 Source Server         : wsl-mysql
 Source Server Type    : MySQL
 Source Server Version : 50735
 Source Host           : 172.20.122.232:3306
 Source Schema         : avbook

 Target Server Type    : MySQL
 Target Server Version : 50735
 File Encoding         : 65001

 Date: 02/09/2021 00:25:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for avbook_mgs_actress
-- ----------------------------
DROP TABLE IF EXISTS `avbook_mgs_actress`;
CREATE TABLE `avbook_mgs_actress`  (
  `actress_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `actress_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`actress_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
