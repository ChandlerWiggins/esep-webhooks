class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.transaction = False
        self.temp_data = {}

    def get(self, key):
        if self.transaction:
            if key in self.temp_data:
                return None  # Only return from temp_data if you decide uncommitted data should be visible as None
        if key in self.data:
            return self.data[key]
        return None

    def put(self, key, value):
        if not self.transaction:
            raise Exception("Transaction not in progress")
        self.temp_data[key] = value

    def begin_transaction(self):
        if self.transaction:
            raise Exception("Transaction already in progress")
        self.transaction = True
        self.temp_data = {}

    def commit(self):
        if not self.transaction:
            raise Exception("No transaction in progress")
        self.data.update(self.temp_data)
        self.temp_data = {}
        self.transaction = False

    def rollback(self):
        if not self.transaction:
            raise Exception("No transaction in progress")
        self.temp_data = {}
        self.transaction = False

if __name__ == "__main__":
    db = InMemoryDB()

    print("Initial get(A):", db.get("A"))  # Should print None

    try:
        db.put("A", 5)  # Should raise an error
    except Exception as e:
        print("Error (no transaction):", e)

    db.begin_transaction()
    db.put("A", 5)
    print("Get within transaction (should be None):", db.get("A"))  # Should print None
    db.put("A", 6)
    db.commit()
    print("Get after commit:", db.get("A"))  # Should print 6

    try:
        db.commit()  # Should raise an error
    except Exception as e:
        print("Error (commit without transaction):", e)

    try:
        db.rollback()  # Should raise an error
    except Exception as e:
        print("Error (rollback without transaction):", e)

    print("Get(B) before transaction:", db.get("B"))  # Should print None
    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print("Get(B) after rollback:", db.get("B"))  # Should print None


