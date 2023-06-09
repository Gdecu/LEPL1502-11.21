//
// Programme arduino du mastermind
// LEPL 1502
// Groupe 11.21 FSA11BA 2023
//

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <string.h>
#include <Servo.h>
 
#define V_out1 A0
#define V_out2 A1 
#define V_out3 A2
#define BUTTON1 2
#define BUTTON2 4
#define BUTTON3 7
#define SERVO 8

LiquidCrystal_I2C lcd(0x27, 20, 4);

const int attemps_tot = 12;
int attemps = attemps_tot;

String history = "";
Servo myservo;

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
  myservo.write(180);                                                    // On ferme la trappe

  while (attemps > 0){                                                  // Le jeu commence et continue tant que le joueur à encore des essais
    lcd.clear();                        
    lcd.setCursor(2, 1);  lcd.print("Il vous reste");
    lcd.setCursor(3, 2);  lcd.print(String(attemps) + " essais !");
    delay(2000);
    lcd.clear();                                                        
    lcd.setCursor(1, 0);  lcd.print("Essais numero : " + String(attemps_tot - attemps + 1));
    lcd.setCursor(1, 1);  lcd.print("Entrer votre code");
    lcd.setCursor(1, 2);  lcd.print("Appuyez sur 2 pour");
    lcd.setCursor(2, 3);  lcd.print("Validez le choix");

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
    
    Serial.println("Bien placees : " + String(result[1]));
    Serial.println("Bonnes couleurs : " + String(result[0]));
    
    String strcode = String(code);  history = history + strcode + " ";
    
    if (result[1] != 4  && attemps !=0) {
      attemps--;                                                        // On enlève un essais et le joueur peut reessayer un coups
      
      Serial.println("Historique : " + String(history));
      Serial.println("Prochain essais");
      
      lcd.clear();
      lcd.setCursor(6,0);  lcd.print("RATE !");
      delay(2000);
      
      lcd.clear();
      lcd.setCursor(1, 1);  lcd.print("Bonnes couleurs: " + String(result[0]));
      lcd.setCursor(2, 2);  lcd.print("Biens placees: " + String(result[1]));
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
        lcd.setCursor(1, 0);  lcd.print("Il ne vous reste");
        lcd.setCursor(1, 1);  lcd.print("plus d'essais !");
        lcd.setCursor(4, 2);  lcd.print("Le code était :");
        lcd.setCursor(8, 4);  lcd.print(String(secret_code));
        delay(2000);}

      else {
        attemps = 0;
        
        lcd.clear();
        lcd.setCursor(3, 0);  lcd.print("BIEN JOUE !");
        lcd.setCursor(4, 1);  lcd.print("Le code etait :");
        lcd.setCursor(8, 2);  lcd.print(String(secret_code));
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
    bool button1State = button1IsPressed();
    bool button2Ismade = button2IsPressed();
    if (!button1State){show_history(history, attemps);}            // Si on appuie bouton1 : l'historique s'affiche et on attend qu'on appuie sur bouton2
    if (!button2Ismade){choiceIsMade = true;}                       // Si on appuie bouton2 : le jeu continue 
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
  // Mélanger les couleurs dans le tableau
  for (int i = 3; i > 0; i--) {
    int j = random(i + 1);
    char temp = colors[i];
    colors[i] = colors[j];
    colors[j] = temp;}
  // Sélectionner les quatre premières couleurs mélangées
  for (int i = 0; i < 4; i++) {code += String(colors[i]);}

  Serial.println("\nLe code secret est : " + code);

return code;}


String det_color(){                                                     // On détermine la couleur mise par le joueur
  int aMoy = 0; int bMoy = 0; int cMoy = 0; int nbr = 20;
  // On effectue une moyenne des entrées pour pouvoir détecter les entrées dont leurs valeures oscillent
  for (int i = 0; i < nbr; i++){
    int a = analogRead(V_out1);
    int b = analogRead(V_out2);
    int c = analogRead(V_out3);
    aMoy += a;  bMoy += b;  cMoy += c;}
  aMoy = aMoy / nbr ; bMoy = bMoy / nbr; cMoy = cMoy / nbr;

  Serial.println(String(aMoy)+ "," + String(bMoy) + "," + String(cMoy));
  if (aMoy < 100 && bMoy < 100 && cMoy < 100) {return ("j");}
  else if (aMoy < 100 && bMoy < 100 && cMoy > 100) {return ("r");}
  else if (aMoy < 100 && bMoy > 100 && cMoy > 100) {return ("b");} 
  else if (aMoy > 100 && bMoy > 100 && cMoy > 100) {return ("v");}}

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
        code += det_color(); 
        Serial.println("Avancé code: "+code);                           // On détermine la couleur mise par le joueur
        myservo.write(180);                                               // On tourne la trappe pour que la bille tombe
        delay(1000);
        myservo.write(90);
        }}
    }
  
  Serial.println("Le code du joueur est : " + String(code));
  
  return (code);}
