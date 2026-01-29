CREATE TABLE
    IF NOT EXISTS vehicle (
        vin VARCHAR(17) PRIMARY KEY CHECK (vin = UPPER(vin)),
        manufacturer_name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        horse_power INTEGER NOT NULL CHECK (horse_power > 0),
        model_name VARCHAR(100) NOT NULL,
        model_year INTEGER NOT NULL CHECK (model_year >= 0),
        purchase_price NUMERIC(12, 2) NOT NULL CHECK (purchase_price >= 0),
        fuel_type VARCHAR(20) NOT NULL
    );