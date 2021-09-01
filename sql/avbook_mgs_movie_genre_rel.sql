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

 Date: 02/09/2021 00:26:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for avbook_mgs_movie_genre_rel
-- ----------------------------
DROP TABLE IF EXISTS `avbook_mgs_movie_genre_rel`;
CREATE TABLE `avbook_mgs_movie_genre_rel`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `censored_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `genre_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_censored_id_genre_id`(`censored_id`, `genre_id`) USING BTREE,
  INDEX `index_genre_id_censored_id`(`genre_id`, `censored_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 682 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
