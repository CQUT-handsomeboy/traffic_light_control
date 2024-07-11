#include <WiFi.h>

#define USE_UDP

#ifdef USE_MQTT
#define MQTT_SERVER "192.168.14.159"
#define MQTT_PORT 1883
#include <ArduinoMqttClient.h>
#endif

#ifdef USE_UDP
#include <WiFiUdp.h>
#define UDP_SERVER "192.168.14.159"
#define UDP_SERVER_PORT 159
char buf[64];
#define UDP_LOCAL_PORT 159

WiFiUDP udp;
#endif

#include <ArduinoJson.h>

typedef enum LED_INDEX
{
  LEFT,MIDDLE,RIGHT,INDEX_NONE
} LED_INDEX;

typedef enum LED_COLOR
{
  RED,GREEN,COLOR_NONE
} LED_COLOR;

#define LEFT_GREEN_N 1
#define LEFT_RED_N 2
#define LEFT_P 3

#define MIDDLE_RED_N 4
#define MIDDLE_GREEN_N 5
#define MIDDLE_P 6

#define RIGHT_GREEN_N 7
#define RIGHT_RED_N 26
#define RIGHT_P 48

#define WIFI_SSID "cxs"
#define WIFI_PASSWORD "@12345678"

#ifdef USE_MQTT
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
#endif

void led_init()
{
  pinMode(LEFT_GREEN_N,OUTPUT);
  digitalWrite(LEFT_GREEN_N,LOW);
  
  pinMode(LEFT_RED_N,OUTPUT);
  digitalWrite(LEFT_RED_N,LOW);

  pinMode(LEFT_P,OUTPUT);
  digitalWrite(LEFT_P,LOW);



  pinMode(MIDDLE_RED_N,OUTPUT);
  digitalWrite(MIDDLE_RED_N,LOW);

  pinMode(MIDDLE_GREEN_N,OUTPUT);
  digitalWrite(MIDDLE_GREEN_N,LOW);

  pinMode(MIDDLE_P,OUTPUT);
  digitalWrite(MIDDLE_P,LOW);

  

  pinMode(RIGHT_GREEN_N,OUTPUT);
  digitalWrite(RIGHT_GREEN_N,LOW);

  pinMode(RIGHT_RED_N,OUTPUT);
  digitalWrite(RIGHT_RED_N,LOW);

  pinMode(RIGHT_P,OUTPUT);
  digitalWrite(RIGHT_P,LOW);
}

void wifi_init()
{
  // 连接WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi连接成功");
  Serial.print("IP地址: ");
  Serial.println(WiFi.localIP());
}

void publishTask(void* parameter)
{
  Serial.println("TEST TASK");
  delay(1000);
}

void otherTask(void* parameter)
{
  Serial.println("OTHER TASK");
  delay(2000);
}

void setup() {
  Serial.begin(115200);
  
#if 1
  led_init();
  wifi_init();
#endif

#ifdef USE_MQTT
  mqtt_init();
#endif

#ifdef USE_UDP
  udp.begin(UDP_LOCAL_PORT);
#endif

}

void left_off()
{
  digitalWrite(LEFT_RED_N,LOW);// 禁用红灯
  digitalWrite(LEFT_GREEN_N,LOW);// 禁用绿灯
  digitalWrite(LEFT_P,LOW); // 最后一步
}

void left_green_on()
{
  digitalWrite(LEFT_RED_N,HIGH);// 禁用红灯
  digitalWrite(LEFT_GREEN_N,LOW);// 启用绿灯
  digitalWrite(LEFT_P,HIGH); // 最后一步
}

void left_red_on()
{
  digitalWrite(LEFT_GREEN_N,HIGH);// 禁用绿灯
  digitalWrite(LEFT_RED_N,LOW);// 启用红灯
  digitalWrite(LEFT_P,HIGH); // 最后一步
}

void right_off()
{
  digitalWrite(RIGHT_RED_N,LOW);// 禁用红灯
  digitalWrite(RIGHT_GREEN_N,LOW);// 禁用绿灯
  digitalWrite(RIGHT_P,LOW); // 最后一步
}

void right_green_on()
{
  digitalWrite(RIGHT_RED_N,HIGH);// 禁用红灯
  digitalWrite(RIGHT_GREEN_N,LOW);// 启用绿灯
  digitalWrite(RIGHT_P,HIGH); // 最后一步
}

void right_red_on()
{
  digitalWrite(RIGHT_GREEN_N,HIGH);// 禁用绿灯
  digitalWrite(RIGHT_RED_N,LOW);// 启用红灯
  digitalWrite(RIGHT_P,HIGH); // 最后一步
}

