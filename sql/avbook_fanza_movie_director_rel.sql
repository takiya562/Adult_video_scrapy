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

 Date: 02/09/2021 00:25:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for avbook_fanza_movie_director_rel
-- ----------------------------
DROP TABLE IF EXISTS `avbook_fanza_movie_director_rel`;
CREATE TABLE `avbook_fanza_movie_director_rel`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `censored_id` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `director_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_censored_id`(`censored_id`) USING BTREE,
  INDEX `index_director_id`(`director_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 130 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;