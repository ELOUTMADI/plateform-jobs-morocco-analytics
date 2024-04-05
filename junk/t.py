for i in range(5):
    try:
        if i == 2:
            raise Exception("Simulated error")
    except Exception as e:
        print(f"Handling exception for i={i}: {e}")
        continue  # Skips the rest of the loop body for this iteration
    print(f"Processing i={i}")
