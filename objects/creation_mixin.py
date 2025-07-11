class CreationMixin:
    def create_day(self, path):
        self.change_value(
            {
                "Activites": {},
                "Repas": {},
                "Transports": {},
                "Hebergements": {}
            },
            path
        )

    def create_place(self, name, days_number):
        self.change_value(
            {},
            [name]
        )
        for i in range(days_number):
            self.create_day([name, f"Jour {i + 1}"])
        for occupation in ["Activites", "Hebergements"]:
            self.change_value(
                {},
                [name] + [occupation]
            )
