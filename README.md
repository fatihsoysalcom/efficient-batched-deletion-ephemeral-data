# Efficient Batched Deletion Ephemeral Data

This example demonstrates how to safely delete large volumes of ephemeral (short-lived) data from a database without causing performance issues. It simulates a scenario with expired "status" records, similar to WhatsApp statuses, and uses a batched deletion strategy to remove them incrementally. This approach prevents database overload by breaking down a massive delete operation into smaller, manageable transactions.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [WhatsApp Durumlarını Veritabanınızı Çökertmeden Nasıl Siliyorsunuz? Büyük Veri Silme Stratejileri](https://fatihsoysal.com/blog/whatsapp-durumlarini-veritabaninizi-cokertmeden-nasil-siliyorsunuz-buyuk-veri-silme-stratejileri/).

## License

MIT — see [LICENSE](LICENSE).
