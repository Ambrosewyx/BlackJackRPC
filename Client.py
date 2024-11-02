import rpyc

conn = rpyc.connect('localhost', 18861)
conn.root.start()
print(conn.root.show_card())


while True:
    print('Hit(1) or Stand(2)')
    choice = input()
    if choice == '1':
        conn.root.player_get_card()
        print(conn.root.show_card())
        if conn.root.player_is_bust():
            print('Player Bust, you lose!')
            break
    elif choice == '2':
        conn.root.dealer_turn()
        print(conn.root.show_card())
        while conn.root.get_max_val("dealer")<17:
            print("Dealer pick 1 new card...")
            conn.root.dealer_get_card()
            print(conn.root.show_card())
        if conn.root.dealer_is_bust():
            print('Dealer Bust, you win!')
            break
        # 抓到比player大为止
        while conn.root.get_max_val("dealer")<conn.root.get_max_val("player"):
            print("Dealer pick 1 new card...")
            conn.root.dealer_get_card()
            print(conn.root.show_card())
        # 判断结果
        if conn.root.dealer_is_bust():
            print('Dealer Bust, you win!')
            break
        elif conn.root.get_max_val("dealer")>conn.root.get_max_val("player"):
            print('dealer win, you lose!')
            break
        else:
            print('it is a push(tie)!')
            break
    else:
        print('Invalid input!')










