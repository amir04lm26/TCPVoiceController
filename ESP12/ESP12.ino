// Include the library:
#include <LiquidCrystal.h>
#include <ESP8266WiFi.h>

#ifndef Config
// WIFI
#define STASSID "Am_H_M"
#define STAPSK  "00@99$00&99"
#define Port 8085
// Consumers
#define r1 4
#define r2 15
#endif

String number = "989398671414";
const char* ssid = STASSID;
const char* password = STAPSK;

WiFiServer server(Port);  
int reconnected = 0, registered = 0;
int wifiReceived = 0, received = 0;
int R1State = 0, R2State = 0;
int ok = 0;
String firstLine = "", SMS_Data = "";
//int SMS_Once = 0, SMS_Remain = 0, SMS_Counter = 0;

// Create an LCD object. Parameters: (RS, E, D4, D5, D6, D7):
LiquidCrystal lcd = LiquidCrystal(2, 5, 13, 12, 14, 16);

// the setup function runs once when you press reset or power the board
void setup() {
  pinMode(r1, OUTPUT);           // set pin to output
  digitalWrite(r1, LOW);        // set default state
  pinMode(r2, OUTPUT);           // set pin to output
  digitalWrite(r2, LOW);        // set default state
  
  // Specify the LCD's number of columns and rows. Change to (20, 4) for a 20x4 LCD:
  lcd.begin(16, 2);
  
  Serial.begin(9600);

  lcd.clear();
  lcd.setCursor(1, 0);
  lcd.print("registering");
  delay(500);
  while(registered == 0){
    // Init module
    //Serial.println("AT");
    Serial.println("AT+CSQ");
    delay(20);
    String res = "";
    while(Serial.available()>0){
      res += Serial.readStringUntil('\n');
    }
    lcd.setCursor(12, 0);
    lcd.print(".");
    int index = res.indexOf("+CSQ:");
    if(index != -1){
      lcd.setCursor(13, 0);
      lcd.print(".");
      int check = res.charAt(index + 6);
      if(isDigit(check)){
        lcd.setCursor(14, 0);
        lcd.print(".");
        String temp = "";
        temp = (char)check;
        if(temp.toInt() > 0){
          lcd.clear();
          lcd.setCursor(3, 0);
          lcd.print("registered");
          
          // Enable Text Mode
          ok = 0;
          while(ok == 0){
            Serial.println("AT+CMGF=1");
            while(Serial.available()>0){
              res += Serial.readStringUntil('\n');
            }
            index = res.indexOf("OK");
            if(index != -1){
              ok = 1;
              lcd.setCursor(6, 1);
              lcd.print(".");
            }else{
              delay(70);
            }
          }

          // Send Status SMS
          ok = 0;
          while(ok == 0){
            Serial.println("AT+CMGS=\"" + number + "\"");
            //Serial.println("AT+CMGS=\"989398671414\"");
            while(Serial.available()>0){
              res += Serial.readStringUntil('\n');
            }
            index = res.indexOf("ERROR");
            //delay(20);
            if(index == -1){
              lcd.setCursor(8, 1);
              lcd.print(".");
              // Set sms message
              delay(500);
              Serial.print("Registed on netword");
              Serial.write(26);Serial.write(26);
              lcd.setCursor(10, 1);
              lcd.print(".");
              ok = 1;
              registered = 1;
            }else{
              delay(70);
            }
          }
        }
      }
    }
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Connecting...");
    reconnected = 1;
    delay(500);
  }

  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("Connected");
  delay(2000);
}

