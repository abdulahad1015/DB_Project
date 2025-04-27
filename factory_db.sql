SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `contractor` (
  `contractor_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `contract_start_date` date DEFAULT NULL,
  `contract_end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `contractor` (`contractor_id`, `user_id`, `contract_start_date`, `contract_end_date`) VALUES
(1, 1, NULL, NULL);

CREATE TABLE `finished_goods` (
  `finished_goods_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_produced` int(11) NOT NULL,
  `warehouse_id` int(11) NOT NULL,
  `date_stored` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `material_collection` (
  `collection_id` int(11) NOT NULL,
  `supervisor_id` int(11) NOT NULL,
  `raw_material_id` int(11) NOT NULL,
  `quantity_collected` int(11) NOT NULL,
  `collection_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `product` (`product_id`, `product_name`, `category`, `description`) VALUES
(1, 'Lomo 7W BULB', 'Bulbs', 'T bulb');

CREATE TABLE `production_line` (
  `production_line_id` int(11) NOT NULL,
  `line_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `production_line` (`production_line_id`, `line_name`) VALUES
(1, 'SMT');

CREATE TABLE `production_order` (
  `order_id` int(11) NOT NULL,
  `contractor_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_ordered` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `production_line_id` int(11) NOT NULL,
  `supervisor_id` int(11) NOT NULL,
  `status` varchar(50) DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `production_report` (
  `report_id` int(11) NOT NULL,
  `supervisor_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_produced` int(11) NOT NULL,
  `quantity_faulty` int(11) DEFAULT NULL,
  `parts_issued` text DEFAULT NULL,
  `report_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `product_raw_material` (
  `product_id` int(11) NOT NULL,
  `raw_material_id` int(11) NOT NULL,
  `quantity_required` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `product_raw_material` (`product_id`, `raw_material_id`, `quantity_required`) VALUES
(1, 1, 5);

CREATE TABLE `raw_material` (
  `raw_material_id` int(11) NOT NULL,
  `material_name` varchar(100) NOT NULL,
  `supplier` varchar(100) DEFAULT NULL,
  `quantity_in_stock` int(11) NOT NULL,
  `import_date` date DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT 0,
  `semi_finish` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `raw_material` (`raw_material_id`, `material_name`, `supplier`, `quantity_in_stock`, `import_date`, `imported`, `semi_finish`) VALUES
(1, '7W ', 'china', 15000, '2024-11-26', 1, 0);

CREATE TABLE `supervisor` (
  `supervisor_id` int(11) NOT NULL,
  `supervisor_name` varchar(100) NOT NULL,
  `contact_info` varchar(100) DEFAULT NULL,
  `contractor_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `role` varchar(50) DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `role`) VALUES
(1, 'abdulahad1015', 'abdulahad1015@gmail.com', '$2b$12$i5p4MPW/Jpr.ITNHhotwveWWqGLNPe8cHhpF8.Y4wYlSgBq8x4DKO', 'admin');

CREATE TABLE `warehouse` (
  `warehouse_id` int(11) NOT NULL,
  `warehouse_type` varchar(50) DEFAULT NULL CHECK (`warehouse_type` in ('Raw Material','Finished Goods')),
  `warehouse_location` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `warehouse` (`warehouse_id`, `warehouse_type`, `warehouse_location`) VALUES
(1, 'Finished Goods', '1st Floor');

ALTER TABLE `contractor`
  ADD PRIMARY KEY (`contractor_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

ALTER TABLE `finished_goods`
  ADD PRIMARY KEY (`finished_goods_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `warehouse_id` (`warehouse_id`);

ALTER TABLE `material_collection`
  ADD PRIMARY KEY (`collection_id`),
  ADD KEY `supervisor_id` (`supervisor_id`),
  ADD KEY `raw_material_id` (`raw_material_id`);

ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

ALTER TABLE `production_line`
  ADD PRIMARY KEY (`production_line_id`);

ALTER TABLE `production_order`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `contractor_id` (`contractor_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `production_line_id` (`production_line_id`),
  ADD KEY `production_order_ibfk_4` (`supervisor_id`);

ALTER TABLE `production_report`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `supervisor_id` (`supervisor_id`),
  ADD KEY `product_id` (`product_id`);

ALTER TABLE `product_raw_material`
  ADD PRIMARY KEY (`product_id`,`raw_material_id`),
  ADD KEY `raw_material_id` (`raw_material_id`);

ALTER TABLE `raw_material`
  ADD PRIMARY KEY (`raw_material_id`);

ALTER TABLE `supervisor`
  ADD PRIMARY KEY (`supervisor_id`),
  ADD KEY `contractor_id` (`contractor_id`);

ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `warehouse`
  ADD PRIMARY KEY (`warehouse_id`);

ALTER TABLE `contractor`
  MODIFY `contractor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `raw_material`
  MODIFY `raw_material_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `warehouse`
  MODIFY `warehouse_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `contractor`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `finished_goods`
  ADD CONSTRAINT `finished_goods_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  ADD CONSTRAINT `finished_goods_ibfk_2` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`warehouse_id`);

ALTER TABLE `material_collection`
  ADD CONSTRAINT `material_collection_ibfk_1` FOREIGN KEY (`supervisor_id`) REFERENCES `supervisor` (`supervisor_id`),
  ADD CONSTRAINT `material_collection_ibfk_2` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material` (`raw_material_id`);

ALTER TABLE `production_order`
  ADD CONSTRAINT `production_order_ibfk_1` FOREIGN KEY (`contractor_id`) REFERENCES `contractor` (`contractor_id`),
  ADD CONSTRAINT `production_order_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  ADD CONSTRAINT `production_order_ibfk_3` FOREIGN KEY (`production_line_id`) REFERENCES `production_line` (`production_line_id`),
  ADD CONSTRAINT `production_order_ibfk_4` FOREIGN KEY (`supervisor_id`) REFERENCES `supervisor` (`supervisor_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `production_report`
  ADD CONSTRAINT `production_report_ibfk_1` FOREIGN KEY (`supervisor_id`) REFERENCES `supervisor` (`supervisor_id`),
  ADD CONSTRAINT `production_report_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

ALTER TABLE `product_raw_material`
  ADD CONSTRAINT `product_raw_material_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_raw_material_ibfk_2` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material` (`raw_material_id`) ON DELETE CASCADE;

ALTER TABLE `supervisor`
  ADD CONSTRAINT `supervisor_ibfk_1` FOREIGN KEY (`contractor_id`) REFERENCES `contractor` (`contractor_id`);
COMMIT;
