#pragma  once

#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <functional>

// Message types enum
//là kiểu liệt kê. Nó cho phép định nghĩa một tập hợp các hằng số có tên
enum class MessageType {
  CONNECTION_INIT,
  SENSOR_DATA,
  SENSOR_ALERT,
  VOICE_COMMAND,
  VOICE_TRANSCRIPTION,
  AI_RESPONSE,
  ACTUATOR_COMMAND,
  BEHAVIOR_UPDATE,
  EMOTION_UPDATE,
  HEARTBEAT,
  STATUS_UPDATE,
  ERROR_MSG,
  ACK
};

// Connection types enum
enum class ConnectionType {
  ESP32_TYPE,
  LAPTOP_AI,
  WEB_CLIENT,
  MOBILE
};

// Alert levels
enum class AlertLevel {
  NORMAL,
  WARNING,
  DANGER,
  CRITICAL
};

// Callback function types
// std::function là một lớp mẫu trong C++ cung cấp một cách để lưu trữ, truyền và gọi các hàm, bao gồm cả các hàm lambda, các con trỏ hàm, và các đối tượng hàm (functors).
//using là một cách để định nghĩa các kiểu dữ liệu mới dựa trên các kiểu dữ liệu hiện có, giúp mã nguồn trở nên dễ đọc và dễ bảo trì hơn. có nghĩa là thay tên cũ bằng tên mới, chức năng giống nhau, chỉ khác tên
using OnConnectCallback = std::function<void()>;
using OnDisconnectCallback = std::function<void()>;
using OnMessageCallback = std::function<void(const JsonDocument&)>;
using OnErrorCallback = std::function<void(const String&)>;
using OnActuatorCommandCallback = std::function<void(const JsonDocument&)>;

class WebSocketClient {
private:
  // Đối tượng WebSocket
  WebSocketsClient webSocket;
  
  // Cấu hình
  String wsServer;
  uint16_t wsPort;
  String robotId;
  String connectionId;
  
  // Trạng thái kết nối
  bool isConnected;
  unsigned long lastHeartbeat;
  unsigned long lastReconnectAttempt;
  uint16_t reconnectInterval;
  uint16_t heartbeatInterval;
  
  // Các hàm callback
                                                                // Ví dụ sử dụng std::function:
                                                                // std::function<void()> f;   // Khai báo một std::function<void()>
                                                                //   f = hello;                 // Gán hàm hello vào f
                                                                //   f();                       // Gọi hàm qua f -> in "Hello World"

                                                                //   // Gán lambda cũng được
                                                                //   f = []() { cout << "Xin chào!\n"; };
                                                                //   f(); // In "Xin chào!"
  OnConnectCallback onConnect;
  OnDisconnectCallback onDisconnect;
  OnMessageCallback onMessage;
  OnErrorCallback onError;
  OnActuatorCommandCallback onActuatorCommand;
  
  // Các hàm hỗ trợ
  String messageTypeToString(MessageType type) const;                 // Chuyển kiểu MessageType sang chuỗi
  MessageType stringToMessageType(const char* typeStr) const;         // Chuyển chuỗi sang kiểu MessageType
  String connectionTypeToString(ConnectionType type) const;           // Chuyển kiểu ConnectionType sang chuỗi
  String alertLevelToString(AlertLevel level) const;                  // Chuyển mức cảnh báo sang chuỗi
  AlertLevel getAlertLevel(const char* sensorType, float value) const;// Xác định mức cảnh báo dựa trên loại cảm biến và giá trị
  String generateUUID() const;                                        // Sinh UUID ngẫu nhiên
  unsigned long getCurrentTimestamp() const;                          // Lấy timestamp hiện tại
  
  // Xử lý các loại tin nhắn
  void handleConnectionAck(const JsonDocument& doc);                  // Xử lý phản hồi xác nhận kết nối
  void handleActuatorCommandMessage(const JsonDocument& doc);         // Xử lý lệnh điều khiển từ server
  void handleAIResponse(const JsonDocument& doc);                     // Xử lý phản hồi từ AI
  
  // Hàm callback tĩnh dùng cho thư viện WebSocket
  static void webSocketEventWrapper(WStype_t type, uint8_t* payload, size_t length);
  static WebSocketClient* instance;                                   // Con trỏ tĩnh đến thể hiện của lớp
  
  void handleWebSocketEvent(WStype_t type, uint8_t* payload, size_t length); // Xử lý sự kiện WebSocket

public:
  // Hàm khởi tạo
  WebSocketClient(const String& server, uint16_t port, const String& robotId);
  
  // Hàm huỷ
  ~WebSocketClient();
  
  // Quản lý kết nối
  void connect();                     // Kết nối đến server
  void disconnect();                  // Ngắt kết nối
  void update();                      // Cập nhật trạng thái WebSocket
  bool isConnectedToServer() const;   // Kiểm tra trạng thái kết nối với server
  
  // Thiết lập callback
  void setOnConnect(OnConnectCallback callback);                      // Thiết lập callback khi kết nối
  void setOnDisconnect(OnDisconnectCallback callback);                // Thiết lập callback khi ngắt kết nối
  void setOnMessage(OnMessageCallback callback);                      // Thiết lập callback khi nhận tin nhắn
  void setOnError(OnErrorCallback callback);                          // Thiết lập callback khi có lỗi
  void setOnActuatorCommand(OnActuatorCommandCallback callback);      // Thiết lập callback khi nhận lệnh điều khiển
  
  // Thiết lập cấu hình
  void setReconnectInterval(uint16_t interval);                       // Đặt khoảng thời gian thử kết nối lại
  void setHeartbeatInterval(uint16_t interval);                       // Đặt khoảng thời gian gửi heartbeat
  
  // Gửi tin nhắn
  void sendMessage(MessageType type, const char* target = nullptr);   // Gửi tin nhắn loại cụ thể
  void sendSensorData(const char* sensorType, float value, 
                      const char* unit, AlertLevel alertLevel);       // Gửi dữ liệu cảm biến
  void sendAcknowledgment(const String& messageId);                   // Gửi xác nhận đã nhận tin nhắn
  void sendError(const String& errorMessage);                         // Gửi thông báo lỗi
  void sendHeartbeat();                                               // Gửi heartbeat để duy trì kết nối
  
  // Các hàm getter
  String getConnectionId() const;                                     // Lấy ID kết nối hiện tại
  String getRobotId() const;                                          // Lấy ID robot
};
