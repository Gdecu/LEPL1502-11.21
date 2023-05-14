//
// Programme arduino du mastermind pour LEPL 1502
// Groupe 11.21 FSA11BA 2022-2023
//

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <string.h>
#include <Servo.h>
 
#define V_out1 A0
#define V_out2 A1 
#define V_out3 A2
#define BUTTON1 2
#define BUTTON2 3
#define BUTTON3 4
#define SERVO 5

LiquidCrystal_I2C lcd(0x27, 20, 4);
Servo myservo;

const int attemps_tot = 12;
int attemps = attemps_tot;
String history = "";

void setup() {
  Serial.begin(9600);
  // On nomme V_out1,2,3 les trois sortie de notre circuit
  pinMode(V_out1, INPUT);
  pinMode(V_out2, INPUT);
  pinMode(V_out3, INPUT);
  pinMode(BUTTON1, INPUT);
  pinMode(BUTTON2, INPUT);
  pinMode(BUTTON3, INPUT);
  myservo.attach(SERVO);
  lcd.init();
  lcd.backlight();
  }

void loop() {
  
  String secret_code; history = "";
  secret_code = gen_code();                                             // On génère le code secret
  attemps = attemps_tot;                                                // On initialise le nbr d'essais
  myservo.write(90);                                                    // On ferme la trappe

  while (attemps > 0){                                                  // Le jeu commence et continue tant que le joueur à encore des essais
    lcd.clear();                        
    lcd.setCursor(2, 1);  lcd.print("Il vous reste");
    lcd.setCursor(3, 2);  lcd.print(String(attemps) + " essais !");
    delay(2000);                                                        
    lcd.setCursor(2, 0);  lcd.print("Essais numéro : " + String(attemps_tot - attemps));
    lcd.setCursor(3, 1);  lcd.print("Entrer votre code");
    lcd.setCursor(0, 1);  lcd.print("Appuyez sur 2 pour");
    lcd.setCursor(2, 1);  lcd.print("validez le choix");

    makeChoice(history, attemps);                                       // On attemps que le joueur appuie sur le bouton2 pour valider son essai

    String code;
    code = player_code();                                               // On enregistre le code du joueur
    
    Serial.println(String(secret_code));
    Serial.println(String(code));
    
    int result[2];
    result[0] = 0;  result[1] = 0;                                      // Initialiser le nombre de bonne couleurs et couleur bien placé à 0
    for (int i = 0; i<4; i++){
        if (code[i] == secret_code[i]) {result[1]++;}                   // On trouve le nbr de couleurs bien placé
        else {for (int j = 0; j<4; j++) {                                         
          if (j != i && code[j] == secret_code[i]){                     // On trouve le nbr de couleurs mals placés
            result[0]++;
            break;}}}}
    
    Serial.println("Bien placées : " + String(result[1]));
    Serial.println("Bonne couleurs : " + String(result[0]));
    
    String strcode = String(code);  history = history + strcode + " ";
    
    if (result[1] != 4  && attemps !=0) {
      attemps--;                                                        // On enlève un essais et le joueur peut reessayer un coups
      
      Serial.println("Historique : " + String(history));
      Serial.println("prochain essais");
      
      lcd.clear();
      lcd.setCursor(6,0);  lcd.print("RATÉ !");
      delay(2000);
      
      lcd.clear();
      lcd.setCursor(1, 1);  lcd.print("Bonne couleurs: " + String(result[0]));
      lcd.setCursor(2, 2);  lcd.print("Bien placé: " + String(result[1]));
      delay(2000);
      lcd.clear();
      lcd.setCursor(1, 0);  lcd.print("Appuyez sur 1 pour");
      lcd.setCursor(1, 1);  lcd.print("voir l'historique");
      lcd.setCursor(1, 2);  lcd.print("Appuyez sur 2 pour");
      lcd.setCursor(1, 3);  lcd.print("le prochain essai");

      makeChoice(history, attemps);                                     // On attemps que le joueur appuie sur le bouton2 pour relancer un essai ou qu'il appuie sur le bouton1 pour voir l'historique
      }
    
    else {                                                              // La partie est finie on en recommence une
      if (attemps == 0){
        lcd.clear();
        lcd.setCursor(1, 1);  lcd.print("Il ne vous reste");
        lcd.setCursor(1, 2);  lcd.print("plus d'essais !");
        delay(2000);}

      else {
        attemps = 0;
        
        lcd.clear();
        lcd.setCursor(3, 0);  lcd.print("BIEN JOUÉ !");
        delay(2000);}

      lcd.clear();
      lcd.setCursor(1, 0);  lcd.print("Appuyez sur 1 pour");
      lcd.setCursor(1, 1);  lcd.print("voir l'historique");
      lcd.setCursor(1, 2);  lcd.print("Appuyez sur 2 pour");
      lcd.setCursor(1, 3);  lcd.print("un nouvelle partie");      
      
      makeChoice(history, attemps);}                                    // On attemps que le joueur appuie sur le bouton2 pour relancer une partie ou qu'il appuie sur le bouton1 pour voir l'historique
    }
  }

