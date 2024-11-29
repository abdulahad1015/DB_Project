-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 29, 2024 at 10:58 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `factory_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `contractor`
--

CREATE TABLE `contractor` (
  `contractor_id` int(11) NOT NULL,
  `contractor_name` varchar(100) NOT NULL,
  `contract_start_date` date DEFAULT NULL,
  `contract_end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `finished_goods`
--

CREATE TABLE `finished_goods` (
  `finished_goods_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_produced` int(11) NOT NULL,
  `warehouse_id` int(11) NOT NULL,
  `date_stored` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `material_collection`
--

CREATE TABLE `material_collection` (
  `collection_id` int(11) NOT NULL,
  `supervisor_id` int(11) NOT NULL,
  `raw_material_id` int(11) NOT NULL,
  `quantity_collected` int(11) NOT NULL,
  `collection_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `category`, `description`) VALUES
(1, 'Lomo 7w', 'Bulbs', 'T bulb');

-- --------------------------------------------------------

--
-- Table structure for table `production_line`
--

CREATE TABLE `production_line` (
  `production_line_id` int(11) NOT NULL,
  `line_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `production_order`
--

CREATE TABLE `production_order` (
  `order_id` int(11) NOT NULL,
  `contractor_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_ordered` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `production_line_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `production_report`
--

CREATE TABLE `production_report` (
  `report_id` int(11) NOT NULL,
  `supervisor_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_produced` int(11) NOT NULL,
  `quantity_faulty` int(11) DEFAULT NULL,
  `parts_issued` text DEFAULT NULL,
  `report_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_raw_material`
--

CREATE TABLE `product_raw_material` (
  `product_id` int(11) NOT NULL,
  `raw_material_id` int(11) NOT NULL,
  `quantity_required` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `raw_material`
--

CREATE TABLE `raw_material` (
  `raw_material_id` int(11) NOT NULL,
  `material_name` varchar(100) NOT NULL,
  `supplier` varchar(100) DEFAULT NULL,
  `quantity_in_stock` int(11) NOT NULL,
  `import_date` date DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT 0,
  `semi_finish` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `raw_material`
--

INSERT INTO `raw_material` (`raw_material_id`, `material_name`, `supplier`, `quantity_in_stock`, `import_date`, `imported`, `semi_finish`) VALUES
(1, '7W ', 'china', 15000, '2024-11-26', 1, 0),
(2, '7W ', 'china', 16531, '2024-11-19', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `supervisor`
--

CREATE TABLE `supervisor` (
  `supervisor_id` int(11) NOT NULL,
  `supervisor_name` varchar(100) NOT NULL,
  `contact_info` varchar(100) DEFAULT NULL,
  `contractor_id` int(11) DEFAULT NULL,
  `assigned_line` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`) VALUES
(1, 'abdulahad1015', 'abdulahad1015@gmail.com', '$2b$12$i5p4MPW/Jpr.ITNHhotwveWWqGLNPe8cHhpF8.Y4wYlSgBq8x4DKO'),
(4, 'abd18', 'abdullahBinKohli18@gmail.com', '$2b$12$NfGirldNdWrzoLCXbxhH/euDRzA2CQjhHLYNyx3zCqNYmIQ4jceei'),
(5, 'obaid18', 'obaidirfan18@gmail.com', '$2b$12$yzBl54wOGTO/LT3SrBq3tuG4HhCnz1TRb6k30WZXAkc4AJyXl4E0S');

-- --------------------------------------------------------

--
-- Table structure for table `warehouse`
--

CREATE TABLE `warehouse` (
  `warehouse_id` int(11) NOT NULL,
  `warehouse_type` varchar(50) DEFAULT NULL CHECK (`warehouse_type` in ('Raw Material','Finished Goods')),
  `warehouse_location` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contractor`
--
ALTER TABLE `contractor`
  ADD PRIMARY KEY (`contractor_id`);

--
-- Indexes for table `finished_goods`
--
ALTER TABLE `finished_goods`
  ADD PRIMARY KEY (`finished_goods_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `warehouse_id` (`warehouse_id`);

--
-- Indexes for table `material_collection`
--
ALTER TABLE `material_collection`
  ADD PRIMARY KEY (`collection_id`),
  ADD KEY `supervisor_id` (`supervisor_id`),
  ADD KEY `raw_material_id` (`raw_material_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `production_line`
--
ALTER TABLE `production_line`
  ADD PRIMARY KEY (`production_line_id`);

--
-- Indexes for table `production_order`
--
ALTER TABLE `production_order`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `contractor_id` (`contractor_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `production_line_id` (`production_line_id`);

--
-- Indexes for table `production_report`
--
ALTER TABLE `production_report`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `supervisor_id` (`supervisor_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `product_raw_material`
--
ALTER TABLE `product_raw_material`
  ADD PRIMARY KEY (`product_id`,`raw_material_id`),
  ADD KEY `raw_material_id` (`raw_material_id`);

--
-- Indexes for table `raw_material`
--
ALTER TABLE `raw_material`
  ADD PRIMARY KEY (`raw_material_id`);

--
-- Indexes for table `supervisor`
--
ALTER TABLE `supervisor`
  ADD PRIMARY KEY (`supervisor_id`),
  ADD KEY `contractor_id` (`contractor_id`),
  ADD KEY `assigned_line` (`assigned_line`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `warehouse`
--
ALTER TABLE `warehouse`
  ADD PRIMARY KEY (`warehouse_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `raw_material`
--
ALTER TABLE `raw_material`
  MODIFY `raw_material_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `finished_goods`
--
ALTER TABLE `finished_goods`
  ADD CONSTRAINT `finished_goods_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  ADD CONSTRAINT `finished_goods_ibfk_2` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`warehouse_id`);

--
-- Constraints for table `material_collection`
--
ALTER TABLE `material_collection`
  ADD CONSTRAINT `material_collection_ibfk_1` FOREIGN KEY (`supervisor_id`) REFERENCES `supervisor` (`supervisor_id`),
  ADD CONSTRAINT `material_collection_ibfk_2` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material` (`raw_material_id`);

--
-- Constraints for table `production_order`
--
ALTER TABLE `production_order`
  ADD CONSTRAINT `production_order_ibfk_1` FOREIGN KEY (`contractor_id`) REFERENCES `contractor` (`contractor_id`),
  ADD CONSTRAINT `production_order_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  ADD CONSTRAINT `production_order_ibfk_3` FOREIGN KEY (`production_line_id`) REFERENCES `production_line` (`production_line_id`);

--
-- Constraints for table `production_report`
--
ALTER TABLE `production_report`
  ADD CONSTRAINT `production_report_ibfk_1` FOREIGN KEY (`supervisor_id`) REFERENCES `supervisor` (`supervisor_id`),
  ADD CONSTRAINT `production_report_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Constraints for table `product_raw_material`
--
ALTER TABLE `product_raw_material`
  ADD CONSTRAINT `product_raw_material_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_raw_material_ibfk_2` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material` (`raw_material_id`) ON DELETE CASCADE;

--
-- Constraints for table `supervisor`
--
ALTER TABLE `supervisor`
  ADD CONSTRAINT `supervisor_ibfk_1` FOREIGN KEY (`contractor_id`) REFERENCES `contractor` (`contractor_id`),
  ADD CONSTRAINT `supervisor_ibfk_2` FOREIGN KEY (`assigned_line`) REFERENCES `production_line` (`production_line_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
