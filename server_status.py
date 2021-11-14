"""server_status makes an mqtt connection to the server and sends machine statistics messages."""

from app.mqtt import connect_mqtt, send_statistics

client = connect_mqtt()
client.loop_start()
send_statistics(client)
