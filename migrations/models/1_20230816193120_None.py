from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `roles` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(32) NOT NULL UNIQUE COMMENT '角色名',
    `description` VARCHAR(256) NOT NULL  COMMENT '角色描述'
) CHARACTER SET utf8mb4 COMMENT='角色表';
CREATE TABLE IF NOT EXISTS `users` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `username` VARCHAR(64) NOT NULL,
    `nickname` VARCHAR(128),
    `is_super` SMALLINT NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    `mobile` VARCHAR(15),
    `email` VARCHAR(64),
    `password` VARCHAR(128) NOT NULL,
    `avatar` VARCHAR(256),
    `last_day` DATE   COMMENT '授权时间',
    `category` SMALLINT NOT NULL  COMMENT '用户类型' DEFAULT 1,
    `user_id` VARCHAR(64) NOT NULL,
    UNIQUE KEY `uid_users_company_e7cc10` (`company_id`, `id`)
) CHARACTER SET utf8mb4 COMMENT='用户表信息';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `carsensors` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `car_id` INT NOT NULL,
    `sensor_id` INT NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `nick_name` VARCHAR(64) NOT NULL,
    `type` VARCHAR(64) NOT NULL,
    `position_x` DOUBLE NOT NULL,
    `position_y` DOUBLE NOT NULL,
    `position_z` DOUBLE NOT NULL,
    `roll` DOUBLE NOT NULL,
    `pitch` DOUBLE NOT NULL,
    `yaw` DOUBLE NOT NULL,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    `data_record` BOOL NOT NULL  DEFAULT 0,
    `semantic` BOOL NOT NULL  DEFAULT 0,
    `instance` BOOL NOT NULL  DEFAULT 0,
    UNIQUE KEY `uid_carsensors_invalid_a5d8ab` (`invalid`, `nick_name`, `type`, `car_id`, `company_id`)
) CHARACTER SET utf8mb4 COMMENT='车辆传感器位置表';
CREATE TABLE IF NOT EXISTS `cars` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc` VARCHAR(64),
    `desc_en` VARCHAR(64),
    `vehicle_color` VARCHAR(64) NOT NULL,
    `light_state` VARCHAR(20),
    `type` VARCHAR(64) NOT NULL,
    `dynamics_id` INT NOT NULL,
    `render_mode` VARCHAR(20),
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_cars_invalid_e28886` (`invalid`, `name`, `user_id`)
) CHARACTER SET utf8mb4 COMMENT='车辆表';
CREATE TABLE IF NOT EXISTS `dynamics` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc` VARCHAR(64),
    `desc_en` VARCHAR(64),
    `param` JSON NOT NULL,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_dynamics_invalid_fa0c9c` (`invalid`, `name`, `user_id`, `company_id`)
) CHARACTER SET utf8mb4 COMMENT='动力学模型';
CREATE TABLE IF NOT EXISTS `jobs` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc_en` VARCHAR(256),
    `desc` VARCHAR(256),
    `status` VARCHAR(10) NOT NULL,
    `render_mode` VARCHAR(10) NOT NULL,
    `controller` VARCHAR(32) NOT NULL,
    `controller_version` VARCHAR(50) NOT NULL,
    `scenario_ids` JSON NOT NULL,
    `car_id` INT NOT NULL,
    `start_time` DATETIME(6),
    `end_time` DATETIME(6),
    `car_snap` JSON,
    `sensors_snap` JSON,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    `view_record` BOOL NOT NULL  DEFAULT 0,
    `show_game_window` BOOL NOT NULL  DEFAULT 0,
    UNIQUE KEY `uid_jobs_invalid_59abe8` (`invalid`, `name`, `user_id`, `company_id`),
    KEY `idx_jobs_user_id_824672` (`user_id`, `status`, `invalid`)
) CHARACTER SET utf8mb4 COMMENT='作业';
CREATE TABLE IF NOT EXISTS `lights` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc` VARCHAR(64),
    `desc_en` VARCHAR(64),
    `sun_azimuth_angle` DOUBLE NOT NULL,
    `sun_altitude_angle` DOUBLE NOT NULL,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_lights_invalid_5a7a1e` (`invalid`, `name`, `user_id`, `company_id`)
) CHARACTER SET utf8mb4 COMMENT='光照';
CREATE TABLE IF NOT EXISTS `scenarioparams` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `scenario_id` INT NOT NULL,
    `item_type` VARCHAR(10) NOT NULL,
    `item_key` VARCHAR(20) NOT NULL,
    `item_value` JSON NOT NULL
) CHARACTER SET utf8mb4 COMMENT='场景参数';
CREATE TABLE IF NOT EXISTS `scenarios` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc` VARCHAR(64)   DEFAULT '',
    `desc_en` VARCHAR(64),
    `tags` JSON NOT NULL,
    `tags_en` JSON,
    `type` VARCHAR(10) NOT NULL,
    `parent_id` INT,
    `lever` VARCHAR(20),
    `map_name` VARCHAR(20),
    `traffic_flow` JSON,
    `open_scenario_json` JSON NOT NULL,
    `ui_entities_json` JSON,
    `environment` JSON,
    `evaluation_standard` JSON,
    `is_temp` BOOL NOT NULL  DEFAULT 0,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `criterion_id` INT,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_scenarios_user_id_678455` (`user_id`, `invalid`, `name`, `parent_id`, `company_id`),
    KEY `idx_scenarios_user_id_79c61b` (`user_id`, `is_temp`)
) CHARACTER SET utf8mb4 COMMENT='场景';
CREATE TABLE IF NOT EXISTS `sensor_data` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `task_id` INT NOT NULL,
    `sensor_type` VARCHAR(64) NOT NULL,
    `sensor_name` VARCHAR(64) NOT NULL,
    `car_sensor_id` INT NOT NULL,
    `process_rate_img` INT,
    `process_rate_video` INT,
    `process_rate_data` INT,
    `process_rate_semantic` INT,
    `process_rate_instance` INT,
    `data_url` VARCHAR(256),
    `platform` VARCHAR(20),
    `data_size` VARCHAR(20),
    `cam_url` VARCHAR(256),
    `process_rate_cam` INT,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1
) CHARACTER SET utf8mb4 COMMENT='传感器数据表';
CREATE TABLE IF NOT EXISTS `sensors` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc` VARCHAR(64),
    `desc_en` VARCHAR(64),
    `type` VARCHAR(64) NOT NULL,
    `group_type` VARCHAR(64) NOT NULL,
    `param` JSON NOT NULL,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_sensors_invalid_a7b261` (`invalid`, `name`, `user_id`, `company_id`)
) CHARACTER SET utf8mb4 COMMENT='传感器表';
CREATE TABLE IF NOT EXISTS `tasks` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `user_id` INT NOT NULL,
    `job_id` INT NOT NULL,
    `job_name` VARCHAR(64) NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `desc` VARCHAR(64) NOT NULL,
    `scenario_id` INT NOT NULL,
    `scenario_tags` JSON NOT NULL,
    `scenario_param` JSON,
    `status` VARCHAR(10),
    `result` JSON,
    `replay_url` VARCHAR(256),
    `cam_url` VARCHAR(256),
    `index` DECIMAL(64,2) NOT NULL  DEFAULT 0,
    `start_time` DATETIME(6),
    `end_time` DATETIME(6),
    `process_rate` VARCHAR(10),
    `running_time` VARCHAR(30),
    `mileage` INT,
    `ret_status` VARCHAR(20),
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_tasks_invalid_e62348` (`invalid`, `name`, `user_id`, `job_id`, `company_id`, `id`),
    KEY `idx_tasks_job_id_70134a` (`job_id`, `status`, `invalid`, `user_id`)
) CHARACTER SET utf8mb4 COMMENT='任务';
CREATE TABLE IF NOT EXISTS `weather` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc` VARCHAR(64),
    `desc_en` VARCHAR(64),
    `cloudiness` DOUBLE NOT NULL,
    `precipitation` DOUBLE NOT NULL,
    `precipitation_deposits` DOUBLE NOT NULL,
    `wind_intensity` DOUBLE NOT NULL,
    `fog_density` DOUBLE NOT NULL,
    `fog_distance` DOUBLE NOT NULL,
    `wetness` DOUBLE NOT NULL,
    `fog_falloff` DOUBLE NOT NULL,
    `fog_visualrange` DOUBLE NOT NULL,
    `sky_visibility` BOOL NOT NULL,
    `cloudstate` VARCHAR(20) NOT NULL,
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_weather_invalid_148bad` (`invalid`, `name`, `user_id`, `company_id`)
) CHARACTER SET utf8mb4 COMMENT='天气';
CREATE TABLE IF NOT EXISTS `traffic_flow` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `actor` VARCHAR(64) NOT NULL,
    `actor_class` VARCHAR(128) NOT NULL
) CHARACTER SET utf8mb4 COMMENT='交通流';
CREATE TABLE IF NOT EXISTS `logs` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `logger` VARCHAR(20) NOT NULL,
    `msg` LONGTEXT NOT NULL,
    `log_level` VARCHAR(10) NOT NULL,
    `task_id` INT NOT NULL,
    `type` VARCHAR(45) NOT NULL,
    `ip` VARCHAR(20) NOT NULL,
    `log_time` DATETIME(6) NOT NULL,
    `game_time` VARCHAR(45) NOT NULL
) CHARACTER SET utf8mb4 COMMENT='日志表';
CREATE TABLE IF NOT EXISTS `evaluation_criteria` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64) NOT NULL,
    `name_en` VARCHAR(64),
    `user_id` INT NOT NULL,
    `desc` VARCHAR(64),
    `desc_en` VARCHAR(64),
    `system_data` BOOL NOT NULL  DEFAULT 0,
    `criteria` JSON,
    `company_id` INT NOT NULL  DEFAULT 1,
    UNIQUE KEY `uid_evaluation__invalid_8be362` (`invalid`, `name`, `user_id`, `company_id`)
) CHARACTER SET utf8mb4 COMMENT='评价准则';
CREATE TABLE IF NOT EXISTS `casbin_rule` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `ptype` VARCHAR(255) NOT NULL,
    `v0` VARCHAR(255),
    `v1` VARCHAR(255),
    `v2` VARCHAR(255),
    `v3` VARCHAR(255),
    `v4` VARCHAR(255),
    `v5` VARCHAR(255)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `controllers` (
    `created_at` DATETIME(6)   COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `invalid` INT NOT NULL  COMMENT '逻辑删除:0=未删除,id=删除' DEFAULT 0,
    `name` VARCHAR(64),
    `user_id` INT NOT NULL,
    `parent_id` INT NOT NULL  DEFAULT 0,
    `desc` VARCHAR(64),
    `company_id` INT NOT NULL  DEFAULT 1,
    `type` VARCHAR(64) NOT NULL,
    `version` VARCHAR(30),
    `setup_file_name` VARCHAR(60),
    `config_file_name` VARCHAR(60),
    `data_flow_file_name` VARCHAR(64),
    UNIQUE KEY `uid_controllers_invalid_345ab3` (`invalid`, `company_id`, `id`)
) CHARACTER SET utf8mb4 COMMENT='车辆控制系统表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
