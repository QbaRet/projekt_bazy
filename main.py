import database as db
current_user=None
def main_menu():
    print("System zarządzania meczami")
    print(f"Zalogowany jako: {current_user[1] if current_user else 'Gość'}")
    print("1. Logowanie")
    print("2. Przeglądaj mecze według sezonu")
    if current_user and current_user[1] == 'admin':
        print("3. Dodaj wyniki meczu (admin)")
    print("0. Wyjście")
    return input("Wybierz opcję: ")
def login():
    global current_user
    user=input("Login: ")
    password=input("Hasło: ")
    result=db.login(user,password)
    if result:
        current_user= result
        print("Zalogowano pomyślnie")
    else:
        print("Nieprawidłowy login lub hasło")
def show_matches_screen():
    season_id = input("Podaj ID sezonu do przeglądu: ")
    matches = db.get_matches_by_season(season_id)
    print(f"\n{'Data':<12} | {'Gospodarz':<15} | {'Gość':<15} | {'Wynik'}")
    print("-" * 50)
    for m in matches:
        wynik = f"{m[4]}:{m[5]}" if m[4] is not None else "-:-"
        print(f"{m[1]:<12} | {m[2]:<15} | {m[3]:<15} | {wynik}")
def admin_panel():
    print("Admin Panel")
    print("1. Dodaj wyniki meczu")
    print("0. Powrót do menu głównego")
    opcja= input("Wybierz opcję: ")
    if opcja=='1':
        match_id= input("Podaj ID meczu: ")
        h_score= input("Wynik gospodarzy: ")
        a_score= input("Wynik gości: ")
        scorers_list=[]
        while True:
            pl_id= input("ID strzelca (lub 'koniec' aby zakończyć): ")
            if pl_id.lower()=='koniec':
                break
            minute= input("Minuta bramki: ")
            scorers_list.append((pl_id, minute))
        db.add_match_results(match_id, h_score, a_score, scorers_list)
if __name__ == '__main__':
    while True:
        choice= main_menu()
        if choice=='1':
            login()
        elif choice=='2':
            show_matches_screen()
        elif choice=='3' and current_user and current_user[1]=='admin':
            admin_panel()
        elif choice=='0':
            print("Wyjście z programu.")
            break
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")