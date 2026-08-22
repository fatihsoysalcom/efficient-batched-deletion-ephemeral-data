# efficient-batched-deletion-ephemeral-data
This example demonstrates how to safely delete large volumes of ephemeral (short-lived) data from a database without causing performance issues. It simulates a scenario with expired "status" records, similar to WhatsApp statuses, and uses a batched deletion strategy to remove them incrementally. This approach prevents database overload by breaking 
