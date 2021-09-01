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

 Date: 02/09/2021 00:26:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for avbook_mgs_movie
-- ----------------------------
DROP TABLE IF EXISTS `avbook_mgs_movie`;
CREATE TABLE `avbook_mgs_movie`  (
  `censored_id` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `release_date` date NULL DEFAULT NULL,
  `video_len` int(10) NOT NULL,
  `actress_id` bigint(20) NULL DEFAULT NULL,
  `maker_id` bigint(20) NULL DEFAULT NULL,
  `label_id` bigint(20) NULL DEFAULT NULL,
  `series_id` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`censored_id`) USING BTREE,
  INDEX `index_maker_id`(`maker_id`) USING BTREE,
  INDEX `index_label_id`(`label_id`) USING BTREE,
  INDEX `index_series_id`(`series_id`) USING BTREE,
  INDEX `index_actress_id`(`actress_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
