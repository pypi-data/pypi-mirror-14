def print_lol (yourlist):
    for item in yourlist:
        if isinstance(item , list):
            print_lol(item)
        else:
            print(item)



history = ['中国',['民国',['奉张时期','满洲国时期','解放期']],'清朝',['明朝',['早期','后金','清']],'元朝','金国',['辽国','女真'],'渤海国','高句丽','鲜卑',['丁零','肃慎','扶余','靺鞨'],'黄帝']
print_lol(history)
