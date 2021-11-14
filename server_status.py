"""server_status makes an mqtt connection to the server and sends machine status messages."""

from app.mqtt import connect_mqtt, send_status

client = connect_mqtt()
client.loop_start()
send_status(client)
