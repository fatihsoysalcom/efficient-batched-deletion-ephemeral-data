import sqlite3
import time
import datetime
import random

# In-memory SQLite database for demonstration. No external dependencies needed.
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create table for statuses, similar to WhatsApp statuses with an expiry time.
cursor.execute('''
    CREATE TABLE statuses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL,
        expires_at TIMESTAMP NOT NULL
    )
''')
conn.commit()

# --- Simulate Data Insertion ---
print("Inserting initial data...")
now = datetime.datetime.now(datetime.timezone.utc)

# Insert a large number of expired statuses (e.g., from 2 days ago, expiring 1 day ago)
# This simulates a backlog of data that needs to be cleaned up.
for i in range(50000):
    created = now - datetime.timedelta(days=2, seconds=random.randint(0, 3600))
    expires = created + datetime.timedelta(days=1) # Expired 1 day ago
    cursor.execute("INSERT INTO statuses (content, created_at, expires_at) VALUES (?, ?, ?)",
                   (f"Expired status {i}", created, expires))

# Insert some current statuses (e.g., from 1 hour ago, expiring in 23 hours)
# These should not be deleted by our cleanup process.
for i in range(20000):
    created = now - datetime.timedelta(hours=1, seconds=random.randint(0, 3600))
    expires = created + datetime.timedelta(days=1) # Expires in ~23 hours
    cursor.execute("INSERT INTO statuses (content, created_at, expires_at) VALUES (?, ?, ?)",
                   (f"Current status {i}", created, expires))

conn.commit()
print(f"Total statuses after insertion: {cursor.execute('SELECT COUNT(*) FROM statuses').fetchone()[0]}")

# --- Deletion Strategy: Batched Deletion ---
# This function demonstrates how to delete expired data in small batches
# to avoid long-running transactions and prevent database overload.
def delete_expired_statuses_batched(batch_size=1000):
    print(f"\nStarting batched deletion of expired statuses (batch size: {batch_size})...")
    total_deleted = 0
    start_time = time.time()
    
    while True:
        # Step 1: Select a small batch of IDs of expired statuses.
        # This SELECT operation is quick and doesn't lock the entire table for long.
        cursor.execute(f'''
            SELECT id FROM statuses
            WHERE expires_at < ?
            ORDER BY expires_at ASC
            LIMIT ?
        ''', (datetime.datetime.now(datetime.timezone.utc), batch_size))
        
        ids_to_delete = [row[0] for row in cursor.fetchall()]
        
        if not ids_to_delete:
            break # No more expired statuses found, exit the loop.
        
        # Step 2: Delete the selected batch of IDs.
        # This DELETE operation is also fast as it targets a specific, small set of rows.
        placeholders = ','.join('?' * len(ids_to_delete))
        cursor.execute(f"DELETE FROM statuses WHERE id IN ({placeholders})", ids_to_delete)
        conn.commit() # Commit after each batch to free up resources and reduce transaction size.
        
        deleted_in_batch = len(ids_to_delete)
        total_deleted += deleted_in_batch
        print(f"  Deleted {deleted_in_batch} statuses in a batch. Total deleted: {total_deleted}")
        
        # Optional: Add a small delay here (e.g., time.sleep(0.01)) to further reduce
        # immediate load on the database in a real-world scenario.
        
    end_time = time.time()
    print(f"Batched deletion complete. Total {total_deleted} statuses deleted in {end_time - start_time:.2f} seconds.")
    return total_deleted

# --- Run the deletion ---
delete_expired_statuses_batched(batch_size=5000) # Demonstrate with a reasonable batch size.

print(f"\nTotal statuses remaining after batched deletion: {cursor.execute('SELECT COUNT(*) FROM statuses').fetchone()[0]}")

# --- Illustrative point (DO NOT RUN ON PRODUCTION WITH BILLIONS OF ROWS!) ---
# A single large DELETE statement like below could cause significant performance issues
# (e.g., locking tables, high I/O, long transaction times) on a database with billions of rows.
# This is what the batched deletion strategy aims to prevent.
#
# def delete_all_expired_at_once():
#     print("\nAttempting single large deletion of all expired statuses...")
#     start_time = time.time()
#     cursor.execute("DELETE FROM statuses WHERE expires_at < ?", (datetime.datetime.now(datetime.timezone.utc),))
#     conn.commit()
#     end_time = time.time()
#     print(f"Single large deletion complete in {end_time - start_time:.2f} seconds.")
#     print(f"Total statuses remaining: {cursor.execute('SELECT COUNT(*) FROM statuses').fetchone()[0]}")
#
# # delete_all_expired_at_once() # Uncomment to see the conceptual alternative (use with caution).

conn.close()
