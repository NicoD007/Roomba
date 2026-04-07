from Core.CleaningModule import CleaningModule

from paho.mqtt import client as mqtt


class MQTTClient:
    "Represents the MQTT client used for robot communication."

    def __init__(
        self,
        userId: str,
        brokerAddress: str,
        port: int,
        topicCommand: str,
        topicStatus: str,
        isConnected: bool,
        cleaningModule: CleaningModule | None = None,
    ) -> None:
        self._user_id = userId
        self._broker_address = brokerAddress
        self._port = port
        self._topic_command = topicCommand
        self._topic_status = topicStatus
        self._is_connected = isConnected
        self._cleaning_module = cleaningModule
        self._client = mqtt.Client(client_id=str(userId))
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    def connect(self) -> bool:
        try:
            self._client.connect(self._broker_address, self._port, 60)
            self._client.loop_start()
            self.subscribe(self._topic_command)
            self._is_connected = True
            return True
        except Exception:
            self._is_connected = False
            return False

    def disconnect(self) -> None:
        if self._is_connected:
            self._client.loop_stop()
            self._client.disconnect()
            self._is_connected = False

    def subscribe(self, topic: str) -> bool:
        if not self._is_connected:
            return False

        result, _ = self._client.subscribe(topic)
        return result == mqtt.MQTT_ERR_SUCCESS

    def publish(self, topic: str, message: str) -> bool:
        if not self._is_connected:
            return False

        result = self._client.publish(topic, message)
        return result.rc == mqtt.MQTT_ERR_SUCCESS

    def handleCommand(self, command: str) -> None:
        normalized_command = command.strip().lower()

        if normalized_command == "start" and self._cleaning_module is not None:
            started = self._cleaning_module.startCleaning()
            self.publish(self._topic_status, "started" if started else "start_failed")
        elif normalized_command == "stop" and self._cleaning_module is not None:
            stopped = self._cleaning_module.stop()
            self.publish(self._topic_status, "stopped" if stopped else "stop_failed")

    def _on_connect(self, client, userdata, flags, rc, properties=None) -> None:
        self._is_connected = rc == 0
        if self._is_connected:
            self._client.subscribe(self._topic_command)
            self.publish(self._topic_status, "connected")

    def _on_message(self, client, userdata, message) -> None:
        payload = message.payload.decode("utf-8", errors="ignore")
        if message.topic == self._topic_command:
            self.handleCommand(payload)