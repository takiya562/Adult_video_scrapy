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

 Date: 02/09/2021 00:25:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for avbook_fanza_movie
-- ----------------------------
DROP TABLE IF EXISTS `avbook_fanza_movie`;
CREATE TABLE `avbook_fanza_movie`  (
  `censored_id` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '番号',
  `title` varchar(225) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `release_date` date NOT NULL COMMENT '发售日期',
  `video_len` int(10) NOT NULL COMMENT '影片时长',
  `maker_id` bigint(20) NULL DEFAULT NULL COMMENT '制作商ID',
  `label_id` bigint(20) NULL DEFAULT NULL COMMENT '发行商ID',
  `series_id` bigint(20) NULL DEFAULT NULL COMMENT '系列ID',
  PRIMARY KEY (`censored_id`) USING BTREE,
  INDEX `index_maker_id`(`maker_id`) USING BTREE,
  INDEX `index_label_id`(`label_id`) USING BTREE,
  INDEX `index_series_id`(`series_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
