DROP DATABASE IF EXISTS order_db;

CREATE DATABASE order_db;

USE order_db

 --- Bookkeeping ---
CREATE TABLE Customers(
	idCustomer INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(31) ,
	surname VARCHAR(63),
	email VARCHAR(127) NOT NULL UNIQUE,
	registered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Payments(
	idPayment INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	amount DECIMAL(4,2) NOT NULL,
	method ENUM('Card', 'Cash', 'Paypal', 'GooglePay', 'ApplePay', 'Link', 'Stripe', 'Other'),
	payed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	external_payment_id VARCHAR(255) UNIQUE
);

--- Data ---
CREATE TABLE Items (
	idItem INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(127) NOT NULL UNIQUE,
	description VARCHAR(511),
	price DECIMAL(3, 1) NOT NULL
);


CREATE TABLE Orders(
	idOrder INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	status ENUM ('placed', 'cancelled', 'payed', 'shipped'),
	placed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	payed_at TIMESTAMP NULL,
	shipped_at TIMESTAMP NULL,
	fk_customer INT NOT NULL,
	shipping_address VARCHAR(511) NOT NULL,
	fk_payment INT,
	FOREIGN KEY(fk_customer) REFERENCES Customers(idCustomer),
	FOREIGN KEY (fk_payment) REFERENCES Payments(idPayment)
);

CREATE TABLE order_has_item(
	fk_item INT NOT NULL,
	fk_order INT NOT NULL,
	quantity INT DEFAULT 1,
	FOREIGN KEY (fk_item) REFERENCES Items(idItem),
	FOREIGN KEY (fk_order) REFERENCES Orders(idOrder),
	PRIMARY KEY (fk_order, fk_item)
);