bool button1IsPressed(){return digitalRead(BUTTON1);}

bool button2IsPressed(){return digitalRead(BUTTON2);}

void makeChoice(String history, int attemps){
  bool choiceIsMade = false;
  while(!choiceIsMade){
    if (button1IsPressed()){show_history(history, attemps);}            // Si on appuie bouton1 : l'historique s'affiche et on attend qu'on appuie sur bouton2
    if (button2IsPressed()){choiceIsMade = true;}                       // Si on appuie bouton2 : le jeu continue 
    }
  }

void show_history(String history, int attemps){                         // On affiche l'historique
  if (attemps >= attemps_tot - 4){
    lcd.clear();
    lcd.setCursor(0,1);  lcd.print(history);
    }
  else if (attemps >= attemps_tot - 8){
    lcd.clear();
    lcd.setCursor(0,1); lcd.print(history);
    lcd.setCursor(0,2); lcd.print(history.substring(20));
    }
  else if (attemps >= attemps_tot - 12){
    lcd.clear();
    lcd.setCursor(0,0); lcd.print(history);
    lcd.setCursor(0,1); lcd.print(history.substring(20,39));
    lcd.setCursor(0,2); lcd.print(history.substring(40));
    }
  else{
    lcd.clear();
    lcd.setCursor(0,0); lcd.print(history);
    lcd.setCursor(0,1); lcd.print(history.substring(20,39));
    lcd.setCursor(0,2); lcd.print(history.substring(40,59));
    lcd.setCursor(0,3); lcd.print(history.substring(60));
    }
  }

String gen_code(){                                                      // Générer aléatoirement le code couleur secret
  String code; 
  char colors[4] = {'b', 'v', 'j', 'r'};

  for (int i = 0; i < 4; i++) {
    int j = random(4);
    code += String(colors[j]);}

  Serial.println("\nLe code secret est : " + String(code));

  return (code);}

String det_color(){                                                     // On détermine la couleur mise par le joueur
  int a = analogRead(V_out1);
  int b = analogRead(V_out2);
  int c = analogRead(V_out3);

  if (a < 2 && b < 2 && c < 2) {return ("b");}
  else if (a < 2 && b < 2 && c > 2) {return ("v");}
  else if (a < 2 && b > 2 && c > 2) {return ("r");} 
  else if (a > 2 && b > 2 && c > 2) {return ("j");}}

String player_code(){                                                   // On détermine le code du joueur
  String code;

  for (int i = 0; i < 4; i++){    
    lcd.clear();
    lcd.setCursor(0, 1);  lcd.print("Retirez la trappe nr"); 
    lcd.setCursor(10, 2);  lcd.print(String(i + 1));
    delay(2000);
    lcd.setCursor(1, 1);  lcd.print("Enfoncez le 3 pour");
    lcd.setCursor(2, 2);  lcd.print("valider le choix"); 
    
    bool button3IsPressed = false;
    while (!button3IsPressed){
      bool button3State = digitalRead(BUTTON3);
      if (!button3State){                                               // Lorsque button3 est enfoncé
        button3IsPressed = true;
        code += det_color();                                            // On détermine la couleur mise par le joueur
        myservo.write(0);                                               // On tourne la trappe pour que la bille tombe
        delay(1000);
        myservo.write(90);
        }}
    }
  
  Serial.println("Le code du joueur est : " + String(code));
  
  return (code);}
