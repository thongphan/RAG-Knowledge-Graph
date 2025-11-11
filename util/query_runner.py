class QueryRunner:
    def __init__(self, kg):
        self.kg = kg
        self.actions = {
            1: ("Count total nodes", self.count_nodes),
            2: ("List all healthcare providers", self.list_providers),
            3: ("List all specializations", self.list_specializations),
            4: ("List all locations", self.list_locations),
            5: ("List patients treated by a specific provider", self.list_patients_by_provider),
        }

    def execute_query(self, query: str, params=None):
        """Wrapper to execute Cypher query with exception handling"""
        try:
            return self.kg.query(query, params)
        except Exception as e:
            print(f"⚠️ Error executing query: {e}")
            return []

    # === Query Methods ===
    def count_nodes(self):
        query = "MATCH (n) RETURN count(n) AS numberOfNodes"
        result = self.execute_query(query)
        if result:
            print(f"There are {result[0]['numberOfNodes']} nodes in the database.")

    def list_providers(self):
        query = "MATCH (n:HealthcareProvider) RETURN n.name AS name"
        self._print_list_result(query, "Healthcare Providers")

    def list_specializations(self):
        query = "MATCH (n:Specialization) RETURN n.name AS name"
        self._print_list_result(query, "Specializations")

    def list_locations(self):
        query = "MATCH (n:Location) RETURN n.name AS name"
        self._print_list_result(query, "Locations")

    def list_patients_by_provider(self):
        query = """
            MATCH (h:HealthcareProvider {name:'Dr. John Smith'})-[:TREATS]->(p:Patient)
            RETURN p.name AS name
        """
        self._print_list_result(query, "Patients treated by")

    # === Helper ===
    def _print_list_result(self, query, title):
        result = self.execute_query(query)
        self._print_result(result, title)

    def _print_result(self, result, title):
        print(f"\n--- {title} ---")
        if not result:
            print("No data found.")
        else:
            for r in result:
                print(f"- {r['name']}")
        print()

# === Main Loop ===
    def run(self):
        while True:
            print("\n=== Healthcare Knowledge Graph Menu ===")
            for key, (desc, _) in self.actions.items():
                print(f"{key}. {desc}")
            print("C. Exit")

            choice = input("Enter a number from 1 to 5 (or C to exit): ").strip().upper()

            if choice == "C":
                print("👋 Exiting program.")
                break

            if choice.isdigit():
                choice = int(choice)
                action = self.actions.get(choice)
                if action:
                    print(f"\n➡️ Running: {action[0]}")
                    action[1]()  # Call the function
                else:
                    print("⚠️ Please enter a number between 1 and 5.")
            else:
                print("⚠️ Invalid input. Please enter 1–5 or C to exit.")