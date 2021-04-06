--
-- Database: `samplevideo_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE IF NOT EXISTS user_details (
  username varchar(255) DEFAULT NULL,
  first_name varchar(50) DEFAULT NULL,
  last_name varchar(50) DEFAULT NULL,
  pass varchar(50) DEFAULT NULL
);

--
-- Dumping data for table `user_details`
--

INSERT INTO user_details (username, first_name, last_name, pass) VALUES
('rogers63', 'david', 'john', 'e6a33eee180b07e563d74fee8c2c66b8');