void loop() 
{
  // Connect to wifi if not connected
  while (WiFi.status() != WL_CONNECTED) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Reconnecting...");
    delay(500);

    if (WiFi.status() == WL_CONNECTED){
      lcd.clear();
      lcd.setCursor(3, 0);
      lcd.print("Connected");
      reconnected = 1;
      delay(1000);
    }
  }

  // Start the TCP server
  if (reconnected == 1) {
    // Start the server
    server.begin();
    lcd.clear();
    lcd.setCursor(1, 0);
    lcd.print("Server Started");
    delay(1000);
    // Show ip address
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(WiFi.localIP().toString());
    firstLine = WiFi.localIP().toString();
    //lcd.setCursor(0, 1);
    //lcd.print(":" + String(Port));
    // Show consumers state
    SetConsumer(R1State, R2State);
    // Reset state
    reconnected = 0;
  }

  // Handle SMS
  SMS_Handler();
  
  // Check if a client has connected
  WiFiClient client = server.available(); 
  if (!client) {
    delay(200);
    return;
  }

  /*lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("new client");*/
  firstLine = "   new client";
  SetConsumer(R1State, R2State);

  client.print("AIHOME");
  while(client){
    // Handle Client
    String req = "";
    if(client.available()>0){
      req += (char)client.read();
      wifiReceived = 1;
    }
    if(wifiReceived){
      int index = req.indexOf("VC");
      if(index != -1 && req.length() > index+4){
        if((req.charAt(index + 2) == 'L' || req.charAt(index + 2) == 'F') && (req.charAt(index + 3) == 'O' || req.charAt(index + 3) == 'F')){
          if(req.charAt(index + 2) == 'L'){
            if(req.charAt(index + 3) == 'O') R1State = 1;
            else R1State = 0;
          }else{
            if(req.charAt(index + 3) == 'O') R2State = 1;
            else R2State = 0;
          }
          SetConsumer(R1State, R2State);
          client.print("VCOKVC");
          client.flush();
          //SMS_Send("Lamp: " + String(R1State) + "\r\nFan: " + String(R2State));
          /*if(!SMS_Remain){
            SMS_Data = "Lamp: " + String(R1State) + "\r\nFan: " + String(R2State);
            SMS_Remain = 1;
          }*/
        }
        else{
          client.print("VCFLVC");
          client.flush();
        }
      }else{
        client.print("VCFLVC");
        client.flush();
      }
      // Handle SMS
      SMS_Handler();
      wifiReceived = 0;
    }
    //wifiReceived = 0;
   }
    
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(WiFi.localIP());
  firstLine = WiFi.localIP().toString();
  // Show consumers state
  SetConsumer(R1State, R2State);
}

void SetConsumer(int r1State, int r2State){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(firstLine);
  if(r1State == 0){
    digitalWrite(r1, LOW);
    lcd.setCursor(0, 1);
    lcd.print("R1:off");
  }else if(r1State == 1){
    digitalWrite(r1, HIGH);
    lcd.setCursor(0, 1);
    lcd.print("R1:on");
  }
  if(r2State == 0){
    digitalWrite(r2, LOW);
    lcd.setCursor(8, 1);
    lcd.print("R2:off");
  }else if(r2State == 1){
    digitalWrite(r2, HIGH);
    lcd.setCursor(8, 1);
    lcd.print("R2:on");
  }
}

void SMS_Handler(void){
  String req = "";
  while(Serial.available()>0){
      req += Serial.readStringUntil('\n');
      received = 1;
  }
  if(received){
    int index = 0;
    index = req.indexOf("\"SM\",");
    int last = req.length();
    //int endIndex = req.indexOf("\n", index + 5);
    if(index != -1){
      String temp = "";
      index = index + 5;
      while(index <= last){
        int check = req.charAt(index);
        if(isDigit(check)){
          temp += (char)check;
          index++;
        }else{
          break;
        }
      }
      //int smsIndex = temp.toInt();
      // Send request to receive the sms message
      Serial.print("AT+CMGR=");
      Serial.println(temp);
      /*delay(10);
      while(Serial.available()>0){
        req += Serial.readStringUntil('\n');
      }*/
    }
    index = req.indexOf("+CMGR:");
    if(index != -1){
      int snd = 0;
      index = req.indexOf("lamp:");
      if(index != -1){
        int chr = req.charAt(index + 5);
        if(chr == '0' || chr == '1'){
          if(chr == '0') R1State = 0;
          else R1State = 1;
          snd = 1;
        }
      }
      index = req.indexOf("fan:");
      if(index != -1){
        int chr = req.charAt(index + 4);
        if(chr == '0' || chr == '1'){
          if(chr == '0') R2State = 0;
          else R2State = 1;
          snd = 1;
        }
      }
      index = req.indexOf("get");
      if(index != -1){
        snd = 1;
      }
      // Show consumers state
      SetConsumer(R1State, R2State);
      if(snd){
        //SMS_Send("Lamp: " + String(R1State) + "\r\nFan: " + String(R2State));
        /*if(!SMS_Remain){
          SMS_Data = "Lamp: " + String(R1State) + "\r\nFan: " + String(R2State);
          SMS_Remain = 1;
        }*/
        snd = 0;
      }
    }
    received = 0;
  }
}
