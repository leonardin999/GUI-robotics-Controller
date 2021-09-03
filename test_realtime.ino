#include <TimerOne.h>
long v1 = 0, v2 = 0, v3 = 0 ,v4 = 0, v5 = 0, v6 = 0;

long the1_pre, the2_pre, the3_pre ,the4_pre, the5_pre, the6_pre;
long the1_flex, the2_flex, the3_flex,the4_flex, the5_flex, the6_flex;
long the1, the2, the3,the4, the5 , the6;
int a=0, b=0, c=0;

//float  tam1 =  3969  ;
//float  tam2 =289 ;
//float tam3 = tam1/tam2 ;
float   vt1 = 0 ,  vt2= 53.0, vt3=43.0 ,vt4=0 ,vt5=0 , vt6=0,delta ; 
float vtmm1,vtmm2 ,vtmm3 ,vtmm4,vtmm5,vtmm6, t_int ,tc, abc;
float z1,z2,z3,z4,z5,z6;
float a1,a2,a3,a4,a5,a6,c1,c2,c3,c4,c5,c6,b1,b2,b3,b4,b5,b6,d1,d2,d3,d4,d5,d6;
float delta1, delta2, delta3;
double gt1, gt2, gt3;
double n1, n2, n3, tp1, tp2, tp3;



void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
Serial.setTimeout(500);//ms
}
void  recieve()
  {
   int j=0,k[7];
 String symbol ;
 String readStringt;
 float y1,y2,y3,y4,y5,y6,tc;
char buffer[50]= {}; 
// while(Serial.available())
// {
  if(Serial.available()>0)
   {

     Serial.readBytes(buffer,50);// s1 is String type variable.
     String data = buffer;
    int lengthdata = data.length();
   // Serial.println(symbolw);
    for (int i=0 ; i< lengthdata ; i++ )
    {
          symbol = data.charAt(i);
          
          if( symbol.equals(",") == true )
          { 
              k[j]=i+1;
             j++;
            }
      }
      String  x1 = data.substring(0,k[0]);
      String  x2 = data.substring(k[0],k[1]);
      String  x3 = data.substring(k[1],k[2]);
      String  x4 = data.substring(k[2],k[3]);
      String  x5 = data.substring(k[3],k[4]);
      String  x6 = data.substring(k[4],k[5]);
      String  x7 = data.substring(k[5],lengthdata);
        y1=x1.toFloat();
        y2=x2.toFloat();
        y3=x3.toFloat();
        y4=x4.toFloat();
        y5=x5.toFloat();
        y6=x6.toFloat();
        tc=x7.toFloat();
      vtmm1=y1;
      vtmm2=y2;
      vtmm3=y3;
      vtmm4=y4;
      vtmm5=y5;
      vtmm6=y6;
      delta = tc/10;
    }
  }
void loop() 
{ 
  recieve();
   if(vt1<vtmm1)
   {
    vt1+=delta;
   }
   else if(vt1>vtmm1)
   {
    vt1-=delta;
   } 
   ///////////
     if(vt2<vtmm2)
   {
    vt2+=delta;
   }
   else if(vt2>vtmm2)
   {
    vt2-=delta;
   } 
      if(vt3<vtmm3)
   {
    vt3+=delta;
   }
   else if(vt3>vtmm3)
   {
    vt3-=delta;
   } 
      if(vt4<vtmm4)
   {
    vt4+=delta;
   }
   else if(vt4>vtmm4)
   {
    vt4-=delta;
   } 
      if(vt5<vtmm5)
   {
    vt5+=delta;
   }
   else if(vt5>vtmm5)
   {
    vt5-=delta;
   } 
      if(vt6<vtmm6)
   {
    vt6+=delta;
   }
   else if(vt6>vtmm6)
   {
    vt6-=delta;
   } 
  Serial.print(vt1);
  Serial.print(" ");
  Serial.print(vt2);
  Serial.print(" ");
  Serial.print(vt3);
  Serial.print(" ");
  Serial.print(vt4);
  Serial.print(" ");
  Serial.print(vt5);
  Serial.print(" ");
  Serial.println(vt6);
  delay(100);  
}
