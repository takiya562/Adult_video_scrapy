/*
 Navicat Premium Data Transfer

 Source Server         : wsl-mysql
 Source Server Type    : MySQL
 Source Server Version : 50735
 Source Host           : 172.22.195.18:3306
 Source Schema         : avbook

 Target Server Type    : MySQL
 Target Server Version : 50735
 File Encoding         : 65001

 Date: 25/09/2021 16:44:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for avbook_s1_actress
-- ----------------------------
DROP TABLE IF EXISTS `avbook_s1_actress`;
CREATE TABLE `avbook_s1_actress`  (
  `id` bigint(20) NOT NULL,
  `actress_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `actress_en_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `birth` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `height` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `three_size` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `birth_place` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `blood_type` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `hobby` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `trick` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `twitter` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ins` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index_actress_name`(`actress_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
