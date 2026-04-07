class MQTTClient:
    "Represents the MQTT client used for robot communication."

    def __init__(self, userId: str, brokerAddress: str, port: int, topicCommand: str, topicStatus: str, isConnected: bool) -> None:
        self._user_id = userId
        self._broker_address = brokerAddress
        self._port = port
        self._topic_command = topicCommand
        self._topic_status = topicStatus
        self._is_connected = isConnected

    def connect(self) -> bool:
        return True #This is just placeholder

    def disconnect(self) -> None:
        pass

    def subscribe(self, topic: str) -> bool:
        return True #This is just placeholder

    def publish(self, topic: str, message: str) -> bool:
        return True #This is just placeholder

    def handleCommand(self, command: str) -> None:
        pass