void middle_off()
{
  digitalWrite(MIDDLE_RED_N,LOW);// 禁用红灯
  digitalWrite(MIDDLE_GREEN_N,LOW);// 禁用绿灯
  digitalWrite(MIDDLE_P,LOW); // 最后一步
}

void middle_green_on()
{
  digitalWrite(MIDDLE_RED_N,HIGH);// 禁用红灯
  digitalWrite(MIDDLE_GREEN_N,LOW);// 启用绿灯
  digitalWrite(MIDDLE_P,HIGH); // 最后一步
}

void middle_red_on()
{
  digitalWrite(MIDDLE_GREEN_N,HIGH);// 禁用绿灯
  digitalWrite(MIDDLE_RED_N,LOW);// 启用红灯
  digitalWrite(MIDDLE_P,HIGH); // 最后一步
}

void led_test()
{
  left_red_on();delay(200);
  left_green_on();delay(200);
  left_off();delay(200);
  
  middle_red_on();delay(200);
  middle_green_on();delay(200);
  middle_off();delay(200);

  right_red_on();delay(200);
  right_green_on();delay(200);
  right_off();delay(200);  
}

void led_control(LED_INDEX led_index,LED_COLOR led_color)
{
  switch(led_index)
  {
    case LEFT:
      switch(led_color)
      {
        case RED:
          middle_off();
          right_off();
          left_red_on();
          break;
        case GREEN:
          middle_off();
          right_off();
          left_green_on();
          break;
      }
      break;
    case RIGHT:
      switch(led_color)
      {
        case RED:
          middle_off();
          left_off();
          right_red_on();
          break;
        case GREEN:
          middle_off();
          left_off();
          right_green_on();
          break;
      }
      break;
    case MIDDLE:
      switch(led_color)
      {
        case RED:
          right_off();
          left_off();
          middle_red_on();
          break;
        case GREEN:
          right_off();
          left_off();
          middle_green_on();
          break;
      }
      break;
    case INDEX_NONE:
    default:
      left_off();
      right_off();
      middle_off();
      break;
  }
}

#ifdef USE_MQTT
void onMqttMessage(int messageSize) {
  // 读取消息
  String topic = mqttClient.messageTopic();
  String payload = mqttClient.readString();
  
  LED_INDEX led_index;
  LED_COLOR led_color;

  if(!topic.compareTo("traffic_light1/control"))
  {
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if(error)
      return;

    String color_string = doc["color"];
    String index_string = doc["index"];

    led_color = (!color_string.compareTo("red")) ? RED : GREEN;
    led_index = (!index_string.compareTo("left")) ? LEFT :
    (
       (!index_string.compareTo("right")) ? RIGHT : MIDDLE
    );
    led_control(led_index,led_color);
  }
}

void mqtt_init()
{
  Serial.print("连接到MQTT服务器!");
  while (!mqttClient.connect(MQTT_SERVER, MQTT_PORT)) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("MQTT服务器连接成功！"); 
  
  mqttClient.subscribe("traffic_light1/control");
  mqttClient.onMessage(onMqttMessage);
}
#endif

#ifdef USE_UDP
void sendUdpMessage(String the_buffer)
{
  udp.beginPacket(UDP_SERVER, UDP_SERVER_PORT);
  udp.write((const uint8_t*)the_buffer.c_str(),strlen(the_buffer.c_str()));
  udp.endPacket();  
}

void handleUdpMessage()
{
  int packetSize = udp.parsePacket();
  int index,color,value;
  if(packetSize)
  {
    udp.read(buf, packetSize);
    char index_buf[16],color_buf[16];
    int value;
    sscanf(buf,"set %s %s %d;",index_buf,color_buf,&value);

//    Serial.printf("index_buf:%s\r\n",index_buf);
//    Serial.printf("color_buf:%s\r\n",color_buf);
//    Serial.printf("value:%d\r\n",value);
    
    LED_INDEX led_index;
    LED_COLOR led_color;

    if(!strcmp("red",color_buf))
      led_color = RED;
    else if(!strcmp("green",color_buf))
      led_color = GREEN;
    else 
      led_color = COLOR_NONE;

    if(!strcmp("middle",index_buf))
      led_index = MIDDLE;
    else if(!strcmp("right",index_buf))
      led_index = RIGHT;
    else if(!strcmp("left",index_buf))
      led_index = LEFT;
    else
      led_index = INDEX_NONE;
    
    
    
    led_control(led_index,led_color);
  }
}
#endif

void loop() 
{
#ifdef USE_MQTT
    mqttClient.poll();
#endif
    handleUdpMessage();
    delay(10);

}
