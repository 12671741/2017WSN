#include <SoftwareSerial.h>
#define TxD 3
#define RxD 4
#include <TFT.h>  // Arduino LCD library
#include <SPI.h>

// pin definition for the Uno
#define cs   10
#define dc   9
#define rst  8
int xPos = 0;
int sensor=0;
TFT TFTscreen = TFT(cs, dc, rst);
SoftwareSerial BTSerial(RxD, TxD); // Recive (RD), Transmit (TxD)
// char array to print to the screen
char sensorval[200];
char charin;
String str="";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  BTSerial.begin(115200); 

  TFTscreen.begin();
  tftinit();
  BTSerial.print("root\n");
  delay(1000);
  BTSerial.print("password\n");
}

void loop() {
  // put your main code here, to run repeatedly:
 // set the font color
 
 if(BTSerial.available()){
// erase the text you just wrote
  tftwrite(sensorval,0,0,0);
  str="";
  while (BTSerial.available()){  
      charin=BTSerial.read();
      str+=String(charin);
    }
  Serial.print(str);
  str.toCharArray(sensorval,200);
  tftwrite(sensorval,255,255,255);
  char* tem=strchr(sensorval,'\n');
  sensor=str.substring(0,tem-sensorval).toInt();
  // wait for a moment
 }
 delay(200);
 drawgraph(sensor);
}

void tftwrite(char sensorval[],int r,int g,int b){
    TFTscreen.stroke(r,b,g);
    TFTscreen.text(sensorval, 0, 5);
}
void tftinit(){
  TFTscreen.background(0, 0, 0);
  TFTscreen.stroke(255, 255, 255);
  TFTscreen.setTextSize(1);
  TFTscreen.text("heart rate", 53, 2);
  TFTscreen.text("temperature", 53, 11);
  TFTscreen.text("humidity", 53, 20);
  TFTscreen.text("bar", 53, 29);
  TFTscreen.text("liftUps", 53, 38);
  TFTscreen.text("sleepy", 53, 47);
  TFTscreen.text("Pace", 3, 70);
  TFTscreen.setTextSize(1);
}
void drawgraph(int sensor){
  sensor = map(sensor, 0, 1023, 0, TFTscreen.height()/9);
  TFTscreen.stroke(250, 180, 10);
  TFTscreen.line(xPos, TFTscreen.height() - sensor, xPos, TFTscreen.height());

  // if the graph has reached the screen edge
  // erase the screen and start again
  if (xPos >= 144) {
    xPos = 0;
    tftinit();
  } else {
    // increment the horizontal position:
    xPos++;
  }
}

