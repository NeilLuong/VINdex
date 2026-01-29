class VehicleNotFoundError(Exception):    
    def __init__(self, vin: str) -> None:
        self.vin = vin
        super().__init__(f"Cannot find vehicle with VIN '{vin}'")