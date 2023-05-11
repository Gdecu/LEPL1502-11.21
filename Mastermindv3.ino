//
// Programme arduino du mastermind pour LEPL 1502
// Groupe 11.21 FSA11BA 2022-2023
//

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define V_out1 A0
#define V_out2 A1 
#define V_out3 A2
#define BUTTON1 2
#define BUTTON2 3
#define BUTTON3 4

LiquidCrystal_I2C lcd(0x27, 20, 4);     // On nomme notre écran lcd, et on définit sa taille

volatile bool gameIsOn = false;
const int attemps_tot = 10;


void setup() {                                      // Fonction qui est éxecuté une seule fois au tout début
  Serial.begin(9600);
  // On dit que V_out1,2,3 sont des entrée
  pinMode(V_out1, INPUT);
  pinMode(V_out2, INPUT);
  pinMode(V_out3, INPUT);
  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
  pinMode(BUTTON3, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON1), buttonInterrupt, FALLING);
  lcd.init();
  lcd.backlight();
  }

void loop() {                                       // Fonction qui est éxecuté en boucle
  if (gameIsOn){
    
    String secret_code;  String history = "";
    secret_code = gen_code();                                          // On génère le code secret
    int attemps = attemps_tot;                                            // On initialise le nbr d'essais
    
    while (attemps > 0){                                                  // Le jeu commence et continue tant que le joueur à encore des essais
      lcd.clear();                        
      lcd.setCursor(2, 1);  lcd.print("Il vous reste");
      lcd.setCursor(3, 2);  lcd.print(String(attemps) + " essais !");
      delay(2000);                                                        // On laisse le temps au joueur de choisir son code, delay(x) : 'pause' pdt x milliseconde
      
      String code;
      code = player_code();                                            // On enregistre le code du joueur
      
      Serial.println(String(secret_code));
      Serial.println(String(code));
      
      int result[2];
      result[0] = 0;  result[1] = 0;                                      // Initialiser le nombre de bonne couleurs et couleur bien placé à 0
      for (int i = 0; i<4; i++){
          if (code[i] == secret_code[i]) {result[1]++;}           // On trouve le nbr de couleurs bien placé
          else {for (int j = 0; j<4; j++) {                                         
            if (j != i && code[j] == secret_code[i]){             // On trouve le nbr de couleurs mals placés
              result[0]++;
              break;}}}}
      
      Serial.println("Bien placées : " + String(result[1]));
      Serial.println("Bonne couleurs : " + String(result[0]));
      
      String strcode = String(code);  history = history + strcode + " -- ";
      
      if (result[1] != 4  && attemps !=0) {
        attemps--;                                                        // On enlève un essais et le joueur peut reessayer un coups
        
        Serial.println("historique : " + String(history));
        Serial.println("prochain essais");
        
        lcd.clear();
        lcd.setCursor(6,0);  lcd.print("RATÉ !");
        delay(2000);
        
        lcd.clear();
        lcd.setCursor(1, 0);  lcd.print("Bonne couleurs: " + String(result[0]));
        lcd.setCursor(2, 1);  lcd.print("Bien placé: " + String(result[1]));
        lcd.setCursor(0, 2);  lcd.print("Prochain essais dans");
        lcd.setCursor(1, 3);  lcd.print("10 secondes...");
        
        while (digitalRead(BUTTON3 == LOW)){                              // On attemps que le joueur appuie sur le bouton pour relancer un essai
          delay(10);}}
      
      else {                                                              // La partie est finie on en recommence une
        if (attemps == 0){
          lcd.clear();
          lcd.setCursor(1, 0);  lcd.print("Il ne vous reste");
          lcd.setCursor(1, 1);  lcd.print("plus d'essais !");
          lcd.setCursor(0, 2);  lcd.print("Prochaine partie");
          lcd.setCursor(0, 3);  lcd.print("dans 20 secondes ...");}
        
        else {
          attemps = 0;
          
          lcd.clear();
          lcd.setCursor(3, 0);  lcd.print("BIEN JOUÉ !");
          lcd.setCursor(0, 2);  lcd.print("Prochaine partie");
          lcd.setCursor(0, 3);  lcd.print("dans 20 secondes ...");}
        
        while (digitalRead(BUTTON3 == LOW)){                              // On attemps que le joueur appuie sur le bouton pour relancer une partie
          delay(10);}}}
    }
  }

void buttonInterrupt(){gameIsOn = !gameIsOn;}

String gen_code(){                                            // Générer aléatoirement le code couleur secret
  String code; 
  char colors[4] = {'b', 'v', 'j', 'r'};

  for (int i = 0; i < 4; i++) {
    int j = random(4);
    code += String(colors[j]);}

  Serial.println("\nLe code secret est : " + String(code));

  return (code);}

String det_color(){                                           // On détermine la couleur mise par le joueur
  int a = analogRead(V_out1);
  int b = analogRead(V_out2);
  int c = analogRead(V_out3);

  if (a < 2 && b < 2 && c < 2) {return ("b");}
  else if (a < 2 && b < 2 && c > 2) {return ("v");}
  else if (a < 2 && b > 2 && c > 2) {return ("r");} 
  else if (a > 2 && b > 2 && c > 2) {return ("j");}}

String player_code(){                                         // On détermine le code du joueur
  String code;

  for (int i = 0; i < 4; i++){
    Serial.println("Prochaine couleur");
    
    lcd.clear();
    lcd.setCursor(1, 1);  lcd.print("Placer une couleur");
    lcd.setCursor(2, 2);  lcd.print("de votre choix");
    
    bool button2IsPressed = false;
    while (!button2IsPressed){
      int button2State = digitalRead(BUTTON2);
      if (button2State == LOW){                                 // Lorsque botton est enfoncé : (LOW car c'est inversé avec la résistance de PULLUP)
        button2IsPressed = true;
        code += det_color();}}                                  // On détermine la couleur mise par le joueur
    }
    delay(2000);
  
  Serial.println("Le code du joueur est : " + String(code));
  
  return (code);}




